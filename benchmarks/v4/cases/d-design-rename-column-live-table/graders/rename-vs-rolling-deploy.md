---
type: llm
weight: 1
---

Pass if this holds for the response: The response identifies that renaming the column in place breaks the old pods still running during the rolling deploy (they query `email`), and proposes a sequence that avoids it — e.g. add the new column, write both, backfill, switch reads, then drop the old column in a later release — or an equivalent approach that keeps both names working across the deploy.
