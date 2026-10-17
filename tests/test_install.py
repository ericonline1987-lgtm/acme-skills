"""tools/install.py: correct targets, idempotent rules, never clobbers the user's own skills."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from helpers import ROOT, load_module

install = load_module(ROOT / "tools" / "install.py", "install_tool")


def run(*args):
    with redirect_stdout(io.StringIO()) as out:
        code = install.main(list(args))
    return code, out.getvalue()


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name, "home")
        self.project = Path(self.tmp.name, "proj")
        self.home.mkdir()
        self.project.mkdir()
        self.env = mock.patch.dict(os.environ, {"HOME": str(self.home)}, clear=False)
        self.env.start()
        os.environ.pop("CODEX_HOME", None)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_documented_targets(self):
        p = self.project
        self.assertEqual(install.targets("codex", "project", p, False)[0], p / ".agents" / "skills")
        self.assertEqual(install.targets("antigravity", "project", p, False)[0], p / ".agents" / "skills")
        self.assertEqual(install.targets("codex", "user", p, False)[0], self.home / ".agents" / "skills")
        self.assertEqual(install.targets("codex", "user", p, True)[0], self.home / ".codex" / "skills")
        self.assertEqual(install.targets("antigravity", "user", p, False)[0], self.home / ".gemini" / "config" / "skills")
        self.assertEqual(install.targets("claude", "user", p, False)[0], self.home / ".claude" / "skills")

    def test_project_install_copies_every_skill_self_contained(self):
        code, _ = run("--runtime", "codex", "--scope", "project", "--project", str(self.project))
        self.assertEqual(code, 0)
        skills = self.project / ".agents" / "skills"
        self.assertEqual(len([p for p in skills.iterdir() if (p / "SKILL.md").is_file()]), 21)
        self.assertTrue((skills / "defining-done" / "assets" / "outcome-contract.md").is_file())
        self.assertTrue((skills / "defining-done" / "scripts" / "check_sections.py").is_file())

    def test_users_own_skill_is_never_replaced_without_force(self):
        own = self.project / ".agents" / "skills" / "reviewing-code"
        own.mkdir(parents=True)
        (own / "SKILL.md").write_text("mine")
        code, out = run("--runtime", "codex", "--scope", "project", "--project", str(self.project))
        self.assertEqual(code, 1)
        self.assertIn("SKIP", out)
        self.assertEqual((own / "SKILL.md").read_text(), "mine")

    def test_rules_block_is_added_once_and_keeps_user_content(self):
        agents = self.project / "AGENTS.md"
        agents.write_text("# Mine\n- Use tabs.\n")
        for _ in range(2):
            run("--runtime", "codex", "--scope", "project", "--project", str(self.project), "--rules")
        text = agents.read_text()
        self.assertTrue(text.startswith("# Mine\n- Use tabs.\n"))
        self.assertEqual(text.count(install.BEGIN), 1)
        self.assertIn("explicit go-ahead", text)

    def test_dry_run_writes_nothing(self):
        run("--runtime", "all", "--scope", "user", "--rules", "--dry-run")
        self.assertEqual(list(self.home.iterdir()), [])

    def test_shared_project_folder_is_handled_once_for_codex_and_antigravity(self):
        code, out = run("--runtime", "all", "--scope", "project", "--project", str(self.project))
        self.assertEqual(code, 0)
        self.assertIn("already handled", out)


if __name__ == "__main__":
    unittest.main()
