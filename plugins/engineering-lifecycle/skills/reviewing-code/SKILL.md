---
name: reviewing-code
description: Review a diff or pull request for whether it achieves its intent safely — correctness, security, callers and history, tests that would catch a regression — with comments grouped by severity and a clear verdict. Use whenever someone shares a diff, PR, patch or snippet and asks for a review, feedback, "is this OK" or "any issues".
---

# Reviewing code

A review answers one question: should this change go in as it is? Every comment should
help answer it.

## Process

1. **Understand intent.** Read the description and linked issue; restate the change's
   outcome in one sentence. If you can't, ask before reviewing.
2. **Check it achieves the intent.** Logic, edge cases (empty, null, huge, concurrent,
   repeated), error handling, and what happens when a dependency fails.
3. **Check what it touches.** Grep callers of every changed signature, config key or
   contract. Check history on lines whose behaviour changed (`git log -L`) for a past
   fix being undone.
4. **Check security and data.** Input validation, injection, authorisation, secrets in
   code or logs, personal data handling, unsafe deserialisation, new dependencies.
5. **Check the tests.** Would a test fail if the change were reverted? Are the edge
   cases from step 2 covered? Do tests assert behaviour, not implementation?
6. **Check legibility.** Names, size, dead code, and comments that explain *why*. Is a
   non-obvious decision recorded?
7. **Verify, don't trust.** Run the tests or the change when you can, and say whether
   you did.

## Comments

Group by severity, each with file and line:

- **Blocking** — bugs, security issues, missing tests for new behaviour, undone past fixes.
- **Should fix** — problems that will cost time later.
- **Nit** — optional; label it.

Each comment: what's wrong, why it matters, and a concrete fix (a snippet when short).
Comment on the code, not the author. Note one genuinely good thing when there is one.

## Verdict

End with: **approve**, **approve with nits**, or **request changes**, plus what you
verified yourself (ran tests, ran the code, read only) and what you didn't check.

## Re-reviews

Review the fixes from the previous round as new changes. A fix that changes a name,
an order, an identity or a concurrency property is a new design decision.
