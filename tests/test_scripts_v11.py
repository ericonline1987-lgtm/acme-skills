"""Unit tests for the scripts added in v1.1, using real throwaway git repositories."""
import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from helpers import PLUGINS_DIR, load_module

ENG = PLUGINS_DIR / "engineering-lifecycle" / "skills"
merge = load_module(ENG / "merging-safely/scripts/merge_evidence.py", "merge_evidence")
svg = load_module(ENG / "verifying-interfaces/scripts/validate_svg.py", "validate_svg")
doc = load_module(PLUGINS_DIR / "professional-craft/skills/writing-documents/scripts/doc_check.py", "doc_check")
weight = load_module(PLUGINS_DIR / "foundations/skills/handling-artifacts/scripts/repo_weight.py", "repo_weight")


def sh(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def write(repo, name, text):
    Path(repo, name).write_text(text)


def new_repo(tmp):
    repo = Path(tmp, "r")
    repo.mkdir()
    sh(repo, "init", "-q", "-b", "main")
    sh(repo, "config", "user.email", "t@example.com")
    sh(repo, "config", "user.name", "t")
    return repo


def quiet(func, *args):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return func(*args)


class MergeEvidenceTests(unittest.TestCase):
    def build(self, tmp):
        """main and release diverge: release edits a and b, main edits b and c."""
        repo = new_repo(tmp)
        for name in "abc":
            write(repo, f"{name}.txt", f"{name}1\n")
        sh(repo, "add", "-A"); sh(repo, "commit", "-qm", "base")
        sh(repo, "checkout", "-qb", "release")
        write(repo, "a.txt", "a-release\n"); write(repo, "b.txt", "b-release\n")
        sh(repo, "commit", "-qam", "release work")
        sh(repo, "checkout", "-q", "main")
        write(repo, "b.txt", "b-main\n"); write(repo, "c.txt", "c-main\n")
        sh(repo, "commit", "-qam", "main work")
        return repo

    def test_pre_merge_model_finds_hotspots(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.build(tmp)
            facts = merge.collect(repo, "release", "HEAD", None, 30)
            self.assertEqual(facts["hotspots"], ["b.txt"])
            self.assertEqual(facts["left_right_counts"], {"only_on_target": 1, "only_on_source": 1})
            self.assertFalse(facts["source_contained_by_ancestry"])
            self.assertEqual(facts["flags"], [])

    def test_good_merge_has_no_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.build(tmp)
            subprocess.run(["git", "-C", str(repo), "merge", "-q", "release"], capture_output=True)
            write(repo, "b.txt", "b-main\nb-release\n")
            sh(repo, "add", "-A"); sh(repo, "commit", "-qm", "merge")
            facts = merge.collect(repo, "release", "HEAD", "HEAD^1", 30)
            self.assertTrue(facts["source_contained_by_ancestry"])
            self.assertEqual(facts["dropped_suspects"], [])
            self.assertIn("a.txt", facts["landed_files"])
            self.assertEqual(facts["flags"], [])

    def test_wholesale_resolution_is_flagged_even_though_ancestry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.build(tmp)
            subprocess.run(["git", "-C", str(repo), "merge", "-q", "release"], capture_output=True)
            write(repo, "a.txt", "a1\n")      # release's change to a.txt thrown away
            write(repo, "b.txt", "b-main\n")  # conflict resolved by taking main
            sh(repo, "add", "-A"); sh(repo, "commit", "-qm", "merge, took main")
            facts = merge.collect(repo, "release", "HEAD", "HEAD^1", 30)
            self.assertTrue(facts["source_contained_by_ancestry"], "ancestry alone looks fine")
            self.assertEqual(facts["dropped_suspects"], ["a.txt"])
            self.assertTrue(facts["flags"])

    def test_dirty_worktree_is_flagged_and_bad_ref_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.build(tmp)
            write(repo, "c.txt", "uncommitted\n")
            self.assertIn("worktree has uncommitted changes", merge.collect(repo, "release", "HEAD", None, 30)["flags"])
            self.assertEqual(quiet(merge.main, ["--repo", str(repo), "--source-ref", "nope"]), 2)

    def test_incoming_list_is_truncated_with_a_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.build(tmp)
            facts = merge.collect(repo, "release", "HEAD", None, 0)
            self.assertEqual(facts["incoming_commits"], [])
            self.assertEqual(facts["incoming_truncated"], 1)


class ValidateSvgTests(unittest.TestCase):
    GOOD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" width="10" height="10">'
            '<title>t</title><defs><linearGradient id="g"/></defs><rect fill="url(#g)"/></svg>')

    def test_clean_file_passes(self):
        self.assertEqual(svg.check(self.GOOD), {"errors": [], "warnings": []})

    def test_each_error_class(self):
        cases = {
            "not well-formed": "<svg",
            "root element": "<html/>",
            "missing viewBox": '<svg xmlns="http://www.w3.org/2000/svg"/>',
            "invalid viewBox": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10"/>',
            "duplicate id": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><g id="x"/><g id="x"/></svg>',
            "missing id": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><use href="#gone"/></svg>',
            "script": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><script>x</script></svg>',
            "event attribute": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1" onload="x()"/>',
        }
        for expected, text in cases.items():
            with self.subTest(expected=expected):
                errors = " ".join(svg.check(text)["errors"])
                self.assertIn(expected, errors)

    def test_external_dependency_is_a_warning(self):
        text = self.GOOD.replace("<title>", '<image href="https://x.test/a.png"/><title>')
        report = svg.check(text)
        self.assertEqual(report["errors"], [])
        self.assertTrue(any("external" in w for w in report["warnings"]))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = Path(tmp, "g.svg"), Path(tmp, "b.svg")
            good.write_text(self.GOOD); bad.write_text("<svg")
            self.assertEqual(quiet(svg.main, [str(good)]), 0)
            self.assertEqual(quiet(svg.main, [str(bad)]), 1)
            self.assertEqual(quiet(svg.main, [str(Path(tmp, "none.svg"))]), 2)


class DocCheckTests(unittest.TestCase):
    def kinds(self, text, budget=500):
        return [d["kind"] for d in doc.check(text, budget, 35)["defects"]]

    def test_clean_document_has_no_defects(self):
        text = "# Search outage\n\nSearch timed out for 29 minutes; the fix ships Sep 3.\n\n## Cause was a zero cache TTL\n\nRolling back restored service.\n"
        self.assertEqual(self.kinds(text), [])

    def test_each_defect_kind(self):
        text = ("# T\n\nThis document summarizes the incident. As mentioned above, it went fine.\n\n"
                "## Overview\n\nOwner TBD.\n\n" + "word " * 40 + "end.\n")
        kinds = self.kinds(text)
        for expected in ("slow opening", "meta-commentary", "label heading", "open placeholder", "long sentence"):
            self.assertIn(expected, kinds)

    def test_budget_excludes_appendix_and_code(self):
        body = "Point first. " * 20
        text = f"# T\n\n{body}\n\n```\n{'code ' * 500}\n```\n\n## Appendix\n\n{'detail ' * 500}\n"
        self.assertNotIn("over budget", self.kinds(text, budget=100))
        self.assertIn("over budget", self.kinds(text, budget=20))

    def test_inline_html_is_not_a_placeholder(self):
        self.assertNotIn("open placeholder", self.kinds('# T\n\nThe fix shipped. See <span class="x">here</span>.\n'))
        self.assertIn("open placeholder", self.kinds("# T\n\nOwner: <name of the owner>.\n"))

    def test_hedging_and_bold(self):
        self.assertIn("heavy hedging", self.kinds("# T\n\nIt might perhaps possibly work, arguably.\n"))
        self.assertIn("bold overuse", self.kinds("# T\n\n**A** **B** **C** text.\n"))

    def test_sentence_after_lowercase_start_is_split(self):
        text = "# T\n\n" + "Short one here. " + "v1.1 then starts a sentence. " * 3 + "\n"
        self.assertNotIn("long sentence", self.kinds(text))


class RepoWeightTests(unittest.TestCase):
    def test_deleted_binary_is_reported_as_not_in_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            Path(repo, "video.bin").write_bytes(bytes(range(256)) * 400)
            write(repo, "README", "hi\n")
            sh(repo, "add", "-A"); sh(repo, "commit", "-qm", "add")
            sh(repo, "rm", "-q", "video.bin"); sh(repo, "commit", "-qm", "remove")
            blobs = weight.largest_blobs(repo, 5, 0)
            self.assertEqual(blobs[0]["path"], "video.bin")
            self.assertFalse(blobs[0]["in_head"])
            self.assertTrue(next(b for b in blobs if b["path"] == "README")["in_head"])
            self.assertEqual(weight.largest_blobs(repo, 5, 50)[0]["path"], "video.bin")
            self.assertEqual(len(weight.largest_blobs(repo, 5, 50)), 1, "min size filters small files")

    def test_not_a_repo_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(quiet(weight.main, ["--repo", tmp]), 2)


if __name__ == "__main__":
    unittest.main()
