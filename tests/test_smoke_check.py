"""tools/smoke_check.py installs into a scratch project and compares the agent's answer."""
import sys
import unittest

from helpers import ROOT, load_module, skill_dirs

smoke = load_module(ROOT / "tools" / "smoke_check.py", "smoke_check")


class SmokeCheckTests(unittest.TestCase):
    def test_expected_skills_are_every_skill(self):
        self.assertEqual(smoke.expected_skills(), sorted(s.name for s in skill_dirs()))

    def test_names_match_as_whole_words_only(self):
        self.assertEqual(smoke.missing_from("writing-documents\nwriting-emails", ["writing-documents", "writing-emails"]), [])
        self.assertEqual(smoke.missing_from("writing-documents-v2", ["writing-documents"]), ["writing-documents"])

    def test_end_to_end_with_a_fake_runtime(self):
        names = " ".join(smoke.expected_skills())
        fake = f"{sys.executable} -c \"import sys; print('\\n'.join(sys.argv[2:]))\" {{prompt}} {names}"
        self.assertEqual(smoke.main(["--runtime", "codex", "--command", fake]), 0)
        partial = f"{sys.executable} -c \"print('defining-done')\" {{prompt}}"
        self.assertEqual(smoke.main(["--runtime", "codex", "--command", partial]), 1)

    def test_command_needs_a_prompt_slot(self):
        self.assertEqual(smoke.main(["--runtime", "codex", "--command", "true"]), 2)


if __name__ == "__main__":
    unittest.main()
