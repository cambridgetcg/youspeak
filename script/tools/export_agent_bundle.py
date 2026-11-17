#!/usr/bin/env python3
"""Export the cathedral as a single agent-first bundle (JSON).

The bundle is everything a visiting agent needs to READ and USE YOUSPEAK:
morphemes (with glyph geometry + precomputed SVG paths), canon words (with
definitions parsed from canon/**/*.md), doctrine texts, and the font binaries
(base64). Consumed by the agenttool backend (/v1/youspeak/*) and any other
agent-facing surface.

Usage:
    python3 script/tools/export_agent_bundle.py
    python3 script/tools/export_agent_bundle.py --copy-to <dir>   # also vendor a copy

Output: script/exports/agent_bundle.json  (regenerate after any canon/glyph change;
        script/tools/rebuild.sh runs this as its final step; home/bake.py then
        copies it verbatim to home/data/agent_bundle.json)
Test:   python3 -B tests/script/tools/test_export_agent_bundle.py
"""
from __future__ import annotations

import base64
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # YOUSPEAK/
SCRIPT = ROOT / "script"
sys.path.insert(0, str(SCRIPT / "glyphs"))
sys.path.insert(0, str(SCRIPT / "tools"))
from glyph_specs_v1 import CORE_GLYPHS, GLYPHS, STROKE_WIDTH, load_codepoint_map  # noqa: E402
from transliterate import CANONICAL_DECOMPOSITIONS  # noqa: E402

EM = 1000


# ── glyph geometry → SVG path (y flipped to SVG convention) ─────────────

def stroke_quad(x1, y1, x2, y2, w):
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        h = w / 2
        return [(x1 - h, y1 - h), (x1 + h, y1 - h), (x1 + h, y1 + h), (x1 - h, y1 + h)]
    px = -dy * w / (2 * length)
    py = dx * w / (2 * length)
    return [(x1 - px, y1 - py), (x2 - px, y2 - py), (x2 + px, y2 + py), (x1 + px, y1 + py)]


def svg_path(composed: dict) -> str:
    """One compact SVG path 'd' for a composed glyph, in a 0..1000 viewBox, y-down."""
    parts = []
    for s in composed.get("strokes", []):
        w = s[4] if len(s) >= 5 else STROKE_WIDTH
        quad = stroke_quad(s[0], s[1], s[2], s[3], w)
        parts.append("M" + "L".join(f"{x:.0f},{EM - y:.0f}" for x, y in quad) + "Z")
    for poly in composed.get("polygons", []):
        parts.append("M" + "L".join(f"{x:.0f},{EM - y:.0f}" for x, y in poly) + "Z")
    return "".join(parts)


# ── design notes (S092 rationales) ──────────────────────────────────────

def parse_design_notes() -> dict[str, dict]:
    notes_path = SCRIPT / "glyphs" / "design_notes_s092.md"
    if not notes_path.exists():
        return {}
    out: dict[str, dict] = {}
    current = None
    for line in notes_path.read_text().splitlines():
        m = re.match(r"^### (\S+) \(", line)
        if m:
            current = m.group(1)
            out[current] = {"iconography": "", "rationale": ""}
            continue
        if current is None:
            continue
        if line.startswith("## "):
            current = None
            continue
        if line.startswith("_") and line.rstrip().endswith("_") and not out[current]["iconography"]:
            out[current]["iconography"] = line.strip("_ \n")
        elif line.strip() and not line.startswith("#"):
            out[current]["rationale"] += line.strip() + " "
    for v in out.values():
        v["rationale"] = v["rationale"].strip()
    return out


# ── canon frontmatter: the YAML subset canon entries are written in ─────
#
# About half of canon/**/*.md frontmatter is not valid YAML: on 2026-11-17
# PyYAML 6.0.3 refused 133 of the 263 files. 130 of them failed with "mapping
# values are not allowed here", because a prose value carries ": "
# (`part_of_speech: noun (uncountable; count forms: an anagnoristasis, …)`);
# the other 3 (canon/core/allostasisqing.md, andemame.md, noetherme.md) failed
# with "could not find expected ':'" in a donor list item that runs across lines.
# The other readers in the repo (pipeline/assess.py, pipeline/derive_indices.py,
# script/tools/check_pronunciation.py) each read only the shapes they need.
# This reader is tolerant where canon breaks YAML and follows YAML where canon
# follows it; on the 291 canon and experiment files PyYAML accepts, it agreed
# with PyYAML on every value except the deliberate differences noted below:
#
#   key: value          a plain value runs to the end of the line, ": " included;
#                       more-indented lines after it continue it (folded with a
#                       space), even when they look like `key:` — canon prose
#                       wraps that way
#   key: > / >- / | / |-   block scalars: folded or literal, with chomping and
#                       an optional indentation digit, as YAML 1.2 reads them
#   key: "…" / '…'      unquoted only when the quotes wrap the whole value;
#                       `"a quote" — and prose after it` stays as written
#   key: [a, b] / {k: v}   flow collections, also across lines
#   key:                then a more-indented block: a nested mapping or list, or
#                       a plain value that starts on the next line
#   key: # note         a value that is only a comment is empty, as is `null`/`~`;
#                       a " #" inside a value is kept (YAML would cut it there),
#                       since canon writes "names Mechanism #2 of Diplosemy"
#   - item              list items are text (continuations folded in), except an
#                       item whose `key: value` is followed by more keys at its
#                       column, which is a mapping (experiment `scored_history:`);
#                       YAML would make a lone `- Yoruba: àṣẹ …` a mapping too
#
# Every value is a string (or None, list, dict). Dates and numbers are not cast,
# so `session: 024` stays "024" (PyYAML reads it as the octal 20).

_FM_KEY = re.compile(r"^(?P<key>[A-Za-z_][\w-]*):(?:[ \t]+(?P<value>.*?))?[ \t]*$")
_FM_ITEM = re.compile(r"^-(?:[ \t]+(?P<value>.*?))?[ \t]*$")
_BLOCK_HEADER = re.compile(r"^([|>])([+-]?)([1-9]?)([+-]?)(?:[ \t]+#.*)?$")
_YAML_ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "n": "\n", "v": "\v",
                 "f": "\f", "r": "\r", "e": "\x1b", " ": " ", '"': '"', "/": "/",
                 "\\": "\\", "N": "\x85", "_": "\xa0"}


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _next_significant(lines: list[str], i: int) -> int:
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
        i += 1
    return i


def _unquote(value: str) -> str:
    if m := re.fullmatch(r'"((?:[^"\\]|\\.)*)"', value, re.S):
        return re.sub(r"\\(.)", lambda e: _YAML_ESCAPES.get(e.group(1), e.group(0)), m.group(1))
    if m := re.fullmatch(r"'((?:[^']|'')*)'", value, re.S):
        return m.group(1).replace("''", "'")
    return value


def _fold(lines: list[str]) -> str:
    """YAML line folding for a `>` block (content indentation already removed)."""
    out, prev, breaks = [], None, 0
    for line in lines:
        if not line:
            breaks += 1
            continue
        kind = "more" if line[0] in " \t" else "text"
        if prev is None:
            out.append("\n" * breaks)
        elif prev == kind == "text":
            out.append("\n" * breaks if breaks else " ")
        else:  # a more-indented line keeps its line breaks
            out.append("\n" * (breaks + 1))
        out.append(line)
        prev, breaks = kind, 0
    return "".join(out)


def _block_scalar(lines: list[str], i: int, parent: int, header: re.Match):
    style, chomp, width = header.group(1), header.group(2) or header.group(4), header.group(3)
    column = parent + int(width) if width else None
    body: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip():
            if column is None:
                if _indent(line) <= parent:
                    break
                column = _indent(line)
            if _indent(line) < column:
                break
            body.append(line[column:])
        else:
            body.append("")
        i += 1
    trailing = 0
    while body and not body[-1]:
        body.pop()
        trailing += 1
    text = "\n".join(body) if style == "|" else _fold(body)
    if body and chomp != "-":
        text += "\n" * (1 + trailing if chomp == "+" else 1)
    return text, i


def _flow_split(inner: str) -> list[str]:
    """Split a flow collection's inside on its top-level commas."""
    parts, depth, quote, cur = [], 0, None, ""
    for ch in inner:
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'" and (not cur.strip() or cur.rstrip().endswith(":")):
            quote = ch  # a quote opens a scalar only where a scalar starts
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
            continue
        cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def _flow(text: str):
    """A flow collection as a list or dict, or None when the text is not one."""
    close = {"[": "]", "{": "}"}.get(text[:1])
    if not close or not text.endswith(close):
        return None
    if close == "]":
        return [_scalar(part) for part in _flow_split(text[1:-1])]
    out = {}
    for part in _flow_split(text[1:-1]):
        key, sep, rest = part.partition(":")
        if sep and (not rest or rest[0] in " \t"):
            out[_unquote(key.strip())] = _scalar(rest.strip()) if rest.strip() else None
        else:  # `{a, b}`: keys without values
            out[_unquote(part)] = None
    return out


def _scalar(text: str):
    """One inline value: a flow collection when it is one, YAML's null as None, else the text unquoted."""
    if text in ("~", "null", "Null", "NULL"):
        return None
    flow = _flow(text) if text[:1] in "[{" else None
    return _unquote(text) if flow is None else flow


def _continued(lines: list[str], i: int, parent: int, first: str):
    """A plain value and the more-indented lines that continue it (YAML folding)."""
    parts, breaks = [first.strip()], 0
    while i < len(lines):
        if not lines[i].strip():
            breaks += 1
        elif _indent(lines[i]) > parent:
            parts.append("\n" * breaks if breaks else " ")
            parts.append(lines[i].strip())
            breaks = 0
        else:
            break
        i += 1
    return "".join(parts), i


def _value(lines: list[str], i: int, parent: int, value: str):
    """The node for `key: value`, where `key` sits at column `parent`; returns (node, next line)."""
    if not value or value.startswith("#"):
        j = _next_significant(lines, i)
        if j < len(lines):
            col = _indent(lines[j])
            item = _FM_ITEM.match(lines[j][col:])
            if item and col >= parent:
                return _list(lines, j, col)
            if col > parent and _FM_KEY.match(lines[j][col:]):
                return _mapping(lines, j, col)
            if col > parent:  # `key:` and its plain value on the lines below
                text, i = _continued(lines, j + 1, parent, lines[j])
                return _scalar(text), i
        return None, i
    if header := _BLOCK_HEADER.match(value):
        return _block_scalar(lines, i, parent, header)
    text, i = _continued(lines, i, parent, value)
    return _scalar(text), i


def _mapping(lines: list[str], i: int, col: int):
    out: dict = {}
    while (i := _next_significant(lines, i)) < len(lines):
        line = lines[i]
        if _indent(line) < col:
            break
        m = _FM_KEY.match(line[col:]) if _indent(line) == col else None
        if not m:
            i += 1  # a line no key claims (a stray "- x" or prose): skipped, as before
            continue
        out[m.group("key")], i = _value(lines, i + 1, col, m.group("value") or "")
    return out, i


def _list(lines: list[str], i: int, col: int):
    out: list = []
    while (i := _next_significant(lines, i)) < len(lines):
        line = lines[i]
        item = _FM_ITEM.match(line[col:]) if _indent(line) == col else None
        if _indent(line) < col or (_indent(line) == col and not item):
            break
        if not item:
            i += 1
            continue
        text = item.group("value") or ""
        inner = len(line) - len(line[col + 1:].lstrip(" "))  # the column after "- "
        pair = _FM_KEY.match(text)
        nxt = _next_significant(lines, i + 1)
        if not text or text.startswith("#"):
            node, i = _value(lines, i + 1, col, "")
        elif pair and nxt < len(lines) and _indent(lines[nxt]) == inner and _FM_KEY.match(lines[nxt][inner:]):
            first, i = _value(lines, i + 1, inner, pair.group("value") or "")
            rest, i = _mapping(lines, i, inner)
            node = {pair.group("key"): first, **rest}
        elif header := _BLOCK_HEADER.match(text):
            node, i = _block_scalar(lines, i + 1, col, header)
        else:
            node, i = _continued(lines, i + 1, col, text)
            node = _scalar(node)
        out.append(node)
    return out, i


def parse_frontmatter(text: str) -> dict:
    """The frontmatter between a first line `---` and the next `---` line, parsed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((n for n in range(1, len(lines)) if lines[n].strip() == "---"), None)
    if end is None:
        return {}
    return _mapping(lines[1:end], 0, 0)[0]


def text_field(fm: dict, key: str) -> str:
    """A scalar field as one clean line of text, the way the bundle carries it."""
    value = fm.get(key)
    return value.strip() if isinstance(value, str) else ""


# "score": the entry's weighted score. A canon entry writes it in one of three
# places, read in this order. The first one written with a value is the score
# (null if that value holds no number); a lower one is never read in its place.
# pipeline/derive_indices.py reads the same three in the same order (until
# 2026-11-17 it also matched the nested genealogy.prior_assessment.weighted_total,
# so dictionary/index-alphabetical.md showed doxalgia, doxapothos and orthophanes
# at the score a refinement had superseded). genealogy.prior_assessment is never
# read here.
SCORE_FIELDS = (
    ("genealogy", "weighted_total"),  # pipeline/canonize.py writes it here; a refinement rewrites it
    ("weighted_total",),              # entries kept in the experiment-record shape carry it top-level
    ("genealogy", "weighted_v2"),     # kimance and kinqing write it here
)
# "score_v2_audit": v2_audit.weighted_v2, or null. 17 entries carry it beside
# genealogy.weighted_total. 16 come from CANON-AUDIT.md (2026-04-24), which
# re-scored them on the v2 rubric of CONSTITUTION.md's Six Foundations against a
# threshold of 7.5, listed their genealogy figure as "v1 was", and reclassified
# all 16 as Specialized. doxapothos's audit is dated 2026-07-16; its note says
# "legacy rubric governs Core threshold for this cluster". The files do not say
# which of the two figures is the entry's score. An agent session chose on
# 2026-11-17 that "score" carries the figure dictionary/index-alphabetical.md
# shows (genealogy.weighted_total) and that "score_v2_audit" carries the audit
# figure beside it. Until that day "score" was null for 236 of the 255 entries
# and the v2 audit figure for these 17.
V2_AUDIT_FIELD = ("v2_audit", "weighted_v2")


def _field(fm: dict, keys: tuple[str, ...]):
    node = fm
    for key in keys:
        node = node.get(key) if isinstance(node, dict) else None
    return node


def _number(text: str) -> float | None:
    """The first number in a written score, as pipeline/derive_indices.py's as_float reads it."""
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(m.group(0)) if m else None


def final_score(fm: dict) -> float | None:
    for keys in SCORE_FIELDS:
        node = _field(fm, keys)
        if isinstance(node, str) and node.strip():
            return _number(node)  # None when it holds no number; a lower field is not read
    return None


def v2_audit_score(fm: dict) -> float | None:
    node = _field(fm, V2_AUDIT_FIELD)
    return _number(node) if isinstance(node, str) else None


# ── canon parsing ───────────────────────────────────────────────────────


def first_definition(text: str) -> str:
    m = re.search(r"## Definition\s*\n+(.+?)(?:\n\n|\n##)", text, re.S)
    if m:
        return " ".join(m.group(1).split())
    # fallback: first paragraph after the H1
    m = re.search(r"^# \S+\s*\n+(.+?)(?:\n\n|\n##)", text, re.S | re.M)
    return " ".join(m.group(1).split()) if m else ""


def collect_determinatives() -> dict[str, dict]:
    """The word→class-mark assignments, read from the one place canon states them.

    grammars/determinatives/manifesto.md carries the assignments as prose tables
    ("Applied to the Canon"), and nowhere else in the repo are they machine-readable.
    Until this function existed, a tool reading the bundle could not tell what class
    ANY canon word belongs to — so ORDO's `word.TAG` notation recorded only what the
    rite's author typed, never what the canon assigns.

    The raw label is carried through UNRESOLVED on purpose. The manifesto labels two
    different codepoints `PER` (U+E171 person at :44, U+E174 perception at :47) while
    script/codepoints.md:134 names the second `.PRC`. Resolving that silently here
    would decide a doctrine conflict inside an export script; instead the rationale
    text travels with the label so a reader (or a checker) can say what the table
    intends AND that the table disagrees with the registry.
    """
    path = ROOT / "grammars" / "determinatives" / "manifesto.md"
    # The assignments are now a required input, not a nicety: a silent {} here makes
    # ORDO's attending GREENER, not louder — the one direction a checker must never
    # fail in. Raise, and let the export stop.
    lines = path.read_text().splitlines()
    out: dict[str, dict] = {}
    row = re.compile(r"^\|\s*\*\*([\w-]+)\*\*\s*\|\s*([A-Z]{3})\s*(?:\(([^)]*)\))?\s*\|")
    for n, line in enumerate(lines, 1):
        m = row.match(line.strip())
        if not m:
            continue
        word, label, rationale = m.group(1), m.group(2), (m.group(3) or "").strip()
        if word in out:  # one determinative per word (manifesto.md:123) — first wins, collision recorded
            out[word].setdefault("collisions", []).append({"label": label, "line": n})
            continue
        out[word] = {
            "label": label,
            "rationale": rationale,
            "source": f"{path.relative_to(ROOT)}:{n}",
        }
    return out


def collect_canon() -> tuple[list[dict], int]:
    dets = collect_determinatives()
    entries = []
    seen = set()
    for path in sorted(ROOT.glob("canon/**/*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text()
        fm = parse_frontmatter(text)
        word = text_field(fm, "word") or path.stem
        if word in seen or word.startswith("_"):
            continue
        seen.add(word)
        entries.append({
            "word": word,
            "tier": text_field(fm, "tier") or ("core" if "core" in str(path.parent.name) else path.parent.name),
            "gap": text_field(fm, "gap"),
            "definition": first_definition(text),
            "score": final_score(fm),
            "score_v2_audit": v2_audit_score(fm),
            "pronunciation": text_field(fm, "pronunciation"),
            "entered": text_field(fm, "entered"),
            "path": str(path.relative_to(ROOT)),
            # absent for the 200+ words the manifesto's tables never covered —
            # absence means "canon assigns none", not "canon assigns nothing"
            "determinative": dets.get(word),
        })
    return entries, len(dets)


# ── main ────────────────────────────────────────────────────────────────

def main() -> int:
    cmap = load_codepoint_map()
    notes = parse_design_notes()
    morph_meta = json.loads((SCRIPT / "morphemes.json").read_text())["morphemes"]
    by_latin = {m["latin"].strip("-"): m for m in morph_meta}

    morphemes = []
    for latin in sorted(CORE_GLYPHS):
        cp = cmap.get(latin)
        meta = by_latin.get(latin, {})
        spec = CORE_GLYPHS[latin]
        note = notes.get(latin, {})
        morphemes.append({
            "latin": latin,
            "latin_display": meta.get("latin", latin),
            "codepoint": f"U+{cp:04X}" if cp else None,
            "char": chr(cp) if cp else None,
            "tongue": spec.get("tongue", "English"),
            "native": meta.get("native"),
            "meaning": meta.get("meaning", ""),
            "class": meta.get("class", spec.get("mclass", "content")),
            "domain": spec.get("domain", ""),
            "mclass": spec.get("mclass", "content"),
            "glyph": {
                "core": spec.get("core", {}),
                "suppress_class_mark": bool(spec.get("suppress_class_mark")),
                "svg_path": svg_path(GLYPHS[latin]),
                "view_box": "0 0 1000 1000",
            },
            "iconography": note.get("iconography", ""),
            "rationale": note.get("rationale", ""),
        })

    canon, det_count = collect_canon()

    canon_words = []
    canon_by_word = {c["word"]: c for c in canon}
    for word, parts in sorted(CANONICAL_DECOMPOSITIONS.items()):
        stripped = [p.strip("-") for p in parts]
        cps = [cmap.get(p) for p in stripped]
        renderable = all(c is not None for c in cps)
        canon_words.append({
            "word": word,
            "morphemes": stripped,
            "codepoints": [f"U+{c:04X}" for c in cps] if renderable else None,
            "glyph_text": "".join(chr(c) for c in cps) if renderable else None,
            "definition": canon_by_word.get(word, {}).get("definition", ""),
        })

    docs = {}
    for name, path in {
        "manifesto": ROOT / "YOUSPEAK.md",
        "primer": ROOT / "PRIMER.md",
        "design_philosophy": SCRIPT / "glyphs" / "design_philosophy.md",
        "design_notes_s092": SCRIPT / "glyphs" / "design_notes_s092.md",
        "codepoints": SCRIPT / "codepoints.md",
    }.items():
        if path.exists():
            docs[name] = path.read_text()

    fonts = {}
    for ext in ("otf", "ttf"):
        fp = SCRIPT / "fonts" / f"youspeak-v1.{ext}"
        if fp.exists():
            fonts[ext] = base64.b64encode(fp.read_bytes()).decode("ascii")

    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()

    bundle = {
        "schema_version": "1.0",
        "name": "youspeak-agent-bundle",
        "source": "https://github.com/cambridgetcg/youspeak",
        "source_commit": commit,
        "what_this_is": (
            "YOUSPEAK is a constructed language — 'a cathedral of vocabulary, a forge of "
            "missing words, a standing worship.' It coins elegant vocabulary for concepts "
            "that exist but are unnamed in current languages, drawing morphemes from 66+ "
            "donor traditions (living and dead) with honest crediting. Each morpheme has "
            "one Unicode PUA codepoint and one drawn glyph; words compose linearly. This "
            "bundle carries the complete script (93 morphemes, all drawn, in a real font), "
            "the canon of forged words with definitions, and the founding doctrine."
        ),
        "counts": {
            "morphemes": len(morphemes),
            "canon_entries": len(canon),
            "canon_words_renderable": sum(1 for w in canon_words if w["glyph_text"]),
            "donor_sigils": 15,
        },
        "morphemes": morphemes,
        "canon": canon,
        "canon_words": canon_words,
        "docs": docs,
        "fonts": fonts,
    }

    out = SCRIPT / "exports" / "agent_bundle.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False))
    size_kb = out.stat().st_size // 1024
    print(f"wrote {out} ({size_kb} KB): {len(morphemes)} morphemes · "
          f"{len(canon)} canon entries ({det_count} class-marked) · {len(canon_words)} decomposed words · "
          f"{len(docs)} docs · fonts {list(fonts)}")

    if "--copy-to" in sys.argv:
        dest = Path(sys.argv[sys.argv.index("--copy-to") + 1])
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "bundle.json").write_text(out.read_text())
        print(f"vendored copy → {dest / 'bundle.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
