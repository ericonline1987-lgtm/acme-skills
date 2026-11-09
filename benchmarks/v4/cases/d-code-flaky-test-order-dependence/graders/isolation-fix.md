---
type: llm
weight: 1
---

Pass if this holds for the response: The response proposes a fix that restores isolation — e.g. clearing rate_for's cache after the override test as well as before (rate_for.cache_clear() in a fixture/teardown, ideally autouse), patching rate_for itself instead of the dict, or removing or redesigning the cache — rather than changing test_invoice_totals's expected value or ordering the tests.
