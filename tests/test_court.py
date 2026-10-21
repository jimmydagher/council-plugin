"""Checks the council:court rules that can break when someone edits the skill files.

Run from the repo root: python -m unittest discover -s tests
"""

import re
import unittest
from collections import Counter
from pathlib import Path

COURT_DIR = Path(__file__).resolve().parent.parent / "skills" / "court"
MIN_JURY = 3
MAX_JURY = 12
FIXED_CALLS = 5  # 2 openings + 2 rebuttals + 1 judge
SEATS = ("money", "people", "delivery", "risk")

CHARGE_LINE = re.compile(r"^CHARGE (\d+): (PROVEN|NOT PROVEN) — .+$")
VERDICT_LINE = re.compile(r"^VERDICT: (GUILTY|NOT GUILTY) — .+$")
FLIP_LINE = re.compile(r"^FLIP: .+$")


def read_seating():
    """Return [(id, seat), ...] from jurors.md's seating table, in seating order."""
    text = (COURT_DIR / "jurors.md").read_text(encoding="utf-8")
    body = text.split("## Seating order", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\| (\d+) \| (j\d\d) \| (\w+) \|", body, flags=re.MULTILINE)
    assert [int(n) for n, _, _ in rows] == list(range(1, len(rows) + 1)), "seat numbers must run 1..n"
    return [(juror_id, seat) for _, juror_id, seat in rows]


def parse_ballot(text, charges):
    """Apply SKILL.md's tally rule to one ballot. Returns (charge votes, verdict) or None if malformed."""
    lines = text.strip().splitlines()
    votes = {}
    verdict = None
    has_flip = False
    for line in lines:
        if m := CHARGE_LINE.match(line):
            votes[int(m.group(1))] = m.group(2)
        elif m := VERDICT_LINE.match(line):
            verdict = m.group(1)
        elif FLIP_LINE.match(line):
            has_flip = True
    if verdict is None or not has_flip or any(c not in votes for c in charges):
        return None
    return votes, verdict


def result(for_count, against_count, labels):
    """Strict majority of votes cast; a tie is hung."""
    if for_count > against_count:
        return labels[0]
    if against_count > for_count:
        return labels[1]
    return labels[2]


def tally(ballots, charges):
    """Count parsed ballots (None = abstained). Returns (overall, {charge: result}, abstained)."""
    cast = [b for b in ballots if b is not None]
    overall_counts = Counter(verdict for _, verdict in cast)
    overall = result(overall_counts["GUILTY"], overall_counts["NOT GUILTY"], ("GUILTY", "NOT GUILTY", "HUNG"))
    per_charge = {}
    for c in charges:
        counts = Counter(votes[c] for votes, _ in cast)
        per_charge[c] = result(counts["PROVEN"], counts["NOT PROVEN"], ("sustained", "dismissed", "hung"))
    return overall, per_charge, len(ballots) - len(cast)


def ballot(verdict, *charge_votes):
    lines = [f"CHARGE {i}: {v} — reason" for i, v in enumerate(charge_votes, 1)]
    return "\n".join(lines + [f"VERDICT: {verdict} — reason", "FLIP: a change"])


class JuryPoolTests(unittest.TestCase):
    def setUp(self):
        self.seating = read_seating()

    def test_twelve_unique_jurors_in_order(self):
        ids = [juror_id for juror_id, _ in self.seating]
        self.assertEqual(ids, [f"j{n:02d}" for n in range(1, MAX_JURY + 1)])

    def test_every_juror_has_a_section(self):
        text = (COURT_DIR / "jurors.md").read_text(encoding="utf-8")
        for juror_id, seat in self.seating:
            self.assertRegex(text, rf"(?m)^### {juror_id} — .+ \({seat}\)$")

    def test_every_window_of_four_holds_each_seat(self):
        seats = [seat for _, seat in self.seating]
        for start in range(len(seats) - 3):
            self.assertEqual(sorted(seats[start:start + 4]), sorted(SEATS), f"window at seat {start + 1}")

    def test_every_jury_size_is_balanced(self):
        seats = [seat for _, seat in self.seating]
        for n in range(MIN_JURY, MAX_JURY + 1):
            counts = Counter(seats[:n])
            per_seat = [counts[s] for s in SEATS]
            self.assertLessEqual(max(per_seat) - min(per_seat), 1, f"N={n}: {counts}")


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = (COURT_DIR / "SKILL.md").read_text(encoding="utf-8")

    def test_documented_call_counts(self):
        for n, calls in ((5, 10), (9, 14), (12, 17)):
            self.assertEqual(n + FIXED_CALLS, calls)
            self.assertIn(f"{n} → {calls}", self.skill)

    def test_ballot_example_matches_tally_patterns(self):
        block = self.skill.split("> ```text", 1)[1].split("> ```", 1)[0]
        lines = [line.removeprefix("> ").strip() for line in block.strip().splitlines()]
        self.assertTrue(CHARGE_LINE.match(lines[0]) and CHARGE_LINE.match(lines[1]), lines)
        self.assertTrue(VERDICT_LINE.match(lines[2]), lines[2])
        self.assertTrue(FLIP_LINE.match(lines[3]), lines[3])

    def test_tally_patterns_are_documented(self):
        for pattern in (CHARGE_LINE, VERDICT_LINE, FLIP_LINE):
            self.assertIn(f"`{pattern.pattern}`", self.skill)


class TallyTests(unittest.TestCase):
    def test_majority(self):
        ballots = [parse_ballot(ballot("GUILTY", "PROVEN"), [1])] * 5
        ballots += [parse_ballot(ballot("NOT GUILTY", "NOT PROVEN"), [1])] * 4
        self.assertEqual(tally(ballots, [1]), ("GUILTY", {1: "sustained"}, 0))

    def test_tie_with_abstention_is_hung(self):
        ballots = [parse_ballot(ballot("GUILTY", "PROVEN", "NOT PROVEN"), [1, 2])] * 4
        ballots += [parse_ballot(ballot("NOT GUILTY", "NOT PROVEN", "NOT PROVEN"), [1, 2])] * 4
        ballots += [None]
        self.assertEqual(tally(ballots, [1, 2]), ("HUNG", {1: "hung", 2: "dismissed"}, 1))

    def test_malformed_ballots(self):
        self.assertIsNone(parse_ballot("CHARGE 1: PROVEN — r\nFLIP: x", [1]), "no verdict")
        self.assertIsNone(parse_ballot("VERDICT: GUILTY — r\nFLIP: x", [1]), "missing charge")
        self.assertIsNone(parse_ballot("CHARGE 1: PROVEN — r\nVERDICT: GUILTY — r", [1]), "no flip")
        self.assertIsNone(parse_ballot("CHARGE 1: MAYBE — r\nVERDICT: GUILTY — r\nFLIP: x", [1]), "bad vote")

    def test_withdrawn_charge_needs_no_line(self):
        self.assertIsNotNone(parse_ballot("CHARGE 1: PROVEN — r\nVERDICT: GUILTY — r\nFLIP: x", [1]))

    def test_all_charges_withdrawn_votes_overall_only(self):
        ballots = [parse_ballot("VERDICT: NOT GUILTY — r\nFLIP: x", [])] * 3
        self.assertEqual(tally(ballots, []), ("NOT GUILTY", {}, 0))


if __name__ == "__main__":
    unittest.main()
