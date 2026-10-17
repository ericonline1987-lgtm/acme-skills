# Runtimes: Claude Code, Codex and Antigravity

**Bottom line:** one set of skill folders serves all three runtimes. Each skill is self-contained (no file outside its own folder), follows the Agent Skills specification, and ships Codex UI metadata; each plugin carries a manifest for every runtime, generated from one source by `tools/build_manifests.py`. Packaging and file placement are tested here; live behaviour was measured in Claude Code only, because no Codex or Antigravity CLI was available to this build.

## Install

| Runtime | Plugin route | Copy route (`tools/install.py`) |
|---|---|---|
| Claude Code | `/plugin marketplace add ericonline1987-lgtm/acme-skills`, then `/plugin install foundations@acme-skills` (and the others) | `--runtime claude` → `~/.claude/skills` or `.claude/skills` |
| Codex | `codex plugin marketplace add ericonline1987-lgtm/acme-skills`, then install from the Plugins Directory | `--runtime codex` → `~/.agents/skills` or `.agents/skills` (`--codex-legacy` → `$CODEX_HOME/skills`) |
| Antigravity | Clone, then `agy plugin install ./plugins/foundations` (and the others) | `--runtime antigravity` → `~/.gemini/config/skills` or `.agents/skills` |

`.agents/skills` is the project folder for both Codex and Antigravity, so `tools/install.py --runtime all --scope project` installs once for both.

Core rules (optional): Claude Code uses the `core-rules` plugin (a session-start hook). Antigravity loads `plugins/core-rules/rules/core.md` natively as a plugin rule. Codex reads rules from `AGENTS.md`, so use `tools/install.py --runtime codex --rules`. The installer writes the rules between marker lines and replaces that block on re-runs.

## What each runtime reads

| | Claude Code | Codex | Antigravity |
|---|---|---|---|
| Plugin manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` (fallback when root `plugin.json` has no `extensions.com.openai`) | root `plugin.json` (`name`, `description`, `$schema` only) |
| Marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` (also reads the Claude file) | — (install by path or URL) |
| Skill folders | `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` + `agents/openai.yaml` | `skills/<name>/SKILL.md` |
| What triggers a skill | `name` + `description` | `name` + `description` only | `name` + `description` |
| Rules | `CLAUDE.md`; plugin hooks | `AGENTS.md` | plugin `rules/*.md`; `.agents/rules/`, `GEMINI.md`, `AGENTS.md` [unverified: third-party guide] |
| Explicit call | `/skill-name` | `$skill-name` | `/skill-name` |

## Rules this repository follows for portability

1. **Self-contained skills.** Codex and Antigravity install skill folders on their own, and `agy plugin install` drops non-skill folders (google-antigravity/antigravity-cli#403). Files several skills share live once in `shared/` and are copied in by `tools/sync_shared.py`; `tests/test_portability.py` copies every skill folder alone and checks each reference resolves.
2. **Spec-only frontmatter.** `name`, `description`, and only the optional fields the specification allows. Codex ignores everything but `name` and `description`, so the description carries the whole trigger.
3. **Neutral instructions.** Skills say what to do, not which product tool to call; the one product-specific command (the Claude Code eval runner) is labelled as such.
4. **Generated, not hand-copied, manifests.** `tools/build_manifests.py --check` and `tools/sync_shared.py --check` run in the test suite, so a stale Codex or Antigravity manifest fails CI.

## What was and wasn't verified

| Check | Status |
|---|---|
| Claude Code plugins validate and install from the marketplace | Verified (`claude plugin validate`, clean-profile install) |
| Every skill passes the Agent Skills naming and frontmatter rules | Verified by `tests/test_skills.py`; the official `skills-ref validate` runs in CI |
| Every skill works when its folder is copied alone | Verified by `tests/test_portability.py` |
| Installer targets, idempotent rules, user skills protected | Verified by `tests/test_install.py` |
| Skill triggering in Claude Code | Measured: see `benchmarks/RESULTS.md` |
| Codex and Antigravity load and trigger the skills | **Not verified here**: no Codex or Antigravity CLI was available. Manifests follow the vendors' published formats. Please report anything that doesn't load. |

## Sources

- Agent Skills specification and validator: [agentskills.io](https://agentskills.io/specification), [agentskills/agentskills](https://github.com/agentskills/agentskills) (commit 69ef37e)
- Codex plugins and marketplaces: [Package your plugin](https://developers.openai.com/codex/plugins/build); examples in [openai/plugins](https://github.com/openai/plugins); `agents/openai.yaml` fields from OpenAI's skill-creator in [openai/skills](https://github.com/openai/skills)
- Codex skill folders: [Agent Skills open standard for Codex CLI](https://codex.danielvaughan.com/2026/05/05/agent-skills-open-standard-portable-skills-codex-cli-cross-agent/) (third party); OpenAI skill-installer (`$CODEX_HOME/skills`)
- Antigravity skills and plugins: [Agent skills](https://antigravity.google/docs/skills/), [Plugins](https://antigravity.google/docs/plugins/); [Where does Antigravity look for Agent Skills?](https://medium.com/google-cloud/where-does-antigravity-look-for-agent-skills-a703518d68c5)
- Antigravity rules files: [Google Antigravity and AGENTS.md](https://thepromptshelf.dev/blog/google-antigravity-agents-md-rules-guide-2026/) (third party)
- Install bug that motivates self-contained skills: [antigravity-cli#403](https://github.com/google-antigravity/antigravity-cli/issues/403)
