"""Checks the council:arena rules that can break when someone edits the skill files.

Run from the repo root: python -m unittest discover -s tests
"""

import re
import unittest
from itertools import combinations
from pathlib import Path

ARENA_DIR = Path(__file__).resolve().parent.parent / "skills" / "arena"
MAX_FIELD = 16
MIN_FIELD = 2
CALLS_PER_MATCH = 5  # 2 attacks + 2 defenses + 1 judgment


def read_card_lists():
    """Return {"Lenses": [...], "Shapes": [...], "Biases": [...]} parsed from cards.md."""
    text = (ARENA_DIR / "cards.md").read_text(encoding="utf-8")
    lists = {}
    for section in ("Lenses", "Shapes", "Biases"):
        body = text.split(f"## {section}", 1)[1].split("\n## ", 1)[0]
        rows = re.findall(r"^\| (\d+) \| ([^|]+) \|", body, flags=re.MULTILINE)
        assert [int(n) for n, _ in rows] == list(range(len(rows))), f"{section} rows must be numbered 0..n-1"
        lists[section] = [name.strip() for _, name in rows]
    return lists


def deal(n, lists):
    """Apply cards.md's dealing rule: competitor i gets part i mod list-size from each list."""
    sizes = [len(lists[s]) for s in ("Lenses", "Shapes", "Biases")]
    return [tuple(i % size for size in sizes) for i in range(n)]


def run_bracket(n, lenses):
    """Simulate SKILL.md's pairing rules; the lower id always wins. Returns (rounds, matches, byes)."""
    alive = list(range(n))
    had_bye = set()
    rounds = matches = 0
    byes = []
    while len(alive) > 1:
        rounds += 1
        pool = sorted(alive)
        advancing = []
        if len(pool) % 2:
            waiting = [c for c in pool if c not in had_bye]
            bye = max(waiting) if waiting else max(pool)
            pool.remove(bye)
            had_bye.add(bye)
            byes.append(bye)
            advancing.append(bye)
        pairs = [[pool[k], pool[k + 1]] for k in range(0, len(pool), 2)]
        for k, pair in enumerate(pairs):
            if lenses[pair[0]] == lenses[pair[1]] and len(pairs) > 1:
                other = pairs[k + 1] if k + 1 < len(pairs) else pairs[k - 1]
                pair[1], other[1] = other[1], pair[1]
        for a, b in pairs:
            matches += 1
            advancing.append(min(a, b))
        alive = advancing
    return rounds, matches, byes


class CardTests(unittest.TestCase):
    def setUp(self):
        self.lists = read_card_lists()

    def test_list_sizes_match_header(self):
        self.assertEqual([len(self.lists[s]) for s in ("Lenses", "Shapes", "Biases")], [10, 8, 6])

    def test_dealing_rule_holds_for_every_field_size(self):
        for n in range(MIN_FIELD, MAX_FIELD + 1):
            cards = deal(n, self.lists)
            self.assertEqual(len(set(cards)), n, f"repeated card at N={n}")
            for a, b in combinations(cards, 2):
                shared = sum(x == y for x, y in zip(a, b))
                self.assertLessEqual(shared, 1, f"N={n}: {a} and {b} share {shared} parts")
            for part in range(3):
                counts = [sum(c[part] == v for c in cards) for v in {c[part] for c in cards}]
                self.assertLessEqual(max(counts) - min(counts), 1, f"N={n}: uneven spread in part {part}")


class BracketTests(unittest.TestCase):
    def setUp(self):
        self.lenses = [card[0] for card in deal(MAX_FIELD, read_card_lists())]

    def test_rounds_matches_and_byes(self):
        expected_rounds = {2: 1, 4: 2, 5: 3, 8: 3, 16: 4}
        for n in range(MIN_FIELD, MAX_FIELD + 1):
            rounds, matches, byes = run_bracket(n, self.lenses)
            self.assertEqual(matches, n - 1, f"N={n}")
            self.assertEqual(len(byes), len(set(byes)), f"N={n}: a competitor got two byes")
            if n in expected_rounds:
                self.assertEqual(rounds, expected_rounds[n], f"N={n}")

    def test_documented_call_counts(self):
        skill = (ARENA_DIR / "SKILL.md").read_text(encoding="utf-8")
        for n, calls in ((4, 19), (8, 43), (16, 91)):
            self.assertEqual(n + CALLS_PER_MATCH * (n - 1), calls)
            self.assertIn(f"{n} → {calls}", skill)


class RubricTests(unittest.TestCase):
    def test_weights_total_100(self):
        text = (ARENA_DIR / "rubric.md").read_text(encoding="utf-8")
        weights = re.findall(r"^\| \*\*\w+\*\* \| (\d+) \|", text, flags=re.MULTILINE)
        self.assertEqual(len(weights), 5)
        self.assertEqual(sum(map(int, weights)), 100)


if __name__ == "__main__":
    unittest.main()
