---
name: building-ai-features
description: Use this skill whenever someone is building or improving a feature powered by a language model — an LLM classifier, chatbot, RAG pipeline, agent or prompt — or choosing a model for one, including when answers are "sometimes wrong". It defines quality with an eval set before tuning prompts, compares models on measured quality and cost, guards against prompt injection and plans monitoring.
---

# Building AI features

Model output is probabilistic, so "it worked when I tried it" proves little. Treat
quality as something you measure on every change, like latency.

## 1. Define quality before writing a prompt

- Write the outcome contract: what the user should be able to do, and the measure that
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
- **Check the outputs exist.** A rate limit, timeout or crash leaves empty or cut-off
  answers that score as failures. Look for them before reading any score.
- **Match the eval to where the feature runs.** A case that assumes files, tools or
  context the harness doesn't provide measures the harness, not the feature.
- **Keep cases that discriminate.** If the baseline (no change, a plain model) passes a
  case too, it can't show the change helped; add one the baseline fails.
- **Test routing on its own.** If the model chooses between tools, prompts or skills,
  measure that choice with should-fire queries and near misses that share keywords.

## 2. Design the context, not just the prompt

- State the task, the audience, the output format and what good looks like, with one or
  two examples of good output and one of a common mistake.
- Give the model only the information it needs, clearly separated and labelled; put
  untrusted input (user text, documents, web pages) in its own marked section.
- Prefer tools and structured output over parsing prose. Keep tool descriptions short
  and specific about when to use each tool.

## 3. Choose the model on evidence

Run the eval set on two or three model sizes. Pick the cheapest that meets the quality
bar; record quality, latency and cost per task for each. Re-run when models change.

## 4. Guard it

- Assume any content the model reads may contain instructions. Limit what the model's
  actions can do: least-privilege tools, confirmation for irreversible actions, no
  secrets in context.
- Validate structured outputs; have a fallback when output is malformed or the model
  declines.
- Decide what the user sees when the model is wrong, slow or unavailable.
- Label AI-generated content where users would want to know.

## 5. Ship and watch

- Log inputs, outputs, tool calls and grader-relevant signals (with privacy controls).
- Track the outcome measure and user corrections, not only errors.
- Sample production traffic into the eval set regularly; every incident becomes a case.

## Report

Eval set size and source, per-criterion scores with run counts, model comparison table
(quality, latency, cost), known failure classes, guards in place, and what isn't covered.
