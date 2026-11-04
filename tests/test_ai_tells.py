"""writing-for-people/scripts/ai_tells.py: catches the countable tells, leaves plain prose alone."""
import tempfile
import unittest
from pathlib import Path

from helpers import PLUGINS_DIR, load_module

tells = load_module(PLUGINS_DIR / "professional-craft/skills/writing-for-people/scripts/ai_tells.py", "ai_tells")

PLAIN = """We moved the offsite from March 3 to March 10. The venue had booked two groups into
the same room, and only noticed on Friday.

Nothing else changes. Same hotel, same agenda, and the shuttle still leaves from the
office at eight. If the new date clashes with something you can't move, tell me by
Wednesday and I'll sort out a video link for that session.

Sorry for the churn. I've asked them for a written confirmation this time.
"""


def categories(text, allow=frozenset()):
    return [(h["category"], h["detail"]) for h in tells.check(text, set(allow))["hits"]]


class AiTellsTests(unittest.TestCase):
    def test_plain_prose_is_clean(self):
        result = tells.check(PLAIN, set())
        self.assertEqual(result["hits"], [])
        self.assertEqual(result["strong"], 0)

    def test_stock_phrases_and_words(self):
        found = categories("In today's fast-paced world, our platform plays a vital role. We leverage seamless tools.")
        self.assertIn(("phrase", "in today's fast-paced world"), found)
        self.assertTrue(any(c == "phrase" and "vital role" in d for c, d in found))
        self.assertIn(("word", "leverage"), found)
        self.assertIn(("word", "seamless"), found)

    def test_constructions(self):
        text = ("It's not just a tool, but a partner.\n"
                "Whether you stop by for coffee or order a cake, we're here.\n"
                "No more spreadsheets, no more guesswork.\n"
                "Sales rose 4%, highlighting the strength of the brand.\n")
        labels = {d for c, d in categories(text) if c == "construction"}
        self.assertEqual(labels, {"not just X but Y", "Whether you... or...", "No more X, no more Y",
                                  "significance tacked on"})

    def test_openers_and_closers(self):
        text = "Great question! Here is the answer.\n\nThe bus leaves at nine.\n\nLet me know if you need anything else."
        found = categories(text)
        self.assertIn(("framing", "announcing opener"), found)
        self.assertIn(("framing", "summary, offer or sign-off"), found)

    def test_format_tells_and_allow_list(self):
        text = "# How We Built The Thing\n\nWe launched today 🚀 #startup\n"
        found = categories(text)
        self.assertIn(("format", "Title Case heading"), found)
        self.assertIn(("format", "emoji"), found)
        self.assertIn(("format", "hashtag"), found)
        self.assertNotIn(("format", "emoji"), categories(text, {"emoji", "hashtags"}))

    def test_one_bold_lead_is_fine_a_list_of_them_is_not(self):
        one = "- **Note** the lid is not dishwasher safe.\n- It holds 750 ml.\n"
        many = "\n".join(f"- **Point {i}** explains something" for i in range(3))
        self.assertNotIn("inline-header bullet", [d for _, d in categories(one)])
        self.assertEqual([d for _, d in categories(many)].count("inline-header bullet"), 3)

    def test_code_is_skipped(self):
        self.assertEqual(categories("Run `leverage --seamless` now.\n\n```\ndelve()\n```\n"), [])

    def test_density_limits(self):
        dashes = " ".join(["It works — mostly — when you try it."] * 10)
        self.assertIn("em dashes: more than one per 200 words", tells.check(dashes, set())["limits"])
        uniform = " ".join(["The team shipped the change to production on Tuesday morning."] * 10)
        self.assertIn("rhythm: sentence lengths too uniform", tells.check(uniform, set())["limits"])

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            clean, dirty = Path(d, "a.md"), Path(d, "b.md")
            clean.write_text(PLAIN)
            dirty.write_text("Certainly! This is a testament to our robust, seamless, innovative work.")
            self.assertEqual(tells.main([str(clean)]), 0)
            self.assertEqual(tells.main([str(dirty)]), 1)
            self.assertEqual(tells.main([str(Path(d, "missing.md"))]), 2)


if __name__ == "__main__":
    unittest.main()
