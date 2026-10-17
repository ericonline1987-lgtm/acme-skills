"""Every skill follows the naming, size, frontmatter and linking rules in docs/PLAN.md."""
import re
import unittest

from helpers import (BODY_MAX_WORDS, DESCRIPTION_MAX_CHARS, NAME_MAX_CHARS, all_skill_names,
                     parse_simple_frontmatter, plugin_dirs, skill_dirs, split_frontmatter)

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Backticked relative file references such as `scripts/x.py` or `../../shared/t.md`.
FILE_REF = re.compile(r"(?<![\w/.-])((?:\.\./)*(?:[\w.-]+/)*[\w.-]+\.(?:py|md|json|sh|csv))\b")
# Backticked tokens that look like a skill name (two or more hyphenated words).
SKILL_LIKE = re.compile(r"`([a-z]+(?:-[a-z]+)+)`")
NOT_SKILLS = {"no-ff", "no-commit", "should-not-fire", "with-without", "skill-fired",
              "add-dirs", "max-turns"}


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.skills = skill_dirs()
        self.assertTrue(self.skills, "no skills found")

    def frontmatter(self, skill):
        lines, body = split_frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"))
        return parse_simple_frontmatter(lines), body

    def test_frontmatter_fields_follow_the_agent_skills_spec(self):
        # agentskills.io specification: required name and description; these optional
        # fields only. Codex reads only name and description, so they carry the trigger.
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                fields, _ = self.frontmatter(skill)
                self.assertTrue({"name", "description"} <= set(fields))
                self.assertTrue(set(fields) <= allowed, set(fields) - allowed)

    def test_name_rules(self):
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                fields, _ = self.frontmatter(skill)
                name = fields["name"]
                self.assertEqual(name, skill.name, "name must match the folder")
                self.assertRegex(name, NAME)
                self.assertLessEqual(len(name), NAME_MAX_CHARS)
                self.assertNotRegex(name, r"claude|anthropic")
                self.assertNotIn("--", name, "the spec forbids consecutive hyphens")

    def test_skill_names_are_unique_across_plugins(self):
        names = [s.name for s in self.skills]
        self.assertEqual(len(names), len(set(names)), "a skill name is used in two plugins")

    def test_description_is_a_trigger_within_budget(self):
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                description = self.frontmatter(skill)[0]["description"]
                self.assertLessEqual(len(description), DESCRIPTION_MAX_CHARS)
                self.assertRegex(description, r"\b(Use|Always use) (this skill )?(when|whenever|before)\b",
                                 "say when to use the skill; it is what triggers it")

    def test_description_is_valid_plain_yaml(self):
        # Strict YAML parsers reject ': ' and ' #' inside an unquoted value, and
        # values may not start with a quote or other indicator character.
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                description = self.frontmatter(skill)[0]["description"]
                self.assertNotIn(": ", description)
                self.assertNotIn(" #", description)
                self.assertNotRegex(description, r"^[\"'&*!|>%@`{\[-]")

    def test_body_within_word_budget(self):
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                words = len(self.frontmatter(skill)[1].split())
                self.assertLessEqual(words, BODY_MAX_WORDS, "move detail into a referenced file")

    def test_file_references_resolve_inside_the_plugin(self):
        for plugin in plugin_dirs():
            for skill in skill_dirs(plugin):
                _, body = self.frontmatter(skill)
                body = re.sub(r"<[^<>\n]+>", "", body)  # <placeholders> are not files
                # Only paths in code spans or link targets are references; prose may
                # name a kind of file ("a CLAUDE.md") without pointing at one.
                spans = re.findall(r"`([^`\n]+)`", body) + re.findall(r"\]\(([^)\s]+)\)", body)
                for ref in {r for span in spans for r in FILE_REF.findall(span)}:
                    if ref.startswith(("docs/", "plugins/")):
                        continue
                    with self.subTest(skill=skill.name, ref=ref):
                        target = (skill / ref).resolve()
                        self.assertTrue(target.exists(), f"{ref} does not exist")
                        self.assertTrue(str(target).startswith(str(plugin.resolve())),
                                        f"{ref} leaves the plugin; installed plugins cannot see it")

    def test_named_skills_exist(self):
        known = all_skill_names()
        for skill in self.skills:
            _, body = self.frontmatter(skill)
            for token in set(SKILL_LIKE.findall(body)):
                if token in NOT_SKILLS:
                    continue
                with self.subTest(skill=skill.name, mentions=token):
                    self.assertIn(token, known, "mentions a skill that does not exist")

    def test_scripts_are_documented_and_runnable_stdlib(self):
        for skill in self.skills:
            for script in (skill / "scripts").glob("*.py") if (skill / "scripts").is_dir() else []:
                with self.subTest(script=str(script.relative_to(skill.parent.parent))):
                    text = script.read_text(encoding="utf-8")
                    self.assertTrue(text.startswith("#!/usr/bin/env python3"))
                    self.assertIn('"""', text[:200], "start with a docstring that explains usage and limits")
                    self.assertIn("Usage:", text, "document how to run it")
                    self.assertNotRegex(text, r"(?m)^\s*(import|from) (requests|yaml)\b",
                                        "scripts must run on the standard library alone")


if __name__ == "__main__":
    unittest.main()
