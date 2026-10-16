# Changelog

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
