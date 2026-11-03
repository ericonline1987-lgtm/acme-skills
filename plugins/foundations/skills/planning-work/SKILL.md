---
name: planning-work
description: Always use this skill when someone needs a plan, estimate or schedule — break this project down, how long will it take, what order should we do this in, a roadmap or milestones, can we hit the deadline — even a rough guess. It splits the work into checkable pieces, orders them by risk and dependency, estimates in ranges with their basis, and flags deadline risk early with options.
---

# Planning work

A plan is a bet on the order of work that surfaces problems soonest. An estimate is a
range with a reason, not a promise.

## Process

1. **Start from the outcome** (see `defining-done`): what done looks like, the
   deadline, and which is fixed, the date or the scope.
2. **Break the work down** until each piece has a done criterion someone else could
   check and fits in a day or two. A piece you can't break down is an unknown; list it.
3. **Map dependencies**: what blocks what, and what waits on other people (reviews,
   approvals, vendors, other teams, store or legal review). Lead times on other people
   are usually the critical path.
4. **Order by risk first.** Start with the piece most likely to change the plan: the
   unproven integration, the performance question, the sign-off, the blocked access.
   Use a short spike when only trying it will tell. Then follow dependencies, then value.
5. **Estimate each piece as a range with its basis**: likely and pessimistic, and what
   the estimate rests on (similar past work, a spike, a guess; say which). Count review,
   testing, deployment and waiting time. A sum of likely values is optimistic; give the
   total as a range with a confidence.
6. **Test against the deadline.** If the pessimistic end misses it, say so now and set
   out options: cut named scope, add people only where work truly splits, or move the
   date. The choice belongs to the person.
7. **Set check-in points**: milestones with an observable result, and the signal to
   re-plan (any piece at twice its range, a dependency that hasn't moved by a date).
8. **Name the first step**: the smallest piece that reduces the biggest risk and can
   start today.

## Output

```
Outcome and deadline: <what, by when, fixed date or fixed scope>
Pieces: | piece | done when | depends on | owner | estimate (likely–pessimistic) | basis |
Critical path: <chain, with waits on other people>
Risks and unknowns: <each with how and when it will be retired>
Deadline check: <fits | at risk — options for the person>
Milestones: <date — observable result>   Re-plan if: <signal>
First step: <today>
```

## Quality bar

- Every piece has a done criterion and an owner or "unassigned".
- No single-number estimate is presented as certain; every range has a basis.
- Waiting on other people is in the plan, not left out of it.
- Deadline risk is stated plainly, with options, at the start rather than discovered late.
