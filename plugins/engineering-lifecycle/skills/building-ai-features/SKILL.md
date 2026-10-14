---
name: building-ai-features
description: Design, build and evaluate features powered by language models — define quality with an eval set before writing prompts, design context and tools, choose models on measured quality and cost, guard against prompt injection, and monitor in production. Use when building or improving an LLM feature, agent, prompt, RAG pipeline or AI workflow.
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
- Run every case several times; report rates with their spread, not single results.

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
