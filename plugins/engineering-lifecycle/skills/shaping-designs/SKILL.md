---
name: shaping-designs
description: Always use this skill when deciding how something should be built or changed — a design doc or RFC, an architecture, API or data model, a migration or schema change; requirements, user stories, acceptance criteria or a spec; an LLM feature (a prompt, a model choice, a chatbot that gets things wrong); or "X or Y", even a quick question. It works through contracts, data, failure and rollout.
---

# Shaping designs

A design is a set of constraints, a target that satisfies all of them, and a safe path
from here to there, with every load-bearing claim graded observed, inferred or
unverified. Most design failures aren't bad ideas; they're a constraint nobody wrote
down, a caller nobody found, or a step that couldn't be undone.

## 1. Outcome and constraints

- State the outcome as something observable ("customers stop abandoning checkout at
  payment"), how it'll be measured, and when. For a feature request, start from the
  problem, not the feature (`references/requirements.md`).
- Put every constraint in one table: constraint, source (the person's words, code,
  policy, data), what it rules out. Include scale, latency, cost, team skills,
  deadlines, and the deployment model (independent deploys, bundled releases where
  customers skip versions, single replica, shared hosts); an argument that holds under
  one model fails under another. When a new constraint arrives, add it and re-derive
  the design from the table instead of patching the last version.

## 2. Inventory what exists

For a change to a running system, list each capability, interface, job and data set as
live, dead or unknown, with evidence. Zero usage counts only with a same-period
baseline showing the probe would have caught use. When the design replaces a mechanism
(a renderer, a script, a pipeline), list every effect the old one has by walking its
code, not from the examples at hand: each branch, default and fallback, each channel it
writes (files, environment, databases, DNS, caches), and whether losing it fails loudly
or silently. Where two live implementations exist, diff them before treating either as
the baseline.

## 3. Options

Include doing less or nothing when that's real, and say how each option is undone. Spike
the riskiest part when argument can't settle it. Asked for a one-line answer? Give the
pick, the constraint that would flip it, and the cheap check that would settle it.

## 4. Detail the recommendation

Work through the references that apply, answering their checklists:

- New or changed APIs, events, config, file formats: `references/interfaces.md`.
- Schema changes, data moves, backfills, anything destructive:
  `references/data-and-migrations.md`.
- Dependencies, load, availability, security, observability:
  `references/failure-and-capacity.md`.
- A feature built on a language model: `references/ai-features.md`.

Each says what the design must state; "it won't fail" and "it scales" are not answers.

Whatever the references, check these inline; capable engineers miss them by default:

- **A cache never decides money or access.** Cached prices, balances or permissions are
  for display; the amount charged or the access granted is read from the source of truth
  (or a signed, short-lived quote) at that moment. A change known in advance (a flash sale
  at 12:00:00) is effective-dated and pre-warmed, not left to a TTL expiring.
- **Clients you can't update.** Old mobile apps and partner integrations live for years.
  Strict decoders reject unknown enum values and new required fields, so add values
  behind a capability or version check, and say what an old client sees.
- **Locks on live tables.** In PostgreSQL, set `lock_timeout` before any `ALTER TABLE`, so
  a queued lock can't stall every query behind it. Build indexes `CONCURRENTLY`; add NOT
  NULL through a `CHECK ... NOT VALID` constraint validated separately. Rename by
  expand, migrate, contract, never in one step while old code runs.
- **Retries need idempotency.** Any retried write with side effects (charge, credit,
  email, webhook) carries a key the receiver stores and checks in the same transaction as
  the effect.

## 5. Blast radius, rollout and rollback

Walk the blast-radius table in `references/design-review.md`, marking every row. Plan
the rollout as steps each safe to stop after: flags, migration order, the smallest
first step that proves the direction, and how each stage is undone. Name what rollback
can't restore.

## 6. Challenge and decide

Attack your own pick (`references/design-review.md`): the best case for the runner-up,
the likeliest failure once built, what would overturn it, each objection ruled on. Get
an independent challenge when reversal is hard. Then decide, or, when the choice is the
person's (scope, cost, cross-team asks, anything irreversible), present it with a
recommendation and stop. Record the decision beside the code.

## Completeness

Run the completeness check in `references/design-review.md` before calling the design
done. A missing row is reported as incomplete, not padded.

## Output

Answer at the size of the question. A Slack-style "thoughts?" gets the recommendation, the
two or three points that change the design, and what to check first, not a design doc.
A design doc asked for as such follows: context and constraints, options, recommendation
and challenge, detailed design, blast radius, rollout and rollback, decision, open
questions with owners. Leave out sections that would only restate the request.

## Not this skill

Making the change once agreed belongs to `changing-code`; reviewing a diff to
`reviewing-code`; merges to `merging-safely`.
