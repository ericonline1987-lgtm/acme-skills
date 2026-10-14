# acme-skills

Agent skills for Claude that aim past output quality: the real outcome happened, people can trust the work without redoing it, each task leaves the next one easier, and the person stays in charge.

In a first measurement, responses met 94% of success criteria with these plugins against 68% for plain Claude on the same 19 tasks [observed, one run per case; see [benchmarks/RESULTS.md](benchmarks/RESULTS.md)].

## Plugins

| Plugin | Skills | Always-on cost |
|---|---|---|
| `foundations` | defining-done · exploring-options · delegating-work · proving-outcomes · tracing-claims · capturing-learning · guarding-agent-actions | ~756 tokens |
| `engineering-lifecycle` | writing-requirements · designing-systems · changing-code · reviewing-code · writing-tests · merging-safely · building-ai-features | ~819 tokens |
| `professional-craft` | writing-documents · briefing-decisions · researching-topics · building-presentations · writing-emails | ~574 tokens |

Each plugin works alone. `foundations` holds the shared work loop (define done → explore → do → prove → hand off → learn), and the other two work better alongside it.

## Install (Claude Code)

```
/plugin marketplace add <your-github-org>/acme-skills
/plugin install foundations@acme-skills
/plugin install engineering-lifecycle@acme-skills
/plugin install professional-craft@acme-skills
```

## What's in the box

```
.claude-plugin/marketplace.json        lists the three plugins
plugins/<plugin>/skills/<skill>/        SKILL.md, plus scripts/ or templates/ where needed
plugins/<plugin>/evals/                 behaviour evals: one should-fire case per skill, should-not-fire cases
plugins/foundations/shared/             outcome contract, hand-off, decision record, delegation brief, evidence ledger
plugins/professional-craft/shared/      house style guide
benchmarks/                             outcome log, scorer, results
tests/                                  offline contract and script tests (CI)
docs/PLAN.md                            goals, principles, architecture, roadmap
```

### Checks that are code, not prose

| Script | What it catches |
|---|---|
| `foundations/skills/proving-outcomes/scripts/evidence_ledger.py` | Claiming a higher rung (deployed, accepted, outcome achieved) than the evidence supports; no outcome check scheduled |
| `foundations/skills/tracing-claims/scripts/claim_check.py` | Figures and absolutes in Markdown with no source or evidence grade |
| `foundations/shared/scripts/check_sections.py` | Contracts, hand-offs and briefs with missing, empty or unfilled sections |
| `foundations/skills/capturing-learning/scripts/add_eval_case.py` | Turns a failure into an eval case, so the fix is measured |
| `benchmarks/score_outcomes.py` | Overclaim rate and outcome achievement on real work, with confidence intervals |

All scripts use only the Python standard library, and each one states what it cannot check.

## Measure it

```
python3 -m unittest discover -s tests                                  # every commit (CI)
claude plugin eval plugins/foundations --runs 3 --judge-model sonnet   # every release; adds a no-plugin baseline
python3 benchmarks/score_outcomes.py benchmarks/outcomes.csv           # weekly, on real work
```

See [benchmarks/README.md](benchmarks/README.md).

## Before publishing

- Replace "Acme" and the owner email in `.claude-plugin/marketplace.json` and each `plugin.json`.
- Fill in the terminology table in `plugins/professional-craft/shared/style-guide.md`.

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). Changes: [CHANGELOG.md](CHANGELOG.md).
