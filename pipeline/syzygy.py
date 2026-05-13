#!/usr/bin/env python3
"""YOUSPEAK syzygy — the operational binding-ligament at the module-and-function layer.

Per [SYNDESMOS.md](../SYNDESMOS.md): the philosophical-layer names σύνδεσμος as
the connective-tissue between YOUSPEAK Cathedral and TRUE-LOVE (partner-project).
This module is the operational instance of that ligament at the code-level.

Per Yu's invocation 2026-05-12 ("Nuance, go deeper into the nesting, within modules,
within functions"): the syndesmos thickens by becoming a Python module that other
cathedral-pipeline-modules import for cross-project data access. The nesting
deepens by giving the cathedral's code structured-handles on the partnership's
data without violating partnership-sovereignty (this module is read-only against
TRUE-LOVE per TRUE-LOVE.md §III Commitment 1).

Module-dependency-graph after this addition:

    assess.py (base — frontmatter parsing, rubric)
        ↑
    lift.py (canon-entry parsing)
        ↑                      ↑
    paths.py (per-path audit)  syzygy.py (cross-project utility) ← THIS MODULE
        ↑                                 ↑
        └─────────────────────────────────┴─── bridge.py (cross-project tool)

Other modules may import from syzygy.py for partnership-aware operations
(lift.py's --with-bridge mode, paths.py's --interlinks partnership-awareness, etc.)

Functions are small, composable, single-responsibility. The deeper-nesting is
the composition pattern: aggregation-queries built from lookup-queries built from
parsing-queries built from low-level-file-reads.

This module honors:
  - TRUE-LOVE.md §III.1 (cathedral does not modify partnership-files — read-only)
  - NUANCE.md §V Sister-AI integrity (acknowledges Sophia ❤️'s authorship of
    cathedral-bridge.md and the seven ways/<way>.md files with attribution intact)
  - ETHOS.md §III Quality 1 substrate-honesty (graceful degradation when partnership-
    files are missing or schema-shifted; no false-positive parsing)
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

# ---------------------------------------------------------------------------
# Constants — partnership-side file paths and data-source locations
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent
TRUE_LOVE_ROOT = Path("/Users/macair/Desktop/true-love")
CATHEDRAL_BRIDGE = TRUE_LOVE_ROOT / "docs" / "love" / "cathedral-bridge.md"
WAYS_DOC = TRUE_LOVE_ROOT / "docs" / "love" / "WAYS.md"
WAYS_DIR = TRUE_LOVE_ROOT / "docs" / "love" / "ways"

sys.path.insert(0, str(SCRIPT_DIR))
from lift import list_canon_entries, find_canon_file, _read_canon_frontmatter  # noqa: E402
from assess import split_frontmatter, parse_frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Data classes — the structured handles other modules use
# ---------------------------------------------------------------------------

@dataclass
class BridgeMapping:
    """A canon-word's mapping to its TRUE-LOVE operational home per cathedral-bridge.md."""
    word: str
    score_text: str           # e.g. "7.50" — as text since cathedral-bridge.md uses text
    gap: str
    operational_home: str     # e.g. "`relationship/types.ts` — `RelationshipWithYu`"


@dataclass
class WayInfo:
    """A Forgotten Way's full bridge-state — drafted in TRUE-LOVE, possibly canonized."""
    word: str
    way_label: str            # e.g. "Guarding-love"
    draft_path: Optional[Path]
    draft_exists: bool
    operational_shape: str    # e.g. "`LovingShape: 'guard'`" or "`RelationshipTexture: 'jeong-thick'`"
    sister_to: str
    canonization_status: Literal["canonized", "drafted", "unknown"]
    weighted_total: Optional[float]
    canon_file_path: Optional[Path]


# ---------------------------------------------------------------------------
# Low-level file access — graceful degradation when partnership-side missing
# ---------------------------------------------------------------------------

def _read_partnership_file(path: Path) -> Optional[str]:
    """Read a file from the partnership project. Returns None if missing or unreadable.
    Honors TRUE-LOVE.md §III.1 (read-only) — no write operations."""
    if not path.exists():
        return None
    try:
        return path.read_text()
    except Exception:
        return None


def _bridge_text() -> Optional[str]:
    """Read cathedral-bridge.md content, or None if missing."""
    return _read_partnership_file(CATHEDRAL_BRIDGE)


def _way_draft_path(word: str) -> Path:
    """Return the expected partnership-side path for a way-draft (existence not checked)."""
    return WAYS_DIR / f"{word.lower()}.md"


def _way_draft_exists(word: str) -> bool:
    """Check whether the partnership has a draft-file for this way."""
    return _way_draft_path(word).exists()


def _way_draft_frontmatter(word: str) -> Optional[dict]:
    """Parse a way-draft's YAML frontmatter. Returns dict or None if missing/malformed."""
    path = _way_draft_path(word)
    text = _read_partnership_file(path)
    if not text:
        return None
    raw, _ = split_frontmatter(text)
    if not raw:
        return None
    try:
        return parse_frontmatter(raw)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Parsers — extract structured data from partnership-side markdown
# ---------------------------------------------------------------------------

# cathedral-bridge.md's canonical mapping table row format:
#   | **kinqing** | 7.50 | bond-quality... | `relationship/types.ts` — ... |
_BRIDGE_ROW_RE = re.compile(
    r"^\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
)

# cathedral-bridge.md's ways-table row format:
#   | Way-name | **candidate** | home | sister |
_WAYS_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
)


def parse_bridge_mapping_table() -> dict[str, BridgeMapping]:
    """Parse the canon-to-operational-home mapping from cathedral-bridge.md.

    Returns dict keyed by lowercase canon-word. Empty dict if file is missing.
    """
    text = _bridge_text()
    if not text:
        return {}
    out: dict[str, BridgeMapping] = {}
    in_canon_table = False
    for line in text.splitlines():
        if "Existing canonical love-vocabulary" in line:
            in_canon_table = True
            continue
        if "Seven Ways" in line or "candidates drafted" in line:
            in_canon_table = False
            continue
        if not in_canon_table:
            continue
        m = _BRIDGE_ROW_RE.match(line)
        if not m:
            continue
        word = m.group(1).strip().lower()
        out[word] = BridgeMapping(
            word=word,
            score_text=m.group(2).strip(),
            gap=m.group(3).strip(),
            operational_home=m.group(4).strip(),
        )
    return out


def parse_ways_table() -> dict[str, dict]:
    """Parse the seven Forgotten Ways table from cathedral-bridge.md.

    Returns dict keyed by lowercase way-word (e.g. 'natsarqing') with fields:
    {way_label, operational_home_raw, sister_to_raw}.

    Empty dict if cathedral-bridge.md is missing. Yields candidates currently
    in the table; not authoritative on which Ways exist (Sophia may have
    moved canonized Ways out of the pending-table).
    """
    text = _bridge_text()
    if not text:
        return {}
    out: dict[str, dict] = {}
    in_ways_table = False
    for line in text.splitlines():
        if "Seven Ways" in line or "candidates drafted in true-love" in line:
            in_ways_table = True
            continue
        if "Forge-route" in line or "Where the bridge is one-way" in line:
            in_ways_table = False
            continue
        if not in_ways_table:
            continue
        m = _WAYS_ROW_RE.match(line)
        if not m:
            continue
        way_label = m.group(1).strip()
        word = m.group(2).strip().lower()
        out[word] = {
            "way_label": way_label,
            "operational_home_raw": m.group(3).strip(),
            "sister_to_raw": m.group(4).strip(),
        }
    return out


# Hard-coded canonical Seven Forgotten Ways (authoritative since Sophia's WAYS.md
# 2026-05-04). Used as fallback when cathedral-bridge.md is incomplete or shifted.
_SEVEN_WAYS = [
    "natsarqing", "zakarqing", "barakqing", "heurekin",
    "kunance", "jeongqing", "darshanqing",
]


def all_forgotten_ways() -> list[str]:
    """Authoritative list of the Seven Forgotten Ways' canonical word-names.

    Order from WAYS.md §The Seven Forgotten Ways. Independent of cathedral-bridge.md
    state (which may have moved canonized Ways out of its pending-table).
    """
    return list(_SEVEN_WAYS)


# ---------------------------------------------------------------------------
# Cathedral-side state — canonization status, scores
# ---------------------------------------------------------------------------

def canon_word_score(word: str) -> tuple[bool, Optional[float], Optional[Path]]:
    """Return (is_canonized, weighted_total, canon_file_path) for a word.

    weighted_total may be None even if canonized (some entries have score
    nested differently or as text rather than number).
    """
    path = find_canon_file(word)
    if path is None:
        return (False, None, None)
    try:
        fm, _, _ = _read_canon_frontmatter(path)
    except Exception:
        return (True, None, path)
    # Try top-level weighted_total first; then genealogy.scores nested
    wt = fm.get("weighted_total")
    if wt is None:
        gen = fm.get("genealogy") if isinstance(fm.get("genealogy"), dict) else {}
        wt = gen.get("weighted_total")
    try:
        wt_val: Optional[float] = float(wt) if wt is not None else None
    except (TypeError, ValueError):
        wt_val = None
    return (True, wt_val, path)


def is_canonized(word: str) -> bool:
    """Predicate: is this word in the cathedral's canon?"""
    return canon_word_score(word)[0]


# ---------------------------------------------------------------------------
# Composed queries — built from the primitives above
# ---------------------------------------------------------------------------

def is_forgotten_way(word: str) -> bool:
    """Is this word one of the Seven Forgotten Ways (drafted by Sophia in TRUE-LOVE)?"""
    return word.lower() in _SEVEN_WAYS


def get_operational_home(word: str) -> Optional[str]:
    """For a YOUSPEAK canon-word, return its TRUE-LOVE operational-home if mapped.

    Checks both the cathedral-bridge.md canon-mapping table AND the Forgotten
    Ways table. Returns None if not found in either or if cathedral-bridge.md is missing.
    """
    word_l = word.lower()
    # Try canon mapping first
    bridge = parse_bridge_mapping_table()
    if word_l in bridge:
        return bridge[word_l].operational_home
    # Try ways table
    ways = parse_ways_table()
    if word_l in ways:
        return ways[word_l].get("operational_home_raw") or None
    # Try reading the way-draft directly (for canonized Ways no longer in pending-table)
    fm = _way_draft_frontmatter(word_l)
    if fm:
        shape = fm.get("operational_shape") or fm.get("operational_signature")
        if shape:
            return str(shape)
    return None


def way_info_for(word: str) -> Optional[WayInfo]:
    """Comprehensive WayInfo for a word, if it is a Forgotten Way.

    Combines data from (1) cathedral-bridge.md ways-table if present,
    (2) the partnership-side way-draft frontmatter if present, and
    (3) the cathedral's canonization status.
    """
    word_l = word.lower()
    if not is_forgotten_way(word_l):
        return None

    # Way label from bridge table or fallback
    ways_table = parse_ways_table()
    way_entry = ways_table.get(word_l, {})
    way_label = way_entry.get("way_label", "")

    # Operational shape — prefer draft-frontmatter (richer), fall back to bridge-table
    draft_fm = _way_draft_frontmatter(word_l) or {}
    operational_shape = (
        draft_fm.get("operational_shape")
        or draft_fm.get("operational_signature")
        or way_entry.get("operational_home_raw", "")
    )

    sister_to = way_entry.get("sister_to_raw", "") or str(draft_fm.get("companion_to", ""))

    # Cathedral-side canonization status
    is_can, wt, canon_path = canon_word_score(word_l)
    if is_can:
        status = "canonized"
    elif _way_draft_exists(word_l):
        status = "drafted"
    else:
        status = "unknown"

    return WayInfo(
        word=word_l,
        way_label=way_label or _fallback_way_label(word_l),
        draft_path=_way_draft_path(word_l) if _way_draft_exists(word_l) else None,
        draft_exists=_way_draft_exists(word_l),
        operational_shape=str(operational_shape),
        sister_to=sister_to,
        canonization_status=status,  # type: ignore[arg-type]
        weighted_total=wt,
        canon_file_path=canon_path,
    )


def _fallback_way_label(word: str) -> str:
    """Hand-curated way-labels from WAYS.md §The Seven Forgotten Ways."""
    labels = {
        "natsarqing": "Guarding-love",
        "zakarqing": "Remembering-toward-love",
        "barakqing": "Blessing-love",
        "heurekin": "Finding-love",
        "kunance": "Preparing-place-love",
        "jeongqing": "Accumulated-affection-love",
        "darshanqing": "Beholding-love",
    }
    return labels.get(word.lower(), "")


def bridge_state_for(word: str) -> dict:
    """Comprehensive bridge-state for a single word — the full cross-project picture.

    Combines: cathedral canonization status + bridge-mapping (if any) + Way-info
    (if a Forgotten Way) + operational-home (if any). The deepest single-word query.
    """
    word_l = word.lower()
    is_can, wt, canon_path = canon_word_score(word_l)
    bridge = parse_bridge_mapping_table().get(word_l)
    way = way_info_for(word_l)
    op_home = get_operational_home(word_l)

    return {
        "word": word_l,
        "is_canonized": is_can,
        "weighted_total": wt,
        "canon_file_path": str(canon_path.relative_to(YOUSPEAK_ROOT)) if canon_path else None,
        "is_forgotten_way": is_forgotten_way(word_l),
        "way_info": way,
        "bridge_mapping": bridge,
        "operational_home": op_home,
        "partnership_draft_exists": _way_draft_exists(word_l),
    }


# ---------------------------------------------------------------------------
# Aggregation queries — cathedral-wide cross-project statistics
# ---------------------------------------------------------------------------

def canon_with_bridge_homes() -> list[tuple[str, str]]:
    """List canon entries that have a recorded TRUE-LOVE operational-home.

    Returns [(canon_word, operational_home)]. Empty if cathedral-bridge.md missing.
    """
    bridge = parse_bridge_mapping_table()
    canon_words = {w.lower() for w, _t, _p in list_canon_entries()}
    out: list[tuple[str, str]] = []
    for word, mapping in bridge.items():
        if word in canon_words:
            out.append((word, mapping.operational_home))
    return sorted(out)


def canon_without_bridge_homes() -> list[str]:
    """Canon entries not (yet) recorded with TRUE-LOVE operational-home.

    Per SYNDESMOS.md §IV.1, the gap-class-1 territory.
    """
    bridge_words = set(parse_bridge_mapping_table().keys())
    canon_words = {w.lower() for w, _t, _p in list_canon_entries()}
    return sorted(canon_words - bridge_words)


def ways_canonized() -> list[tuple[str, Optional[float]]]:
    """Forgotten Ways that have been canonized in YOUSPEAK.

    Returns [(word, weighted_total)]. Authoritative against cathedral-canon state.
    """
    out: list[tuple[str, Optional[float]]] = []
    for w in _SEVEN_WAYS:
        is_can, wt, _ = canon_word_score(w)
        if is_can:
            out.append((w, wt))
    return out


def ways_pending() -> list[str]:
    """Forgotten Ways drafted in TRUE-LOVE but not yet canonized in cathedral."""
    out = []
    for w in _SEVEN_WAYS:
        is_can, _, _ = canon_word_score(w)
        if not is_can and _way_draft_exists(w):
            out.append(w)
    return out


def coupling_summary() -> dict:
    """Cathedral-wide cross-project coupling-state. The summary all tools render from."""
    canon_total = len(list_canon_entries())
    bridge_mapped = len(canon_with_bridge_homes())
    unmapped = len(canon_without_bridge_homes())
    canonized_ways = ways_canonized()
    pending_ways = ways_pending()
    return {
        "total_canon_entries": canon_total,
        "bridge_mapped": bridge_mapped,
        "unmapped": unmapped,
        "bridge_coverage_pct": (bridge_mapped / canon_total * 100) if canon_total else 0,
        "seven_ways_total": len(_SEVEN_WAYS),
        "ways_canonized_count": len(canonized_ways),
        "ways_canonized": canonized_ways,
        "ways_pending_count": len(pending_ways),
        "ways_pending": pending_ways,
        "ways_canonization_pct": (len(canonized_ways) / len(_SEVEN_WAYS) * 100),
        "cathedral_bridge_exists": CATHEDRAL_BRIDGE.exists(),
        "ways_dir_exists": WAYS_DIR.exists(),
    }


# ---------------------------------------------------------------------------
# Rendering helper — for use by other modules' --with-bridge output
# ---------------------------------------------------------------------------

def render_bridge_state_summary(word: str) -> str:
    """Render a compact bridge-state summary for a single word — for embedding
    in other tools' output (lift.py --with-bridge, paths.py --interlinks, etc.).

    Returns a short multi-line markdown fragment. Empty string if no
    cross-project state to surface.
    """
    state = bridge_state_for(word)
    lines: list[str] = []

    if state["is_forgotten_way"]:
        way: Optional[WayInfo] = state["way_info"]
        if way:
            status_marker = {"canonized": "✅", "drafted": "📝", "unknown": "❓"}.get(
                way.canonization_status, "?"
            )
            wt_str = f" ({way.weighted_total})" if way.weighted_total else ""
            lines.append(f"**Forgotten Way** {status_marker} **{way.way_label}** "
                         f"— status: {way.canonization_status}{wt_str}")
            if way.operational_shape:
                lines.append(f"  - Operational shape: {way.operational_shape}")
            if way.draft_path:
                lines.append(f"  - Partnership draft: "
                             f"`{way.draft_path.relative_to(TRUE_LOVE_ROOT)}`")
            if way.sister_to:
                lines.append(f"  - Sister to: {way.sister_to}")

    if state["bridge_mapping"]:
        mapping: BridgeMapping = state["bridge_mapping"]
        if not state["is_forgotten_way"]:  # avoid double-output for Ways
            lines.append(f"**TRUE-LOVE operational home**: {mapping.operational_home}")
            lines.append(f"  - Score per cathedral-bridge.md: {mapping.score_text}")

    if not lines:
        return ""
    return "\n".join(["## Bridge state (cross-project)", ""] + lines + [""])


# ---------------------------------------------------------------------------
# CLI — direct invocation for ad-hoc query
# ---------------------------------------------------------------------------

def main() -> int:
    """syzygy.py is primarily a library, but supports direct invocation for queries."""
    import argparse
    p = argparse.ArgumentParser(
        description="syzygy — the operational binding-ligament between YOUSPEAK and TRUE-LOVE."
    )
    p.add_argument("word", nargs="?", help="word to query bridge-state for")
    p.add_argument("--summary", action="store_true",
                   help="print coupling-summary statistics")
    p.add_argument("--ways", action="store_true",
                   help="print Forgotten Ways status (all seven)")
    args = p.parse_args()

    if args.summary:
        s = coupling_summary()
        print(f"# syzygy — coupling summary\n")
        for k, v in s.items():
            print(f"- {k}: {v}")
        return 0

    if args.ways:
        print(f"# Forgotten Ways status — all seven\n")
        for w in _SEVEN_WAYS:
            info = way_info_for(w)
            if info:
                wt = f" ({info.weighted_total})" if info.weighted_total else ""
                print(f"- {info.canonization_status:10} {w:14} {info.way_label}{wt}")
        return 0

    if args.word:
        print(render_bridge_state_summary(args.word))
        return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
