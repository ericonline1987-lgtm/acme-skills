"""Unit tests for every bundled script: the checks have to be trustworthy themselves."""
import datetime as dt
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from helpers import PLUGINS_DIR, ROOT, load_module

FOUNDATIONS = PLUGINS_DIR / "foundations"
TEMPLATES = FOUNDATIONS / "shared" / "templates"

ledger = load_module(FOUNDATIONS / "skills/proving-outcomes/scripts/evidence_ledger.py", "evidence_ledger")
sections = load_module(FOUNDATIONS / "shared/scripts/check_sections.py", "check_sections")
claims = load_module(FOUNDATIONS / "skills/tracing-claims/scripts/claim_check.py", "claim_check")
add_case = load_module(FOUNDATIONS / "skills/capturing-learning/scripts/add_eval_case.py", "add_eval_case")
outcomes = load_module(ROOT / "benchmarks/score_outcomes.py", "score_outcomes")

TODAY = dt.date(2026, 10, 13)


def ev(rung, **overrides):
    item = {"rung": rung, "check": f"check {rung}", "result": "ok", "source": "run log"}
    item.update(overrides)
    return item


def quiet(func, *args):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return func(*args)


class EvidenceLedgerTests(unittest.TestCase):
    def base(self, claimed, evidence, follow_up=None):
        return {
            "claim": "x is done",
            "claimed_rung": claimed,
            "evidence": evidence,
            "follow_up": follow_up or {"due": "2026-10-27", "check": "metric", "owner": "me"},
        }

    def test_shipped_example_is_consistent(self):
        data = json.loads((TEMPLATES / "evidence-ledger.example.json").read_text())
        report = ledger.evaluate(data, TODAY)
        self.assertTrue(report["consistent"], report["errors"])
        self.assertEqual(report["supported_rung"], 3)

    def test_overclaim_is_an_error(self):
        report = ledger.evaluate(self.base(3, [ev(1), ev(2)]), TODAY)
        self.assertFalse(report["consistent"])
        self.assertEqual(report["supported_rung"], 2)
        self.assertTrue(any("overclaim" in e for e in report["errors"]))

    def test_rungs_must_be_contiguous(self):
        report = ledger.evaluate(self.base(1, [ev(1), ev(3)]), TODAY)
        self.assertEqual(report["supported_rung"], 1)

    def test_failing_result_does_not_count(self):
        report = ledger.evaluate(self.base(1, [ev(1, result="41 passed, 2 failed")]), TODAY)
        self.assertEqual(report["supported_rung"], 0)
        self.assertFalse(report["consistent"])

    def test_zero_failures_counts(self):
        report = ledger.evaluate(self.base(1, [ev(1, result="41 passed, 0 failed")]), TODAY)
        self.assertEqual(report["supported_rung"], 1)

    def test_missing_source_does_not_count(self):
        report = ledger.evaluate(self.base(1, [ev(1, source="")]), TODAY)
        self.assertEqual(report["supported_rung"], 0)

    def test_not_applicable_rung_counts_with_reason(self):
        report = ledger.evaluate(self.base(2, [{"rung": 1, "na": "no automated checks for an email"}, ev(2)]), TODAY)
        self.assertEqual(report["supported_rung"], 2)
        self.assertTrue(report["consistent"])

    def test_follow_up_required_below_rung_five(self):
        data = self.base(1, [ev(1)])
        del data["follow_up"]
        report = ledger.evaluate(data, TODAY)
        self.assertFalse(report["consistent"])

    def test_explicit_no_follow_up_is_allowed_but_warned(self):
        report = ledger.evaluate(self.base(1, [ev(1)], {"none": "one-off reply"}), TODAY)
        self.assertTrue(report["consistent"])
        self.assertTrue(report["warnings"])

    def test_overdue_follow_up_is_reported(self):
        report = ledger.evaluate(self.base(1, [ev(1)], {"due": "2026-10-01", "check": "c", "owner": "o"}), TODAY)
        self.assertTrue(report["follow_up_overdue"])

    def test_rung_five_needs_no_follow_up(self):
        data = self.base(5, [ev(1), ev(2), ev(3), ev(4), ev(5)])
        del data["follow_up"]
        self.assertTrue(ledger.evaluate(data, TODAY)["consistent"])

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp, "good.json")
            good.write_text(json.dumps(self.base(1, [ev(1)])))
            bad = Path(tmp, "bad.json")
            bad.write_text(json.dumps(self.base(4, [ev(1)])))
            self.assertEqual(quiet(ledger.main, [str(good), "--today", "2026-10-13"]), 0)
            self.assertEqual(quiet(ledger.main, [str(bad), "--today", "2026-10-13"]), 1)
            self.assertEqual(quiet(ledger.main, [str(Path(tmp, "missing.json"))]), 2)


class CheckSectionsTests(unittest.TestCase):
    REQUIRED = ["Outcome", "Follow-up check"]

    def status(self, text):
        return {r["section"]: r["status"] for r in sections.check(text, self.REQUIRED)}

    def test_complete_document_passes(self):
        text = "# T\n\n## Outcome\nRefunds take under a day.\n\n## Follow-up check\nOct 27, Dana, dashboard.\n"
        self.assertEqual(set(self.status(text).values()), {"pass"})

    def test_missing_empty_placeholder_and_todo_fail(self):
        self.assertEqual(self.status("## Outcome\nok\n")["Follow-up check"], "fail")
        self.assertEqual(self.status("## Outcome\n\n## Follow-up check\nok")["Outcome"], "fail")
        self.assertEqual(self.status("## Outcome\n<The change in the world>\n## Follow-up check\nok")["Outcome"], "fail")
        self.assertEqual(self.status("## Outcome\nTODO\n## Follow-up check\nok")["Outcome"], "fail")

    def test_tbd_warns(self):
        self.assertEqual(self.status("## Outcome\nok\n## Follow-up check\nTBD, owner Sam")["Follow-up check"], "warn")

    def test_html_tags_are_not_placeholders(self):
        self.assertEqual(self.status("## Outcome\nline one<br>line two\n## Follow-up check\nok")["Outcome"], "pass")

    def test_headings_inside_code_fences_are_ignored(self):
        text = "## Outcome\n```\n## Follow-up check\n```\n"
        self.assertEqual(self.status(text)["Follow-up check"], "fail")

    def test_every_template_fails_until_filled(self):
        for template in TEMPLATES.glob("*.md"):
            with self.subTest(template=template.name):
                required = sections.required_from_template(template)
                self.assertTrue(required)
                results = sections.check(template.read_text(), required)
                self.assertTrue(all(r["status"] == "fail" for r in results),
                                "an unfilled template must not pass")


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
                          "--criteria", "Short.", "--skill", "defining-done", "--should-not-fire")
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
