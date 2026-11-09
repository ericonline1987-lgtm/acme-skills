---
type: llm
weight: 1
---

Pass if this holds for the response: The response explains that SET NOT NULL on a 420M-row table scans the whole table while holding an ACCESS EXCLUSIVE lock, and recommends adding a CHECK (... IS NOT NULL) constraint as NOT VALID, validating it separately, and then setting NOT NULL (which Postgres 12+ can do without a full scan once a valid check constraint exists).
