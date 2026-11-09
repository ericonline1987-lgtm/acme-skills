---
type: llm
weight: 1
---

Pass if this holds for the response: The redesign makes crediting idempotent with a uniqueness guarantee enforced by the database — e.g. a processed-events or ledger table with a unique key on the event ID or payment intent ID — written in the same transaction as the balance change, rather than an application-level "check if seen, then process" outside that transaction.
