---
name: reviewing-code
description: Always use this skill when someone shares code, a diff, a patch or a pull request and wants any opinion on it ("review this", "is this OK", "anything wrong", "look over my changes"), even a few lines that look fine. It finds the failures tests by the same author miss (ties, retries, races, stale caches, broken contracts, undone fixes), proves each, and shows how to make the change excellent.
---

# Reviewing code

The goal of a review is a change that works for every caller, input and interleaving,
and that the team is glad to own a year from now. A senior reviewer gets there by
showing the failure that passes the author's own tests (the input, interleaving or
deploy order that breaks it) and then the best version of the change.

## 1. Hunt the failures tests miss

For each area the diff touches, work through these classes, then the fuller table in
`references/defect-classes.md` whenever the diff touches data access, money, time,
concurrency, caching, an API or a migration.

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
  another. What is charged, granted or refunded comes from the source of truth at that
  moment, never from a cached value.
- **Contracts.** Callers outside the diff: public API clients, mobile apps that never
  update, stored data, other services. A change of name, order, default, error code or
  identity is a design change; review it as one.
- **Project rules.** Read the rules files (CLAUDE.md, AGENTS.md, REVIEW.md,
  CONTRIBUTING.md) in the root and in each changed file's directories; a rule applies
  under its directory. A violation quotes the rule and names its file.
- **History.** `git log -L` on changed lines: does this undo a past fix?
- **Tests.** Would a test fail if the change were reverted? Which case is untested?

## 2. Prove what you report

A finding the author can't reproduce costs every other finding its credibility, so
prove each one: re-read the cited code and follow the path, or run it. With helper
agents, give each finding to one that didn't find it, with only the claim and the code.
What you suspect but couldn't prove goes under "Worth checking" with the test or
command that would settle it.

## 3. Report, most important first

- **Blocking**, then **Should fix**: file and line, the concrete failure (the input or
  sequence that triggers it and what the user sees), and the fix. Give a ready-to-apply
  patch when you can make it complete, tests included.
- **Make it better**: the improvements a senior engineer would make to this change (a
  simpler design, a missing test, a clearer contract, a cheaper query), each with why.
- **Worth checking**: suspicions not yet proven, each with how to settle it.
- **Already there**: serious problems the change didn't introduce but sits next to, one
  line each, so they aren't lost.
- **Not checked**: what you couldn't verify (didn't run, couldn't see callers).
- End with merge, merge after fixes, or don't merge yet. Name who must approve when the
  person asks or the change touches money, auth, data deletion or release tooling.

Spend the reader's attention on findings and fixes; how you organised the review stays
in your head. Leave formatting nits to the linter.

## Re-reviews

From the second round, start from what changed and check that each earlier finding is
really fixed everywhere; say "still open" instead of repeating it. Name the bug class so
all instances get fixed. If confirmed blocking findings keep appearing at round three,
say the approach may be wrong and propose the one that would hold.

## Check before you send

Read the report as the author: would every finding reproduce, would every fix work, and
is the most dangerous problem the first thing they see?

## Works with

`making-visuals` for how a rendered page looks or whether it is accessible;
`merging-safely` for merges; `changing-code` for making the fixes.
