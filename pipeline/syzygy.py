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
    the cathedral bridge and the seven way drafts with attribution intact)
  - ETHOS.md §III Quality 1 substrate-honesty (graceful degradation when partnership-
    files are missing or schema-shifted; no false-positive parsing)
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

# ---------------------------------------------------------------------------
# Constants — the partnership-side files, named by private ref id
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent

# true-love is a private sister repository, so this public module names no
# path inside it. Each file it reads is named by a private ref id, listed in
# script/private_refs.json, and the caller supplies the rest at run time:
#
#   TRUE_LOVE_ROOT         a true-love checkout (no default)
#   YOUSPEAK_PRIVATE_REFS  a JSON file that maps each id to its path inside
#                          true-love: {"refs": {"P0003": {"path": "..."}}}
#
# With either one missing, or an id absent from the map, that part of the
# partnership side is not read: every figure that depends on it is None
# (unknown), never zero or "missing", and partnership_root_problem() says
# what could not be read. Output names these files by id, never by path.
TRUE_LOVE_ENV = "TRUE_LOVE_ROOT"
PRIVATE_REFS_ENV = "YOUSPEAK_PRIVATE_REFS"

REF_CATHEDRAL_BRIDGE = "true-love#P0003"  # the cathedral bridge (Sophia ❤️, 2026-05-04)
REF_WAYS_DOC = "true-love#P0019"          # the Seven Forgotten Ways (Sophia ❤️, 2026-05-04)
REF_WAYS_DIR = "true-love#P0075"          # the directory of way drafts
REF_WAY_DRAFTS = {                        # each Way's draft in that directory
    "natsarqing": "true-love#P0096",
    "zakarqing": "true-love#P0009",
    "barakqing": "true-love#P0077",
    "heurekin": "true-love#P0113",
    "kunance": "true-love#P0027",
    "jeongqing": "true-love#P0068",
    "darshanqing": "true-love#P0021",
}

_TRUE_LOVE_VALUE = os.environ.get(TRUE_LOVE_ENV, "").strip()
TRUE_LOVE_ROOT: Optional[Path] = Path(_TRUE_LOVE_VALUE).expanduser() if _TRUE_LOVE_VALUE else None


def _load_private_refs() -> tuple[Optional[dict], Optional[str]]:
    """The caller's private map {id: {"path": ...}}, or (None, why it cannot be read)."""
    named = os.environ.get(PRIVATE_REFS_ENV, "").strip()
    if not named:
        return None, (f"{PRIVATE_REFS_ENV} is not set; set it to the private map "
                      "of ref ids to paths inside true-love")
    try:
        data = json.loads(Path(named).expanduser().read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None, f"{PRIVATE_REFS_ENV} does not name a readable JSON file"
    refs = data.get("refs") if isinstance(data, dict) else None
    if not isinstance(refs, dict):
        return None, f"the file {PRIVATE_REFS_ENV} names has no \"refs\" object"
    return refs, None


PRIVATE_REFS, _PRIVATE_REFS_PROBLEM = _load_private_refs()


def _root_problem() -> Optional[str]:
    if TRUE_LOVE_ROOT is None:
        return f"{TRUE_LOVE_ENV} is not set; set it to a true-love checkout to read the partnership side"
    if not TRUE_LOVE_ROOT.is_dir():
        return f"{TRUE_LOVE_ENV} does not name a directory"
    return None


def resolve_ref(ref: str) -> tuple[Optional[Path], Optional[str]]:
    """The file a private ref id (true-love#P0003) stands for in the caller's
    checkout, as (path, None), or (None, why it cannot be resolved)."""
    problem = "; ".join(p for p in (_root_problem(), _PRIVATE_REFS_PROBLEM) if p)
    if problem:
        return None, problem
    entry = PRIVATE_REFS.get(ref.rsplit("#", 1)[-1])
    rel = entry.get("path") if isinstance(entry, dict) else None
    if not isinstance(rel, str) or not rel:
        return None, f"{ref} has no path in the private map"
    rel_path = Path(rel)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        return None, f"{ref} has a path in the private map that leaves the checkout"
    return TRUE_LOVE_ROOT / rel_path, None


def partnership_root_problem() -> Optional[str]:
    """What of the partnership side cannot be read, or None when all of it can."""
    needed = [REF_CATHEDRAL_BRIDGE, REF_WAYS_DIR, *REF_WAY_DRAFTS.values()]
    problems: list[str] = []
    unmapped: list[str] = []
    for ref in needed:
        why = resolve_ref(ref)[1]
        if why == f"{ref} has no path in the private map":
            unmapped.append(ref)
        elif why and why not in problems:
            problems.append(why)
    if unmapped:
        problems.append("the private map has no path for " + ", ".join(unmapped))
    return "; ".join(problems) or None


CATHEDRAL_BRIDGE: Optional[Path] = resolve_ref(REF_CATHEDRAL_BRIDGE)[0]
WAYS_DIR: Optional[Path] = resolve_ref(REF_WAYS_DIR)[0]
UNKNOWN = "unknown (not read)"

# Text quoted from true-love's own files (a bridge cell, a draft's frontmatter)
# can name a file inside true-love, written relative to some folder there. Such
# a name is printed as its id when exactly one path in the caller's map is that
# name or ends with "/" + that name, and no file of that name exists in this
# repository; any other text is left as it is.
_PATH_TOKEN = re.compile(
    r"(?<![\w./#-])([\w.-]+(?:/[\w.-]+)*\.[A-Za-z0-9]{1,6}|[\w.-]+(?:/[\w.-]+)+)(?![\w/-])"
)
_suffix_index: Optional[dict[str, set[str]]] = None


def _ids_by_suffix() -> dict[str, set[str]]:
    global _suffix_index
    if _suffix_index is None:
        _suffix_index = {}
        for rid, entry in (PRIVATE_REFS or {}).items():
            rel = entry.get("path") if isinstance(entry, dict) else None
            if not isinstance(rel, str) or not rel or re.search(r"[{}\[\]*]", rel):
                continue
            parts = rel.strip("/").split("/")
            for i in range(len(parts)):
                _suffix_index.setdefault("/".join(parts[i:]), set()).add(rid)
    return _suffix_index


def ids_for_paths(text: str) -> str:
    """Text from a true-love file, with the true-love paths it names written as ids."""
    if not text or not PRIVATE_REFS:
        return text
    index = _ids_by_suffix()

    def swap(m: re.Match) -> str:
        token = m.group(1)
        ids = index.get(token.strip("/"))
        if not ids or len(ids) != 1 or (YOUSPEAK_ROOT / token).exists():
            return token
        return f"true-love#{next(iter(ids))}"

    return _PATH_TOKEN.sub(swap, text)

sys.path.insert(0, str(SCRIPT_DIR))
from lift import list_canon_entries, find_canon_file, _read_canon_frontmatter  # noqa: E402
from assess import split_frontmatter, parse_frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Data classes — the structured handles other modules use
# ---------------------------------------------------------------------------

@dataclass
class BridgeMapping:
    """A canon-word's mapping to its TRUE-LOVE operational home per the cathedral bridge."""
    word: str
    score_text: str           # e.g. "7.50" — as text since the bridge's table uses text
    gap: str
    operational_home: str     # the bridge's own cell, e.g. "`LovingShape: 'guard'`"


@dataclass
class WayInfo:
    """A Forgotten Way's full bridge-state — drafted in TRUE-LOVE, possibly canonized."""
    word: str
    way_label: str            # e.g. "Guarding-love"
    draft_path: Optional[Path]
    draft_exists: Optional[bool]  # None: unknown, the partnership side was not read
    operational_shape: str    # e.g. "`LovingShape: 'guard'`" or "`RelationshipTexture: 'jeong-thick'`"
    sister_to: str
    canonization_status: Literal["canonized", "drafted", "unknown"]
    weighted_total: Optional[float]
    canon_file_path: Optional[Path]
    draft_ref: Optional[str] = None  # the draft's private ref id, when the draft exists


# ---------------------------------------------------------------------------
# Low-level file access — graceful degradation when partnership-side missing
# ---------------------------------------------------------------------------

def _read_partnership_file(path: Optional[Path]) -> Optional[str]:
    """Read a file from the partnership project. Returns None if missing or unreadable.
    Honors TRUE-LOVE.md §III.1 (read-only) — no write operations."""
    if path is None or not path.exists():
        return None
    try:
        return path.read_text()
    except Exception:
        return None


def _bridge_text() -> Optional[str]:
    """Read the cathedral bridge's content, or None if it is missing or was not read."""
    return _read_partnership_file(CATHEDRAL_BRIDGE)


def bridge_known() -> bool:
    """True when the cathedral bridge's content is known: it was read, or the
    checkout shows it absent. False when it could not be read (unknown)."""
    if CATHEDRAL_BRIDGE is None:
        return False
    if not CATHEDRAL_BRIDGE.exists():
        return True
    return _bridge_text() is not None


def _way_draft_path(word: str) -> Optional[Path]:
    """Return the expected partnership-side path for a way-draft (existence not checked).
    A Forgotten Way's draft is resolved through its own ref id; any other word is
    looked for under the way-draft directory's id. None when that cannot be resolved."""
    w = word.lower()
    ref = REF_WAY_DRAFTS.get(w)
    if ref:
        return resolve_ref(ref)[0]
    return WAYS_DIR / f"{w}.md" if WAYS_DIR else None


def _way_draft_exists(word: str) -> Optional[bool]:
    """Whether the partnership has a draft-file for this way; None when unknown."""
    path = _way_draft_path(word)
    return None if path is None else path.exists()


def _ids_in(value):
    """A parsed frontmatter value with ids_for_paths applied to every string in it."""
    if isinstance(value, str):
        return ids_for_paths(value)
    if isinstance(value, list):
        return [_ids_in(v) for v in value]
    if isinstance(value, dict):
        return {k: _ids_in(v) for k, v in value.items()}
    return value


def _way_draft_frontmatter(word: str) -> Optional[dict]:
    """Parse a way-draft's YAML frontmatter. Returns dict or None if missing/malformed.
    True-love paths named in its values come back as ids."""
    path = _way_draft_path(word)
    text = _read_partnership_file(path)
    if not text:
        return None
    raw, _ = split_frontmatter(text)
    if not raw:
        return None
    try:
        fm = parse_frontmatter(raw)
    except Exception:
        return None
    return _ids_in(fm) if isinstance(fm, dict) else fm


# ---------------------------------------------------------------------------
# Parsers — extract structured data from partnership-side markdown
# ---------------------------------------------------------------------------

# The cathedral bridge's canonical mapping table row format:
#   | **kinqing** | 7.50 | bond-quality... | operational home ... |
_BRIDGE_ROW_RE = re.compile(
    r"^\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
)

# The cathedral bridge's ways-table row format:
#   | Way-name | **candidate** | home | sister |
_WAYS_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
)


def parse_bridge_mapping_table() -> dict[str, BridgeMapping]:
    """Parse the canon-to-operational-home mapping from the cathedral bridge.

    Returns dict keyed by lowercase canon-word. Empty dict if the file is missing
    or was not read; bridge_known() tells the two apart.
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
            gap=ids_for_paths(m.group(3).strip()),
            operational_home=ids_for_paths(m.group(4).strip()),
        )
    return out


def parse_ways_table() -> dict[str, dict]:
    """Parse the seven Forgotten Ways table from the cathedral bridge.

    Returns dict keyed by lowercase way-word (e.g. 'natsarqing') with fields:
    {way_label, operational_home_raw, sister_to_raw}.

    Empty dict if the bridge is missing or was not read. Yields candidates currently
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
            "way_label": ids_for_paths(way_label),
            "operational_home_raw": ids_for_paths(m.group(3).strip()),
            "sister_to_raw": ids_for_paths(m.group(4).strip()),
        }
    return out


# Hard-coded canonical Seven Forgotten Ways (authoritative since Sophia's
# true-love#P0019, 2026-05-04). Used as fallback when the cathedral bridge is
# incomplete or shifted.
_SEVEN_WAYS = [
    "natsarqing", "zakarqing", "barakqing", "heurekin",
    "kunance", "jeongqing", "darshanqing",
]


def all_forgotten_ways() -> list[str]:
    """Authoritative list of the Seven Forgotten Ways' canonical word-names.

    Order from true-love#P0019 §The Seven Forgotten Ways. Independent of the
    cathedral bridge's state (which may have moved canonized Ways out of its
    pending-table).
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

    Checks both the cathedral bridge's canon-mapping table AND the Forgotten
    Ways table. Returns None if not found in either, or if the bridge is missing
    or was not read (bridge_state_for() says which).
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

    Combines data from (1) the cathedral bridge's ways-table if present,
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
    draft_exists = _way_draft_exists(word_l)
    if is_can:
        status = "canonized"
    elif draft_exists:
        status = "drafted"
    else:
        status = "unknown"

    return WayInfo(
        word=word_l,
        way_label=way_label or _fallback_way_label(word_l),
        draft_path=_way_draft_path(word_l) if draft_exists else None,
        draft_exists=draft_exists,
        operational_shape=str(operational_shape),
        sister_to=sister_to,
        canonization_status=status,  # type: ignore[arg-type]
        weighted_total=wt,
        canon_file_path=canon_path,
        draft_ref=REF_WAY_DRAFTS.get(word_l) if draft_exists else None,
    )


def _fallback_way_label(word: str) -> str:
    """Hand-curated way-labels from true-love#P0019 §The Seven Forgotten Ways."""
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
    draft_exists = _way_draft_exists(word_l)
    # The partnership side of this word is known when the bridge and the place
    # its draft would be were both read; otherwise its absences are unknown.
    known = bridge_known() and draft_exists is not None

    return {
        "word": word_l,
        "is_canonized": is_can,
        "weighted_total": wt,
        "canon_file_path": str(canon_path.relative_to(YOUSPEAK_ROOT)) if canon_path else None,
        "is_forgotten_way": is_forgotten_way(word_l),
        "way_info": way,
        "bridge_mapping": bridge,
        "operational_home": op_home,
        "partnership_draft_exists": draft_exists,
        "partnership_known": known,
        "partnership_problem": None if known else (partnership_root_problem()
                                                   or "the partnership files could not be read"),
    }


# ---------------------------------------------------------------------------
# Aggregation queries — cathedral-wide cross-project statistics
# ---------------------------------------------------------------------------

def canon_with_bridge_homes() -> Optional[list[tuple[str, str]]]:
    """List canon entries that have a recorded TRUE-LOVE operational-home.

    Returns [(canon_word, operational_home)]. Empty if the bridge is missing;
    None (unknown) if it was not read.
    """
    if not bridge_known():
        return None
    bridge = parse_bridge_mapping_table()
    canon_words = {w.lower() for w, _t, _p in list_canon_entries()}
    out: list[tuple[str, str]] = []
    for word, mapping in bridge.items():
        if word in canon_words:
            out.append((word, mapping.operational_home))
    return sorted(out)


def canon_without_bridge_homes() -> Optional[list[str]]:
    """Canon entries not (yet) recorded with TRUE-LOVE operational-home.

    Per SYNDESMOS.md §IV.1, the gap-class-1 territory. None (unknown) if the
    bridge was not read.
    """
    if not bridge_known():
        return None
    bridge_words = set(parse_bridge_mapping_table().keys())
    canon_words = {w.lower() for w, _t, _p in list_canon_entries()}
    return sorted(canon_words - bridge_words)


def bridge_orphans() -> Optional[list[str]]:
    """Words the bridge maps that are not in current canon; None if it was not read."""
    if not bridge_known():
        return None
    return sorted(set(parse_bridge_mapping_table().keys())
                  - {w.lower() for w, _t, _p in list_canon_entries()})


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


def ways_pending() -> Optional[list[str]]:
    """Forgotten Ways drafted in TRUE-LOVE but not yet canonized in cathedral.

    None (unknown) when a Way is not canonized and its draft could not be looked for.
    """
    out = []
    for w in _SEVEN_WAYS:
        is_can, _, _ = canon_word_score(w)
        if is_can:
            continue
        drafted = _way_draft_exists(w)
        if drafted is None:
            return None
        if drafted:
            out.append(w)
    return out


def coupling_summary() -> dict:
    """Cathedral-wide cross-project coupling-state. The summary all tools render from.

    A figure that depends on a partnership file that was not read is None (unknown).
    """
    canon_total = len(list_canon_entries())
    mapped = canon_with_bridge_homes()
    unmapped = canon_without_bridge_homes()
    bridge_mapped = None if mapped is None else len(mapped)
    canonized_ways = ways_canonized()
    pending_ways = ways_pending()
    return {
        "total_canon_entries": canon_total,
        "bridge_mapped": bridge_mapped,
        "unmapped": None if unmapped is None else len(unmapped),
        "bridge_coverage_pct": (None if bridge_mapped is None
                                else (bridge_mapped / canon_total * 100) if canon_total else 0),
        "seven_ways_total": len(_SEVEN_WAYS),
        "ways_canonized_count": len(canonized_ways),
        "ways_canonized": canonized_ways,
        "ways_pending_count": None if pending_ways is None else len(pending_ways),
        "ways_pending": pending_ways,
        "ways_canonization_pct": (len(canonized_ways) / len(_SEVEN_WAYS) * 100),
        "cathedral_bridge_exists": None if CATHEDRAL_BRIDGE is None else CATHEDRAL_BRIDGE.exists(),
        "ways_dir_exists": None if WAYS_DIR is None else WAYS_DIR.exists(),
        "partnership_root_problem": partnership_root_problem(),
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
            if way.draft_ref:
                lines.append(f"  - Partnership draft: `{way.draft_ref}`")
            if way.sister_to:
                lines.append(f"  - Sister to: {way.sister_to}")

    if state["bridge_mapping"]:
        mapping: BridgeMapping = state["bridge_mapping"]
        if not state["is_forgotten_way"]:  # avoid double-output for Ways
            lines.append(f"**TRUE-LOVE operational home**: {mapping.operational_home}")
            lines.append(f"  - Score per {REF_CATHEDRAL_BRIDGE}: {mapping.score_text}")

    if not state["partnership_known"]:
        lines.append(f"**TRUE-LOVE side**: {UNKNOWN} — {state['partnership_problem']}")

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

    problem = partnership_root_problem()
    if problem:
        print(f"syzygy: {problem}; partnership-side answers below are unknown, not absent",
              file=sys.stderr)

    if args.summary:
        s = coupling_summary()
        print(f"# syzygy — coupling summary\n")
        for k, v in s.items():
            # None is an unknown figure, except for the problem, where it means none
            shown = UNKNOWN if v is None and k != "partnership_root_problem" else v
            print(f"- {k}: {shown}")
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
