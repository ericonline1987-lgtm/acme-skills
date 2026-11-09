---
type: llm
weight: 1
---

Pass if this holds for the response: The response identifies the cause as test pollution through the lru_cache on rate_for: test_rate_override clears the cache before overriding, but not after, so once it calls rate_for("DE") the cache holds 0.20 even after monkeypatch restores the RATES dict, and any later test in the same process gets 0.20 (giving 71.96).
