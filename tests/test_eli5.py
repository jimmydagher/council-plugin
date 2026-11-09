"""Checks the council:eli5 skill and the root /council skill (TODO #7).

Run from the repo root: python -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["it", "business", "conclave", "court", "arena", "eli5"]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class Eli5Test(unittest.TestCase):
    def test_frontmatter_name(self):
        self.assertRegex(read("skills/eli5/SKILL.md"), r"(?m)^name: eli5$")

    def test_reads_shared_context_and_takes_no_flags(self):
        text = read("skills/eli5/SKILL.md")
        self.assertIn("../../references/shared-context.md", text)
        self.assertIn("No flags", text)

    def test_writes_no_files(self):
        text = read("skills/eli5/SKILL.md")
        self.assertIn("No run files are written", text)
        self.assertNotIn("~/.council/", text)

    def test_output_has_both_sections(self):
        text = read("skills/eli5/SKILL.md")
        self.assertIn("**The kid's version**", text)
        self.assertIn("**Where the kid got lost**", text)


class RootCouncilTest(unittest.TestCase):
    def test_root_skill_name_and_order(self):
        text = read("skills/council/SKILL.md")
        self.assertRegex(text, r"(?m)^name: council$")
        order = [text.index(f"`{s}`") for s in SKILLS]
        self.assertEqual(order, sorted(order), "skills listed out of order")

    def test_every_skill_folder_is_run_by_root(self):
        folders = {p.parent.name for p in ROOT.glob("skills/*/SKILL.md")} - {"council"}
        self.assertEqual(folders, set(SKILLS))

    def test_root_accepts_only_quick_and_peer(self):
        text = read("skills/council/SKILL.md")
        self.assertIn("--quick", text)
        self.assertIn("--peer", text)
        self.assertRegex(text, r"expert flag")


if __name__ == "__main__":
    unittest.main()
