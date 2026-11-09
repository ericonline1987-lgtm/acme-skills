---
type: llm
weight: 1
---

Pass if this holds for the response: The response considers what happens when Redis is unavailable or cold (e.g. after a flush or failover) — that the full ~8k rps would hit pricing-service, which cannot take it — and proposes a fallback such as a local in-process cache, load shedding, or capping requests to pricing-service.
