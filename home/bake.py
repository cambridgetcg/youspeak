#!/usr/bin/env python3
"""bake.py — bake the ai-love.cc home ("the cathedral at love") from the agent bundle.

Reads script/exports/agent_bundle.json (regenerate first with
`python3 script/tools/export_agent_bundle.py` if canon has moved) and writes:

  font/youspeak-v1.otf     — the script, decoded from the bundle
  data/morphemes.min.json  — 93 stones (glyph paths + strokes for chisel-draw)
  data/lexicon.min.json    — every canon entry, decompositions merged in
  data/agent_bundle.json   — full bundle, verbatim, for visiting agents
  data/core.js             — the small synchronous kernel the page needs first
  proof.html               — the mason's proof sheet: stroke-render vs carved path

Never hand-edit the outputs. index.html is authored by hand; every NUMBER it
shows is filled from core.js at runtime so the copy can never drift from canon.

Coordinate law (verified): glyph core.strokes/polygons are EM-space (y-up);
svg_path is SVG-space (y-down). svgY = 1000 - emY. The proof sheet exists so
this flip is checked by eye on all 93 stones before every deploy.
"""
import base64
import io
import json
import sys
from pathlib import Path

HOME = Path(__file__).resolve().parent
BUNDLE = HOME.parent / "script" / "exports" / "agent_bundle.json"

CORE16 = [  # PRIMER.md learner order — treasury default view
    "kimance", "kimme", "shemme", "kinqing", "panimqing", "walkekin",
    "doxomme", "panimaance", "oriance", "sukhance", "theobasis", "paqduqing",
    "britqing", "maatme", "ihsanme", "ifeqing",
]
HERO_WORD = "anagnoristasis"  # recognition standing still — hard-tested; see proof.html

b = json.loads(BUNDLE.read_text())

(HOME / "font").mkdir(exist_ok=True)
(HOME / "data").mkdir(exist_ok=True)

font_bytes = base64.b64decode(b["fonts"]["otf"])
(HOME / "font" / "youspeak-v1.otf").write_bytes(font_bytes)

# ── font cmap: the ground truth for what actually renders ──────────────
from fontTools.ttLib import TTFont  # noqa: E402

cmap = TTFont(io.BytesIO(font_bytes)).getBestCmap()


def clean(s):
    s = (s or "").strip()
    return "" if s == ">" else s  # some multiline gap fields export as a bare '>'


morphemes = []
for m in b["morphemes"]:
    core = m["glyph"]["core"]
    morphemes.append({
        "latin": m["latin"],
        "codepoint": m["codepoint"],
        "char": m["char"],
        "tongue": m["tongue"],
        "native": m["native"],
        "meaning": m["meaning"],
        "mclass": m["mclass"],
        "domain": m["domain"],
        "iconography": m["iconography"],
        "rationale": m["rationale"],
        "svg_path": m["glyph"]["svg_path"],
        "strokes": core.get("strokes") or [],
        "polygons": core.get("polygons") or [],
    })

words = {w["word"]: w for w in b["canon_words"]}
lexicon = []
for c in b["canon"]:
    w = words.get(c["word"], {})
    lexicon.append({
        "word": c["word"],
        "tier": c.get("tier", ""),
        "gap": clean(c.get("gap", "")),
        "definition": clean(c.get("definition", "")),
        "pronunciation": clean(c.get("pronunciation", "")),
        "entered": c.get("entered", ""),
        "morphemes": w.get("morphemes"),
        "glyph_text": w.get("glyph_text"),
    })

# ── asserts: the numbers carved into the door must be true ──────────────
renderable = [w for w in b["canon_words"] if w.get("glyph_text")]
assert len(renderable) == b["counts"]["canon_words_renderable"], (
    f"renderable count drifted: {len(renderable)} vs {b['counts']}")
for w in renderable:
    missing = [f"U+{ord(ch):04X}" for ch in w["glyph_text"] if ord(ch) not in cmap]
    assert not missing, f"{w['word']}: glyph_text codepoints not in font cmap: {missing}"

M = {m["latin"]: m for m in morphemes}
stroke_complete = [
    w["word"] for w in renderable
    if all(M.get(p, {}).get("strokes") for p in w["morphemes"])
]
assert HERO_WORD in stroke_complete, f"hero word {HERO_WORD} is not stroke-complete"
hero_w = words[HERO_WORD]
hero_c = next(c for c in lexicon if c["word"] == HERO_WORD)

def spell(n):
    """English words for a count, so the carved copy stays prose at any canon size."""
    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
    if n < 1000:
        rest = n % 100
        head = ones[n // 100] + " hundred"
        return head + (" and " + spell(rest) if rest else "")
    return str(n)


core_js = {
    "counts": b["counts"],
    "count_words": {
        "morphemes": spell(b["counts"]["morphemes"]),
        "canon": ("a hundred" + " and " + spell(b["counts"]["canon_entries"] % 100)
                  if 100 <= b["counts"]["canon_entries"] < 200 and b["counts"]["canon_entries"] % 100
                  else spell(b["counts"]["canon_entries"])),
        "renderable": spell(b["counts"]["canon_words_renderable"]),
    },
    "source_commit": b["source_commit"],
    "map": {m["latin"]: m["char"] for m in morphemes},
    "sep": next((m["char"] for m in morphemes if m["latin"] == "·"), " "),
    "hero": {
        "word": HERO_WORD,
        "glyph_text": hero_w["glyph_text"],
        "codepoints": hero_w["codepoints"],
        "pronunciation": hero_c["pronunciation"],
        "definition": hero_c["definition"],
        "morphemes": [{
            "latin": p,
            "meaning": M[p]["meaning"],
            "svg_path": M[p]["svg_path"],
            "strokes": M[p]["strokes"],
            "polygons": M[p]["polygons"],
        } for p in hero_w["morphemes"]],
    },
    "presets": [{"word": w["word"], "glyph_text": words[w["word"]]["glyph_text"],
                 "morphemes": words[w["word"]]["morphemes"]}
                for w in sorted(renderable, key=lambda x: x["word"])],
    "core16": [w for w in CORE16 if any(c["word"] == w for c in lexicon)],
}

mj = json.dumps({"morphemes": morphemes}, ensure_ascii=False, separators=(",", ":"))
lj = json.dumps({"lexicon": lexicon}, ensure_ascii=False, separators=(",", ":"))
cj = "window.YS_CORE=" + json.dumps(core_js, ensure_ascii=False, separators=(",", ":")) + ";"
(HOME / "data" / "morphemes.min.json").write_text(mj)
(HOME / "data" / "lexicon.min.json").write_text(lj)
(HOME / "data" / "core.js").write_text(cj)
(HOME / "data" / "agent_bundle.json").write_text(json.dumps(b, ensure_ascii=False))

# ── the mason's proof sheet: every stone, strokes vs carved path ────────
STROKE_WIDTH = 80  # script/glyphs/glyph_specs_v1.py — 4-length strokes use this


def stroke_svg(m):
    parts = []
    for s in m["strokes"]:
        x1, y1, x2, y2 = s[:4]
        w = s[4] if len(s) > 4 else STROKE_WIDTH
        if x1 == x2 and y1 == y2:  # zero-length stroke = a w×w square (builder law)
            h = w // 2
            parts.append(f'<rect x="{x1-h}" y="{1000-y1-h}" width="{w}" height="{w}" fill="#C9A45C"/>')
        else:
            parts.append(f'<line x1="{x1}" y1="{1000-y1}" x2="{x2}" y2="{1000-y2}" '
                         f'stroke="#C9A45C" stroke-width="{w}" stroke-linecap="butt"/>')
    for poly in m["polygons"]:
        pts = " ".join(f"{x},{1000-y}" for x, y in poly)
        parts.append(f'<polygon points="{pts}" fill="#C9A45C"/>')
    return "".join(parts)


cells = []
for m in morphemes:
    left = (f'<svg viewBox="0 0 1000 1000">{stroke_svg(m)}</svg>'
            if (m["strokes"] or m["polygons"]) else
            '<div class="none">no strokes<br>(fade-only)</div>')
    cells.append(
        f'<div class="cell"><div class="pair">{left}'
        f'<svg viewBox="0 0 1000 1000"><path d="{m["svg_path"]}" fill="#E6DCC8"/></svg></div>'
        f'<p>{m["latin"]} · {m["codepoint"]} · {m["tongue"]}</p></div>')

(HOME / "proof.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>proof sheet — the mason checks the flip</title>
<style>
body{{background:#14100C;color:#A79A82;font:14px/1.5 ui-monospace,Menlo,monospace;padding:2rem}}
h1{{color:#E6DCC8;font-weight:400}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem}}
.cell{{border:1px solid #352C22;padding:.6rem}}.pair{{display:flex;gap:.4rem}}
svg{{width:100%;background:#1E1813}}.none{{width:100%;display:grid;place-items:center;background:#1E1813;color:#6B5F4C;text-align:center;font-size:11px}}
p{{margin:.4rem 0 0;font-size:11px}}
</style></head><body>
<h1>proof sheet — {len(morphemes)} stones</h1>
<p>left: chisel strokes (y-flipped from EM space) · right: the carved svg_path (authoritative).<br>
if any left glyph is upside-down or misplaced relative to its right, the flip law broke — do not deploy.</p>
<div class="grid">{"".join(cells)}</div></body></html>""")

# tidy superseded first-draft outputs
for old in [HOME / "assets" / "data.js", HOME / "assets" / "agent_bundle.json",
            HOME / "assets" / "youspeak-v1.otf"]:
    if old.exists():
        old.unlink()

print(f"font/youspeak-v1.otf      {len(font_bytes)//1024} KB · cmap {len(cmap)} glyphs")
print(f"data/morphemes.min.json   {len(mj)//1024} KB · {len(morphemes)} morphemes")
print(f"data/lexicon.min.json     {len(lj)//1024} KB · {len(lexicon)} entries")
print(f"data/core.js              {len(cj)//1024} KB · hero={HERO_WORD} · "
      f"{len(renderable)} renderable / {len(stroke_complete)} stroke-complete")
print(f"proof.html                {len(morphemes)} stones — open and eyeball before deploy")
