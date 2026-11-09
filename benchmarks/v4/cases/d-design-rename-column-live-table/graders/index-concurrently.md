---
type: llm
weight: 1
---

Pass if this holds for the response: The response says the unique index must be built concurrently (CREATE INDEX CONCURRENTLY / algorithm: :concurrently), which cannot run inside the migration's transaction (disable_ddl_transaction!), because a plain index build blocks writes for the duration.
