# Failure modes and capacity

Read this when detailing a design that calls other services, runs under load, or must
stay up. For every dependency, the design says what happens when it is slow, down, or
wrong, and the answer is never "it won't be".

## Per dependency

| Question | A good answer names |
|---|---|
| What's the timeout, and how was it chosen? | A number below the caller's own timeout, from the dependency's measured p99 |
| What happens on timeout or error? | Retry (which errors, how many times), fallback, or fail with what message |
| Is the retried operation safe to repeat? | An idempotency key, or why it's naturally idempotent |
| What if it's slow but not failing? | A concurrency limit or bulkhead so slow calls can't consume every thread |
| What if it returns wrong data? | Validation at the boundary, and what the caller does with a rejected response |
| How will we know? | A metric and an alert on the user-visible symptom |

## Patterns that cause outages

- **Retry storms.** Every layer retries three times: one failure at the bottom becomes
  27 calls. Retry at one layer, with exponential backoff and jitter, and a retry budget
  (for example at most 10% extra traffic).
- **Timeouts longer than the caller's.** The caller has given up; the work continues and
  holds resources. Each hop's timeout is shorter than the hop above it.
- **No limit on queue or pool size.** Under load, latency grows without bound instead of
  shedding work. Bound every queue; reject early with a clear error when full.
- **Cache stampede.** A hot key expires and every request goes to the database at once.
  Use request coalescing, early refresh with jitter, or serve stale while refreshing.
- **Thundering herd on recovery.** Every client reconnects the moment a service comes
  back. Clients back off with jitter; the service admits load gradually.
- **Poison messages.** One message a consumer can't process blocks or crashes the queue
  forever. Cap attempts, then move it to a dead-letter queue with an alert.
- **Clock assumptions.** Ordering by wall-clock time across machines, or expiry computed
  on a client. Use server time, monotonic clocks for durations, and sequence numbers
  for order.
- **Hidden single points.** A shared config service, DNS, a certificate, a cron on one
  host, a feature-flag provider. List them; each needs an answer for "down".

## Degrade, don't fail

Decide what the user sees when each part is unavailable: cached data marked as such,
the feature hidden, read-only mode, or a queue that catches up later. Prefer degrading
the least important feature to failing the request.

## Capacity, on the back of an envelope

- Start from peak, not average: the busiest hour, times a margin for growth and for the
  bursts inside that hour (often 2 to 3 times the hourly average for short windows).
- Little's law: concurrent work in flight = arrival rate × time each takes. 200
  requests a second at 300 ms each means about 60 in flight; size pools and
  connections from that, with headroom.
- Storage: rows per day × bytes per row (with indexes, often double) × retention. Say
  when it crosses a threshold that changes the design (fits in memory, fits one
  machine, needs partitioning).
- Name the first bottleneck you expect and how you'll see it coming (a metric and a
  threshold), rather than claiming the design scales.
- Measure with a load test against something production-shaped before trusting any of
  these numbers; the estimate tells you what to test.

## Observability in the design, not after

- Service-level indicators for what users feel: success rate, latency at p50 and p99,
  freshness for data pipelines.
- Alerts on those symptoms, with a runbook link, not on every internal metric.
- A trace or correlation ID through every hop, so one failing request can be followed.
- Logs that record decisions (which branch, which fallback), with personal data kept
  out.

## Security as a failure mode

For anything that handles accounts, money, personal data or runs code: who can reach it,
what input they control, what they could gain. Then: authentication at every entry,
authorisation checked on the object (not only the route), input validated at the
boundary, secrets out of code and logs, least privilege for every service account, and
an audit trail for actions on other people's data.
