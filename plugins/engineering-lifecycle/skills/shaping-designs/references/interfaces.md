# Interfaces and contracts

Read this when a design adds or changes an API, an event, a file format, a config key,
a CLI, or any boundary another team or a later version will depend on. A contract is
everything a caller can observe and come to rely on, including what you never wrote
down: field order, error text, timing, defaults.

## Compatibility

- **Additive is safe; everything else is a new version.** Adding an optional field, a
  new endpoint, a new enum value that old callers can ignore: compatible. Removing or
  renaming a field, changing its type, unit or meaning, tightening validation, changing
  a default, making something required: breaking, even when the schema still parses.
- **Changing what a field means is the worst break**, because nothing fails. A
  `duration` that moves from seconds to milliseconds passes every type check.
  Introduce a new field (`duration_ms`) and retire the old one.
- **Enums grow.** Callers must treat unknown values as a known fallback; say so in the
  contract, and test it from the client side before you add the first new value.
- **Defaults are contract.** Changing a default is a behaviour change for every caller
  who never set it, which is usually most of them.
- **Deprecate in three steps:** announce with a date and the replacement, measure who
  still uses it (logs over a period with a baseline), then remove. Zero calls with no
  baseline proves nothing about the callers who run monthly.
- **Hyrum's law is real.** With enough callers, someone depends on the order of a list,
  the wording of an error, or a field that's "internal". Before changing observable
  behaviour, look at what callers actually do (logs, code search across consumers).

## Requests and responses

- **Idempotency.** Any operation a client may retry (payments, orders, sends) takes an
  idempotency key, and the server stores the result per key for longer than the
  client's retry window. Without it, a timeout that arrives after the work succeeded
  causes a duplicate.
- **Pagination.** Cursor-based for anything that changes while being read; offset
  paging skips or repeats rows when items are inserted. Cap the page size on the
  server, whatever the client asks for.
- **Errors.** A stable machine-readable code, a human message, and which field is at
  fault. Distinguish "your request is wrong" (don't retry), "try again later" (retry
  with backoff) and "conflict" (re-read, then decide). Clients decide on the code, never
  on the message text.
- **Time, money and identity.** Timestamps in UTC with an explicit offset in the
  format; durations with a unit in the name. Money as integer minor units or a decimal
  string, plus a currency code; never floats. IDs as opaque strings, not integers
  callers might do arithmetic on.
- **Partial results.** For batch operations, report success and failure per item; a
  single status for a batch of 500 forces the client to guess.
- **Limits.** Document size limits, rate limits and timeouts as part of the contract,
  and what the caller sees when they're exceeded.

## Events and messages

- Delivery is at least once in practice; consumers deduplicate by an event ID.
- Order is guaranteed only within a partition or key; design consumers that tolerate
  reordering across keys, or partition by the entity whose order matters.
- Schema changes follow the same additive rules, and old events stay readable for as
  long as they can be replayed.
- Publish the fact ("order 123 paid at …"), not an instruction to a specific consumer;
  the producer shouldn't need to know who listens.

## Configuration and files

- A config key is an interface the moment someone sets it. Renaming one needs the old
  name accepted (with a warning) for a release.
- Validate config at startup and fail loudly on unknown keys, so a typo doesn't
  silently fall back to a default.
- File formats carry a version marker from the first release.

## Checklist for a new or changed interface

| Question | Answered by |
|---|---|
| Who calls it today, and who will? | Code search across consumers, access logs with a baseline |
| Is every change additive? If not, what is the new version and the migration path? | The diff of the contract |
| What happens on retry, timeout, duplicate and reorder? | Idempotency key, event ID, ordering key |
| What does each error mean for the caller, and which are retryable? | The error table |
| What are the limits, and what happens at them? | Documented limits and their responses |
| How will we know who still uses the old version? | A metric or log keyed by version |
