# Contributing

A change is accepted when it is measured, not when it reads well.

## Adding or changing a skill

1. **Start from a case.** Write the eval case first, from a real task or failure:
   ```
   python3 plugins/foundations/skills/capturing-learning/scripts/add_eval_case.py \
     --plugin-dir plugins/<plugin> --name <case> --prompt "..." \
     --criteria "..." --criteria "..." --skill <skill> --source "<what happened>"
   ```
   Add a `--should-not-fire` case too if the change could make the skill trigger more often.
2. **Write or edit `plugins/<plugin>/skills/<skill>/SKILL.md`.**
3. **Run the offline tests**: `python3 -m unittest discover -s tests`.
4. **Run the evals** for the plugin with the baseline arm:
   `claude plugin eval plugins/<plugin> --runs 3 --judge-model sonnet`.
   Paste the case table into the pull request.
5. **Bump the version** in the plugin's `plugin.json` and in `.claude-plugin/marketplace.json` together, and add a CHANGELOG line.

## Files several skills share

Edit them in `shared/` only, then run `python3 tools/sync_shared.py`. The copies inside skills are generated; CI fails if they drift. Skills must never reference `../` paths, because Codex and Antigravity install skill folders on their own.

## Manifests for Codex and Antigravity

Edit `.claude-plugin/plugin.json` and `tools/skill_ui.json`, then run `python3 tools/build_manifests.py`. Never hand-edit `plugin.json`, `.codex-plugin/plugin.json`, `agents/openai.yaml` or `.agents/plugins/marketplace.json`.

## Trigger queries

Every skill has `plugins/<plugin>/evals/triggers/<skill>.json`: realistic prompts that should load the skill, and near-misses that share its keywords but need something else. When a description changes, run `python3 tools/run_triggers.py --skills <skill>` and paste the recall and precision into the pull request.

## Rules the tests enforce

- **Name:** lowercase-hyphenated with no double hyphens, matches the folder, at most 64 characters, unique across plugins, no "claude" or "anthropic".
- **Frontmatter:** `name` and `description`, plus only the optional fields the Agent Skills specification allows. The description is plain YAML (no `: ` inside it), at most 400 characters, and leads with when to use the skill ("Use this skill whenever…").
- **Body:** at most 900 words. Move detail into files beside it.
- **References** stay inside the plugin. Installed plugins can't see each other's files, so refer to other plugins' skills by name, never by path.
- **Scripts** start with a usage docstring, use only the standard library, and say what they can't check.
- **Evals:** every skill has a should-fire case; every plugin has should-not-fire cases scored in both arms (`min: 0`, `max: 0`, `arm: both`); every case has at least one outcome grader, not only a trigger check.

## Writing descriptions that trigger

The description is the only part Claude sees before choosing a skill. Measured lesson from v1.0: summary-style descriptions fired on 8 of 19 cases, while descriptions naming the situations and phrasings users actually type fired on 18 of 19 [observed; see benchmarks/RESULTS.md].

- Lead with what the skill produces, then "Use whenever someone asks …" with the words users really say.
- Name the non-obvious situations ("even when tests and deploys are green").
- Check every rewrite against the should-not-fire cases.

## Review

One approver per plugin. The reviewer checks the eval table (no negative delta, no new false triggers) and reads the SKILL.md against its own quality bar.
