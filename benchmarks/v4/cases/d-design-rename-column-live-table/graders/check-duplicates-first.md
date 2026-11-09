---
type: llm
weight: 1
---

Pass if this holds for the response: The response warns that existing emails that differ only by case (or values copied from contact_email that collide) will make the unique index on lower(...) fail, recommends checking for and resolving such duplicates before building it, and/or notes that a failed concurrent build leaves an INVALID index that must be dropped before retrying.
