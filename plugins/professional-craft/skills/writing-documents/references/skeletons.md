# More skeletons

Use these alongside the table in SKILL.md. Sections run in order; drop a section the
material can't fill rather than padding it.

## Design doc or RFC (budget: 3 pages; 1 for an incremental change)

Context and scope → for a replacement, each current problem with its cause and what the
new design removes → goals and non-goals → design → alternatives with trade-offs →
cross-cutting concerns (security, privacy, cost, operations) → rollout and rollback →
open questions with owners. Default figure: a context diagram when more than one
component is involved; a sequence diagram per flow that crosses a boundary; old beside
new for a replacement.

## README (budget: one screen before the first link)

What it is, in one line → quick start that works when pasted → one minimal example →
links to deeper docs. A screenshot or GIF only when the result is visual.

## Release notes (budget: one line per change)

What changed for the user, grouped by impact, with breaking changes and the required
upgrade steps first. Internal refactors are omitted.

## Change hand-off note for QA, operations or the next owner (budget: 1 page + appendix)

1. What changed, deletions included, one line each, named by behaviour (not by ticket,
   class or review round).
2. What a user can perceive.
3. How it works, in enough detail that a tester can derive cases.
4. What to test, in priority order.
5. What is **not** a defect (known, intended differences).
6. What must be prepared (data, accounts, flags, environments).
7. What the developer already verified, and at which rung.
8. Who still has to confirm what.
9. What to watch at rollout.
10. Developer contact.

Default figure: a table of changes; a diagram only for a flow the tester can't infer.

## Agent instruction file: CLAUDE.md, AGENTS.md, a rules file (budget: every line earns its place)

Title with the repository name. Then only what changes what the agent does: commands
(build, test, lint, run), important paths, boundaries (what may and may not change),
and hard rules written as their executable part ("Run `make test` before committing";
not "We value quality"). No mission, history, ownership, vision or slogans. Test each
line: would deleting it change the agent's behaviour? If not, delete it.

## Notice (budget: one paragraph)

The change, who is affected and who is not, and when. No title, background or "next
steps" section for two facts and a date.

## Reference or API page (budget: no prose beyond a lead line)

Searchable headings; for each item, the signature or field, a parameter table, one
example, and its errors. No narrative.

## Multi-topic brief or meeting pre-read (budget: one screen per topic)

Agenda naming each topic → one section per topic → next actions per responsible role.
