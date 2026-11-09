---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Can you turn this into a Mermaid diagram for the design doc? Reviewers keep misreading the prose version.

Refund flow (current):

1. Support agent clicks Refund in the Admin UI. Admin UI calls refunds-api `POST /refunds`.
2. refunds-api writes a refund row (status=pending) to Postgres, publishes `RefundRequested` to Kafka, and returns 202 to the Admin UI.
3. refund-worker consumes `RefundRequested` and calls the payment provider's refund endpoint (idempotency key = refund id).
4. Provider returns success → worker sets status=succeeded and publishes `RefundSucceeded`. notification-service consumes it and emails the customer.
5. Provider returns 4xx (e.g. charge already refunded, charge too old) → status=failed, publishes `RefundFailed`. No retry.
6. Provider times out or returns 5xx → worker retries with exponential backoff, up to 5 attempts. After the 5th failure the message goes to `refunds.DLQ` and the status stays pending. On-call is paged when DLQ depth > 0.
7. Separately, the provider sends a `refund.updated` webhook to webhooks-api, which updates the refund row only if its status is still pending. (This is how refunds that timed out but actually succeeded at the provider get resolved.)
8. Admin UI polls `GET /refunds/{id}` every 5s to show the current status.
