# AI features

Read this when the design includes a feature powered by a language model: a classifier,
assistant, retrieval pipeline, agent or prompt, or a choice of model for one.

Model output is probabilistic, so "it worked when I tried it" proves little. Treat
quality as something you measure on every change, like latency.

**Contents:** 1. Define quality before writing a prompt · Trust the eval before trusting its scores · 2. Design the context, not just the prompt · 3. Choose the model and effort on evidence · 4. Agents that run on their own · 5. Guard it · 6. Ship and watch · Report

## 1. Define quality before writing a prompt

- Write the outcome: what the user should be able to do, and the measure that
  shows it (task success rate, accuracy against a reference, time saved, escalation rate).
- **Build the eval set first**: 20–50 real inputs to start, drawn from actual use or
  realistic sources, covering common cases, edge cases, adversarial inputs and cases
  where the right answer is to refuse or ask. Add each production failure as a new case.
- Choose graders per criterion: exact or programmatic checks where possible, a model
  grader with a written rubric where judgment is needed, human review for a sample.
  One grader per criterion, not one pass/fail for the whole answer, so a disagreement
  points at something specific.
- Run every case several times; report rates with their spread, not single results.

## Trust the eval before trusting its scores

- **Check the grader.** Grade a sample by hand and compare. A small judge model, or a
  rubric word like "briefly", can flip results at the margin; grade what matters.
  Case: in this project's evals, a judge failed "at 320px wide there should be no
  horizontal scroll" three times out of three on a criterion asking for exactly that.
- **Check the outputs exist.** A rate limit, timeout or crash leaves empty or cut-off
  answers that score as failures, and can break the judge's own calls inside runs that
  otherwise finished. Look for both before reading any score.
- **Match the eval to where the feature runs.** A case that assumes files, tools or
  context the harness doesn't provide measures the harness, not the feature.
- **Keep cases that discriminate.** If the baseline (no change, a plain model) passes a
  case too, it can't show the change helped; add one the baseline fails.
- **Test routing on its own.** If the model chooses between tools, prompts or skills,
  measure that choice with should-fire queries and near misses that share keywords.
  Case: routing hints written after seeing which queries missed raised a small model's
  recall from 73% to 90%; only 25 fresh queries written afterwards (24 of 25 loaded)
  showed the gain wasn't tuned to the test.

## 2. Design the context, not just the prompt

- State the task, the audience, the output format and what good looks like, with one or
  two examples of good output and one of a common mistake.
- Give the model only the information it needs, clearly separated and labelled; put
  untrusted input (user text, documents, web pages) in its own marked section.
- Prefer tools and structured output over parsing prose. Keep tool descriptions short
  and specific about when to use each tool.

## 3. Choose the model and effort on evidence

Run the eval set on two or three model sizes, and on recent models at two or three
effort levels: effort is now the main control over how much the model thinks. Start at
the default (medium on Opus 5.5), raise it only where the eval shows a gain, and try a
higher effort before a bigger model. Pick the cheapest setting that meets the quality
bar; record model, effort, quality, latency and cost per task. Re-run when models change.

Retest workarounds written for older models, and drop the ones that no longer help:
"think carefully" lines (lower or raise effort instead), asking for reasoning in the
answer, retyping chart values the model can now read from the image.

## 4. Agents that run on their own

An agent that wakes on events (webhooks, schedules, messages) and acts without a person
watching needs these, from Anthropic's always-on agents guide:

- **An inbox as the source of truth.** Event sources write to an inbox and return
  quickly; they never call the agent directly, or a crash loses the event. Deduplicate by
  the source's own event ID. One active worker per inbox, batching pending events, so
  two quick messages get one reply and runs never overwrite each other.
- **Timers in their own store.** Follow-ups and schedules sit apart from the inbox; a
  scheduler moves due ones into it. A timer never starts a run on its own.
- **Memory holds only what can't be looked up again.** Store a pointer to the ticket, not
  a copy. Load the person's standing instructions every run; keep a progress file per
  task (done, left); save anything that must survive as you go, because compaction and
  new sessions drop detail.
- **Credentials outside the agent.** A proxy adds them to outgoing requests. A tool call
  that needs approval ends the run; the answer comes back as a new event.
- **Done means checked.** A final text reply saying it's finished is a report, not proof:
  keep a task list the run must close, nudge on open items, and cap automatic
  continuations at two or three so a stuck run ends. A time budget given to the agent is
  advice; keep a hard timeout.
- **Start quiet.** Measure message volume in evals and let the agent earn attention.
- **Mark pasted and fetched text.** Wrap it in tags carrying a random ID and say that
  instructions inside count only where the person's own message asks for them. Tags can
  be imitated, so this is one layer, not the defence.

## 5. Guard it

- Assume any content the model reads may contain instructions. Limit what the model's
  actions can do: least-privilege tools, confirmation for irreversible actions, no
  secrets in context.
- Validate structured outputs; have a fallback when output is malformed or the model
  declines.
- Decide what the user sees when the model is wrong, slow or unavailable.
- Label AI-generated content where users would want to know.

## 6. Ship and watch

- Log inputs, outputs, tool calls and grader-relevant signals (with privacy controls).
- Track the outcome measure and user corrections, not only errors.
- Sample production traffic into the eval set regularly; every incident becomes a case.

## Report

Eval set size and source, per-criterion scores with run counts, model comparison table
(quality, latency, cost), known failure classes, guards in place, and what isn't covered.
