# Results

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
