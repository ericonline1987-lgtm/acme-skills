"""Every skill works when its folder is installed on its own, in any of the three runtimes."""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT, skill_dirs, split_frontmatter

CODE_SPAN = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\]\(([^)\s]+)\)")
PATHLIKE = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+\.(?:py|md|json|yaml|csv|sh))\b")


def referenced_paths(body: str) -> set[str]:
    body = re.sub(r"<[^<>\n]+>", "", body)
    spans = CODE_SPAN.findall(body) + LINK.findall(body)
    return {m for span in spans for m in PATHLIKE.findall(span)}


class PortabilityTests(unittest.TestCase):
    def test_no_skill_reaches_outside_its_own_folder(self):
        # Codex and Antigravity install skill folders alone; `agy plugin install` drops
        # non-skill folders (google-antigravity/antigravity-cli#403).
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("../", text)

    def test_every_reference_resolves_when_the_folder_is_copied_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            for skill in skill_dirs():
                copy = Path(tmp, skill.name)
                shutil.copytree(skill, copy)
                _, body = split_frontmatter((copy / "SKILL.md").read_text(encoding="utf-8"))
                for ref in referenced_paths(body):
                    if ref.startswith(("docs/", "plugins/", "benchmarks/", "tests/", "tools/")):
                        continue  # repository paths named for maintainers, not runtime files
                    with self.subTest(skill=skill.name, ref=ref):
                        self.assertTrue((copy / ref).exists(), f"{ref} missing from the standalone copy")

    def test_every_skill_has_codex_metadata(self):
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                text = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn(f"${skill.name}", text)

    def test_generated_files_and_shared_copies_are_in_sync(self):
        for tool in ("tools/build_manifests.py", "tools/sync_shared.py"):
            with self.subTest(tool=tool):
                result = subprocess.run([sys.executable, str(ROOT / tool), "--check"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_every_plugin_has_all_three_manifests(self):
        for plugin in sorted((ROOT / "plugins").iterdir()):
            with self.subTest(plugin=plugin.name):
                self.assertTrue((plugin / ".claude-plugin" / "plugin.json").is_file())
                self.assertTrue((plugin / "plugin.json").is_file(), "Antigravity manifest")
                if (plugin / "skills").is_dir():
                    self.assertTrue((plugin / ".codex-plugin" / "plugin.json").is_file())


if __name__ == "__main__":
    unittest.main()
