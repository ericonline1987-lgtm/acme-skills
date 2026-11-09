---
type: llm
weight: 1
---

Pass if this holds for the response: The diagram makes clear that refunds-api returns 202 to the Admin UI right after writing the pending row and publishing RefundRequested — before the provider is called — and that the Admin UI learns the outcome by polling GET /refunds/{id}, not from the original request.
