# acme-skills

Agent skills for Claude that aim past output quality: the real outcome happened, people can trust the work without redoing it, each task leaves the next one easier, and the person stays in charge.

In a head-to-head on cases written by another skill set's author, these skills passed 5 of 12 against 3 of 12 for that set and 2 of 12 for plain Claude, and matched or beat it on every case [observed, one run per case; see [benchmarks/RESULTS.md](benchmarks/RESULTS.md)].

## Plugins

| Plugin | Skills | Always-on cost |
|---|---|---|
| `foundations` | defining-done · exploring-options · delegating-work · proving-outcomes · tracing-claims · capturing-learning · guarding-agent-actions · handling-artifacts | ~878 tokens |
| `engineering-lifecycle` | writing-requirements · designing-systems · changing-code · reviewing-code · writing-tests · merging-safely · verifying-interfaces · building-ai-features | ~971 tokens |
| `professional-craft` | writing-documents · briefing-decisions · researching-topics · building-presentations · writing-emails | ~574 tokens |
| `core-rules` (optional, recommended) | Seven always-on working rules injected at session start. One makes the agent load the matching skill: on short prompts, skills loaded on 21 of 30 queries for the five least-used skills with the rules against 12 of 30 without, and 63 of 78 across all skills, with no false loads [observed, one run per query] | ~260 tokens |

Each plugin works alone. `foundations` holds the shared work loop (define done → explore → do → prove → hand off → learn), and the other two work better alongside it.

## Install

Works in **Claude Code, Codex and Antigravity** from the same skill folders. Details and sources: [docs/RUNTIMES.md](docs/RUNTIMES.md).

**Claude Code**

```
/plugin marketplace add ericonline1987-lgtm/acme-skills
/plugin install foundations@acme-skills
/plugin install engineering-lifecycle@acme-skills
/plugin install professional-craft@acme-skills
/plugin install core-rules@acme-skills        # optional
```

**Codex**

```
codex plugin marketplace add ericonline1987-lgtm/acme-skills
```

Then install the plugins from the Plugins Directory. For the optional rules, run `python3 tools/install.py --runtime codex --rules`, which adds them to `AGENTS.md`.

**Antigravity**

```
git clone https://github.com/ericonline1987-lgtm/acme-skills && cd acme-skills
agy plugin install ./plugins/foundations      # and the others; ./plugins/core-rules adds the rules
```

**Any runtime, without a marketplace**

```
python3 tools/install.py --runtime all --scope project --project ~/code/my-app --rules --dry-run
```

It copies the self-contained skill folders into each runtime's skill directory. It skips any skill it didn't install (tested in tests/test_install.py), and a dry run shows every action first.

## What's in the box

```
.claude-plugin/marketplace.json        lists the four plugins
plugins/<plugin>/skills/<skill>/        SKILL.md, agents/openai.yaml, plus scripts/, assets/ or references/
plugins/<plugin>/evals/                 behaviour evals, plus triggers/<skill>.json query sets
plugins/<plugin>/{plugin.json, .codex-plugin/}   Antigravity and Codex manifests (generated)
.agents/plugins/marketplace.json        Codex marketplace (generated)
shared/                                 single source for files several skills use (synced into skills)
tools/                                  installer, manifest generator, shared-file sync, trigger runner
benchmarks/                             outcome log, scorer, results, head-to-head bundles and cases
tests/                                  offline contract and script tests (CI)
docs/PLAN.md, PLAN-v1.1.md, RUNTIMES.md  goals, roadmap, coverage plan, runtime support
LICENSE, NOTICE, SECURITY.md            licence, third-party material, how to report problems
```

### Checks that are code, not prose

| Script | What it catches |
|---|---|
| `engineering-lifecycle/skills/merging-safely/scripts/merge_evidence.py` | A merge that silently dropped one side's changes, even when git's ancestry checks pass |
| `engineering-lifecycle/skills/verifying-interfaces/scripts/validate_svg.py` | Malformed SVGs, bad viewBox, duplicate ids, broken references, scripts, external dependencies |
| `professional-craft/skills/writing-documents/scripts/doc_check.py` | Slow openings, meta-commentary, long sentences, label headings, hedging, open placeholders, over budget |
| `foundations/skills/handling-artifacts/scripts/repo_weight.py` | Which objects take the most space in a repository's history, including files deleted from the tree but still taking space |
| `foundations/skills/proving-outcomes/scripts/evidence_ledger.py` | Claiming a higher rung (deployed, accepted, outcome achieved) than the evidence supports; no outcome check scheduled |
| `foundations/skills/tracing-claims/scripts/claim_check.py` | Figures and absolutes in Markdown with no source or evidence grade |
| `foundations/skills/defining-done/scripts/check_sections.py` | Contracts, hand-offs and briefs with missing, empty or unfilled sections |
| `foundations/skills/capturing-learning/scripts/add_eval_case.py` | Turns a failure into an eval case, so the fix is measured |
| `benchmarks/score_outcomes.py` | Overclaim rate and outcome achievement on real work, with confidence intervals |

All scripts use only the Python standard library, and each one states what it cannot check.

## Measure it

```
python3 -m unittest discover -s tests                                  # every commit (CI)
python3 tools/run_triggers.py --max-cost-usd 10                        # trigger recall and precision
claude plugin eval plugins/foundations --runs 3 --judge-model sonnet   # every release; adds a no-plugin baseline
python3 benchmarks/score_outcomes.py benchmarks/outcomes.csv           # weekly, on real work
```

See [benchmarks/README.md](benchmarks/README.md).

## Make it yours

Fork it, fill in the terminology table in `shared/style-guide.md` with your own product names and preferred terms, and run `python3 tools/sync_shared.py` to copy it into the writing skills.

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). Changes: [CHANGELOG.md](CHANGELOG.md). Security: [SECURITY.md](SECURITY.md).

## License

MIT, see [LICENSE](LICENSE). Third-party material is listed in [NOTICE](NOTICE).
