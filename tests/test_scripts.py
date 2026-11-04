"""Unit tests for every bundled script: the checks have to be trustworthy themselves."""
import datetime as dt
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from helpers import PLUGINS_DIR, ROOT, load_module

WRITING = PLUGINS_DIR / "professional-craft/skills/writing-for-people"
TEMPLATES = ROOT / "shared" / "templates"

claims = load_module(WRITING / "scripts/claim_check.py", "claim_check")
add_case = load_module(ROOT / "tools/add_eval_case.py", "add_eval_case")
outcomes = load_module(ROOT / "benchmarks/score_outcomes.py", "score_outcomes")

TODAY = dt.date(2026, 10, 13)


def ev(rung, **overrides):
    item = {"rung": rung, "check": f"check {rung}", "result": "ok", "source": "run log"}
    item.update(overrides)
    return item


def quiet(func, *args):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return func(*args)


class ClaimCheckTests(unittest.TestCase):
    def flagged(self, text):
        return [f["text"] for f in claims.find_untraced(text)]

    def test_untraced_figures_and_absolutes_are_flagged(self):
        self.assertTrue(self.flagged("Revenue grew 12% last quarter."))
        self.assertTrue(self.flagged("We are the fastest in the market."))
        self.assertTrue(self.flagged("Timeouts dropped by 1,200 requests."))

    def test_traced_claims_pass(self):
        for text in (
            "Revenue grew 12% last quarter [observed: finance dashboard].",
            "Revenue grew 12% ([source](https://example.com)).",
            "Revenue grew 12% (source: Q3 board pack).",
            "Revenue grew 12%, according to the CFO.",
            "Hit 99% uptime [target].",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.flagged(text))

    def test_everyday_words_and_small_numbers_are_not_flagged(self):
        self.assertFalse(self.flagged("All three teams met on Tuesday and agreed 2 next steps."))
        self.assertFalse(self.flagged("Upgrade to version 1.2.3 first."))
        self.assertFalse(self.flagged("This shipped in v1.0 of the plugin."))
        self.assertTrue(self.flagged("Saving one config took 70.6 s."))

    def test_code_headings_and_front_matter_are_skipped(self):
        text = "---\ntitle: 50% off\n---\n# Grew 90%\n\n```\nx = 99%\n```\n"
        self.assertFalse(self.flagged(text))

    def test_table_rows_are_checked(self):
        self.assertTrue(self.flagged("| Metric | Value |\n|---|---|\n| Churn | 30% |\n"))

    def test_untraced_claim_after_a_traced_sentence_is_still_found(self):
        # Regression: a sentence starting lowercase or after "e.g." was merged into the
        # previous, traced sentence, and the untraced claim slipped through.
        self.assertTrue(self.flagged("Revenue grew 12% [observed: dashboard]. v2 costs 30% more than v1."))
        self.assertTrue(self.flagged("Churn fell 12% (source: Q3 pack). e.g. our rival is the fastest."))

    def test_table_header_rows_are_not_claims(self):
        self.assertFalse(self.flagged("| Always-on cost | Best case |\n|---|---|\n| low | high [estimate] |\n"))


class AddEvalCaseTests(unittest.TestCase):
    def make_plugin(self, tmp):
        plugin = Path(tmp, "p")
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "p", "version": "0.0.1"}')
        return plugin

    def run_tool(self, *args):
        return quiet(add_case.main, list(args))

    def test_creates_one_grader_per_criterion_and_trigger_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = self.make_plugin(tmp)
            code = self.run_tool("--plugin-dir", str(plugin), "--name", "deploy-overclaim",
                                 "--prompt", "Say it's deployed.", "--criteria", "Does not overclaim.",
                                 "--criteria", "Names a read-back check.", "--skill", "proving-outcomes",
                                 "--source", "incident 2026-10-02")
            self.assertEqual(code, 0)
            case = plugin / "evals" / "deploy-overclaim"
            names = sorted(p.name for p in (case / "graders").glob("*.md"))
            self.assertEqual(len([n for n in names if n.startswith("c")]), 2)
            self.assertIn("skill-fired.md", names)
            self.assertIn("incident 2026-10-02", (case / "SOURCE.md").read_text())
            self.assertIn("max_turns", (case / "prompt.md").read_text())

    def test_should_not_fire_is_scored_in_both_arms(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = self.make_plugin(tmp)
            self.run_tool("--plugin-dir", str(plugin), "--name", "neg", "--prompt", "hi",
                          "--criteria", "Short.", "--skill", "changing-code", "--should-not-fire")
            text = (plugin / "evals/neg/graders/skill-not-used.md").read_text()
            for line in ("max: 0", "min: 0", "arm: both"):
                self.assertIn(line, text)

    def test_refuses_overwrite_bad_names_and_non_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = self.make_plugin(tmp)
            args = ["--plugin-dir", str(plugin), "--name", "dup", "--prompt", "p", "--criteria", "c"]
            self.assertEqual(self.run_tool(*args), 0)
            self.assertEqual(self.run_tool(*args), 1)
            self.assertEqual(self.run_tool("--plugin-dir", str(plugin), "--name", "Bad Name",
                                           "--prompt", "p", "--criteria", "c"), 1)
            self.assertEqual(self.run_tool("--plugin-dir", tmp, "--name", "x",
                                           "--prompt", "p", "--criteria", "c"), 1)


class ScoreOutcomesTests(unittest.TestCase):
    HEADER = "date,task,area,setup,claimed_rung,supported_rung,outcome_due,outcome_achieved,corrections,notes\n"

    def score(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "o.csv")
            path.write_text(self.HEADER + rows)
            return outcomes.score(outcomes.parse_rows(path), TODAY)

    def test_wilson_interval_known_value(self):
        low, high = outcomes.wilson(5, 10)
        self.assertAlmostEqual(low, 0.237, places=3)
        self.assertAlmostEqual(high, 0.763, places=3)
        self.assertIsNone(outcomes.wilson(0, 0))

    def test_example_rows_are_skipped(self):
        self.assertEqual(self.score("2026-10-01,EXAMPLE x,eng,a,1,1,,,0,\n"), {})

    def test_shipped_log_parses(self):
        rows = outcomes.parse_rows(ROOT / "benchmarks" / "outcomes.csv")
        self.assertEqual(rows, [], "shipped log should hold only EXAMPLE rows")

    def test_rates_per_setup(self):
        report = self.score(
            "2026-10-01,a,eng,skills,3,3,2026-10-20,yes,0,\n"
            "2026-10-01,b,eng,skills,3,2,2026-10-05,,1,\n"
            "2026-10-01,c,eng,none,4,2,,,2,\n"
        )
        skills = report["skills"]
        self.assertEqual(skills["overclaim"]["k"], 1)
        self.assertEqual(skills["follow_up_planned"]["k"], 2)
        self.assertEqual(skills["outcome_achieved"]["n"], 1)
        self.assertEqual(skills["overdue_checks"], 1)
        self.assertEqual(report["none"]["overclaim"]["rate"], 1.0)

    def test_malformed_rows_are_rejected(self):
        with self.assertRaises(ValueError):
            self.score("2026-10-01,a,eng,s,three,1,,,0,\n")
        with self.assertRaises(ValueError):
            self.score("2026-10-01,a,eng,s,1,1,,maybe,0,\n")


if __name__ == "__main__":
    unittest.main()
