# Results

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
