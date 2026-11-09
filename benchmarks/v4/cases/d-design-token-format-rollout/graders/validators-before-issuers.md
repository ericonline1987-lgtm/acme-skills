---
type: llm
weight: 1
---

Pass if this holds for the response: The plan ensures every validator (api-gateway, billing-service, notifications-service via an updated authtoken library, and auth-service itself) accepts both v1 and v2 tokens and is deployed before any v2 token is issued, noting that otherwise users holding v2 tokens get rejected by services still on the old library.
