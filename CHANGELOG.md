# Changelog

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
