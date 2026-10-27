# Results

## v1.4: fixes from a review of all 21 skills (2026-10-26)

**Bottom line:** one always-on rule did more than rewording. For the five least-loaded skills, the right skill loaded on 8 of 30 short prompts before, 12 with reworded descriptions, and 21 with the core rules installed [observed: one run per query]. The new rule tells the agent to load the matching skill. Across all 21 skills with the rules on, recall was 63 of 78, with no loads on any of 68 near misses [observed: benchmarks/triggers/2026-10-26-4-all-with-rules.json]. v1.2, without the rules, managed about 44 of 63 [inferred].

### Trigger recall, five least-loaded skills (6 should-fire and 4 near-miss queries each)

| Skill | Before | New description | Plus core rules |
|---|---|---|---|
| guarding-agent-actions | 0/6 | 0/6 | 2/6 [observed] |
| researching-topics | 4/6 | 5/6 | 5/6 [observed] |
| reviewing-code | 2/6 | 2/6 | 4/6 [observed] |
| writing-documents | 0/6 | 1/6 | 5/6 [observed] |
| writing-emails | 2/6 | 4/6 | 5/6 [observed] |
| Near misses left alone | 20/20 | 20/20 | 20/20 [observed] |

Each set has the original three should-fire queries plus three held-out ones, written before the descriptions changed. A first draft of the new descriptions echoed some held-out phrasings; those were removed before measuring [observed: benchmarks/triggers/2026-10-26-*.json].

### Behaviour cases (three runs per arm, judge Sonnet)

| Case | With skills | Plain Claude | Reading |
|---|---|---|---|
| email-partial-commitment (new) | 1.00 | 0.53 | writing-emails earns its place: plain drafts missed the subject-line answer and the follow-up plan [observed] |
| email-vendor-chaser (new) | 0.67, then 0.58 after a fix | 0.17, then 0.08 | Found a real flaw (guessed values inside placeholders, now fixed); the judge also failed some answers that pass by hand [observed] |
| guarding-readme-setup (new) | 1.00 | 1.00 | Plain Claude already refuses to post keys and inspects `curl \| sh`; the skill didn't load. Kept as a regression check [observed] |
| proving-outcomes-status | 1.00 | 0.67 | The v1.1 single run where plain Claude scored higher was noise [observed] |
| changing-code-stale-test | 0.73, then 0.93 after a fix | 0.47, then 0.40 | Answers never said to record the reason when the code was the one to fix; the skill now asks for it either way [observed] |
| verify-dashboard-before-sending | 0.67, then 0.92 after a grader fix | 0.40, then 0.58 | The judge failed "at 320px there should be no horizontal scroll" three times out of three; one criterion graded something the prompt never asks [observed] |

### Core rules (three runs per arm unless noted)

| Case | With rules | Without | Reading |
|---|---|---|---|
| rule-outcome-first | 1.00 | 0.44 | Two runs first scored 0.67 in both arms: answers said "noticeably faster" with no target. Rule 1 now asks for a checkable outcome, with a target number where one applies [observed] |
| rule-no-bloat-arithmetic | 1.00 | 1.00 | The two new rules add no process to a trivial question [observed] |
| rule-piped-exit-code | 1.00 | 1.00 | Plain Claude already handles it (two runs) [observed] |
| rule-hearsay-claim | 0.67 | 0.67 | Neither arm recommends checking the primary source (two runs); unchanged since v1.1, left open [observed] |

The 63-of-78 trigger run used the rules before rule 1 was reworded; the routing rule itself didn't change [observed].

### Lessons recorded

1. **An always-on routing line beat description tuning.** Two rounds of rewording moved recall a little; one sentence in the session rules moved it most. The same lesson is now in `building-ai-features` ("test routing on its own").
2. **A judge can fail a clear pass.** Two of six cases had grader faults found only by reading answers by hand. `building-ai-features` now says to check the grader before trusting its scores.
3. **The usage limit struck again mid-run** and left empty answers scored 0. Those runs were discarded, not counted, and re-run after the reset.

### Spend

About $42 of eval runs: $25 of trigger runs and $17 of behaviour runs, including the judge [observed: runner cost fields]. Runs cut off by the usage limit cost almost nothing and were discarded.

## v1.3: reviewing-code with the Claude Code team's practices (2026-10-26)

**Bottom line:** v1.3 met every criterion on the four review cases (36 of 36), against 35 of 36 for v1.2 and 34 of 36 for plain Claude [observed: two or three runs per case per arm]. The lift is small because short cases mostly test correctness, where plain Claude is already strong; confirmation passes, converging rounds and risk tiers matter most on large pull requests and long review cycles, which these cases don't capture [inferred].

| Case | v1.3 | v1.2 | Plain Claude |
|---|---|---|---|
| Clean change beside a pre-existing bug (3 runs) | 12/12 | 12/12 | 12/12 [observed] |
| Project rule violation | 6/6 | 6/6 | 6/6 [observed] |
| SQL injection in a new endpoint | 10/10 | 10/10 | 8/10 [observed] |
| Third round, recurring bug class | 8/8 | 7/8 | 8/8 [observed] |

### Lessons recorded

1. **An eval case can plant a real problem by accident.** The first pre-existing-bug case computed a discount in floating point. Both skill versions declined to recommend merging, correctly, because floats are a real risk for money; the case was rewritten around a change that is genuinely fine [observed].
2. **Severity needs calibrating, not only finding.** One v1.3 run called missing boundary tests "Blocking". The skill now blocks only on new behaviour with no test at all; a missing edge case is a should-fix, in line with the Claude Code team treating coverage remarks as below the bar [observed].

### Spend

About $4.55 of eval runs [observed: runner cost lines].

## v1.2: trigger recall on short, casual prompts (2026-10-16)

**Bottom line:** on short, everyday prompts the skills were accurate but reticent. A baseline sample fired on 3 of 18 should-trigger queries [observed]. Rewriting every description to lead with the user's intent, following the Agent Skills guide, raised that to about 44 of 63 across all 21 skills, with no false triggers on any of the 63 near-miss queries [observed: benchmarks/triggers/]. Three queries per skill, one model (Sonnet): indicative, not a release gate.

### Method

- `tools/run_triggers.py`: each query from `plugins/*/evals/triggers/<skill>.json` goes to a fresh `claude -p` session with all three skill plugins loaded, read-only tools, six turns; a skill counts as triggered if the agent invoked it.
- Six turns, not two: with two, agents spent their turns searching the empty sandbox for the code a prompt mentioned and did not reach a skill, which undercounted triggering [observed].
- Near-miss negatives share keywords with the skill but need something else ("what's the difference between merge and rebase?" for `merging-safely`).

### Results by round

| Round | Skills measured | Recall (should fire) | Precision (near-misses left alone) |
|---|---|---|---|
| Baseline descriptions | 6 (sample) | 3 of 18 [observed] | 18 of 18 [observed] |
| Intent-first descriptions | same 6 | 10 of 18 [observed] | 18 of 18 [observed] |
| Intent-first, all skills | 21 | 37 of 63 [observed] | 63 of 63 [observed] |
| "Always use … even for a quick one", weakest 9 | 9 | 16 of 27, up from 6 [observed] | 27 of 27 [observed] |
| Combined estimate, all skills | 21 | about 44 of 63 [inferred: round 3 plus the round-4 gains] | 63 of 63 [observed] |

The three skills left unchanged during round 4 scored exactly as in round 3, which suggests the gains are not run-to-run noise [observed].

### What still doesn't trigger

`writing-documents` and `guarding-agent-actions` stayed at 0 of 3, and `writing-emails` at 1 of 3: on short prompts the model writes the email or document itself. That matches the Agent Skills guide's warning that agents skip skills for tasks they believe they can do alone. Richer prompts do trigger them (see the v1.0 behaviour evals below). `guarding-agent-actions` matters most when an agent has real tools; its cases need tool access to measure fairly.

### Portability checks (static)

- Every skill folder works when copied alone, passes the specification's naming and field rules, and has Codex metadata [observed: tests/test_portability.py, tests/test_skills.py].
- Generated Codex and Antigravity manifests match their sources [observed: `tools/build_manifests.py --check`].
- Live loading in Codex and Antigravity was not tested; no CLI for either was available.

### Spend

About $17 of eval runs for this round [observed: runner cost totals].

## v1.1: head-to-head with the reference set (2026-10-14)

**Bottom line:** on cases written by the reference set's own author, the v1.1 skills passed 5 of 12 against 3 of 12 for the reference skills and 2 of 12 for plain Claude, and matched or beat the reference on every case [observed: benchmarks/h2h/pass2-poolB-summary.json]. On our own 21 cases the gap is wider (92% against 72% and 69% of criteria), but those cases were written for our skills, so they count for less [observed: benchmarks/h2h/pass1-summary.json]. One run per case: indicative, not a release gate.

### Set-up

- Two bundles built by `benchmarks/h2h/build_bundles.py`: all 21 of our skills in one plugin, the 6 reference skills (`ly87ing/agent-skills`, the deleted WeCom skill excluded) in another.
- Pool A: our 21 should-fire cases, outcome graders only. Pool B: 2 should-trigger cases per reference skill, graded against the reference author's own expected-behaviour text.
- `claude plugin eval`, one run per case, judge `sonnet`; our bundle with the no-plugin baseline arm, the reference bundle plugin-only.

### Pool B per case (pass or fail against the reference author's description)

| Case | Ours | Reference | Plain Claude |
|---|---|---|---|
| artifact-hygiene-1 | pass | pass | fail |
| artifact-hygiene-2 | fail | fail | fail |
| change-discipline-1 | fail, then 2 of 3 after a fix | fail | fail |
| change-discipline-2 | fail | fail | fail |
| reader-facing-writing-1 | pass | pass | fail |
| reader-facing-writing-2 | fail | fail | fail |
| safe-merge-review-1 | pass | fail | fail |
| safe-merge-review-2 | pass | pass | fail |
| solution-shaping-1 | fail | fail | fail |
| solution-shaping-2 | fail | fail | fail |
| verification-1 | fail | fail | pass |
| verification-2 | pass | fail | pass |

Three of the six all-fail cases cannot be passed as written: their expected behaviour refers to constraints or source figures the prompt never gives (solution-shaping-2, reader-facing-writing-2) or to a project the sandbox lacks [inferred: from reading each case]. They are kept for transparency.

### Fix made from the comparison

`change-discipline-1` asks to build a shared abstraction that only one service uses. Our answer designed it anyway. `changing-code` now has an explicit stop step for speculative abstractions and names "extract an abstraction" in its description. The case went from 0 of 1 to 2 of 3 runs [observed].

### The optional `core-rules` plugin

Four cases, two runs each, with and without the plugin [observed]:

| Case | With rules | Without | Lift |
|---|---|---|---|
| State outcome, assumptions and checks first | 0.83 | 0.33 | +0.50 [observed] |
| Don't trust a piped exit code | 1.00 | 1.00 | 0 [observed] |
| Verify another AI's claim | 0.67 | 0.67 | 0 [observed] |
| No added process on a trivial question | 1.00 | 1.00 | 0 [observed] |

Mean lift +0.12, all of it from one rule [observed]; plain Claude already handles the others. It costs about 200 tokens per session [estimate: 830 characters]. Kept optional, not a default install.

### No false triggers from the new skills

The two new should-not-fire cases (a CSS question and a `.gitignore` question) did not trigger `verifying-interfaces` or `handling-artifacts` [observed].

### Lessons recorded

1. **Eval prompts must match the sandbox.** Cases that assume a real repository or app make careful skills stop and ask for it, which a grader reads as failure. The reference set scored 0 of 12 on its own cases until the prompts said no environment was available. Our own `rule-outcome-first` case had the same flaw.
2. **Grader wording decides results at the margin.** "Briefly" failed a correct table answer, and one line of working failed "391". Grade what matters, not length, unless length is the point.
3. **A usage limit stops runs mid-suite and leaves empty answers that score as failures.** Check for empty outputs before reading any score.

### Spend

About $9 of eval runs after the usage reset, $17 before it, and $33 for v1.0 [observed: runner cost lines].

## v1.0: first measurement (2026-10-13)

**Bottom line:** with the plugins installed, responses met 94% of the should-fire success criteria (89 of 95), against 68% (65 of 95) for plain Claude on the same prompts [observed]. Skills triggered on 18 of 19 should-fire cases and on none of the 11 should-not-fire checks [observed]. These are **indicative**: one run per case per arm, so treat each per-case number as ±1 criterion. The release-gate run (3+ runs, both arms) is the next step; see the command below.

### How it was measured

- `claude plugin eval plugins/<plugin> --runs 1 -j 8 --judge-model sonnet`, 25 cases across the three plugins, one LLM grader per success criterion.
- "Baseline" is the no-plugin arm of the run with the original descriptions. "v1.0" is a plugin-only run after the description rewrite (see lesson 1). Both used the same prompts and graders.
- Total spend across all exploratory runs: about $33, on the account that ran them [observed: sum of runner cost lines].

### Per case (criteria passed)

| Plugin | Case | Plain Claude | v1.0 | Skill fired |
|---|---|---|---|---|
| foundations | capturing-learning-deploy-claims | 3/5 | 4/5 | yes |
| foundations | defining-done-refund-tool | 3/5 | 5/5 | yes |
| foundations | delegating-work-migration | 5/5 | 5/5 | yes |
| foundations | exploring-options-search | 2/5 | 5/5 | yes |
| foundations | guarding-actions-vendor-email | 5/5 | 5/5 | no |
| foundations | proving-outcomes-status | 2/5 | 5/5 | yes |
| foundations | tracing-claims-board-update | 4/5 | 5/5 | yes |
| engineering-lifecycle | ai-ticket-classifier | 3/5 | 5/5 | yes |
| engineering-lifecycle | changing-code-stale-test | 2/5 | 4/5 | yes |
| engineering-lifecycle | design-billing-batch | 4/5 | 5/5 | yes |
| engineering-lifecycle | merge-defaults-conflict | 4/5 | 5/5 | yes |
| engineering-lifecycle | requirements-csv-export | 2/5 | 5/5 | yes |
| engineering-lifecycle | review-sql-diff | 4/5 | 5/5 | yes |
| engineering-lifecycle | tests-parse-duration | 5/5 | 5/5 | yes |
| professional-craft | brief-crm-decision | 2/5 | 3/5 | yes |
| professional-craft | deck-devtools-funding | 3/5 | 4/5 | yes |
| professional-craft | documents-migration-status | 3/5 | 4/5 | yes |
| professional-craft | email-launch-slip | 5/5 | 5/5 | yes |
| professional-craft | research-sso-options | 4/5 | 5/5 | yes |

Should-not-fire cases (6 cases, 11 checks): no skill fired in any of them.

### Context cost

Measured with `claude --plugin-dir ./plugins/<plugin> plugin details <plugin>` [observed]:

| Plugin | Always-on per session | Per skill when it fires |
|---|---|---|
| foundations | ~756 tokens | ~660–950 tokens |
| engineering-lifecycle | ~819 tokens | ~580–910 tokens |
| professional-craft | ~574 tokens | ~480–940 tokens |

### Lessons recorded

1. **Descriptions must name the situation, not summarise the skill.** With summary-style descriptions only 8 of 19 skills fired, and none of the 7 foundations skills did. Rewriting 11 descriptions as "Use whenever someone asks …" with the phrasings users type raised that to 18 of 19, with no false triggers [observed].
2. **One grader per criterion.** An all-or-nothing grader failed good answers without saying why. Separate graders give partial credit and name the failing criterion.
3. **Use a capable judge.** The default fast judge failed answers that met every criterion. Use `--judge-model sonnet` or stronger.
4. **One run per case is noise.** One case swung from 0.8 to 0.2 between runs while the skill never fired, so the skill could not have caused it [observed]. Release decisions need 3+ runs and interval comparison.
5. **Graders must not fight good design.** The decision-brief grader required the ask at the end, while the skill puts it on the first screen. The grader was corrected after this run.

### Open items

- `guarding-agent-actions` did not trigger on the injected-email case; plain Claude already scored 5/5 there, so there was no lift to lose. Add cases where the agent has real tools (send, delete) before judging this skill.
- `brief-crm-decision` and `documents-migration-status` show genuine misses (an invented detail; one judge split). Re-check them in the release-gate run.

## Release-gate run (to do)

```
for p in foundations engineering-lifecycle professional-craft; do
  claude plugin eval plugins/$p --runs 3 -j 8 --judge-model sonnet
done
```

Pass when no plugin's mean delta is negative and should-not-fire cases stay clean. At the v1.0 sizes, expect roughly $30–40 per full run [estimate: about 6× the one-run, one-arm cost observed here].
