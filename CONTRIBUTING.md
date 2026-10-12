# Contributing a skill

## Adding a skill
1. Pick the plugin it belongs in (`engineering-lifecycle` or `professional-craft`).
2. Create `plugins/<plugin>/skills/<skill-name>/SKILL.md`.
3. Name it lowercase-hyphenated, gerund form (`writing-…`, `reviewing-…`), under 64 characters, and without "claude" or "anthropic".

## SKILL.md checklist
- [ ] Frontmatter has `name` (matches folder) and `description`.
- [ ] `description` says **what it does** and **when to use it** — this is what triggers the skill.
- [ ] Body is short: process steps, quality bar, output format.
- [ ] Long templates, checklists, or examples live in files next to SKILL.md and are referenced by relative path.
- [ ] Shared conventions point to the plugin's own `shared/` folder rather than being copied in. (An installed plugin can only see files inside its own folder.)

## Before opening a PR
- Try the skill on at least three real prompts, including one where it should **not** trigger.
- Bump the plugin `version` in both `plugin.json` and `.claude-plugin/marketplace.json`.

## Review
One approver per plugin. Reviewers check the description triggers correctly and the output meets the skill's own quality bar.
