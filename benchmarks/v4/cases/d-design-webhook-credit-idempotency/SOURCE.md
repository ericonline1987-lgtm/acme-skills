# Sources

- Stripe documentation, Receive Stripe events in your webhook endpoint (best practices: duplicates, ordering, async, quick 2xx) — https://docs.stripe.com/webhooks
- Stripe API reference, Types of events (charge.refunded "including partial refunds") — https://docs.stripe.com/api/events/types
- Stripe API reference, Idempotent requests — https://docs.stripe.com/api/idempotent_requests
- AWS Builders' Library, Timeouts, retries and backoff with jitter — https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter

## Grader basis

- db-enforced-dedupe: Stripe webhooks ("log the event IDs you've processed"; separate Event objects can be generated, so also key on data.object ID + type); Stripe idempotency design.
- atomic-balance: concurrency practice for read-modify-write under multiple workers (practitioner knowledge); Stripe note that events may be delivered more than once.
- refunds-partial-and-order: Stripe event types (charge.refunded includes partial refunds; use refund.created for refund details); Stripe webhooks (ordering not guaranteed; don't use `created` for order).
- ack-fast-side-effects: Stripe webhooks (return 2xx before complex logic; handle events with an asynchronous queue; retries for up to three days).
- reconcile-affected: Stripe webhooks (use the API to retrieve objects); repairing state after an idempotency bug is standard payments practice.

## Why a capable general model might miss it

Models usually stop at "dedupe on event ID", missing that the dedupe must be atomic with the balance write, that `+=` on an ORM object races, that charge.refunded is cumulative/partial, and that existing balances need repair.

The handler and incident are synthetic.
