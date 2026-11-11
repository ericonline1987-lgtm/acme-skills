# acme-skills

Seven agent skills that push the work past what a capable model produces by default, in four areas: writing that reads as a person wrote it, visuals people look at, design judgment, and changing, reviewing and merging code.

Each skill states the result the work must achieve, adds the specialist checks a strong model skips (a cache deciding what's charged, a cursor that skips rows, a merge that silently dropped a fix, a sentence that could describe any product), and ends by checking the output against the goal. Scripts check what a model can't check reliably by reading, such as changes a merge silently dropped.

## Install

**Claude Code** (recommended: all three plugins)

```
/plugin marketplace add ericonline1987-lgtm/acme-skills
/plugin install professional-craft@acme-skills
/plugin install engineering-lifecycle@acme-skills
/plugin install core-rules@acme-skills
```

Install the plugins rather than copying the skill folders. Each plugin adds one session-start line naming its skills and when each applies; without it, agents often skip skills, and small models skip them almost always [observed; see [benchmarks/RESULTS.md](benchmarks/RESULTS.md)].

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

It copies the self-contained skill folders into each runtime's skill directory, skips any skill it didn't install, and a dry run shows every action first. `python3 tools/smoke_check.py` then confirms a runtime sees every skill. Runtime details: [docs/RUNTIMES.md](docs/RUNTIMES.md).

## The skills

| Plugin | Skill | Use it for |
|---|---|---|
| `professional-craft` | `writing-for-people` | Any text a person will read: emails, replies, briefs, posts, summaries, explanations, or making text sound less like AI. Forms for each kind of writing, a catalogue of machine-written patterns with rewrites, `ai_tells.py`, `claim_check.py`, `doc_check.py` |
| | `making-visuals` | Decks and talks, charts and diagrams, dashboards, pages and app screens, and checking the rendered result at real size. `validate_svg.py` |
| `engineering-lifecycle` | `shaping-designs` | Design docs, APIs, data models, migrations, requirements, LLM features, "X or Y?". Interfaces, data moves, failure and capacity, rollout and rollback |
| | `changing-code` | Bugs, failing or flaky tests, incidents, refactors, upgrades. Diagnosis before fixing, history and callers, tests that fail for the right reason |
| | `reviewing-code` | Any diff or pull request. The failures tests miss, each checked before it's reported, plus how to make the change excellent |
| | `merging-safely` | Merges, conflicts, readiness checks, audits of merges already done. `merge_evidence.py` flags changes a merge dropped even when ancestry checks pass |
| | `handling-artifacts` | Files a task creates or ships: where each belongs, cleanup, redaction, packaging, repository weight. `repo_weight.py` |
| `core-rules` | 8 always-on rules | Aim for a top practitioner's result, evidence before claims, no invented facts, untrusted text as leads, a go-ahead before outward or destructive actions, secrets kept out, load the matching skill |

## How well it works

Measured on 24 cases that an agent wrote without seeing these skills or the comparison set, judged blind in both orders by two models [observed; method in [docs/PLAN-v4.md](docs/PLAN-v4.md), numbers in [benchmarks/RESULTS.md](benchmarks/RESULTS.md)]:

- Judges preferred these skills' answers over `ly87ing/agent-skills` in 0.71 of comparisons (0.60 to 0.81), and over Sonnet with only unrelated skills loaded in 0.68 (0.59 to 0.77) [observed].
- On the checklists the case author wrote, the score rose from 0.899 to 0.938 [observed]. Sonnet alone already meets most specialist criteria, so expect a solid but not dramatic gain, mostly on the checks a strong model skips [inferred].
- On the held-out half of the cases, the lead over the reference set was 0.61 (0.45 to 0.76), which is not yet enough to call it proven [observed].

## Measure it yourself

```
python3 -m unittest discover -s tests                                  # every commit (CI)
python3 tools/run_triggers.py --max-cost-usd 10                        # does the right skill load?
tools/run_gate.sh "$PWD/benchmarks/gate/runs" <plugin:case> ...       # with and without each plugin
```

The neutral comparison is reproducible from [benchmarks/v4/README.md](benchmarks/v4/README.md).

## Make it yours

Fill in the terminology table in `shared/style-guide.md` with your own product names and preferred terms, and run `python3 tools/sync_shared.py`.

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). Changes: [CHANGELOG.md](CHANGELOG.md). Security: [SECURITY.md](SECURITY.md). Earlier plans: [docs/history/](docs/history/).

## License

MIT, see [LICENSE](LICENSE). Third-party material is listed in [NOTICE](NOTICE).
