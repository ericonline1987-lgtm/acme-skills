---
name: changing-code
description: Changes existing code so the cause is fixed and nothing else breaks — diagnoses first, reads git history and every caller, writes tests that fail for the right reason. Use whenever someone wants code changed, fixed or tested (a bug, a failing or flaky test, something broken or slow, an incident, a signature or default change, a rename, an upgrade, a refactor), even one line.
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
   or issue that made the test stale, or that shows the code regressed). Case: answers
   that found the test stale cited the commit, but when the code had regressed they
   restored it with no reason recorded, leaving the next reader the same puzzle.
3. **Confirm the cause** with two independent lines of evidence (a reproduction and a
   trace, or a trace and the code path) before a non-obvious or large fix. If the cause
   isn't known yet, or something is broken, slow or flaky, diagnose it first with
   `references/diagnosis.md`; if people are affected now, that starts with mitigation.
4. **Find every caller.** Grep the symbol, config key, route or path as a literal string
   across code, scripts, manifests, docs and other repos you can reach. Check ignore
   rules didn't hide directories from the search.
5. **Choose the scope that fixes the class, not the example**: a general rule inside
   the component you own, covering every caller you found. A new obligation on teams you
   don't control is their decision; propose it to them.
6. **Design abstractions from real users.** Asked for a shared abstraction, base class
   or framework that only one place uses today? An abstraction designed from one user
   guesses at the others' needs, so say so, then build the version that serves the real
   user best (often local first, with the seam where a second user would plug in), and
   name what would justify extracting further. If the person still wants the general
   version, build it well.

## The change

- Make the change that fully meets the outcome, in the local style, and nothing that
  hides it in the diff: other improvements you spot go in their own commit or a note.
- Keep refactoring and behaviour changes in separate commits.
- Upgrading a dependency: read its changelog for every version you skip, move one major
  version at a time, run the full tests, and read the lockfile diff for unexpected
  transitive changes.
- Remove the code your change made dead; list other dead code you found for the person.
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
- Before you hand it over, read the diff as its next maintainer: is the cause fixed, is
  every caller safe, and would the tests catch this coming back?

## Go deeper when the change needs it

- Touches a shared function, public API, config or schema, module dependencies, a file
  copied across repositories, or a step that runs more than once: read
  `references/boundaries.md`.
- Involves formatting, naming, input validation, config file syntax, comments, or
  deleting a test or guard: read `references/style-and-validation.md`.

## Ask first when

- History shows the code sits on an unresolved design, security or contract decision.
- The fix is large, crosses team boundaries, or the cause isn't confirmed.
- You find changes in the working tree you didn't make. They are the person's until
  proven otherwise; never restore or clean them without asking.
