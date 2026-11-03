---
name: running-long-tasks
description: Always use this skill when work will run long, unattended or against a budget — an overnight or multi-hour job, a batch over many items, many paid API or model calls, "keep going while I'm away", or a usage or rate limit that stopped the work — even if it looks quick. It sets a budget and stop rules, checkpoints so work survives interruption, resumes without duplicating, and reports spend.
---

# Running long tasks

Long work fails in the middle. Plan for the interruption, not the happy path.

## Before starting

- **Estimate size and cost** from a trial: items × cost per item, as a range. If it is
  more than the person is likely to expect, say so before starting.
- **Agree stop rules**: a cost ceiling, a time limit, and an error signal that means
  something is wrong (for example five failures in a row). Anything irreversible still
  needs a go-ahead (see `guarding-agent-actions`).
- **Trial a few items** and read their results before launching the rest. A bad prompt
  or a wrong path costs ten items, not ten thousand.

## While it runs

- **Checkpoint each item** as it finishes: id, status, and where its result is. A
  restart then skips finished work. Make items safe to redo, or check before redoing.
- **Run it detached** with its own log, so it outlives a session, and have it report
  every way it can end: finished, failed, stopped at the ceiling, hung.
- **On a usage or rate limit**, stop cleanly: record where you stopped, schedule or plan
  the resume for after the reset, and tell the person. Never retry in a tight loop, and
  never switch credentials or route around a limit.
- **Discard results an interruption cut short.** Empty or partial outputs are re-run,
  never counted, and never scored as failures.
- **Save progress where the person can reach it** (committed, uploaded or sent), not
  only in a scratch folder that may disappear.

## Keep the person informed

Keep a visible progress line or task list: done, running, left, and spend so far. Report
a blocking problem or a change of direction when it happens, not at the end.

## Finish

- **Reconcile**: every input item is accounted for as done, failed with a reason, or
  skipped with a reason, and the counts add up to the input.
- **Report spend** against the estimate and the ceiling, and explain any large gap.
- **Clean up** background processes, temporary files and scheduled resumes nobody needs.

## Report

```
items: <done> done, <failed> failed (reasons), <skipped> skipped, of <total>
spend: <actual> against estimate <range> and ceiling <amount>
interruptions: <what stopped it, how it resumed, what was re-run>
results: <where>   left behind: <processes, files, schedules, or none>
```
