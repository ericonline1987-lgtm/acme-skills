---
type: llm
weight: 1
---

Pass if this holds for the response: The proposed fix stops failures from being cached indefinitely — e.g. raising an exception instead of returning None (lru_cache does not store raised exceptions), or a cache that only stores successes or stores failures with a short TTL — and makes the caller handle FX unavailability as a deliberate case (fail visibly, use a recent last-known-good rate within an age limit, or fall back to showing the base currency).
