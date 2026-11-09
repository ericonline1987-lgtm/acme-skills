---
type: llm
weight: 1
---

Pass if this holds for the response: The diagram shows all three provider outcomes as distinct paths: success (status succeeded, RefundSucceeded, customer email), 4xx (status failed, RefundFailed, no retry), and timeout/5xx (retries with backoff up to 5 attempts, then refunds.DLQ with status still pending and on-call paged).
