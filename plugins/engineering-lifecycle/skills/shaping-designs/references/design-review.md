# Blast radius, challenge and the decision record

Read this before calling a design complete, and when reviewing someone else's.

## Blast radius

For a design that moves, splits, merges, retires or upgrades a running component, mark
every row affected, not affected, or unknown. An unknown names who can answer it; if the
code or data at hand can answer it, answer it yourself before listing it as a question.

| Row | Question | Evidence that answers it |
|---|---|---|
| Entry routes | Which gateway routes, prefixes and allow-lists reach it, and which change? | Gateway and ingress config |
| Per-environment config | Which keys differ by environment, and where do they live? | Config repo diff across environments, rendered values |
| Storage and shared volumes | What does it mount or own, and who else uses that? | Manifests, mount lists, database grants |
| Jobs and monitoring | Which crons, probes, dashboards and alerts name it? | Monitoring and scheduler config |
| Replicas and consistency | With more than one instance, how do caches, files and notifications stay consistent? | Replica counts, refresh paths |
| Upgrade and rollback | Does it survive a skipped version? What is the rollback unit? | Upgrade scripts, migration order, bundle definition |
| Other teams | What must another team do, by when, and what blocks if they don't? | Interface inventory, owners |
| External callers | Who outside the design calls it, and what do they see after? | Access logs with a same-period baseline |

## Challenge the recommendation

- State the strongest case for the option you'd reject, the likeliest way the chosen
  one fails once built, and the evidence that would overturn it. Aim first at claims
  graded inferred or unverified. A list of risks with mitigations is not a challenge.
- Rule on every objection: adopted (and the design changed), rejected with evidence, or
  open with who decides. One that would reverse a decision the person made goes to
  them, not into the design.
- **Independent challenge** when undoing the change wouldn't undo its effects (data
  rewritten, other teams acting, money spent, the rollback unit wider than the change):
  give a reviewer who hasn't seen the discussion only the constraints, the target, the
  design and its evidence, and ask how it fails, not whether it's good. A reviewer who
  watched the design form is not independent; if none is available, say so.
- Each mitigation says when it fires, what it checks, and what happens when the check
  fails. Naming a technique ("we'll add a circuit breaker") is not a mitigation.

## Completeness check

| Before calling it complete | Passes when |
|---|---|
| Constraints | Every row has a source |
| Inventory (changes to a running system) | Every item has evidence; every "dead" has a baseline; a replaced mechanism's effects are listed by mechanism, each loud or silent |
| Target | One sentence, with the deployment model it assumes |
| Interfaces, data, failure modes | Each has its reference checklist answered or marked not applicable |
| Blast radius | Every row marked; every unknown has an owner |
| Claims | Every load-bearing claim graded observed, inferred or unverified |
| Challenge | Done and every objection ruled on; independent when reversal is hard, or the report says it wasn't |
| Open decisions | Listed with who decides |
| First step | Named, small, and it proves the direction |

A design missing a row is reported incomplete, not padded. A "no gaps" verdict names
what was enumerated and how: a search for missing topics can't find a class nobody
listed, and a reviewer told earlier rounds passed leans toward finding nothing.

## Decision record

Keep it beside the code (for example `docs/decisions/NNNN-title.md`):

```
# Decision: <title>
Context: <situation and constraints, with dates and sources>
Options: <each in a line, including the one not chosen and "do nothing" if real>
Decision: <what, and who decided>
Why: <evidence, each claim graded>
Consequences: <what gets easier, harder, and what must now stay true>
Revisit when: <the signal or date that reopens it>
```

## Reviewing someone else's design

Read it as the implementer and as the on-call engineer. For each section ask the
question it must answer, and record each gap with the row above it belongs to:

- Problem: could someone else state it and its measure from the doc alone?
- Options: were real alternatives compared on the same fields, including doing less?
- Interfaces and data: is every change additive, and is the migration stepwise?
- Failure: what happens when each dependency is slow, down or wrong?
- Rollout: what's the smallest first step, and how is each stage undone?
