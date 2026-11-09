# Sources

- ankane/strong_migrations README — https://github.com/ankane/strong_migrations
- PostgreSQL documentation, ALTER TABLE — https://www.postgresql.org/docs/current/sql-altertable.html
- PostgreSQL documentation, CREATE INDEX — https://www.postgresql.org/docs/current/sql-createindex.html
- GoCardless, Zero-downtime Postgres migrations: the hard parts — https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/
- Martin Fowler, ParallelChange — https://martinfowler.com/bliki/ParallelChange.html

## Grader basis

- rename-vs-rolling-deploy: strong_migrations (renaming a column in use breaks the application; create new, write both, backfill, move reads, drop); Fowler ParallelChange (expand/migrate/contract).
- not-null-without-long-lock: PostgreSQL ALTER TABLE (SET NOT NULL scan skipped when a valid CHECK proves no NULLs; NOT VALID + VALIDATE CONSTRAINT takes SHARE UPDATE EXCLUSIVE); strong_migrations NOT NULL recipe.
- index-concurrently: strong_migrations (non-concurrent index blocks writes; disable_ddl_transaction!); PostgreSQL CREATE INDEX (CONCURRENTLY cannot run in a transaction block).
- check-duplicates-first: PostgreSQL CREATE INDEX (uniqueness violation during a concurrent build leaves an "invalid" index; drop and retry).
- lock-timeout: GoCardless (lock queue: a waiting ALTER blocks later queries; set lock_timeout); strong_migrations (short lock timeout).

## Why a capable general model might miss it

Models know "use CONCURRENTLY" but rarely reason about rolling deploys (old code against new schema), Postgres's NOT NULL scan behaviour, or the lock queue, so they approve a plan that takes the site down.

The table, sizes and migration are synthetic.
