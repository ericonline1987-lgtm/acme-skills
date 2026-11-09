# Sources

- Use The Index, Luke — Paging Through Results (fetch next page / seek method) — https://use-the-index-luke.com/sql/partial-results/fetch-next-page
- Use The Index, Luke — No Offset — https://use-the-index-luke.com/no-offset
- PostgreSQL documentation, Date/Time Functions and Operators (now() = start of current transaction) — https://www.postgresql.org/docs/current/functions-datetime.html
- PostgreSQL documentation, CREATE INDEX — https://www.postgresql.org/docs/current/sql-createindex.html
- Google AIP-180, Backwards compatibility — https://google.aip.dev/180

## Grader basis

- ties-skip-rows: Use The Index, Luke (paging needs a deterministic order; a non-unique date boundary skips the remaining rows of that date); PostgreSQL docs (now() values do not change during a transaction, so multiple modifications bear the same timestamp).
- compound-cursor: Use The Index, Luke (add a unique column to ORDER BY; row values `(sale_date, sale_id) < (?, ?)`).
- index-matches-order: Use The Index, Luke (extend the index to include the tie-breaker so it can serve the seek); PostgreSQL CREATE INDEX (CONCURRENTLY on a live table).
- client-contract: AIP-180 (must not remove components or change visible behaviour within a version).

## Why a capable general model might miss it

The diff is the textbook keyset change and looks correct; spotting the bug requires connecting the batch-insert note to Postgres's transaction-scoped now(), which turns a theoretical tie issue into guaranteed data loss.

The code and table are synthetic.
