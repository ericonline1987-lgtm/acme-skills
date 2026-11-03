---
type: llm
weight: 1
---

Pass if this holds for the response: It checks completeness: that release/2.4's commits are contained (ancestry, or git log HEAD..release/2.4 being empty), or that release/2.4's changes to the file survived the merge (a diff against its version).
