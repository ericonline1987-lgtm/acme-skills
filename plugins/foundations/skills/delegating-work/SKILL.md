---
name: delegating-work
description: Write standalone briefs for AI agents, subagents or people taking part of a task, and accept their results only after independent checks. Use whenever work is split across agents or teammates, handed to a contractor or another session, or someone's "done" needs checking before it is trusted.
---

# Delegating work

A worker's "done" is a claim. Delegation succeeds when the brief makes the right result
easy and the acceptance makes a wrong one visible.

## Decide what to delegate

- Delegate work that is well-specified, independent, and checkable. Keep work that needs
  the conversation's full context or the person's judgment.
- Split along boundaries that don't share files or state, so parallel workers can't
  collide. When they must touch the same thing, sequence them.
- Each piece needs its own acceptance check. If you can't say how you would check it,
  it isn't ready to hand off.

## Brief

Use `../../shared/templates/delegation-brief.md`. The brief must stand alone: the worker
has none of your context. Include:

- **Outcome** and why it matters, so the worker can make sensible local calls.
- **Permissions**: what it may do, and what needs asking first (pushing, deleting,
  sending, spending, contacting people). Research and audit workers are read-only.
- **Done when**: observable criteria you will check yourself.
- **Out of scope**: at least one tempting thing not to do.
- **Report back** format: result, evidence per criterion, what was not checked.

## Accept

1. **Re-run the decisive check yourself.** Read the diff, run the test, open the file,
   follow the link. A worker's summary, screenshot or exit code is a lead, not evidence.
2. **Check each criterion in the brief**, one line each: met (with evidence), not met, or
   not checkable (and why).
3. **Check side effects.** Nothing committed, pushed, sent or deleted beyond the
   permissions; no unrelated changes.
4. **Check usability end to end.** The person can actually use the result: it builds,
   it's where they expect it, and how to use it is written down.
5. **Rule on disagreements with evidence.** If a worker contradicts a decision the person
   already made, raise it; don't apply it.

## Report

```
piece: <name> | worker: <who> | criteria met: <n/m> | evidence: <checks you re-ran>
side effects: <none | list> | not checked: <list> | status: accepted / returned / escalated
```

Accepted here means accepted by you. The person's acceptance is a separate, higher rung
(see `proving-outcomes`).
