# Requirements

Read this when the work starts from a feature idea, a request, a thread or a ticket, or
when someone asks for a PRD section, user stories or acceptance criteria.

## Problem before feature

- State the problem in one sentence with no solution words: who has it, what it is, why
  now. "Add a button" is a solution; "returning customers can't find past orders" is a
  problem. If you can't write it, ask before writing anything else.
- Define success as an outcome with a measure: the metric or observable behaviour, its
  current value (or TBD with an owner who can get it), the target, and when it's checked.
  The measure should tell you, after launch, whether this was worth building.
- Name the decisions that stay with the person: scope changes, trade-offs between stated
  goals, anything irreversible or that commits money, people or reputation.

## Stories and acceptance criteria

One story per distinct goal:

```
As a <type of user>, I want <capability>, so that <outcome>.

Given <starting state> when <action> then <observable result>
Given ... when ... then ...
```

- Each criterion is checkable by someone who didn't write it, against something they
  can observe. "Fast" is not a criterion; "results appear within 2 s at p95 for an
  account with 10,000 orders" is.
- At least one criterion per story covers a failure or edge case. The ones teams miss:
  empty state, very large inputs, concurrent edits, the action done twice, a slow or
  failed dependency, a user without permission, a deleted or merged account, and time
  zones around midnight.
- For anything security-sensitive, criteria that say what must *not* happen ("the reset
  page responds the same whether or not the address has an account").

## Non-functional needs that apply

Performance (with numbers and load), availability, security and privacy (what data,
who sees it, retention), accessibility, auditability, and for AI features the quality
threshold and how it's evaluated (`ai-features.md`).

## Scope

- At least one line of what's out of scope, naming the tempting thing.
- The riskiest assumption and the cheapest way to test it before building: a prototype,
  a fake door, a manual pilot, a spike. When the outcome is uncertain, that test is the
  first deliverable.
- Open questions, each with an owner.

## Sections

Problem → Success measure → Users → Stories with acceptance criteria → Non-functional
→ Out of scope → First test → Open questions.
