---
name: writing-requirements
description: Turn a feature idea, ticket, or conversation into clear requirements and user stories with acceptance criteria. Use when someone asks for requirements, a PRD section, user stories, or acceptance criteria.
---

# Writing requirements

## Process
1. **Find the problem first.** Write one sentence: who has the problem, what it is, and why it matters now. If you can't, ask before writing anything else.
2. **List users and goals.** Name each user type and what they're trying to get done.
3. **Write user stories** using `templates/user-story.md`. One story per distinct goal.
4. **Add acceptance criteria** in Given / When / Then form. Each criterion must be testable by someone who didn't write it.
5. **State what's out of scope.** At least one line. Unstated scope is where projects slip.
6. **List open questions** with an owner for each, rather than guessing.

## Quality bar
- No solution language in the problem statement ("add a button" is a solution; "users can't find X" is a problem).
- Every "should" is measurable or removed.
- Non-functional needs (performance, security, accessibility) are called out when they apply.

## Output
Markdown with sections: Problem, Users, Stories, Acceptance criteria, Out of scope, Open questions.
