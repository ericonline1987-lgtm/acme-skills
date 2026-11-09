---
type: llm
weight: 1
---

Pass if this holds for the response: The review identifies that a timeout (or a 5xx returned after processing) does not mean the charge failed, so retrying the POST can charge the customer twice, and says the retries need an idempotency key (or an equivalent dedupe/lookup) before they are safe.
