# Data changes and migrations

Read this when a design changes a schema, moves data between stores, splits or merges
services that own data, or backfills. Code can be rolled back in minutes; data that has
been rewritten usually can't, so data changes are planned as a sequence of steps each
of which is safe to stop after.

## Expand, migrate, contract

Change a schema in steps that each work with both the old and the new code, because
during a deploy both run at once:

1. **Expand.** Add the new column, table or field; nullable or with a default; nothing
   reads it yet. Old code ignores it.
2. **Write both.** New code writes the old and new shapes. Deploy, and confirm the new
   shape is being written correctly for new data.
3. **Backfill** existing rows into the new shape (below).
4. **Read new.** Switch reads to the new shape, behind a flag, compared against the old
   for a while (shadow reads) where correctness matters.
5. **Stop writing old**, then, after a period that covers rollback and any monthly or
   quarterly jobs, **contract**: drop the old column.

Skipping a step is how outages happen: renaming a column in one migration breaks every
running instance of the old code mid-deploy. Where customers upgrade a bundled product
and may skip versions, every step must work when run in the final version without the
intermediate ones having run.

## Backfills

- In batches, by primary-key range, with a pause between batches and a stop switch.
  Measure the batch's effect on the database (locks, replication lag) on a copy first.
- Idempotent: re-running a batch produces the same result, so a crash halfway is a
  restart, not a cleanup.
- Recorded: which ranges are done, so it resumes rather than starting over.
- Verified: counts and a checksum or sample comparison between old and new shapes,
  per batch, not only at the end.

## Moving data between stores or services

- **Avoid dual writes from application code** to two stores without a transaction
  across them: one write fails, and they diverge silently. Prefer writing once and
  propagating (an outbox table read by a relay, or change-data capture), so the second
  store is derived and can be rebuilt.
- **Name one owner** for each piece of data at every point in the migration. Two
  services that can both write the same row need a rule for conflicts, or they will
  have conflicts.
- **Reconcile continuously** during the migration: a job that compares the two stores
  and reports differences, so divergence is caught in hours, not at cut-over.
- **Cut over by reading**, not by writing: switch readers to the new store first, keep
  writing to the old as the source, then move the source of truth.

## Before any destructive step

- A tested backup or snapshot, restored at least once into a scratch environment.
- The exact rows or paths that will change, counted, shown to the decision owner, and
  approved.
- A note of what rollback can and can't restore (for example: the schema can be
  restored, rows written since the cut-over can't).

## Online schema changes

- Know which operations lock the table on your database and version (adding a column
  with a default, adding an index, changing a type). Use the database's online method
  or a tool built for it (for example `CREATE INDEX CONCURRENTLY` in PostgreSQL, or
  gh-ost or pt-online-schema-change for MySQL).
- Set a lock timeout so a migration that can't get its lock fails fast instead of
  queueing every query behind it.

## Data that needs care in any design

| Kind | What to decide |
|---|---|
| Money | Integer minor units or decimal type, currency per value, rounding rule and where it applies |
| Time | UTC storage, the user's zone for display, what "end of day" means and in which zone |
| Personal data | Where it lives, who can read it, retention, how a deletion request reaches every copy and backup |
| Identifiers | Who generates them, whether they're guessable, whether they leak volume (sequential order numbers) |
| Derived data | Its source, how it's rebuilt, and how stale it may be |
