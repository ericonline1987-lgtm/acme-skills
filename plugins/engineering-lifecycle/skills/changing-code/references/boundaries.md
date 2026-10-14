# Changes that cross a boundary

Read this when the change touches something other code depends on: a shared function or
type, a public API, a config key or schema, a dependency between modules, a file that
exists in several repositories, or a setup or migration step that runs more than once.

## 1. Map the boundary before touching it

- Name the entry point, every caller you found, who owns each side, and any generated or
  synced copies.
- Classify the change: local, shared within the module, cross-module, cross-repository.
  The wider the class, the stronger the case needed for doing it now.
- Prefer a change at the edge (the one caller that needs new behaviour) over a change to
  the shared core. If it must be shared, say who else is affected and how you checked.

## 2. Keep dependencies pointing inward

- Interfaces (UI, CLI, HTTP handlers) depend on application code; application code
  depends on domain code; infrastructure (databases, queues, vendors) sits behind an
  adapter. A change that makes domain code import infrastructure is a design change:
  raise it rather than slip it in.
- No new abstraction until there are two real users or a boundary problem it solves.
  Name the users.
- Reuse what the project already has (helpers, fixtures, UI components, test harnesses).
  Search before writing; a second copy of an existing helper is a defect.

## 3. Copies across repositories

If the same file lives in several repositories (vendored, generated, or synced), find the
single upstream, fix it there, and let the sync carry it. Patching one copy creates drift
that the next sync silently undoes or doubles.

## 4. Splitting a module that does too much

Split along responsibilities that already exist in the code (a parser, a client, a
policy), not by line count. Leave generated files, data and vendored code alone. Move
first, change behaviour in a later commit, so each diff is reviewable.

## 5. Contracts: config, schema, workflow

For each contract change, write down:

| Question | Example answer |
|---|---|
| Default when the new value is absent | Old behaviour; logged once |
| What happens on a bad value | Fail at startup with the key name (fail closed) |
| Migration needed? Who runs it, in what order? | Yes; runs before the deploy, idempotent |
| Rollback path | Previous release reads the new field and ignores it |

## 6. Steps that run more than once must converge

Setup, provisioning, sync and migration steps must be idempotent: running twice gives
the same result as running once. Apply only the missing difference, remove what should
no longer exist, and never duplicate. Test by running it twice in a row.

## 7. Shared infrastructure has a resource budget

Anything that runs on shared or production machines must bound its CPU, memory, disk
and I/O, back off under pressure, and be safe to stop midway. State the expected
footprint in the change description.

## 8. Read-only helpers stay read-only

When audits or searches are delegated to helper agents, record each repository's state
first (`git rev-parse HEAD`, `git status --short`), give them read-only instructions,
apply their findings yourself, and afterwards confirm nothing changed, was committed or
was pushed under your name.

## 9. Before calling it done

Re-read the full diff for circular dependencies, a public surface that grew by accident,
and ownership that is now unclear.
