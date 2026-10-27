# Changelog

## 1.4.0 (2026-10-26)

Fixes from a review of all 21 skills: skills that rarely loaded, eval cases that couldn't tell a skill from plain Claude, and lessons that lived only in the results file. See benchmarks/RESULTS.md.

### Changed
- `core-rules` (1.3.0): rule 1 asks for a checkable outcome, with a target number where one applies; a seventh rule makes the agent load the matching skill before answering, even when the task looks simple; rule 6 also keeps passwords, tokens and keys out of output, logs and commits. Now recommended for every install.
- Descriptions of `guarding-agent-actions`, `researching-topics`, `reviewing-code`, `writing-documents` and `writing-emails` name the request categories people actually use.
- `guarding-agent-actions`: following a file's instructions authorises the task, not every command in it; stop on piping a download into a shell, sending data out or posting a secret.
- `writing-emails`: unknowns stay bare placeholders, never guessed values; a chaser always carries a reply-by date.
- `changing-code`: the commit message records the reason whichever way a stale-test question is decided.
- `building-ai-features`: a new section on trusting an eval before its scores (check the grader by hand, check outputs exist, match the harness, keep cases that discriminate, test routing on its own), from this project's own measurement lessons.
- `designing-systems`: the options method points to `exploring-options`; high-impact designs need an independent challenge.
- `handling-artifacts`: the history-rewrite procedure moved to `references/rewriting-history.md`, which also covers secrets committed to history; `proving-outcomes` points to it rather than repeating the rule.
- `merging-safely` uses the same verdicts as `reviewing-code`.
- `doc_check.py` ignores placeholders inside inline code, which are syntax, not gaps. Regression test added.
- `tools/run_triggers.py --with-rules` loads the core-rules plugin to measure its effect.

### Added
- Eval cases `email-partial-commitment`, `email-vendor-chaser` and `guarding-readme-setup`; four held-out trigger queries for each of the five reworded skills.

### Fixed
- `verify-dashboard-before-sending`: removed a criterion the prompt never asks for and reworded one the judge failed on correct answers.

## 1.3.0 (2026-10-26)

`reviewing-code` adopts the Claude Code team's review practices. See benchmarks/RESULTS.md.

### Changed
- `reviewing-code` (engineering-lifecycle 1.3.0): a risk tier set by what the change touches decides review depth and required human approval; findings come from separate single-purpose passes (bugs in the diff, introduced risks, callers and history, project rules, tests); every finding is confirmed independently before it is reported; an explicit list of things never to report (pre-existing problems, style, linter-enforced issues, generic advice, deliberately silenced issues); project rules files are checked by path and quoted; re-reviews look only at new changes, never repeat a finding, name the bug class and stop line-editing at round three; suggestions only when they fully fix the issue; the verdict is a recommendation, never a substitute for the human approval the tier requires.

### Added
- Eval cases `review-preexisting-bug`, `review-third-round` and `review-project-rule`.

## 1.2.0 (2026-10-16)

First-class Codex and Antigravity support, and descriptions tuned for trigger recall. See docs/RUNTIMES.md and benchmarks/RESULTS.md.

### Added
- Codex packaging: `.codex-plugin/plugin.json` per plugin, `.agents/plugins/marketplace.json`, and `agents/openai.yaml` for every skill.
- Antigravity packaging: root `plugin.json` per plugin; `core-rules` loads as a native Antigravity rule.
- `tools/install.py`: installs into Claude Code, Codex or Antigravity at user or project scope, optionally adding the core rules to `CLAUDE.md`, `AGENTS.md` or Antigravity's rules; idempotent, never replaces a skill it didn't install.
- `tools/build_manifests.py` and `tools/sync_shared.py`: generate the per-runtime manifests and copy shared files into skills, each with a `--check` mode run by the tests.
- Trigger query sets (`plugins/*/evals/triggers/`, 126 queries with near-miss negatives) and `tools/run_triggers.py`.
- `docs/RUNTIMES.md`, `tests/test_portability.py`, `tests/test_install.py`; the official `skills-ref` validator in CI.

### Changed
- Skills are self-contained: templates, the section checker and the style guide are copied into the skills that use them, from one source in `shared/`. No skill references a file outside its own folder.
- All 21 descriptions lead with the user's intent ("Use this skill whenever…"); trigger recall on short prompts rose from 3 of 18 to about 44 of 63 with no false triggers, at the same length cap.
- The frontmatter test now allows the specification's optional fields and rejects consecutive hyphens in names.

## 1.1.1 (2026-10-15)

Pre-publication audit.

### Fixed
- `claim_check.py` missed an untraced claim when it followed a sourced sentence and started lowercase or after "e.g."; sentences are now split at every full stop. Regression test added.
- `doc_check.py` reported inline HTML such as `<span>` as an unfilled placeholder. Regression test added.

### Changed
- `merge_evidence.py` finds dropped changes with one tree diff instead of one git call per file.
- `verifying-interfaces` description names "make sure it works" and browser or end-to-end tests; it now triggered in 2 of 2 runs on the dashboard case, with no trigger on the CSS question [observed].
- `writing-tests` covers browser tests (UI surface and success criteria first, then Playwright); `changing-code` asks for the stale-test reason in the commit message.
- Personal email removed from `marketplace.json`.

### Added
- `NOTICE` for the reference author's MIT-licensed eval text in `benchmarks/h2h/cases/b-*`.

## 1.1.0 (2026-10-14)

Full coverage of the reference set (`ly87ing/agent-skills`), measured head-to-head. See docs/PLAN-v1.1.md and benchmarks/RESULTS.md.

### Added
- `verifying-interfaces` (engineering-lifecycle): browser and rendered-UI evidence, Playwright practice, rendered-surface checks, `validate_svg.py`.
- `handling-artifacts` (foundations): file placement, cleanup, redaction for the widest reader, packaging deliverables, repository weight, `repo_weight.py`.
- `core-rules` plugin (optional): six always-on rules injected at session start, with eval cases.
- `merging-safely`: `merge_evidence.py` (flags changes dropped by a merge even when ancestry checks pass), post-merge error patterns, merge-request resolution, multi-repo reporting.
- `changing-code`: boundary and style references; a stop step before speculative abstractions.
- `writing-documents`: more skeletons (README, release notes, QA hand-off, agent instruction files), figures and HTML guidance, `doc_check.py`.
- `designing-systems`: replaced-mechanism inventory (loud or silent) and a completeness check.
- `benchmarks/h2h/`: bundle builder, shared cases, results.

### Changed
- All plugins at 1.1.0. Tests now cover plugins without skills and the rules plugin's contract.

## 1.0.0 (2026-10-13)

Goals move from output quality to outcomes, trust, compounding learning and human decision rights. See docs/PLAN.md.

### Added
- `foundations` plugin: defining-done, exploring-options, delegating-work, proving-outcomes, tracing-claims, capturing-learning, guarding-agent-actions.
- Templates: outcome contract, hand-off report, decision record, delegation brief, evidence ledger.
- Scripts: evidence_ledger.py, claim_check.py, check_sections.py, add_eval_case.py, benchmarks/score_outcomes.py.
- Skills: changing-code, merging-safely, building-ai-features (engineering-lifecycle); briefing-decisions, researching-topics (professional-craft).
- Eval suites for all three plugins (19 should-fire cases, 6 should-not-fire cases, one grader per criterion).
- Offline test suite and CI; outcome log and results file.

### Changed
- All 0.1 skills rewritten around their outcome: requirements start from a success measure, designs compare real options, reviews check history and callers, tests must be shown to fail, documents pass a fresh-reader test, emails plan their follow-up.
- Skill descriptions rewritten as triggers after measurement showed 8 of 19 firing; now 18 of 19 with no false triggers.

## 0.1.0 (2026-10-11)

- Initial scaffold: engineering-lifecycle and professional-craft with seven starter skills.
