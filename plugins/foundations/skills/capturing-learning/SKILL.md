---
name: capturing-learning
description: Turn a repeated mistake, correction or lesson into a checkable rule placed where it is enforced — an eval or test case, an automated check, or a proposed skill or instruction change. Use whenever someone says a problem keeps happening, asks how to stop it recurring, or corrects how an agent behaved.
---

# Capturing learning

A team compounds when each task leaves the next one easier. Most lessons die in a chat
transcript; this skill puts them where they will be used.

## When to run

- At the end of substantial work (one quick pass, not a retrospective).
- Immediately after a failure, an overclaim, or a person correcting the agent.
- When the same question, fix or explanation appears a second time.

## Process

1. **State the lesson in one sentence** as a rule someone could follow: "Check the
   deployed image tag, not the release name, before claiming rung 2." Not "be careful".
2. **Decide where it belongs:**

   | Lesson type | Destination |
   |---|---|
   | An agent behaviour that went wrong or right | An eval case (step 3), then a skill change |
   | Why a choice was made | A decision record: `../../shared/templates/decision-record.md` |
   | A fact about this codebase or team | The project's own docs or agent instructions file |
   | A recurring multi-step procedure | A new skill, proposed to the person |
   | A one-off | Nothing. Say so. |

3. **Test before you change.** For an agent behaviour, write the case first so the fix is
   measurable:
   `python3 scripts/add_eval_case.py --plugin-dir <plugin> --name <case> --prompt "..."
   --criteria "..." --criteria "..." --skill <skill> --source "<what happened, when>"`,
   one `--criteria` per observable thing a good answer does.
   Use `--should-not-fire` when the lesson is that a skill triggered where it shouldn't.
   Then change the skill and run `claude plugin eval <plugin> --case <case>`.
4. **Keep the person in charge.** Propose changes to shared skills, docs and instruction
   files; don't apply them silently. Say what changes for future tasks.
5. **Record it in the hand-off** under "Learned", with where it went.

## Quality bar

- The lesson is specific enough to fail a test.
- Each lesson has exactly one home; no duplicate copies that drift.
- Removed or wrong guidance is deleted, not left beside the correction.
