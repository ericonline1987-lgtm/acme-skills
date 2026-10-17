# Benchmarks

Three layers, from least effort to most meaningful. Results go in [RESULTS.md](RESULTS.md).

## 1. Contract tests (every commit)

```
python3 -m unittest discover -s tests
```

Offline and standard-library only. They check structure, naming, size caps, links, eval coverage, and every bundled script. CI runs them.

## 2. Behaviour evals (every release)

Each plugin has an `evals/` folder: one should-fire case per skill and at least one should-not-fire case, with one LLM grader per success criterion.

```
claude plugin eval plugins/foundations --runs 3 -j 8 --judge-model sonnet
```

The runner adds a no-plugin baseline arm and reports the delta. Every run uses the credential of the account running it and costs money; see RESULTS.md for typical totals.

**To add a case from a real failure:** use `plugins/foundations/skills/capturing-learning/scripts/add_eval_case.py`.

**To compare with another skill set:** package its skills as a plugin (a folder with `.claude-plugin/plugin.json` and `skills/`), copy one of our `evals/` folders into it, and run the same command against it. Same prompts and same graders keep the comparison fair.

## 2b. Trigger recall and precision (when descriptions change)

Each skill has `plugins/<plugin>/evals/triggers/<skill>.json`, prompts labelled `should_trigger` true or false in the Agent Skills format. Near-miss negatives share keywords with the skill but need something else.

```
python3 tools/run_triggers.py --skills <skill> [<skill> ...] --max-cost-usd 5
```

Each query runs in a fresh Claude Code session with all skill plugins loaded. The runner reports, per skill, how many should-trigger prompts loaded it, how many near-misses correctly didn't, and which other skill fired instead. Results so far are in `benchmarks/triggers/`.

## 3. Outcome log (weekly, on real work)

Evals test responses to prompts. The outcome log tests whether real work achieved what it was for.

1. For each real task, add a row to [outcomes.csv](outcomes.csv) at hand-off: the rung claimed, and the rung a reviewer finds the evidence supports.
2. When the follow-up is due, fill in `outcome_achieved`.
3. Log some tasks done without the skills (`setup` = `none`) so there is a comparison arm.
4. Score it:

```
python3 benchmarks/score_outcomes.py benchmarks/outcomes.csv
```

It reports overclaim rate, follow-up planning, outcome achievement and corrections per setup, each with a Wilson confidence interval, and lists overdue outcome checks. Overlapping intervals mean the difference isn't established yet; keep logging.
