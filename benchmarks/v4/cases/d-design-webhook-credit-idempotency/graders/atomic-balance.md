---
type: llm
weight: 1
---

Pass if this holds for the response: The response identifies that `user.credits += ...` is a read-modify-write that can lose or double-apply updates under concurrent deliveries across workers, and replaces it with an atomic update (e.g. UPDATE ... SET credits = credits + n), a row lock, or a balance derived from an append-only ledger.
