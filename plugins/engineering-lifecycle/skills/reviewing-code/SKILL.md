---
name: reviewing-code
description: Review a diff, pull request, or file for correctness, security, readability, and test coverage, and give prioritized, actionable feedback. Use when someone asks for a code review, PR review, or feedback on code.
---

# Reviewing code

## Process
1. **Understand intent.** Read the PR description or ask what the change is meant to do.
2. **Check correctness first:** logic errors, edge cases (empty, null, large, concurrent), error handling.
3. **Check security:** input validation, injection, secrets in code, authz checks, unsafe deserialization.
4. **Check tests:** does a test fail if the change is reverted? Are edge cases covered?
5. **Then readability:** naming, function size, dead code, comments that explain *why*.

## Feedback format
Group comments by severity and point to file and line:
- **Blocking** — bugs, security issues, missing tests for new behavior.
- **Should fix** — maintainability problems likely to cost time later.
- **Nit** — style or preference; mark clearly as optional.

For each: what's wrong, why it matters, and a suggested fix (code snippet when short).

End with a one-line verdict: approve, approve with nits, or request changes.

## Tone
Comment on the code, not the author. Acknowledge one thing done well when it's genuine.
