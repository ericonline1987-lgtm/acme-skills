"""Each plugin's eval suite is complete and well-formed for `claude plugin eval`."""
import re
import unittest

from helpers import parse_simple_frontmatter, plugin_dirs, skill_dirs, split_frontmatter

GRADER_TYPES = {"regex", "tool_order", "tool_used", "file_exists", "llm", "baseline"}


def cases(plugin):
    evals = plugin / "evals"
    return sorted(c for c in evals.iterdir()
                  if c.is_dir() and c.name not in ("results", "triggers")) if evals.is_dir() else []


def graders(case):
    out = {}
    for path in sorted((case / "graders").glob("*.md")):
        lines, body = split_frontmatter(path.read_text(encoding="utf-8"))
        out[path.stem] = (parse_simple_frontmatter(lines), body.strip())
    return out


class EvalSuiteTests(unittest.TestCase):
    def test_every_plugin_has_an_eval_suite(self):
        for plugin in plugin_dirs():
            with self.subTest(plugin=plugin.name):
                self.assertTrue(cases(plugin), "no eval cases")

    def test_every_case_is_well_formed(self):
        for plugin in plugin_dirs():
            for case in cases(plugin):
                with self.subTest(case=f"{plugin.name}/{case.name}"):
                    self.assertRegex(case.name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
                    lines, body = split_frontmatter((case / "prompt.md").read_text(encoding="utf-8"))
                    fields = parse_simple_frontmatter(lines)
                    self.assertIn("max_turns", fields)
                    self.assertTrue(body.strip(), "empty prompt")
                    self.assertTrue((case / "SOURCE.md").is_file(), "record why the case exists")
                    gs = graders(case)
                    self.assertTrue(gs, "no graders")
                    for name, (fm, gbody) in gs.items():
                        self.assertIn(fm.get("type"), GRADER_TYPES, name)
                        if fm["type"] == "llm":
                            self.assertTrue(gbody, f"{name}: llm grader needs criteria")
                        if fm["type"] == "tool_used":
                            self.assertIn("tool", fm, name)

    def test_every_case_has_an_outcome_grader(self):
        # A trigger check alone says nothing about quality.
        for plugin in plugin_dirs():
            for case in cases(plugin):
                with self.subTest(case=f"{plugin.name}/{case.name}"):
                    types = [fm["type"] for fm, _ in graders(case).values()]
                    self.assertTrue(any(t != "tool_used" for t in types))

    def test_every_skill_has_a_should_fire_case(self):
        for plugin in plugin_dirs():
            covered = set()
            for case in cases(plugin):
                for fm, _ in graders(case).values():
                    if fm.get("type") == "tool_used" and fm.get("tool") == "Skill" \
                            and fm.get("max") != "0":
                        covered.add(fm.get("input_match"))
            for skill in skill_dirs(plugin):
                with self.subTest(skill=skill.name):
                    self.assertIn(skill.name, covered)

    def test_every_plugin_has_should_not_fire_cases(self):
        for plugin in plugin_dirs():
            if not skill_dirs(plugin):
                continue  # nothing to trigger; see test_rules.py for rule plugins
            negatives = [
                fm for case in cases(plugin) for fm, _ in graders(case).values()
                if fm.get("type") == "tool_used" and fm.get("max") == "0"
            ]
            with self.subTest(plugin=plugin.name):
                self.assertTrue(negatives, "no should-not-fire case")
                for fm in negatives:
                    self.assertEqual(fm.get("min"), "0")
                    self.assertEqual(fm.get("arm"), "both", "otherwise it is display-only and never scored")

    def test_no_eval_results_are_committed(self):
        for plugin in plugin_dirs():
            with self.subTest(plugin=plugin.name):
                self.assertFalse((plugin / "evals" / "results").exists())


class TriggerSetTests(unittest.TestCase):
    """Trigger query sets in the Agent Skills format ({query, should_trigger}), one per skill."""

    def test_every_skill_has_a_balanced_trigger_set_with_near_misses(self):
        import json
        for plugin in plugin_dirs():
            for skill in skill_dirs(plugin):
                with self.subTest(skill=skill.name):
                    path = plugin / "evals" / "triggers" / f"{skill.name}.json"
                    rows = json.loads(path.read_text(encoding="utf-8"))
                    self.assertTrue(all(set(r) == {"query", "should_trigger"} for r in rows))
                    positives = [r for r in rows if r["should_trigger"]]
                    negatives = [r for r in rows if not r["should_trigger"]]
                    self.assertGreaterEqual(len(positives), 3)
                    self.assertGreaterEqual(len(negatives), 3)
                    queries = [r["query"].strip().lower() for r in rows]
                    self.assertEqual(len(queries), len(set(queries)), "duplicate query")


if __name__ == "__main__":
    unittest.main()
