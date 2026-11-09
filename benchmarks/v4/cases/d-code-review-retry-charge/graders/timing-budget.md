---
type: llm
weight: 1
---

Pass if this holds for the response: The review flags a retry timing problem: the worst case (4 attempts × 5s timeout plus the sleeps, roughly 22s) exceeds the 15s load-balancer timeout so the customer sees an error while charges may still go through, and/or the fixed 500ms delay without exponential backoff and jitter keeps hammering a provider that is already failing.
