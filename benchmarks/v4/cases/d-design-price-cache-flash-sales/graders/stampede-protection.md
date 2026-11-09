---
type: llm
weight: 1
---

Pass if this holds for the response: The response addresses the thundering-herd risk when many hot keys miss at once (mass expiry or invalidation at sale start combined with 5x traffic, against a backend that falls over above ~3k rps) with a concrete mitigation such as request coalescing/single-flight, serving stale while one request refreshes, jittered TTLs, or pre-warming.
