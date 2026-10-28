"""Checks that no council skill writes its run files into the project (TODO #6).

Run from the repo root: python -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# file -> the run-folder root it must name
RUN_ROOTS = {
    "skills/arena/SKILL.md": "~/.council/arena/<run-id>/",
    "skills/court/SKILL.md": "~/.council/court/<run-id>/",
    "skills/conclave/SKILL.md": "~/.council/conclave/<run-id>/",
    "references/peer-review.md": "~/.council/<area>/<run-id>/",
}
# every markdown file a user-facing run could read or that documents the rule
SCANNED = [*ROOT.glob("skills/**/*.md"), *ROOT.glob("references/*.md"), ROOT / "README.md"]
STALE_PATH = re.compile(r"(?<![~/\w])\.(arena|court|conclave|council)/<run-id>")
CWD_WRITE = re.compile(r"in the current (folder|directory)", re.IGNORECASE)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class RunFilesTest(unittest.TestCase):
    def test_each_skill_names_its_profile_root(self):
        for rel, root in RUN_ROOTS.items():
            with self.subTest(file=rel):
                self.assertIn(root, read(rel))

    def test_no_in_project_run_folder_left(self):
        for path in SCANNED:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(STALE_PATH.search(text), "bare .<skill>/<run-id> path")
                self.assertIsNone(CWD_WRITE.search(text), "run files written to the current folder")

    def test_skills_state_the_safety_rules(self):
        for rel in RUN_ROOTS:
            with self.subTest(file=rel):
                text = read(rel)
                self.assertIn("-2", text, "collision suffix")
                self.assertRegex(text, r"never (fall back|write into)", "no project fallback")


if __name__ == "__main__":
    unittest.main()
