"""script/tools/export_agent_bundle.py: scores and gaps reach the bundle as canon wrote them.

Until 2026-11-17 the exporter read the score with a regex that missed
`weighted_total:` (236 of 255 entries exported a null score) and read only
single-line frontmatter values (187 gaps exported as the bare YAML indicator
`>` or `>-`). These checks would have caught both. The committed bundles must
also equal what the exporter produces from canon now, so a stale bundle fails.

Run: python3 -B tests/script/tools/test_export_agent_bundle.py
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "script" / "tools"))
import export_agent_bundle as exporter  # noqa: E402

INDICATORS = {">", ">-", ">+", "|", "|-", "|+"}
BUNDLES = [ROOT / "script" / "exports" / "agent_bundle.json",
           ROOT / "home" / "data" / "agent_bundle.json"]
REGENERATE = ("python3 script/tools/export_agent_bundle.py, then python3 home/bake.py")
# A score of record, found without the exporter's parser: a weighted_total or
# weighted_v2 line with a number, anywhere in the frontmatter.
SCORE_LINE = re.compile(r"^\s*weighted_(?:total|v2):\s*-?\d", re.M)
MISSING = object()


def frontmatter_text(path: Path) -> str:
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    return m.group(1) if m else ""


def canon_drift(committed: list[dict], fresh: list[dict]) -> dict[str, list[str]]:
    """How a committed bundle's canon list differs from the exporter's: what differs -> words."""
    old = {e.get("word"): e for e in committed}
    new = {e["word"]: e for e in fresh}
    out: dict[str, list[str]] = {}
    for w in old.keys() - new.keys():
        out.setdefault("entry only in the committed bundle", []).append(w)
    for w in new.keys() - old.keys():
        out.setdefault("entry missing from the committed bundle", []).append(w)
    for w, e in new.items():
        for k in set(old.get(w, e)) | set(e):
            if old.get(w, e).get(k, MISSING) != e.get(k, MISSING):
                out.setdefault(f"field {k}", []).append(w)
    if not out and committed != fresh:
        out["entry order"] = []
    return out


class ReaderTest(unittest.TestCase):
    def test_block_scalars_and_the_score_of_record(self):
        # The genealogy is ordered as canon orders it (canon/doxalgia.md): the
        # score of record first, then the prior_assessment it superseded.
        fm = exporter.parse_frontmatter(
            "---\n"
            "word: sample\n"
            "gap: >\n"
            "  folded across\n"
            "  two lines\n"
            "pronunciation: >-\n"
            "  /ˈsæm.pəl/\n"
            "note: |\n"
            "  kept\n"
            "  as written\n"
            "genealogy:\n"
            "  scores:\n"
            "    gap_validity: 8\n"
            "  weighted_total: 7.75\n"
            "  prior_assessment:\n"
            "    date: 2026-04-17\n"
            "    weighted_total: 6.10\n"
            "    verdict: refine\n"
            "  later: {date: 2026-04-17, weighted_total: 6.75}\n"
            "v2_audit:\n"
            "  date: 2026-04-24\n"
            "  weighted_v2: 5.25\n"
            "---\n")
        self.assertEqual(exporter.text_field(fm, "gap"), "folded across two lines")
        self.assertEqual(exporter.text_field(fm, "pronunciation"), "/ˈsæm.pəl/")
        self.assertEqual(fm["note"], "kept\nas written\n")
        self.assertEqual(exporter.final_score(fm), 7.75)
        self.assertEqual(exporter.v2_audit_score(fm), 5.25)

    def test_a_plain_value_that_starts_below_its_key(self):
        # PyYAML reads both of these as the text; the reader used to return {} and so "".
        fm = exporter.parse_frontmatter("---\ngap:\n  the text\n  and more\nword: x\n---\n")
        self.assertEqual(exporter.text_field(fm, "gap"), "the text and more")
        self.assertEqual(fm["word"], "x")
        fm = exporter.parse_frontmatter("---\ngap:\n  # a note\n  the text\n---\n")
        self.assertEqual(exporter.text_field(fm, "gap"), "the text")

    def test_the_first_written_score_field_is_the_score(self):
        def score(genealogy_value):
            return exporter.final_score(exporter.parse_frontmatter(
                f"---\ngenealogy:\n  weighted_total: {genealogy_value}\nweighted_total: 6.0\n---\n"))
        # Read the way pipeline/derive_indices.py reads it: the first number in the value.
        self.assertEqual(score("~7.8"), 7.8)
        # Written but holding no number: null, never the lower-priority 6.0.
        self.assertIsNone(score("pending"))
        # Not written at all: the next field is the score.
        self.assertEqual(score("~"), 6.0)

    def test_superseded_and_audit_figures_in_canon(self):
        # Each of these carries genealogy.weighted_total, a block-form
        # prior_assessment.weighted_total after it, and a v2_audit.weighted_v2.
        by_word = {e["word"]: e for e in exporter.collect_canon()[0]}
        for word, score, prior, audit in [("doxalgia", 7.55, 6.9, 6.0),
                                          ("doxapothos", 7.65, 7.25, 6.2),
                                          ("orthophanes", 7.55, 7.4, 5.75)]:
            with self.subTest(word=word):
                fm = exporter.parse_frontmatter((ROOT / by_word[word]["path"]).read_text())
                self.assertEqual(float(fm["genealogy"]["prior_assessment"]["weighted_total"]), prior)
                self.assertEqual(by_word[word]["score"], score)
                self.assertEqual(by_word[word]["score_v2_audit"], audit)


class CanonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canon, _ = exporter.collect_canon()

    def check_entries(self, entries, where):
        for e in entries:
            with self.subTest(where=where, word=e["word"]):
                for field in ("word", "tier", "gap", "pronunciation", "entered", "definition"):
                    self.assertNotIn(e[field].strip(), INDICATORS, f"{field} is a bare YAML indicator")
                if SCORE_LINE.search(frontmatter_text(ROOT / e["path"])):
                    self.assertIsNotNone(e["score"], f"{e['path']} records a score; the bundle says null")

    def test_exporter_output(self):
        self.assertTrue(self.canon)
        self.check_entries(self.canon, "export_agent_bundle.collect_canon()")

    def test_committed_bundles(self):
        # Equal to collect_canon(), so the checks above hold for them too.
        # source_commit and the rest of the bundle are not compared.
        for path in BUNDLES:
            rel = path.relative_to(ROOT)
            with self.subTest(bundle=str(rel)):
                drift = canon_drift(json.loads(path.read_text())["canon"], self.canon)
                if drift:
                    self.fail(f"{rel} is stale against canon; regenerate with {REGENERATE}.\n" + "\n".join(
                        f"  {what} ({len(words)}): {', '.join(sorted(words)[:8])}"
                        f"{', …' if len(words) > 8 else ''}" for what, words in sorted(drift.items())))


if __name__ == "__main__":
    unittest.main()
