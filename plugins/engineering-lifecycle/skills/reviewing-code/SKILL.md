---
name: reviewing-code
description: Always use this skill when someone shares code, a diff, a patch or a pull request and wants any opinion on it — "review this", "is this OK", "anything wrong", "look over my changes" — even a few lines that look fine at a glance. It finds the failures tests by the same author miss (ties, retries, races, stale caches, broken contracts, undone fixes) and confirms each one before reporting it.
---

# Reviewing code

A capable model already reads diffs carefully. What a senior reviewer adds is the
failure that passes the author's own tests: the input, interleaving or deploy order that
breaks the change, shown concretely. Report only what you can show; a false finding
costs every later finding its credibility.

## 1. Find the failures tests miss

For each area the diff touches, check the classes below, then the fuller table in
`references/defect-classes.md` (open it whenever the diff touches data access, money,
time, concurrency, caching, an API or a migration).

- **Ordering and ties.** A cursor or "since" filter on a non-unique column (timestamps
  written in one transaction share `now()`) skips or repeats rows; key on
  `(column, id)`. Rows from transactions that commit late appear behind a cursor that
  already passed them. Fetch one extra row to know whether a next page exists.
- **Retries and timeouts.** A retry around a call with side effects (charge, email,
  write) repeats them unless an idempotency key is sent and honoured. A client timeout
  shorter than the server's work turns success into a retry.
- **Races.** Check-then-act, read-modify-write without a version, a lock held across a
  network call, async work not awaited.
- **Caches and derived values.** A key missing a dimension serves one user's data to
  another. A cached value must never decide money or access: what is charged, granted or
  refunded is read from the source of truth at that moment.
- **Contracts.** Callers outside the diff: public API clients, mobile apps that never
  update, stored data, other services. A change of name, order, default, error code or
  identity is a design change; review it as one.
- **Project rules.** Read the rules files (CLAUDE.md, AGENTS.md, REVIEW.md,
  CONTRIBUTING.md) in the root and in each changed file's directories; a rule applies
  only under its directory. A violation quotes the rule and names its file.
- **History.** `git log -L` on changed lines: does this undo a past fix?
- **Tests.** Would a test fail if the change were reverted?

## 2. Confirm before you report

Re-read the cited code and follow the path, or run it. With helper agents, give each
finding to one that didn't find it, with only the claim and the code. Drop anything
unconfirmed; if you couldn't verify something, say so instead of guessing.

Don't report: problems that existed before the change (one line under "Noticed, out of
scope" if serious), style or anything a linter enforces, generic advice with no specific
failure behind it, issues deliberately silenced with a reason.

## 3. Report

- **Blocking**, then **Should fix**, each with file and line, the concrete failure
  (the input or sequence that triggers it and what the user sees), and the fix. Give a
  ready-to-apply patch only when it fixes the problem completely.
- **Suggestions**: a few improvements specific to this change that a senior reviewer
  would raise, each one line.
- **Not checked**: what you couldn't verify (didn't run, couldn't see callers).
- End with merge, merge after fixes, or don't merge yet. Add who must approve only when
  the person asks or the change touches money, auth, data deletion or release tooling.

Keep process out of the report: no tiers, pass names or checklists, only findings.

## Re-reviews

From the second round, review only what changed. Never repeat a finding; say "still
open". Name the bug class so all instances get fixed. If confirmed blocking findings keep
appearing at round three, say the approach may be wrong.

## Not this skill

How a rendered page looks or whether it is accessible: `making-visuals`. Merges:
`merging-safely`. Making the change: `changing-code`.
