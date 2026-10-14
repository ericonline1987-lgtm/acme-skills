---
name: defining-done
description: Turn a request into an outcome contract before building — the observable result, how success is measured, what is out of scope, and which decisions stay with the user. Use whenever someone asks to start, build, set up or "help me get started on" a tool, feature, project or process, especially one touching money, customers or data.
---

# Defining done

Most rework comes from finishing the wrong thing well. Spend a minute up front on
the outcome, not the output.

## Process

1. **Name the outcome, not the deliverable.** "Customers stop abandoning checkout at the
   payment step" is an outcome; "a PR that fixes the timeout" is a deliverable. Ask
   "so that what?" until the answer is something someone could observe in the world.
2. **Name the evidence.** What would show the outcome happened: a metric and threshold,
   a person's confirmation, a behaviour seen in real use. If nothing could show it, the
   outcome is too vague; sharpen it.
3. **Set the follow-up.** Outcomes often lag delivery. Write down when the evidence will
   be checked, how, and by whom. "None" is allowed with a reason (for example, a
   one-off reply whose outcome is the reply itself).
4. **Reserve the person's decisions.** List choices the agent must surface rather than
   make: scope changes, trade-offs between stated goals, anything irreversible, anything
   that commits money, people or reputation.
5. **Mark assumptions.** Each one is something that could be checked; say which.
6. **Confirm when it matters.** For quick, cheap-to-redo work, state the contract in one
   line and start. For expensive or irreversible work, get a yes on the contract first.

## Scale it to the task

| Task size | Contract |
|---|---|
| Small (minutes, easy to redo) | One sentence: outcome + how you will know |
| Medium (hours, or shared with others) | The template, briefly |
| Large or irreversible | The full template, confirmed before work starts |

Template: `../../shared/templates/outcome-contract.md`. Check a filled one with
`python3 ../../shared/scripts/check_sections.py <file> --template ../../shared/templates/outcome-contract.md`.

## Quality bar

- The outcome is observable by someone other than the author.
- At least one thing is explicitly out of scope.
- Every irreversible step is listed under decisions reserved for the person.
- No invented facts: unknowns are written as assumptions or TBD with an owner.

## Hand-off

The contract travels with the work. `proving-outcomes` checks the result against it, and
the hand-off report quotes its outcome line verbatim.
