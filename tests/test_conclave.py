"""Checks the council:conclave rules that can break when someone edits the skill files.

Run from the repo root: python -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCLAVE_DIR = ROOT / "skills" / "conclave"
MIN_SEATS = 3
MAX_SEATS = 12
CONFIRM_ABOVE = 20

POSITION_LINE = re.compile(r"^POSITION: .+$")
CLAIM_LINE = re.compile(r"^CLAIM (\d+) \[(FACT|INFERENCE|ASSUMPTION|UNKNOWN)\]: .+$")
BLIND_SPOT_LINE = re.compile(r"^BLIND SPOT: .+$")
ASK_LINE = re.compile(r"^ASK: .+$")
CHALLENGE_LINE = re.compile(r'^CHALLENGE (l\d\d): ".+" — .+$')
VIEW_LINE = re.compile(r"^VIEW (l\d\d): (AGREE|DISAGREE|NO VIEW) — .+$")
STANCE_LINE = re.compile(r"^STANCE: (BACK|BACK IF|OPPOSE) — .+$")
MOVED_LINE = re.compile(r"^MOVED: (YES|NO) — .+$")
COMPROMISE_LINE = re.compile(r"^COMPROMISE: .+$")
KILL_LINE = re.compile(r"^KILL: .+$")
FORMAT_LINES = (
    POSITION_LINE, CLAIM_LINE, BLIND_SPOT_LINE, ASK_LINE, CHALLENGE_LINE,
    VIEW_LINE, STANCE_LINE, MOVED_LINE, COMPROMISE_LINE, KILL_LINE,
)
COUNTED_LINES = (STANCE_LINE, MOVED_LINE)


def full_calls(n):
    return 3 * n + 1


def quick_calls(n):
    return n + 1


def read_seating():
    """Return [(id, counterweight id), ...] from lenses.md's seating table, in seating order."""
    text = (CONCLAVE_DIR / "lenses.md").read_text(encoding="utf-8")
    body = text.split("## Seating order", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\| (\d+) \| (l\d\d) \| [^|]+ \| (l\d\d) \|", body, flags=re.MULTILINE)
    assert [int(n) for n, _, _ in rows] == list(range(1, len(rows) + 1)), "seat numbers must run 1..n"
    return [(lens_id, partner) for _, lens_id, partner in rows]


def format_blocks(skill_text):
    """Return the lines of every blockquoted ```text example in SKILL.md."""
    blocks = re.findall(r"> ```text\n(.*?)> ```", skill_text, flags=re.DOTALL)
    return [[line.removeprefix("> ").strip() for line in block.strip().splitlines()] for block in blocks]


def read_stance(text):
    """Apply SKILL.md's count rule to one round 3 file. Returns (stance, moved) or None if malformed."""
    stance = moved = None
    for line in text.strip().splitlines():
        if m := STANCE_LINE.match(line):
            stance = m.group(1)
        elif m := MOVED_LINE.match(line):
            moved = m.group(1)
    return None if stance is None or moved is None else (stance, moved)


def count(stances):
    """Reading of the stances cast (None = abstained): strict majority, otherwise split."""
    cast = [s for s in stances if s is not None]
    yes = sum(1 for stance, _ in cast if stance in ("BACK", "BACK IF"))
    no = sum(1 for stance, _ in cast if stance == "OPPOSE")
    if yes > no:
        reading = "leaning yes"
    elif no > yes and no > len(cast) - no:
        reading = "leaning no"
    else:
        reading = "split"
    return reading, yes, no, len(stances) - len(cast)


def stance_file(stance):
    return f"STANCE: {stance} — reason\nMOVED: NO — held\nCOMPROMISE: x\nKILL: y"


class LensPoolTests(unittest.TestCase):
    def setUp(self):
        self.seating = read_seating()

    def test_twelve_unique_lenses_in_order(self):
        ids = [lens_id for lens_id, _ in self.seating]
        self.assertEqual(ids, [f"l{n:02d}" for n in range(1, MAX_SEATS + 1)])

    def test_pairs_are_mutual_and_adjacent(self):
        partner = dict(self.seating)
        for n in range(1, MAX_SEATS, 2):
            a, b = f"l{n:02d}", f"l{n + 1:02d}"
            self.assertEqual((partner[a], partner[b]), (b, a))

    def test_every_lens_has_a_section_with_its_fields(self):
        text = (CONCLAVE_DIR / "lenses.md").read_text(encoding="utf-8")
        for lens_id, _ in self.seating:
            section = re.search(rf"(?ms)^### {lens_id} — .+?(?=^### |\Z)", text)
            self.assertIsNotNone(section, lens_id)
            for field in ("**Method:**", "**Blind spot:**", "**Must answer:**"):
                self.assertIn(field, section.group(0), f"{lens_id} {field}")

    def test_every_panel_size_has_at_most_one_unpaired_lens(self):
        partner = dict(self.seating)
        ids = [lens_id for lens_id, _ in self.seating]
        for n in range(MIN_SEATS, MAX_SEATS + 1):
            seated = ids[:n]
            unpaired = [lens_id for lens_id in seated if partner[lens_id] not in seated]
            self.assertEqual(len(unpaired), n % 2, f"N={n}: {unpaired}")


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = (CONCLAVE_DIR / "SKILL.md").read_text(encoding="utf-8")

    def test_documented_call_counts(self):
        for n, calls in ((3, 10), (6, 19), (12, 37)):
            self.assertEqual(full_calls(n), calls)
            self.assertIn(f"{n} → {calls}", self.skill)
        for n, calls in ((3, 4), (4, 5)):
            self.assertEqual(quick_calls(n), calls)
            self.assertIn(f"{n} → {calls}", self.skill)

    def test_confirmation_threshold(self):
        self.assertIn(f"over {CONFIRM_ABOVE}", self.skill)
        self.assertLessEqual(full_calls(6), CONFIRM_ABOVE, "the default panel must not need confirmation")
        self.assertGreater(full_calls(7), CONFIRM_ABOVE)

    def test_format_examples_match_patterns(self):
        lines = [line for block in format_blocks(self.skill) for line in block]
        self.assertTrue(lines)
        seen = set()
        for line in lines:
            matched = [p for p in FORMAT_LINES if p.match(line)]
            self.assertTrue(matched, f"example line matches no format: {line!r}")
            seen.update(matched)
        self.assertEqual(seen, set(FORMAT_LINES), "every format has an example")

    def test_counted_patterns_are_documented(self):
        for pattern in COUNTED_LINES:
            self.assertIn(f"`{pattern.pattern}`", self.skill)

    def test_flags_are_documented(self):
        for flag in ("--quick", "--seats N"):
            self.assertIn(flag, self.skill)

    def test_every_panel_size_is_in_range(self):
        self.assertIn("whole number 3-12", self.skill)


class CountTests(unittest.TestCase):
    def test_majority_of_yes_side(self):
        stances = [read_stance(stance_file(s)) for s in ("BACK", "BACK", "BACK IF", "BACK IF", "OPPOSE", "OPPOSE")]
        self.assertEqual(count(stances), ("leaning yes", 4, 2, 0))

    def test_tie_is_split(self):
        stances = [read_stance(stance_file(s)) for s in ("BACK", "BACK IF", "BACK", "OPPOSE", "OPPOSE", "OPPOSE")]
        self.assertEqual(count(stances), ("split", 3, 3, 0))

    def test_majority_of_oppose(self):
        stances = [read_stance(stance_file(s)) for s in ("OPPOSE", "OPPOSE", "OPPOSE", "BACK IF")]
        self.assertEqual(count(stances), ("leaning no", 1, 3, 0))

    def test_abstentions_are_excluded(self):
        stances = [read_stance(stance_file(s)) for s in ("BACK", "OPPOSE", "BACK IF", "OPPOSE")] + [None, None]
        self.assertEqual(count(stances), ("split", 2, 2, 2))

    def test_malformed_stance_files(self):
        self.assertIsNone(read_stance("MOVED: NO — x"), "no stance")
        self.assertIsNone(read_stance("STANCE: BACK — x"), "no moved")
        self.assertIsNone(read_stance("STANCE: MAYBE — x\nMOVED: NO — x"), "bad stance")
        self.assertIsNone(read_stance("STANCE: BACK - x\nMOVED: NO — x"), "plain hyphen instead of em dash")


class PluginTests(unittest.TestCase):
    def test_plugin_json_mentions_conclave(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertIn("council:conclave", manifest["description"])
        self.assertIn("conclave", manifest["keywords"])

    def test_readme_and_shared_context_cover_conclave(self):
        for path in ("README.md", "references/shared-context.md"):
            self.assertIn("council:conclave", (ROOT / path).read_text(encoding="utf-8"), path)


if __name__ == "__main__":
    unittest.main()
