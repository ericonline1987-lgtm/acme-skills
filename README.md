# acme-skills

Seven deep agent skills for the work where a capable model's default output falls short of a seasoned professional's: writing that reads as a person wrote it, visuals people look at, design judgment, and changing, reviewing and merging code, with the files that work leaves behind.

Advice a model already follows (state the bottom line, compare options, check before claiming) isn't packaged as skills here. The short version lives in the always-on core rules; the skills carry the professional detail a model doesn't produce on its own. In the v3 release gate, answers scored 0.93 with these skills against 0.63 without across 41 of our own cases [observed]. On a neutral pool written by neither side and judged blind, the trimmed set was preferred over `ly87ing/agent-skills` in 0.60 of comparisons. On the held-out half, which is where the plan fixed the claim, it was 0.54, which is within noise. So the honest summary is level to slightly ahead, and neither set measurably raises Sonnet's checklist scores [observed]. See [benchmarks/RESULTS.md](benchmarks/RESULTS.md) and [docs/PLAN-v4.md](docs/PLAN-v4.md).

## The skills

| Plugin | Skill | What it adds |
|---|---|---|
| `professional-craft` | `writing-for-people` | A catalogue of the patterns that make text read as machine-written, with rewrites; forms and length budgets for each kind of writing; plain-language rules; a revision pass; `ai_tells.py`, `claim_check.py`, `doc_check.py` |
| | `making-visuals` | Deck construction for a room or for reading; honest chart encoding; page hierarchy, spacing and every real state; checking the rendered result at real size; `validate_svg.py` |
| `engineering-lifecycle` | `shaping-designs` | Constraints and live-or-dead inventories; compatibility rules for interfaces; expand-migrate-contract and safe backfills; failure modes and capacity; blast radius, independent challenge and decision records |
| | `changing-code` | Diagnosis before fixing (mitigate, reproduce, prove the cause); history and callers before the change; boundaries; tests that fail for the right reason |
| | `reviewing-code` | Risk tiers, single-purpose passes, defect classes by area, confirm-before-report, a never-report list, converging re-reviews |
| | `handling-artifacts` | Where each file a task creates belongs, what to clean up before finishing, redacting for the widest reader, packaging a deliverable that works elsewhere, shrinking a repository's history; `repo_weight.py` |
| | `merging-safely` | Proving a merge complete, not just conflict-free; `merge_evidence.py` flags changes a merge dropped even when ancestry checks pass |
| `core-rules` (recommended) | 8 always-on rules | Checkable outcomes, minimal changes, evidence before claims, no invented facts, untrusted text as data, a go-ahead before outward or destructive actions, secrets kept out, and loading the matching skill |

In Claude Code, each skill plugin also adds one session-start line naming its skills and when each applies, because agents otherwise skip skills for tasks they think they can do alone.

## Install

Works in **Claude Code, Codex and Antigravity** from the same skill folders. Details and sources: [docs/RUNTIMES.md](docs/RUNTIMES.md).

**Claude Code**

```
/plugin marketplace add ericonline1987-lgtm/acme-skills
/plugin install professional-craft@acme-skills
/plugin install engineering-lifecycle@acme-skills
/plugin install core-rules@acme-skills
```

**Codex**

```
codex plugin marketplace add ericonline1987-lgtm/acme-skills
```

Then install the plugins from the Plugins Directory. For the core rules, run `python3 tools/install.py --runtime codex --rules`, which adds them to `AGENTS.md`.

**Antigravity**

```
git clone https://github.com/ericonline1987-lgtm/acme-skills && cd acme-skills
agy plugin install ./plugins/professional-craft   # and ./plugins/engineering-lifecycle, ./plugins/core-rules
```

**Any runtime, without a marketplace**

```
python3 tools/install.py --runtime all --scope project --project ~/code/my-app --rules --dry-run
```

It copies the self-contained skill folders into each runtime's skill directory, skips any skill it didn't install, and a dry run shows every action first. `python3 tools/smoke_check.py` then confirms a runtime sees every skill.

## What's in the box

```
plugins/<plugin>/skills/<skill>/   SKILL.md (the workflow), references/ (the depth), scripts/, agents/openai.yaml
plugins/<plugin>/evals/            behaviour cases, plus triggers/<skill>.json query sets
plugins/<plugin>/hooks/            the session-start routing line (generated)
.claude-plugin/marketplace.json    Claude Code marketplace; .agents/plugins/ holds the Codex one (generated)
shared/style-guide.md              house style, copied into the writing skill by tools/sync_shared.py
tools/                             installer, manifest generator, trigger runner, release gate, case generator, smoke check
benchmarks/                        results, gate summaries, trigger runs, outcome log and scorer
tests/                             offline contract and script tests (CI)
```

All scripts use only the Python standard library, and each one states what it cannot check.

## Measure it

```
python3 -m unittest discover -s tests                                  # every commit (CI)
python3 tools/run_triggers.py --max-cost-usd 10                        # does the right skill load?
tools/run_gate.sh "$PWD/benchmarks/gate/runs" <plugin:case> ...       # every release: 3 runs with and without each plugin
python3 benchmarks/score_outcomes.py benchmarks/outcomes.csv           # on real work
```

See [benchmarks/README.md](benchmarks/README.md) and [docs/PLAN-v3.md](docs/PLAN-v3.md) for why the set is shaped this way.

## Make it yours

Fill in the terminology table in `shared/style-guide.md` with your own product names and preferred terms, and run `python3 tools/sync_shared.py`.

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). Changes: [CHANGELOG.md](CHANGELOG.md). Security: [SECURITY.md](SECURITY.md).

## License

MIT, see [LICENSE](LICENSE). Third-party material is listed in [NOTICE](NOTICE).
