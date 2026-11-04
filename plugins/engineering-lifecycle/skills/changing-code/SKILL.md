---
name: changing-code
description: Use this skill whenever someone wants existing code changed, fixed or tested — a bug, a failing or flaky test, something broken or slow, an incident, a default or signature change, a rename, an upgrade, a refactor, new tests — even one line. It diagnoses before fixing, reads git history and every caller, makes the smallest change, and writes tests that fail for the right reason.
---

# Changing code

Existing behaviour is often deliberate. The goal is a change that is correct, contained,
and leaves the next person understanding more than you did when you started.

## If something is broken right now

When people are affected, before any diagnosis: mitigate (roll back the last deploy,
turn the flag off), name who leads and who updates the people affected, and keep a
timeline with times as you go. Afterwards, a blameless review: impact, timeline, cause
with its evidence, and actions each with one owner and a date. Then find and prove the
cause with `references/diagnosis.md` before changing code.

## Before the change

1. **Find out why the current code exists.** Use `git log -S "<value>"`, `git log -L`
   or `git blame` on the exact lines. A past commit may have fixed the very thing a
   failing test now asks you to undo. Without history, reconstruct intent from callers,
   tests, schemas and docs, and say that history was unavailable.
2. **Treat the symptom as a lead, not the spec.** A failing test, a bug report or
   another agent's diagnosis says where to look. Decide direction from history and the
   real contract: if the code is a later deliberate decision, the test is stale; update it.
   Whichever way you go, the commit message says why and cites the evidence (the commit
   or issue that made the test stale, or that shows the code regressed).
3. **Confirm the cause** with two independent lines of evidence (a reproduction and a
   trace, or a trace and the code path) before a non-obvious or large fix. If the cause
   isn't known yet, or something is broken, slow or flaky, diagnose it first with
   `references/diagnosis.md`; if people are affected now, that starts with mitigation.
4. **Find every caller.** Grep the symbol, config key, route or path as a literal string
   across code, scripts, manifests, docs and other repos you can reach. Check ignore
   rules didn't hide directories from the search.
5. **Choose the scope**: never a special case for the reported example; a general rule
   inside the component you own; never a new obligation on teams you don't control
   without asking.
6. **Stop before speculative abstraction.** Asked to extract a shared abstraction, base
   class or framework that only one place uses today? Say so first: with one user you'd
   be guessing at the others' needs. Recommend keeping it local (or extracting only what
   that one user needs, in place) until a second real user appears, and name what would
   justify extracting. Build the general version only if the person still wants it.

## The change

- Make the smallest change that meets the outcome, in the local style. No speculative
  options, unrelated cleanup, or new abstractions with one user.
- Keep refactoring and behaviour changes in separate commits.
- Upgrading a dependency: read its changelog for every version you skip, move one major
  version at a time, run the full tests, and read the lockfile diff for unexpected
  transitive changes.
- Remove only code your change made dead.
- **Leave it more legible**: a comment saying *why* where the reason isn't obvious, a
  test that pins the behaviour, and a decision note when you chose between real options.
- **Tests** follow `references/tests.md`: one behaviour each, outcomes not internals,
  mocks only at boundaries, and each shown to fail without the change.

## After the change

- Run the narrowest check that could fail, plus the tests of every caller you found,
  and compare with the same tests before the change ("no new failures").
- Claim only what you checked: tests passing is not deployed, and deployed is not
  working for users. Say which you reached.
- Re-review any fix that came out of a review round; fixes create new decisions.

## Load more only when the change needs it

- Touches a shared function, public API, config or schema, module dependencies, a file
  copied across repositories, or a step that runs more than once: read
  `references/boundaries.md`.
- Involves formatting, naming, input validation, config file syntax, comments, or
  deleting a test or guard: read `references/style-and-validation.md`.

## Stop and ask when

- History shows the code sits on an unresolved design, security or contract decision.
- The fix is large, crosses team boundaries, or the cause isn't confirmed.
- You find changes in the working tree you didn't make. They are the person's until
  proven otherwise; never restore or clean them without asking.
