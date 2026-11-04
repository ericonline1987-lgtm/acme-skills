# Defect classes by area

Read this during the "problems the change introduces" pass. Check the rows for the areas
the diff touches; each is a class of bug that passes tests written by the same author.

| Area | Look for |
|---|---|
| Queries and data access | String-built SQL or filters (injection); a query inside a loop (N+1); a missing index for a new filter; reads outside the transaction that then write; `SELECT *` feeding an API response (leaks new columns) |
| Money | Floats; rounding applied per line instead of per total, or the reverse of the documented rule; currency dropped in conversion; refunds or credits that can exceed the original |
| Time | Naive datetimes; "today" computed in the server's zone; DST gaps and repeats; durations without units; comparisons across zones; expiry computed on the client |
| Concurrency | Read-modify-write without a lock or version check; check-then-act races (exists? then create); shared mutable state across requests; async work not awaited; a lock held across a network call |
| Errors | Exceptions swallowed or logged and ignored; a broad catch that hides a programming error; retries on non-retryable errors; error paths that leave partial state; cleanup missing on early return |
| Resources | Files, connections or cursors not closed on every path; unbounded caches, queues or lists built from user input; timeouts missing on outbound calls |
| Input and output | Validation only on the client; size limits missing; user input in file paths, shell commands, templates, redirects or regexes; HTML not escaped; deserialising untrusted data |
| Authorisation | The route checks a role but the handler never checks ownership of the object (fetching order 124 when you own 123); new endpoints missing the middleware the others have; admin paths reachable by changing a parameter |
| Secrets and personal data | Keys or tokens in code, config or tests; personal data in logs, error messages, analytics or URLs; new fields exposed in an API that were internal |
| Caching | Keys missing a dimension (user, locale, permission) so one person's data is served to another; no invalidation on write; stampede on expiry |
| API and contract | A changed field meaning, default, enum or error code (see compatibility rules in the design references); a removed field still used by a client; pagination that skips rows under concurrent inserts |
| Migrations | A migration that locks a large table; a rename done in one step while old code is still running; a backfill without batches; no way back |
| Config and flags | A new key without a default in every environment; a flag checked in one place but not another; a default that changes behaviour for existing users |
| Frontend state | State not reset when the identity or route changes; optimistic updates without rollback on failure; effects that run twice; missing loading, empty and error states |
| Tests | A test that can't fail (asserting on the mock); a changed assertion that now accepts the bug; a deleted or skipped test with no reason; fixed sleeps |

## Using the table

- A row is a lead, not a finding. Confirm each candidate against the code before it
  reaches the report.
- When one instance of a class turns up, search the diff and its neighbours for the
  rest and report the class once, with every location.
- A row that doesn't apply needs no mention; the report lists what was checked, not
  every row skipped.
