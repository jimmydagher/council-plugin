"""Checks the --peer mode rules that can break when someone edits the peer-review or area skill files.

Run from the repo root: python -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PEER_FILE = ROOT / "references" / "peer-review.md"
AREAS = ("it", "business")
MAX_EXPERTS = 4
TOP_POINTS = (3, 2, 1)

FINDINGS_HEADER = re.compile(r"^FINDINGS:( none)?$")
FINDING_LINE = re.compile(r"^- (Critical|High|Medium|Low) \| .+ \| .+$")
MARK_LINE = re.compile(r"^F(\d+): (HOLDS|OVERSTATED|WRONG|OUT OF LANE) — .+$")
TOP_LINE = re.compile(r"^TOP: F\d+(, F\d+){0,2}$")
MISSED_HEADER = re.compile(r"^MISSED:( none)?$")
FORMAT_LINES = (FINDINGS_HEADER, FINDING_LINE, MARK_LINE, TOP_LINE, MISSED_HEADER)
TALLIED_LINES = (MARK_LINE, TOP_LINE, FINDING_LINE)


def calls(n):
    return 2 * n + 1


def format_blocks(text):
    """Return the lines of every blockquoted ```text example."""
    blocks = re.findall(r"> ```text\n(.*?)> ```", text, flags=re.DOTALL)
    return [[line.removeprefix("> ").strip() for line in block.strip().splitlines()] for block in blocks]


def anonymize(findings_by_expert):
    """Apply peer-review.md's order: round-robin across experts, starting with the last in canonical order.

    findings_by_expert is [(expert, [finding, ...]), ...] in canonical order. Returns {"F1": (expert, finding), ...}.
    """
    reversed_experts = list(reversed(findings_by_expert))
    ordered = []
    depth = max((len(f) for _, f in reversed_experts), default=0)
    for i in range(depth):
        for expert, findings in reversed_experts:
            if i < len(findings):
                ordered.append((expert, findings[i]))
    return {f"F{n}": item for n, item in enumerate(ordered, start=1)}


def parse_peer(text, shown):
    """Parse one peer file. Returns (marks {F: mark}, top [F...], ignored [line...]); shown = numbers in its input."""
    marks, top, ignored = {}, [], []
    for line in text.strip().splitlines():
        if m := MARK_LINE.match(line):
            number = f"F{m.group(1)}"
            if number not in shown or number in marks:
                ignored.append(line)
            else:
                marks[number] = m.group(2)
        elif TOP_LINE.match(line):
            for number in line.removeprefix("TOP: ").split(", "):
                if number in shown:
                    top.append(number)
                else:
                    ignored.append(f"TOP {number}")
    return marks, top, ignored


def tally(peer_results):
    """Apply peer-review.md's tally rules. peer_results = [(marks, top), ...]. Returns {F: (holds, over, wrong, points, status)}."""
    rows = {}
    numbers = {n for marks, top in peer_results for n in list(marks) + top}
    for number in numbers:
        found = [marks[number] for marks, _ in peer_results if number in marks]
        holds, over, wrong = found.count("HOLDS"), found.count("OVERSTATED"), found.count("WRONG")
        points = sum(TOP_POINTS[top.index(number)] for _, top in peer_results if number in top)
        in_lane = holds + over + wrong
        if in_lane == 0:
            status = "unchecked"
        elif holds * 2 > in_lane:
            status = "upheld"
        else:
            status = "contested"
        rows[number] = (holds, over, wrong, points, status)
    return rows


class PeerFileTests(unittest.TestCase):
    def setUp(self):
        self.text = PEER_FILE.read_text(encoding="utf-8")

    def test_documented_call_counts(self):
        for n, expected in ((2, 5), (3, 7), (4, 9)):
            self.assertEqual(calls(n), expected)
            self.assertIn(f"{n} → {expected}", self.text)
        self.assertIn("2N + 1", self.text)

    def test_format_examples_match_patterns(self):
        lines = [line for block in format_blocks(self.text) for line in block]
        self.assertTrue(lines)
        seen = set()
        for line in lines:
            matched = [p for p in FORMAT_LINES if p.match(line)]
            self.assertTrue(matched, f"example line matches no format: {line!r}")
            seen.update(matched)
        self.assertEqual(seen, set(FORMAT_LINES), "every format has an example")

    def test_tallied_patterns_are_documented(self):
        for pattern in TALLIED_LINES:
            self.assertIn(f"`{pattern.pattern}`", self.text)

    def test_one_expert_error_is_stated(self):
        self.assertIn("peer review needs two or more experts; add an expert flag or drop --peer", self.text)

    def test_empty_peer_input_costs_no_call(self):
        stage2 = self.text.split("### 4. Stage 2", 1)[1].split("> You are", 1)[0]
        self.assertIn("gets no peer check and no call", stage2)
        self.assertIn("No findings to check", stage2)

    def test_labels_are_withheld_from_peers(self):
        self.assertIn("never given to a peer", self.text)
        stage2 = self.text.split("### 4. Stage 2", 1)[1].split("### 5.", 1)[0]
        self.assertNotIn("labels.md", stage2)

    def test_tally_examples_match_rules(self):
        # 3 peers HOLDS / HOLDS / WRONG → upheld; HOLDS / OVERSTATED → contested; all OUT OF LANE → unchecked.
        self.assertIn("HOLDS / HOLDS / WRONG → upheld", self.text)
        self.assertEqual(tally([({"F1": m}, []) for m in ("HOLDS", "HOLDS", "WRONG")])["F1"][4], "upheld")
        self.assertIn("HOLDS / OVERSTATED → contested", self.text)
        self.assertEqual(tally([({"F1": m}, []) for m in ("HOLDS", "OVERSTATED")])["F1"][4], "contested")
        self.assertIn("OUT OF LANE / OUT OF LANE → unchecked", self.text)
        self.assertEqual(tally([({"F1": "OUT OF LANE"}, [])] * 2)["F1"][4], "unchecked")


class AnonymizeTests(unittest.TestCase):
    def test_round_robin_from_last_expert(self):
        labels = anonymize([("security", ["s1", "s2"]), ("standards", ["t1"]), ("infra", ["i1", "i2", "i3"])])
        self.assertEqual(
            [labels[f"F{n}"] for n in range(1, 7)],
            [("infra", "i1"), ("standards", "t1"), ("security", "s1"),
             ("infra", "i2"), ("security", "s2"), ("infra", "i3")],
        )

    def test_expert_with_no_findings(self):
        labels = anonymize([("finance", []), ("legal", ["l1"])])
        self.assertEqual(labels, {"F1": ("legal", "l1")})


class TallyTests(unittest.TestCase):
    def test_points_and_out_of_lane(self):
        shown = {"F1", "F2", "F3"}
        a = parse_peer("F1: HOLDS — r\nF2: OUT OF LANE — r\nF3: WRONG — r\nTOP: F1, F3, F2", shown)
        b = parse_peer("F1: OVERSTATED — should be Low: r\nF2: OUT OF LANE — r\nF3: WRONG — r\nTOP: F3, F1", shown)
        rows = tally([a[:2], b[:2]])
        self.assertEqual(rows["F1"], (1, 1, 0, 5, "contested"))
        self.assertEqual(rows["F2"], (0, 0, 0, 1, "unchecked"))
        self.assertEqual(rows["F3"], (0, 0, 2, 5, "contested"))

    def test_marks_on_unshown_or_repeated_numbers_are_ignored(self):
        marks, top, ignored = parse_peer("F1: HOLDS — r\nF1: WRONG — r\nF9: WRONG — own finding\nTOP: F1, F9", {"F1", "F2"})
        self.assertEqual(marks, {"F1": "HOLDS"})
        self.assertEqual(top, ["F1"])
        self.assertEqual(len(ignored), 3)

    def test_malformed_lines_are_not_marks(self):
        marks, top, _ = parse_peer("F1: HOLDS - plain hyphen\nF2: MAYBE — r\nTOP: F1 F2", {"F1", "F2"})
        self.assertEqual((marks, top), ({}, []))


class AreaSkillTests(unittest.TestCase):
    def test_area_skills_wire_peer_mode(self):
        for area in AREAS:
            text = (ROOT / "skills" / area / "SKILL.md").read_text(encoding="utf-8")
            for needle in ("--peer", "../../references/peer-review.md", "**Peer-contested:**", "Peer Review"):
                self.assertIn(needle, text, f"{area}: {needle}")

    def test_each_area_has_four_experts(self):
        for area in AREAS:
            text = (ROOT / "skills" / area / "SKILL.md").read_text(encoding="utf-8")
            experts = re.findall(r"^\| `--\w+` \|", text, flags=re.MULTILINE)
            self.assertEqual(len(experts), MAX_EXPERTS, area)

    def test_shared_context_names_the_mode_flag(self):
        text = (ROOT / "references" / "shared-context.md").read_text(encoding="utf-8")
        self.assertIn("`--peer` is the one mode flag", text)
        self.assertIn("peer review needs two or more experts; add an expert flag or drop --peer", text)
        self.assertIn("peer-review.md", text)


class PluginTests(unittest.TestCase):
    def test_plugin_json_mentions_peer(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertIn("--peer", manifest["description"])
        self.assertIn("peer-review", manifest["keywords"])

    def test_readme_and_changelog_cover_peer(self):
        self.assertIn("## Peer review (`--peer`)", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("(TODO #5)", (ROOT / "meta" / "CHANGELOG.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
