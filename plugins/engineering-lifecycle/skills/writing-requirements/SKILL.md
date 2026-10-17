---
name: writing-requirements
description: Use this skill whenever someone asks for requirements, a PRD section, user stories, acceptance criteria or a spec, or wants a feature idea or thread turned into something a team can build. It starts from the problem and a measurable success outcome, then writes stories with testable Given/When/Then criteria, edge cases, privacy needs and what is out of scope.
---

# Writing requirements

Requirements exist to make the right thing get built. Start from the change the feature
should cause, not from the feature.

## Process

1. **State the problem in one sentence**: who has it, what it is, and why now. No
   solution words ("add a button" is a solution; "returning customers can't find past
   orders" is a problem). If you can't write it, ask before writing anything else.
2. **Define success as an outcome with a measure**: the metric or observable behaviour,
   its current value if known, the target, and when it will be checked. This is the
   feature's outcome contract (see `defining-done` if installed). Unknown baselines are
   written TBD with an owner, never guessed.
3. **Name users and their goals.** One line per user type.
4. **Write user stories** with `templates/user-story.md`, one per distinct goal.
5. **Write acceptance criteria** as Given / When / Then. Each must be checkable by
   someone who didn't write it, and at least one per story covers a failure or edge case.
6. **Cover non-functional needs that apply**: performance, security and privacy,
   accessibility, and for AI features, quality thresholds and how they are evaluated
   (see `building-ai-features`).
7. **State what's out of scope.** At least one line.
8. **Find the cheapest test of the riskiest assumption** — a prototype, a fake door,
   a manual pilot — and list it as the first step when the outcome is uncertain.
9. **List open questions** with an owner each.

## Quality bar

- The success measure would tell you, after launch, whether this was worth building.
- Every "should" is measurable or removed.
- Each acceptance criterion maps to a story; each story maps to the problem.

## Output

Markdown with sections: Problem, Success measure, Users, Stories, Acceptance criteria,
Non-functional, Out of scope, First test, Open questions.
