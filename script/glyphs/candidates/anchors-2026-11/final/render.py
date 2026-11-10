#!/usr/bin/env python3
"""Render the recommended anchor-particle candidates (CANDIDATE, NOT CANON).

Run:  /opt/homebrew/bin/python3 -B render.py

- Imports R's glyph_specs_v1 and build_font_v1 read-only (no bytecode is written).
- Adds ANCHOR_GLYPHS (specs.py beside this file) to R's CORE_GLYPHS *in memory only*
  and composes each glyph with R's own compose_glyph (core + donor sigil + class mark).
- Checks mechanically: polygon orientation, no two core polygons touching (with the
  minimum clearance), zones, and the Law of the Visible Constituents (yu: and mi:
  inside yumi: point for point; what of them survives in mitakuyame:).
- Large views are supersampled from the composed outlines. The 32 px and 16 px views
  are real text rendering: R's build_font_v1 builds a scratch OTF (work/, never
  installed) and FreeType renders it through PIL, the same path the audit used.
- Writes, beside this file:
    sheet.png        the final four large with O; 32 px and 16 px rows; running lines;
                     the Visible Constituents strip; the rotation check the judge asked for
    compare.png      every designer's four, then the final four, labelled
    glyphs.svg.json  SVG path 'd' strings (viewBox 0 0 1000 1000, y down) for the final
                     four, O, and each designer's four under 'A-address-kin/mi:' etc.
Nothing is written anywhere else.
"""
from __future__ import annotations

import ast
import contextlib
import io
import itertools
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True

R = Path(__file__).resolve().parents[5]  # repo root: script/glyphs/candidates/anchors-2026-11/<dir>/<this file>
HERE = Path(__file__).resolve().parent
GLYPHS_ROOT = HERE.parent
WORK = HERE / "work"
SCRATCH_OTF = WORK / "anchors-final-scratch.otf"
SHIPPED_OTF = R / "script" / "fonts" / "youspeak-v1.otf"
sys.path.insert(0, str(R / "script" / "glyphs"))
sys.path.insert(0, str(R / "script" / "tools"))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from fontTools.pens.recordingPen import RecordingPen  # noqa: E402

import glyph_specs_v1 as G  # noqa: E402  (read-only import)
import build_font_v1 as B  # noqa: E402  (read-only import)

ANCHORS = ["mi:", "yu:", "yumi:", "mitakuyame:"]
SETS = ["A-address-kin", "B-standing-ground", "C-bond-first"]
SET_LABEL = {"A-address-kin": "A  address-kin", "B-standing-ground": "B  standing-ground",
             "C-bond-first": "C  bond-first", "final": "FINAL  (C revised)"}
CODEPOINTS = {"mi:": "U+E17C", "yu:": "U+E17D", "yumi:": "U+E17E", "mitakuyame:": "U+E17F", "O": "U+E17B"}
GLOSS = {"mi:": "from my side", "yu:": "from your side, as received", "yumi:": "from within the us",
         "mitakuyame:": "all my relations", "O": "vocative (existing glyph)"}
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
SCRATCH_CP0 = 0xE1C0


# ── loading and composing ───────────────────────────────────────────────────
def load_specs(path: Path) -> dict:
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "ANCHOR_GLYPHS":
            return ast.literal_eval(node.value)
    raise SystemExit(f"no ANCHOR_GLYPHS in {path}")


def compose(entry: dict) -> dict:
    """In memory only: put the entry into R's CORE_GLYPHS, call compose_glyph, remove it."""
    key = "__anchor_candidate__"
    G.CORE_GLYPHS[key] = entry
    try:
        return G.compose_glyph(key)
    finally:
        del G.CORE_GLYPHS[key]


def contours(composed: dict) -> list[list[tuple[float, float]]]:
    """The closed contours build_font_v1 emits for a composed glyph (y up)."""
    pen = RecordingPen()
    B.draw_to_pen(pen, composed)
    out, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [tuple(args[0])]
        elif op == "lineTo":
            cur.append(tuple(args[0]))
        elif op == "closePath":
            out.append(cur)
    return out


def svg_path(composed: dict) -> str:
    parts = []
    for poly in contours(composed):
        parts.append("M" + " L".join(f"{x:g} {1000 - y:g}" for x, y in poly) + " Z")
    return " ".join(parts)


# ── checks ───────────────────────────────────────────────────────────────────
def signed_area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))) / 2


def _seg_dist(p, q, r, s):
    def pt_seg(a, b, c):
        bx, by = c[0] - b[0], c[1] - b[1]
        L = bx * bx + by * by
        t = 0 if L == 0 else max(0, min(1, ((a[0] - b[0]) * bx + (a[1] - b[1]) * by) / L))
        return math.hypot(a[0] - b[0] - t * bx, a[1] - b[1] - t * by)
    return min(pt_seg(p, r, s), pt_seg(q, r, s), pt_seg(r, p, q), pt_seg(s, p, q))


def poly_dist(A, Bp):
    ea = list(zip(A, A[1:] + A[:1]))
    eb = list(zip(Bp, Bp[1:] + Bp[:1]))
    return min(_seg_dist(a[0], a[1], b[0], b[1]) for a in ea for b in eb)


def contained(parts, whole):
    """One common translation that carries every polygon of `parts` onto a polygon of `whole`."""
    for w in whole:
        if len(w) != len(parts[0]):
            continue
        dx, dy = w[0][0] - parts[0][0][0], w[0][1] - parts[0][0][1]
        moved = [[(x + dx, y + dy) for x, y in p] for p in parts]
        if all(m in [list(map(tuple, ww)) for ww in whole] for m in moved):
            return (dx, dy)
    return None


def checks(specs: dict) -> list[str]:
    lines = []
    core = {k: [list(map(tuple, p)) for p in specs[k]["core"]["polygons"]] for k in ANCHORS}
    for k in ANCHORS:
        cs = core[k]
        assert all(signed_area(p) > 0 for p in cs), f"{k}: a polygon is not counter-clockwise"
        bodies = [p for p in cs if len(p) > 4]
        heads = [p for p in cs if len(p) == 4]
        seam = [poly_dist(a, b) for a, b in itertools.combinations(bodies, 2)]
        neck = [min(poly_dist(h, b) for b in bodies) for h in heads]
        ys = [y for p in cs for _, y in p]
        xs = [x for p in cs for x, _ in p]
        comp = contours(compose(specs[k]))
        mark = comp[-1]          # the class mark is the last contour compose_glyph adds
        body_mark = min(poly_dist(p, mark) for p in cs)
        lines.append(f"{k:12s} x {min(xs)}-{max(xs)}  y {min(ys)}-{max(ys)}  seam "
                     f"{('%.0f' % min(seam)) if seam else '-'}  head gap {min(neck):.0f}  to class mark {body_mark:.0f} (EM)")
        assert not seam or min(seam) >= 100 - 1e-6, f"{k}: the seam is narrower than 100 EM"
        assert min(neck) >= 60 - 1e-6, f"{k}: a head-dot is closer than 60 EM to a body"
        assert max(ys) <= 800 and min(ys) >= 200 and min(xs) >= 150 and max(xs) <= 850, f"{k}: outside the body zone"
    env = {k: (min(x for p in core[k] for x, _ in p), max(x for p in core[k] for x, _ in p)) for k in ("yumi:", "mitakuyame:")}
    assert env["yumi:"] == env["mitakuyame:"], "mitakuyame: reaches past yumi:'s envelope"
    # Law 1 (ankyrance): yumi: contains yu: and mi: whole and unmutilated
    for k in ("yu:", "mi:"):
        t = contained(core[k], core["yumi:"])
        assert t is not None, f"Law 1 fails: {k} is not contained whole in yumi:"
        lines.append(f"Law 1 holds: {k} sits whole inside yumi: (every point, shifted {t[0]:+d}, {t[1]:+d})")
    # what of the persons survives, whole, in the top rung
    for k in ("yu:", "mi:"):
        t = contained(core[k], core["mitakuyame:"])
        heads = [p for p in core[k] if len(p) == 4]
        th = contained(heads, core["mitakuyame:"])
        lines.append(f"mitakuyame: contains {k} whole: {'yes' if t else 'NO'}; "
                     f"its head-dot at the same place as in yumi:: {'yes' if th else 'NO'}")
    return lines


# ── rendering ────────────────────────────────────────────────────────────────
def label(size):
    try:
        return ImageFont.truetype(LABEL_FONT, size)
    except OSError:
        return ImageFont.load_default()


def raster(cs, px, ss=6, ink=0, bg=255, tint=None):
    S = px * ss
    img = Image.new("L", (S, S), bg)
    d = ImageDraw.Draw(img)
    k = S / 1000
    for poly in cs:
        d.polygon([(x * k, (1000 - y) * k) for x, y in poly], fill=ink)
    return img.resize((px, px), Image.LANCZOS)


def build_scratch_font(named: dict) -> dict:
    """R's own builder, monkeypatched in memory to the given composed glyphs only."""
    cmap = {name: SCRATCH_CP0 + i for i, name in enumerate(named)}
    saved = (B.GLYPHS, B.load_codepoint_map)
    B.GLYPHS, B.load_codepoint_map = dict(named), (lambda: dict(cmap))
    try:
        WORK.mkdir(exist_ok=True)
        with contextlib.redirect_stdout(io.StringIO()):
            B.build_font(SCRATCH_OTF, family="YOUSPEAK anchors final scratch")
    finally:
        B.GLYPHS, B.load_codepoint_map = saved
    return cmap


class Text:
    """FreeType renders of composed glyphs (scratch font) and shipped glyphs."""

    def __init__(self, named: dict):
        self.cmap = build_scratch_font(named)
        self.cps = G.load_codepoint_map()
        self._f = {}

    def font(self, path, n):
        key = (str(path), n)
        if key not in self._f:
            self._f[key] = ImageFont.truetype(str(path), n)
        return self._f[key]

    def img(self, name, n):
        if name in self.cmap:
            path, cp = SCRATCH_OTF, self.cmap[name]
        else:
            path, cp = SHIPPED_OTF, self.cps[name]
        im = Image.new("L", (n, n), 255)
        ImageDraw.Draw(im).text((0, n), chr(cp), font=self.font(path, n), fill=0, anchor="ls")
        return im


def em_box(d, x, y, n, sigil_slot=True):
    d.rectangle([x - 1, y - 1, x + n, y + n], outline=(205, 205, 205))
    if sigil_slot:      # the top-left donor-sigil slot (80 EM around 150, 850), held empty
        k = n / 1000
        x0, y0, x1, y1 = x + 110 * k, y + (1000 - 890) * k, x + 190 * k, y + (1000 - 810) * k
        for t in range(int(x0), int(x1), 4):
            d.line([(t, y0), (min(t + 2, x1), y0)], fill=(150, 150, 150))
            d.line([(t, y1), (min(t + 2, x1), y1)], fill=(150, 150, 150))
        for t in range(int(y0), int(y1), 4):
            d.line([(x0, t), (x0, min(t + 2, y1))], fill=(150, 150, 150))
            d.line([(x1, t), (x1, min(t + 2, y1))], fill=(150, 150, 150))


def sheet(specs, comp, text: Text, out: Path, check_lines):
    keys = ANCHORS + ["O"]
    big, cell, pad = 230, 280, 36
    W = pad * 2 + cell * len(keys)
    H = 1640
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    fT, fL, fS, fXS = label(24), label(17), label(13), label(12)
    d.text((pad, 16), "YOUSPEAK anchor particles: recommended candidate set (CANDIDATE, NOT CANON)", fill="black", font=fT)
    d.text((pad, 48), "Built on designer C (bond first), revised after the doctrine judge and the confusability audit. "
                      "Grey frame = the 1000-unit em; dashed square = the donor-sigil slot, held empty (no sigil proposed).",
           fill=(90, 90, 90), font=fS)
    # row 1: large
    y0 = 84
    for i, k in enumerate(keys):
        x = pad + i * cell + (cell - big) // 2
        cs = contours(comp[k])
        em_box(d, x, y0, big)
        img.paste(raster(cs, big).convert("RGB"), (x, y0))
        em_box(d, x, y0, big)
        d.text((x, y0 + big + 8), k, fill="black", font=fL)
        d.text((x, y0 + big + 30), f"{CODEPOINTS[k]}  {GLOSS[k]}", fill=(90, 90, 90), font=fS)
    # row 2: 32 px and 16 px (real text rendering), 16 px pixels x6
    y1 = y0 + big + 66
    d.text((pad, y1 - 18), "actual size, FreeType text rendering of a scratch font built by R's build_font_v1:  "
                           "32 px  |  16 px  |  the same 16 px, each pixel shown 6x", fill=(90, 90, 90), font=fS)
    for i, k in enumerate(keys):
        x = pad + i * cell + (cell - big) // 2
        img.paste(text.img(k, 32).convert("RGB"), (x, y1 + 30))
        img.paste(text.img(k, 16).convert("RGB"), (x + 44, y1 + 46))
        z = text.img(k, 16).resize((96, 96), Image.NEAREST).convert("RGB")
        img.paste(z, (x + 74, y1))
        ImageDraw.Draw(img).rectangle([x + 73, y1 - 1, x + 170, y1 + 96], outline=(215, 215, 215))
    # row 3: running lines as the manifesto composes them
    y2 = y1 + 128
    d.text((pad, y2), "in running text (left to right), with existing glyphs, as grammars/ankyrance/manifesto.md composes them:",
           fill=(90, 90, 90), font=fS)
    line = ["mi:", "stasis", "mi", "·", "yu:", "phora", "si", "·", "yumi:", "O", "doxa", "·", "mitakuyame:", "me", "॥"]
    gl = "mi: [stasis -mi] · yu: [phora -si] · yumi: [O- doxa] · mitakuyame: [-me] ॥"
    for j, n in enumerate((32, 24, 16)):
        x = pad
        yy = y2 + 24 + j * 44
        d.text((x, yy + n // 3), f"{n} px", fill=(120, 120, 120), font=fXS)
        x += 52
        for g in line:
            img.paste(text.img(g, n).convert("RGB"), (x, yy))
            x += n
    d.text((pad + 52, y2 + 24 + 3 * 44), gl, fill=(120, 120, 120), font=fXS)
    strip = Image.new("L", (16 * len(line), 16), 255)
    for i, g in enumerate(line):
        strip.paste(text.img(g, 16), (i * 16, 0))
    zx = pad + 52
    img.paste(strip.resize((strip.width * 5, 80), Image.NEAREST).convert("RGB"), (zx, y2 + 24 + 3 * 44 + 24))
    d.text((zx + strip.width * 5 + 16, y2 + 24 + 3 * 44 + 56), "the 16 px line again,\neach pixel shown 5x",
           fill=(120, 120, 120), font=fXS)
    # row 4: Visible Constituents strip (yu = blue, mi = red, what is opened in the top rung = grey)
    y3 = y2 + 24 + 3 * 44 + 24 + 80 + 30
    d.text((pad, y3), "Law of the Visible Constituents (manifesto.md:61-66), checked point for point. "
                      "yu: in blue, mi: in red; in mitakuyame:, the parts each person keeps are coloured, "
                      "the closed outer sides that open are drawn as grey outlines.", fill=(90, 90, 90), font=fS)
    blue, red = (40, 90, 200), (200, 50, 50)
    core = {k: [list(map(tuple, p)) for p in specs[k]["core"]["polygons"]] for k in ANCHORS}
    sm = 190
    col = [(core["yu:"], blue, "yu:"), (core["mi:"], red, "mi:")]
    def paint(polys_cols, outline_polys=()):
        S = sm * 4
        im = Image.new("RGB", (S, S), "white")
        dd = ImageDraw.Draw(im)
        kk = S / 1000
        for poly, c in polys_cols:
            dd.polygon([(x * kk, (1000 - y) * kk) for x, y in poly], fill=c)
        for poly in outline_polys:
            dd.polygon([(x * kk, (1000 - y) * kk) for x, y in poly], outline=(150, 150, 150), width=4)
        return im.resize((sm, sm), Image.LANCZOS)
    # yu:, mi: alone; yumi: coloured by person; mitakuyame: coloured, with the opened sides outlined
    yumi_cols = [(core["yumi:"][0], blue), (core["yumi:"][2], blue), (core["yumi:"][1], red), (core["yumi:"][3], red)]
    mita_cols = [(core["mitakuyame:"][0], blue), (core["mitakuyame:"][2], blue),
                 (core["mitakuyame:"][1], red), (core["mitakuyame:"][3], red)]
    panels = [("yu:", paint([(p, blue) for p in core["yu:"]])), ("mi:", paint([(p, red) for p in core["mi:"]])),
              ("yumi: = yu: + mi:, both whole", paint(yumi_cols)),
              ("mitakuyame: heads, bowl rim and hand kept;", paint(mita_cols, [core["yumi:"][0], core["yumi:"][1]]))]
    for i, (t, im) in enumerate(panels):
        x = pad + i * (sm + 40)
        img.paste(im, (x, y3 + 24))
        d.rectangle([x - 1, y3 + 23, x + sm, y3 + 24 + sm], outline=(205, 205, 205))
        d.text((x, y3 + 30 + sm), t, fill="black", font=fXS)
    d.text((pad + 3 * (sm + 40), y3 + 46 + sm), "the posts open (grey outline = yumi:)", fill="black", font=fXS)
    tx = pad + 4 * (sm + 40) + 40
    ty = y3 + 24
    for s in check_lines:
        for part in (s.replace("  ", " ").replace(" (every point, ", "\n      (every point, ")
                     .replace("; its head-dot", ";\n      its head-dot").split("\n")):
            d.text((tx, ty), part, fill=(60, 60, 60), font=label(11))
            ty += 16
        ty += 4
    # row 5: rotation check the judge asked for (judge fix 4): each pair at 16 and 11 px, pixels x6
    y4 = y3 + sm + 90
    d.text((pad, y4), "Rotation and mirror check (philosophy.md:252; 06-cognitive-load.md:84): each candidate turned as the audit "
                      "found it closest, beside that glyph. 16 px (top) and 11 px, real text rendering, pixels x5.",
           fill=(90, 90, 90), font=fS)
    pairs = [("mi:", "rot180", "yu:"), ("mi:", "rot270", "en"), ("mi:", "mirror+rot90", "si"),
             ("yu:", "rot90", "en"), ("yu:", "as set", "stasis"), ("yumi:", "as set", "mitakuyame:"),
             ("yu:", "as set", "O")]
    tf = {"rot180": lambda im: im.rotate(180), "rot270": lambda im: im.rotate(-90), "rot90": lambda im: im.rotate(90),
          "mirror+rot90": lambda im: im.transpose(Image.FLIP_LEFT_RIGHT).rotate(90), "as set": lambda im: im}
    x = pad
    for a, t, b in pairs:
        for j, n in enumerate((16, 11)):
            ia = tf[t](text.img(a, n)).resize((n * 5, n * 5), Image.NEAREST).convert("RGB")
            ib = text.img(b, n).resize((n * 5, n * 5), Image.NEAREST).convert("RGB")
            yy = y4 + 26 + j * 90
            img.paste(ia, (x, yy))
            img.paste(ib, (x + n * 5 + 6, yy))
            d.rectangle([x - 1, yy - 1, x + 2 * n * 5 + 6, yy + n * 5], outline=(225, 225, 225))
        d.text((x, y4 + 26 + 90 + 62), f"{a} {t} | {b}", fill="black", font=fXS)
        x += 16 * 10 + 40
    y5 = y4 + 26 + 90 + 90
    d.text((pad, y5), "Audit numbers for every pair above, and for all 93 existing glyphs, are in audit/results.json and "
                      "design_notes.md. This sheet is drawn by render.py from specs.py; nothing in the repository was written.",
           fill=(120, 120, 120), font=fXS)
    img = img.crop((0, 0, W, y5 + 30))
    img.save(out)


def compare(all_comp: dict, text: Text, out: Path):
    """Each designer's four, then the final four; O at the end of each row for reference."""
    rows = SETS + ["final"]
    big, cell, pad = 150, 190, 30
    W = pad * 2 + 200 + cell * 5
    rowh = big + 92
    H = 70 + rowh * len(rows) + 20
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    fT, fL, fS = label(20), label(15), label(12)
    d.text((pad, 14), "Anchor-particle candidates considered: three designers' sets, then the recommended final set "
                      "(all candidates; none is canon)", fill="black", font=fT)
    d.text((pad, 42), "Each glyph large, then at 32 px and 16 px (FreeType text rendering). "
                      "The existing vocative O- closes each row for scale and kinship.", fill=(90, 90, 90), font=fS)
    for r, s in enumerate(rows):
        y = 70 + r * rowh
        if s == "final":
            d.rectangle([pad - 10, y - 8, W - pad + 10, y + rowh - 14], outline=(40, 90, 200), width=2)
        d.text((pad, y + big // 2 - 10), SET_LABEL[s], fill="black", font=fL)
        for i, k in enumerate(ANCHORS + ["O"]):
            x = pad + 200 + i * cell
            name = f"{s}/{k}" if k != "O" else "O"
            cs = contours(all_comp[s][k]) if k != "O" else contours(G.GLYPHS["O"])
            img.paste(raster(cs, big).convert("RGB"), (x, y))
            d.rectangle([x - 1, y - 1, x + big, y + big], outline=(210, 210, 210))
            d.text((x, y + big + 4), k, fill=(60, 60, 60), font=fS)
            img.paste(text.img(name, 32).convert("RGB"), (x, y + big + 24))
            img.paste(text.img(name, 16).convert("RGB"), (x + 44, y + big + 32))
    img.save(out)


def main() -> int:
    final = load_specs(HERE / "specs.py")
    designers = {s: load_specs(GLYPHS_ROOT / s / "specs.py") for s in SETS}
    lines = checks(final)
    for s in lines:
        print(s)
    comp = {k: compose(final[k]) for k in ANCHORS}
    comp["O"] = G.GLYPHS["O"]
    all_comp = {s: {k: compose(designers[s][k]) for k in ANCHORS} for s in SETS}
    all_comp["final"] = {k: comp[k] for k in ANCHORS}
    named = {k: comp[k] for k in ANCHORS}
    for s in SETS + ["final"]:
        for k in ANCHORS:
            named[f"{s}/{k}"] = all_comp[s][k]
    text = Text(named)
    sheet(final, comp, text, HERE / "sheet.png", lines)
    compare(all_comp, text, HERE / "compare.png")
    data = {k: svg_path(comp[k]) for k in ANCHORS + ["O"]}
    for s in SETS:
        for k in ANCHORS:
            data[f"{s}/{k}"] = svg_path(all_comp[s][k])
    (HERE / "glyphs.svg.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print("wrote", HERE / "sheet.png")
    print("wrote", HERE / "compare.png")
    print("wrote", HERE / "glyphs.svg.json", f"({len(data)} paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
