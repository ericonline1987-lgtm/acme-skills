# Plan: skills that aim past "high quality"

**Bottom line:** most agent skill sets, including the strong ones, aim at the quality of one task's output: correct, checked, safe, readable. v1.0 of this repo treats that as the floor. It aims at four things beyond it: the real outcome happened, people can trust the work without redoing it, the next task starts ahead of this one, and the human stays in charge and keeps getting sharper. Every skill serves one of those goals, and every claim of improvement is measured against a no-skills baseline, not asserted.

## 1. Goals

| Floor (most skill sets stop here) | Goal beyond it | How we will know |
|---|---|---|
| Prove it works | **Prove it mattered**: the outcome the work was for actually happened | Share of tasks whose follow-up check confirms the outcome |
| A complete, evidenced plan | **Explore before committing**: compare cheap real alternatives, not one plan on paper | Share of design tasks that compared ≥2 options on evidence |
| Don't break what exists | **Leave it easier to change**: every change records why | Decision records written; time-to-understand on the next change |
| The reader understands | **The reader decides and acts well** | A fresh reader can act on the document without questions |
| Clean, safe files | **Trust by default**: every load-bearing claim is traceable | Overclaim rate (claimed more than the evidence shows) |
| The agent avoids mistakes | **The team compounds**: each failure becomes a test, each good pattern a skill | Eval cases added per month; repeat-failure rate |
| (rarely addressed) | **The human stays in charge** | Decisions surfaced to the person rather than made silently |

## 2. Design principles

1. **Outcome over output.** "Done" names a change in the world and the evidence that shows it, not a file produced.
2. **Enforce with code where possible.** Checks that can be a script are a script (`evidence_ledger.py`, `claim_check.py`, `check_sections.py`). Prose is kept for judgment.
3. **Small context footprint.** Descriptions of at most 400 characters, SKILL.md bodies of at most 900 words, and detail in templates loaded on demand. Tests enforce both caps.
4. **One owner per decision.** Each concern lives in one skill; other skills point to it by name rather than copying it.
5. **Human decision rights are explicit.** Every plan and hand-off lists the decisions that belong to the person, and irreversible actions wait for their go-ahead.
6. **Work with the host, not against it.** No skill overrides platform or session instructions.
7. **Measured, not asserted.** A skill stays only if it beats the no-plugin baseline on its eval cases.
8. **Every failure becomes a test.** A lesson is written up as an eval case before the skill is changed.

## 3. Architecture

Three plugins in one marketplace. `foundations` holds the work loop every task shares; the two domain plugins apply it to engineering and to professional writing. Each plugin works alone, and works better with `foundations` installed.

```
define done ──► explore options ──► do the work ──► prove outcome ──► hand off ──► capture learning
 (defining-done)  (exploring-options)  (domain skills)  (proving-outcomes)  (handoff report)  (capturing-learning)
        ▲                                   │
        └──── delegating-work, tracing-claims, guarding-agent-actions apply throughout ────┘
```

| Plugin | Skill | Goal it serves |
|---|---|---|
| foundations | defining-done | Prove it mattered; human in charge |
| | exploring-options | Explore before committing |
| | delegating-work | Trust by default (accept against a contract) |
| | proving-outcomes | Prove it mattered; trust by default |
| | tracing-claims | Trust by default |
| | capturing-learning | Team compounds |
| | guarding-agent-actions | Human in charge; safety |
| engineering-lifecycle | writing-requirements | Prove it mattered (outcome metric up front) |
| | designing-systems | Explore before committing |
| | changing-code | Leave it easier to change |
| | reviewing-code | Trust by default |
| | writing-tests | Prove it works (the floor, done well) |
| | merging-safely | Trust by default |
| | building-ai-features | AI-era work: evals before prompts |
| professional-craft | writing-documents | Reader decides and acts well |
| | briefing-decisions | Reader decides; human in charge |
| | building-presentations | Reader decides and acts well |
| | writing-emails | Prove it mattered (the email's one outcome) |
| | researching-topics | Trust by default |

## 4. Measurement

Three layers, from least to most effort, and from least to most meaningful.

| Layer | What it checks | When | Tool |
|---|---|---|---|
| Contract tests | Structure, naming, size caps, links, eval coverage, script behaviour | Every commit (CI) | `python3 -m unittest discover -s tests` |
| Behaviour evals | Each skill's output against criteria, **with vs. without the plugin**, one grader per criterion, a capable judge, 3+ runs | Every release | `claude plugin eval plugins/<plugin> --runs 3 --judge-model sonnet` |
| Outcome log | Did the real outcome happen? Was anything overclaimed? How many corrections? | Weekly, on real work | `benchmarks/outcomes.csv` + `benchmarks/score_outcomes.py` |

**Release gate:** CI green, and the eval delta against the baseline is not negative for any plugin. A skill whose cases show no lift over two releases is revised or removed.

**Targets for the first 8 weeks** (to be adjusted once the baseline is in):

- [target] Overclaim rate below 5% of tasks, with the upper 95% bound reported, not just the point rate.
- Every task with a stated outcome has a follow-up check recorded.
- [target] Positive eval delta on at least 80% of should-fire cases.
- [target] `foundations` adds at most about 1,500 tokens of descriptions to a session. Measured at about 756 [observed: `claude plugin details`].

**Comparing with another skill set** (for example `ly87ing/agent-skills`): package its skills as a plugin, copy one of our `evals/` folders into it, and run the same cases. Same prompts and graders for both arms, so the comparison is fair.

## 5. Roadmap

| Phase | When | Deliverable | Exit check |
|---|---|---|---|
| 0. Foundation | Done in v1.0 | 19 skills across 3 plugins, templates, 4 checker scripts plus the outcome scorer, eval suites, offline tests, CI; first indicative measurement and one tuning round | Met: tests pass, manifests validate, criteria pass rate 94% against 68% for plain Claude, 18 of 19 skills trigger [observed, n=1 per case] |
| 1. Baseline | Weeks 1–2 | Release-gate eval run (3 runs, both arms); log 20 real tasks in the outcome log | Gate numbers with intervals recorded in `benchmarks/RESULTS.md` |
| 2. Tune | Weeks 3–6 | Every observed failure added as an eval case; agentic cases with real tools for `guarding-agent-actions`; cut skills with no lift | Delta positive on ≥80% of cases |
| 3. Enforce | Weeks 6–8 | Promote checks that showed lift to hooks (for example, run `evidence_ledger.py` before a task is reported done) | Overclaim rate under target for 2 weeks |
| 4. Roll out | After week 8 | Tagged releases (`claude plugin tag`), team install guide, owner per plugin | Two teams using pinned versions |

## 6. What the first measurement taught

Recorded in full in `benchmarks/RESULTS.md`; the ones that change this plan:

1. **Triggering is the first bottleneck.** A skill that doesn't fire adds nothing. Descriptions are written as triggers ("Use whenever someone asks …") and are tested with should-not-fire cases.
2. **Measurement needs care.** One grader per criterion, a capable judge, and 3+ runs; single runs swung by ±0.6 on one case [observed].
3. **Plain Claude is already strong on safety.** The injection case scored 5/5 without the plugin [observed], so `guarding-agent-actions` needs agentic cases with real tools before its value can be judged.

## 7. Risks

| Risk | Mitigation |
|---|---|
| Skills trigger too often and bloat context | Size caps in tests; should-NOT-fire eval cases in every plugin |
| Follow-up checks get skipped because outcomes lag | `proving-outcomes` writes the check date into the hand-off; the outcome log flags overdue checks |
| LLM-graded evals are noisy | 3+ runs per case, Wilson intervals, outcome graders rather than trajectory graders |
| Process overhead slows small tasks | Every skill scales down: a one-line contract for a small task is valid |
| Checker scripts give false confidence | Each script states what it cannot see; heuristics report "not checked" rather than "pass" |

## 8. Decisions that are yours

- Org name and whether the repo is public or private.
- Which 20 real tasks go into the outcome log first.
- Whether to promote checks to hooks in phase 3, which makes them mandatory rather than advisory.
- The eval budget per release (each run uses your own Claude credential).
