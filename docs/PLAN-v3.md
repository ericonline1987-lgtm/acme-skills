# Plan v3: fewer skills, deeper

**Bottom line:** v3 replaces 25 broad skills with seven deep ones in the four areas where a capable model's default output is visibly weaker than a seasoned professional's: writing that reads as a person wrote it, visual documents and interfaces, R&D and design judgment, and code change, review and merge. Advice a model already follows (state the bottom line, compare options, verify before claiming) moves into the always-on core rules or is deleted.

## Why

- In the v2.0 gate, plain Claude scored 0.80 to 0.90 on nine skills' cases [observed: benchmarks/gate/2026-11-02-summary.json]. Those skills mostly restated good general practice, and they cost always-on description tokens in every session.
- The reference set (`ly87ing/agent-skills`) has six skills averaging about 4,100 words each, with reference files [observed: word count]. v2.0 averaged about 700 per skill [observed]. Its depth comes from rules anchored in real failures, enumerations a reviewer can tick off, and worked examples.
- None of the v2.0 skills addressed the patterns that make text read as machine-written.

## The seven skills

| Plugin | Skill | Absorbs from v2.0 | New depth |
|---|---|---|---|
| professional-craft | `writing-for-people` | writing-documents, briefing-decisions, writing-emails, tracing-claims, researching-topics (citing) | A catalogue of AI tells with rewrites, rhythm and register, accessibility, a revision pass, `ai_tells.py` |
| professional-craft | `making-visuals` | building-presentations, figures-and-html, verifying-interfaces | Deck construction, chart choice and honesty, page layout, rendered-surface checks, Playwright |
| engineering-lifecycle | `shaping-designs` | designing-systems, writing-requirements, exploring-options, defining-done, building-ai-features | Interfaces and contracts, data and migrations, failure modes, capacity, design review |
| engineering-lifecycle | `changing-code` | changing-code, debugging-failures, writing-tests | Diagnosis before change, boundaries, test design that fails for the right reason |
| engineering-lifecycle | `reviewing-code` | reviewing-code | Defect classes by area, a review-depth reference |
| engineering-lifecycle | `merging-safely` | merging-safely | A command-level merge workflow, an audit mode |
| engineering-lifecycle | `handling-artifacts` | handling-artifacts | Kept: plain Claude fails file placement and cleanup (restored after the head-to-head) |

Removed: the `foundations` plugin (its proof ladder, outcome-first and safety rules live in core rules), `planning-work`, `running-long-tasks`, `delegating-work`, `capturing-learning`, `authoring-skills` (its method moves to CONTRIBUTING.md). They stay in git history.

## How depth is judged

- Each skill has at least two cases (most have five or more), run without the skill as well as with it, and kept only where plain Claude falls short.
- Writing cases use deterministic graders where a tell can't be quoted innocently (emoji, headings) and judge criteria scoped to the draft itself for phrases and constructions, so an answer that quotes a tell to explain it isn't failed.
- Release gate as in v2.0: three runs per arm, every case, failing answers read by hand.

## Not in scope

Languages other than English for the writing guidance. File formats (.docx, .pptx): the skills shape content and design, not file production.
