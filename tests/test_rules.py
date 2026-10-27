"""The core-rules plugin injects a short rules file at session start, and is measured."""
import json
import re
import unittest

from helpers import PLUGINS_DIR

PLUGIN = PLUGINS_DIR / "core-rules"
RULES = PLUGIN / "rules" / "core.md"
# Every line is paid for in every session; raise only with a measured reason (docs/PLAN-v1.1.md).
MAX_RULE_CHARS = 1200
MAX_RULES = 8


class CoreRulesTests(unittest.TestCase):
    def test_hook_injects_the_rules_file_at_session_start(self):
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())["hooks"]
        commands = [h["command"] for group in hooks["SessionStart"] for h in group["hooks"]]
        self.assertTrue(any("${CLAUDE_PLUGIN_ROOT}/rules/core.md" in c for c in commands))
        self.assertTrue(RULES.is_file())

    def test_rules_stay_short(self):
        text = RULES.read_text()
        rules = [line for line in text.splitlines() if line.startswith("- ")]
        self.assertLessEqual(len(text), MAX_RULE_CHARS)
        self.assertLessEqual(len(rules), MAX_RULES)
        self.assertNotIn("<!--", text, "comments are billed every session; put notes in the README")

    def test_rules_are_portable(self):
        # No tool or product names, so the same lines work in any agent runtime.
        self.assertNotRegex(RULES.read_text(), r"\b(Bash|Edit|Write|WebFetch|mcp__\w+|ToolSearch)\b")

    def test_every_rule_has_an_eval_case_and_one_checks_for_bloat(self):
        sources = [p.read_text() for p in (PLUGIN / "evals").glob("*/SOURCE.md")]
        rule_count = len([l for l in RULES.read_text().splitlines() if l.startswith("- ")])
        covered = {int(n) for s in sources for n in re.findall(r"rules? (\d)", s)}
        covered |= {int(n) for s in sources for m in re.findall(r"rules ([\d and,]+)", s) for n in re.findall(r"\d", m)}
        self.assertTrue(any("must not add process" in s for s in sources), "need a no-bloat case")
        # Rules 2 and 6 are behaviour a text-only eval cannot exercise (edits, outward actions);
        # they are covered by the skills' own cases (changing-code, guarding-agent-actions).
        # Rule 7 (load the matching skill) is measured by tools/run_triggers.py --with-rules.
        self.assertTrue({1, 3, 4, 5} <= covered, f"rules with cases: {sorted(covered)} of {rule_count}")


if __name__ == "__main__":
    unittest.main()
