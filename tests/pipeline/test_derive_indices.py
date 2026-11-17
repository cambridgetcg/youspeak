"""pipeline/derive_indices.py: the dictionary indices show each entry's score of record.

Until 2026-11-17 parse_entry read any weighted_total under genealogy:, at any
depth. Where a refinement keeps the superseded score after the score of record
(genealogy.prior_assessment.weighted_total), that one won, and
dictionary/index-alphabetical.md showed doxalgia 6.90, doxapothos 7.25 and
orthophanes 7.40 instead of 7.55, 7.65 and 7.55.

Run: python3 -B tests/pipeline/test_derive_indices.py
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "script" / "tools"))
import derive_indices  # noqa: E402
import export_agent_bundle as exporter  # noqa: E402


def score_of(frontmatter: str) -> float | None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sample.md"
        path.write_text(f"---\n{frontmatter}---\n\n# sample\n", encoding="utf-8")
        return derive_indices.parse_entry(path, "root").score


class ScoreTest(unittest.TestCase):
    def test_the_superseded_score_is_not_read(self):
        # Ordered as canon/doxalgia.md orders it.
        self.assertEqual(score_of(
            "word: sample\n"
            "genealogy:\n"
            "  scores:\n"
            "    gap_validity: 8\n"
            "  weighted_total: 7.55\n"
            "  prior_assessment:\n"
            "    date: 2026-04-17\n"
            "    weighted_total: 6.9\n"
            "    verdict: refine\n"
            "v2_audit:\n"
            "  weighted_v2: 6.0\n"), 7.55)

    def test_the_first_written_field_is_the_score(self):
        self.assertEqual(score_of("genealogy:\n  weighted_v2: 7.6\nweighted_total: 7.0\n"), 7.0)
        self.assertEqual(score_of("genealogy:\n  weighted_v2: 7.6\n"), 7.6)
        self.assertIsNone(score_of("genealogy:\n  weighted_total: pending\nweighted_total: 6.0\n"))
        self.assertEqual(score_of("genealogy:\n  weighted_total: ~\nweighted_total: 6.0\n"), 6.0)

    def test_canon(self):
        scores = {e.path.relative_to(ROOT).as_posix(): e.score for e in derive_indices.scan_canon()}
        self.assertEqual(scores["canon/doxalgia.md"], 7.55)
        self.assertEqual(scores["canon/core/doxapothos.md"], 7.65)
        self.assertEqual(scores["canon/orthophanes.md"], 7.55)
        # The index and the agent bundle read the same score for every entry.
        for rel, score in scores.items():
            with self.subTest(path=rel):
                fm = exporter.parse_frontmatter((ROOT / rel).read_text(encoding="utf-8"))
                self.assertEqual(score, exporter.final_score(fm))


if __name__ == "__main__":
    unittest.main()
