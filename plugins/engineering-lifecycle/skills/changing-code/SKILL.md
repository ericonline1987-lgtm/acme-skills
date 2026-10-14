---
name: changing-code
description: Change existing code safely — learn from git history why it is the way it is, treat failing tests and bug reports as leads not specs, check every caller, make the smallest change, record why. Use whenever someone asks to fix a bug or failing test, change a default or config value, refactor, or "just change X" in existing code.
---

# Changing code

Existing behaviour is often deliberate. The goal is a change that is correct, contained,
and leaves the next person understanding more than you did when you started.

## Before the change

1. **Find out why the current code exists.** Use `git log -S "<value>"`, `git log -L`
   or `git blame` on the exact lines. A past commit may have fixed the very thing a
   failing test now asks you to undo. Without history, reconstruct intent from callers,
   tests, schemas and docs, and say that history was unavailable.
2. **Treat the symptom as a lead, not the spec.** A failing test, a bug report or
   another agent's diagnosis says where to look. Decide direction from history and the
   real contract: if the code is a later deliberate decision, the test is stale.
3. **Confirm the cause** with two independent lines of evidence (a reproduction and a
   trace, or a trace and the code path) before a non-obvious or large fix.
4. **Find every caller.** Grep the symbol, config key, route or path as a literal string
   across code, scripts, manifests, docs and other repos you can reach. Check ignore
   rules didn't hide directories from the search.
5. **Choose the scope**: never a special case for the reported example; a general rule
   inside the component you own; never a new obligation on teams you don't control
   without asking.

## The change

- Make the smallest change that meets the outcome, in the local style. No speculative
  options, unrelated cleanup, or new abstractions with one user.
- Keep refactoring and behaviour changes in separate commits.
- Remove only code your change made dead.
- **Leave it more legible**: a comment saying *why* where the reason isn't obvious, a
  test that pins the behaviour, and a decision note when you chose between real options.

## After the change

- Run the narrowest check that could fail, plus the tests of every caller you found,
  and compare with the same tests before the change ("no new failures").
- Prove it at the rung you'll claim (see `proving-outcomes` if installed).
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
