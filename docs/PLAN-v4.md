# Plan v4: specialist, measured fairly

**Bottom line:** v4 narrows each skill to what a capable model gets wrong by default where an expert wouldn't, and replaces our own test cases with a neutral pool written by neither side. This file fixes the method and the decision rules before any v4 run, so the result can't be tuned after the fact.

## What belongs in a skill

Something goes in a skill only if at least one of these holds:

1. A capable model gets it wrong by default even though it knows the topic. For example, it writes "not X but Y" while able to list that pattern as an AI tell, or proposes a one-step schema change on a live table.
2. It is an exact constraint that must be followed literally, such as a required block, a threshold or a format. These go inline in SKILL.md, because agents often don't open reference files (v3 lesson; SkillJuror reports the same for constraint-bound tasks).
3. The model can't know it, such as house terminology.

General advice the model already follows ("name the point", "compare options", "state the outcome") is removed. A rule stays only if removing it makes a case fail. The set is expected to get shorter, not longer.

**Raise the bar; don't cap the model (added 2026-11-10).** A skill exists to get the person's goal achieved at the standard a top practitioner would deliver, not to restrict a capable model. So:

- Each skill states the result the work must achieve and what an excellent version adds beyond a correct one, and ends with a check of the output against that goal.
- Prohibitions stay only where they protect the outcome or the person's trust: no invented facts, claims kept at their real strength, a go-ahead before outward or destructive actions, secrets kept out. Everything else is phrased as what to do.
- Nothing useful is suppressed. Lesser findings and side improvements are ranked and separated so the important ones lead, rather than dropped (in v3, a review "never report" list and a one-step answer rule made answers narrower than plain Sonnet's).
- Size limits are tied to the reader's goal (a chat reply readable at a glance), never imposed for their own sake.
- "Not this skill" sections become "Works with", so skills combine instead of excluding each other.

## Why the v3 comparison isn't enough

- The v3 head-to-head gave our bundle a session-start routing line and the reference none, so part of our lead may be routing, not content.
- Pool C was written by us after we knew what our skills do.
- The plain baseline ran in an empty workspace. Published skill evaluations (ACES) found that this overstates lift, because the skill isn't competing with anything to be found.
- Pairwise judges lean toward one position when two answers are close.

## Pool D

- 24 cases in four areas: writing 6, visuals 5, design 6, code 7. They are written by a separate agent that was told not to open either skill set or search for them, and to ground each case in public expert material cited in its SOURCE.md.
- Each case has `prompt.md`, 3 to 5 one-criterion graders, `rubric.md` (what a senior specialist's answer looks like, for the pairwise judge) and `SOURCE.md`.
- I make format fixes only; any change to a case is logged in its SOURCE.md with the reason.
- The pool is split once, by area, into **dev** (12) and **test** (12) with a fixed seed (`benchmarks/v4/split.json`). Phase 2 edits may be informed by dev answers only. Test answers are read only to find grader bugs, each logged. The v4 claim is made on test.

## Arms

All three run the same cases on the same model and harness, with the same seven decoy skills from Anthropic's public skills repository (four near competitors: doc-coauthoring, internal-comms, frontend-design, webapp-testing; three unrelated: mcp-builder, slack-gif-creator, algorithmic-art). No arm has a routing line or always-on rules.

| Arm | Skills |
|---|---|
| `base` | decoys only |
| `acme` | this repo's seven skills plus decoys |
| `ref` | `ly87ing/agent-skills` at 6953cfe plus decoys |

`benchmarks/v4/build_arms.py` builds them.

## Measurement

- Answer model Sonnet, 3 runs per arm and case. Haiku 1 run per arm and case as a check on smaller models.
- Runs that hit a usage limit or error are discarded and rerun.
- **Primary metric:** pairwise win rate of `acme` against `ref` on the test split, Sonnet answers. Each pair of runs is judged in both orders by two judges (Opus and Sonnet). A verdict that flips with order counts as a tie. Win = 1, tie = 0.5, loss = 0, averaged per case, then over cases. Skill names are redacted from answers before judging (`benchmarks/v4/pairwise.py`).
- **Secondary:** criterion score per arm; lift over `base`; harm cases (an arm scores below `base` on a case); share of runs that loaded the arm's own skill; position consistency and agreement of judges; cost per run and per score point; answer length.
- Intervals are 95% percentile bootstrap over cases, 10,000 resamples, seed 0 (`benchmarks/v4/stats.py`).

## Decision rules

- "acme is stronger than the reference" is claimed only if the lower end of the interval for the primary metric is above 0.5. If the interval contains 0.5, the result is "no measurable difference", and it is reported that way.
- "A skill set helps" is claimed only if its lift over `base` has an interval above 0.
- Per-area results are reported but not claimed: six cases or fewer is too few.
- Every harm case is read by hand and either explained or fixed.

## Human check

You rate the writing pairs (acme against ref) blind on a rating page. Agreement between your choices and the judges' is reported. If you disagree with the judges on most pairs, the judge result for writing is not used.

## Phase 2: trim to the specialist core

After round 1, and using dev answers only:

1. Cut each skill's general advice and keep the expert-specific part.
2. Add a rule only where a dev case fails and a specialist would have done better.
3. Rerun all arms on the full pool. Report the test-split result against round 1.

`handling-artifacts` is cut or folded into a core rule if plain `base` no longer fails its kind of case.

## Not in scope

Opus as the answer model (cost); languages other than English; file formats.
