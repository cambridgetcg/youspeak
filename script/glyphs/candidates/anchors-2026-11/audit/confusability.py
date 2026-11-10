#!/usr/bin/env python3
"""Confusability audit of the candidate glyph sets for the four YOUSPEAK anchor
particles (mi: yu: yumi: mitakuyame:, U+E17C-E17F), by measurement.

Run:   /opt/homebrew/bin/python3 -B confusability.py

Reads (never writes) the YOUSPEAK repository R and the three candidate folders.
Writes only beside this file:
  results.json     the table and the calibration
  neighbours.png   each candidate beside its three nearest existing glyphs at 32 px
  neighbours_16px.png  the same at 16 px (companion; small size is where confusion bites)
  build/anchor-candidates-audit.otf
                   a scratch font made by R's own build_font_v1.build_font() so the
                   candidates go through the same composer, outliner and rasteriser
                   as the shipped glyphs. It is never installed.

Method, in short
  * Existing 93 glyphs: rendered by FreeType (PIL ImageFont) from the shipped
    R/script/fonts/youspeak-v1.otf at the Private Use codepoints in morphemes.json.
  * Candidates: each set's specs.py entry is composed by R's compose_glyph()
    (core + sigil + class mark), outlined by build_font_v1 into a scratch OTF, and
    rendered by the same FreeType call. The same scratch font also carries the 93
    existing specs, and their renders are checked pixel-for-pixel against the
    shipped font, so the two paths are shown to be the same path.
  * Cross-check renderer: an independent supersampled nonzero-winding rasteriser
    over the same composed outlines (no hinting, no FreeType).
  * Sizes are px per em (font size): 16, 24, 32 (11 px is a supplementary 8 pt row).
  * Binarise at 50 % coverage; centre each mask on its ink centroid.
  * M1 = IoU (Jaccard) of the binary masks; M2 = zero-mean normalised
    cross-correlation of the binary masks after a Gaussian blur (sigma 0.7 px),
    over a fixed (2 em + 4 px) square canvas. Both take the best of 3x3 integer
    shifts (+-1 px) after centring.
  * Transforms: the candidate under all 8 symmetries of the square (identity,
    rotations by 90/180/270, mirror left-right, mirror top-bottom, and the two
    diagonal mirrors), re-centred after transforming.
  * Calibration: every existing glyph against the other 92 under the same measure,
    giving the inventory's nearest-neighbour distribution and closest pairs.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # with -B: nothing is written into R or the candidate folders

import importlib.util
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[5]  # repo root: script/glyphs/candidates/anchors-2026-11/<dir>/<this file>
HERE = Path(__file__).resolve().parent
GLYPHS_ROOT = HERE.parent
OUT_JSON = HERE / "results.json"
OUT_PNG = HERE / "neighbours.png"
BUILD_DIR = HERE / "build"
SCRATCH_OTF = BUILD_DIR / "anchor-candidates-audit.otf"
SHIPPED_OTF = R / "script" / "fonts" / "youspeak-v1.otf"
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

SETS = ["A-address-kin", "B-standing-ground", "C-bond-first"]
ANCHORS = ["mi:", "yu:", "yumi:", "mitakuyame:"]
SIZES = [16, 24, 32]
SUPP_SIZES = [11]  # ~8 pt at 96 dpi; Cohesion Rule 6 names 8 pt. Reported, not judged on.
THRESH = 128       # binarise at 50 % coverage
SHIFT = 1          # +-1 px search after centring
BLUR_SIGMA = 0.7   # px, for M2
GEOM_SS = 6        # supersampling per axis for the cross-check rasteriser
SCRATCH_CP0 = 0xE1A0  # scratch codepoints for candidates inside the scratch font only

MEASURES = ["iou", "ncc"]
TRANSFORMS = ["identity", "rot90", "rot180", "rot270",
              "mirror_lr", "mirror_tb", "mirror_diag", "mirror_antidiag"]
T_FUNCS = {
    "identity": lambda a: a,
    "rot90": lambda a: np.rot90(a, 1),       # 90 deg counter-clockwise
    "rot180": lambda a: np.rot90(a, 2),
    "rot270": lambda a: np.rot90(a, 3),      # 90 deg clockwise
    "mirror_lr": lambda a: a[:, ::-1],       # left <-> right
    "mirror_tb": lambda a: a[::-1, :],       # top <-> bottom
    "mirror_diag": lambda a: a.T,
    "mirror_antidiag": lambda a: np.rot90(a, 2).T,
}
SHIFTS = [(dy, dx) for dy in range(-SHIFT, SHIFT + 1) for dx in range(-SHIFT, SHIFT + 1)]

# Existing pairs that are transforms of each other BY DESIGN. Their designed transform
# relation is exempt from the "tolerated closeness" threshold (06-cognitive-load.md:84
# allows reflections/rotations only for intended pairs); their identity score still counts.
DESIGNED_TWINS = {
    frozenset({"strophe", "anastro"}): "anastro is 'a clockwise-reverse spiral (mirror of strophe's spiral)' "
                                       "(script/glyphs/README.md:211), the inversion pair",
    frozenset({"「", "」"}): "」 is the 'exact 180-degree rotation of bracket-open' (design_notes_s092.md:142)",
}
# Existing glyphs the brief and the designers name as the anchors' kin or hazards.
NAMED = ["O", "mi", "si", "chu", "auth", ".REL", ".PER", "[selah]", "kin", "panim", "stasis"]

# ── R's own modules, imported read-only ─────────────────────────────────────
sys.path.insert(0, str(R / "script" / "glyphs"))
sys.path.insert(0, str(R / "script" / "tools"))
import glyph_specs_v1 as gs  # noqa: E402
import build_font_v1 as bf   # noqa: E402


def load_morphemes():
    data = json.loads((R / "script" / "morphemes.json").read_text())
    disp, cps = {}, {}
    for m in data["morphemes"]:
        key = m["latin"].strip("-")           # same rule as glyph_specs_v1.load_codepoint_map
        cps[key] = int(m["codepoint"].replace("U+", ""), 16)
        disp[key] = m["latin"]
    return cps, disp


def load_candidates():
    out = {}
    for s in SETS:
        p = GLYPHS_ROOT / s / "specs.py"
        spec = importlib.util.spec_from_file_location(f"cand_{s.replace('-', '_')}", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out[s] = mod.ANCHOR_GLYPHS
    return out


def compose_candidate(entry):
    """Compose exactly as the builder does: put the entry into CORE_GLYPHS (in memory
    only) and call R's compose_glyph()."""
    key = "__audit_candidate__"
    gs.CORE_GLYPHS[key] = entry
    try:
        return gs.compose_glyph(key)
    finally:
        del gs.CORE_GLYPHS[key]


def contours_of(composed):
    cs = []
    for st in composed.get("strokes", []):
        if len(st) >= 5:
            x1, y1, x2, y2, w = st[:5]
        else:
            x1, y1, x2, y2 = st
            w = gs.STROKE_WIDTH
        cs.append([tuple(map(float, p)) for p in bf.stroke_to_polygon(x1, y1, x2, y2, w)])
    for poly in composed.get("polygons", []):
        if poly:
            cs.append([tuple(map(float, p)) for p in poly])
    return cs


def svg_contours(d):
    """Parse an M/L/Z path in a y-down 1000 viewBox into y-up font-unit contours."""
    toks = re.findall(r"[MLZmlz]|-?\d+(?:\.\d+)?", d)
    cs, cur, i = [], [], 0
    while i < len(toks):
        t = toks[i]
        if t in "Mm":
            if cur:
                cs.append(cur)
            cur = [(float(toks[i + 1]), 1000.0 - float(toks[i + 2]))]
            i += 3
        elif t in "Ll":
            cur.append((float(toks[i + 1]), 1000.0 - float(toks[i + 2])))
            i += 3
        elif t in "Zz":
            if cur:
                cs.append(cur)
            cur = []
            i += 1
        else:  # implicit lineto
            cur.append((float(toks[i]), 1000.0 - float(toks[i + 1])))
            i += 2
    if cur:
        cs.append(cur)
    return cs


# ── rasterisers ──────────────────────────────────────────────────────────────
def canvas_size(n):
    return 2 * n + 4


def render_font(font, cp, n):
    c = canvas_size(n)
    m = (c - n) // 2
    img = Image.new("L", (c, c), 0)
    ImageDraw.Draw(img).text((m, m + n), chr(cp), font=font, fill=255, anchor="ls")
    return np.asarray(img).copy()


def render_geom(contours, n, ss=GEOM_SS, c=None):
    """Independent nonzero-winding rasteriser, supersampled ss x ss per pixel."""
    c = canvas_size(n) if c is None else c
    m = (c - n) // 2
    idx = (np.arange(c * ss) + 0.5) / ss
    X = (idx - m) * 1000.0 / n
    Y = (m + n - idx) * 1000.0 / n          # row -> font y (y up)
    wind = np.zeros((c * ss, c * ss), np.int32)
    for cont in contours:
        pts = np.asarray(cont, float)
        x0, y0 = pts[:, 0], pts[:, 1]
        x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
        for a, b, cc, d in zip(x0, y0, x1, y1):
            if b == d:
                continue
            lo, hi = min(b, d), max(b, d)
            rows = np.nonzero((Y >= lo) & (Y < hi))[0]
            if rows.size == 0:
                continue
            yy = Y[rows][:, None]
            isl = (cc - a) * (yy - b) - (X[None, :] - a) * (d - b)
            if d > b:   # upward edge
                wind[rows] += (isl > 0).astype(np.int32)
            else:       # downward edge
                wind[rows] -= (isl < 0).astype(np.int32)
    cov = (wind != 0).reshape(c, ss, c, ss).mean(axis=(1, 3))
    return np.round(cov * 255).astype(np.uint8)


# ── normalisation and measures ───────────────────────────────────────────────
def centre(mask):
    ys, xs = np.nonzero(mask)
    if xs.size == 0:
        return mask.copy()
    c = mask.shape[0]
    t = (c - 1) / 2.0
    dy, dx = int(round(t - ys.mean())), int(round(t - xs.mean()))
    out = np.roll(np.roll(mask, dy, 0), dx, 1)
    ys2, xs2 = np.nonzero(out)
    assert ys2.min() > SHIFT and xs2.min() > SHIFT and ys2.max() < c - 1 - SHIFT and xs2.max() < c - 1 - SHIFT, \
        "canvas too small for centring without wrap-around"
    return out


def blur_matrix(c, sigma):
    r = max(1, int(math.ceil(3 * sigma)))
    k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * sigma ** 2))
    k /= k.sum()
    K = np.zeros((c, c))
    for i in range(c):
        for j, w in zip(range(i - r, i + r + 1), k):
            if 0 <= j < c:
                K[i, j] = w
    return K


class Bank:
    """A stack of centred binary masks, flattened, with their blurred versions."""

    def __init__(self, names, masks, K):
        self.names = list(names)
        self.masks = np.stack([masks[n] for n in self.names]).astype(bool)
        self.K = K
        k, c, _ = self.masks.shape
        self.P = c * c
        self.M = self.masks.reshape(k, -1).astype(np.float64)
        self.msum = self.M.sum(1)
        B = (K @ self.masks.astype(np.float64) @ K.T).reshape(k, -1)
        self.B = B
        self.bsum = B.sum(1)
        self.bsq = (B * B).sum(1)


def query(qmask, bank):
    """Score one centred mask, under all 8 transforms, against every mask in bank.
    Returns {measure: array (8 transforms, K)} and the best shift index for IoU."""
    out = {m: np.zeros((len(TRANSFORMS), len(bank.names))) for m in MEASURES}
    best_shift = np.zeros((len(TRANSFORMS), len(bank.names)), int)
    n = bank.P
    for ti, t in enumerate(TRANSFORMS):
        q = centre(T_FUNCS[t](qmask))
        qs = np.stack([np.roll(np.roll(q, dy, 0), dx, 1) for dy, dx in SHIFTS]).astype(np.float64)
        Qm = qs.reshape(len(SHIFTS), -1)
        inter = Qm @ bank.M.T
        union = Qm.sum(1)[:, None] + bank.msum[None, :] - inter
        iou = inter / np.maximum(union, 1e-9)
        out["iou"][ti] = iou.max(0)
        best_shift[ti] = iou.argmax(0)
        qb = (bank.K @ qs @ bank.K.T).reshape(len(SHIFTS), -1)
        sq, sqq = qb.sum(1), (qb * qb).sum(1)
        num = n * (qb @ bank.B.T) - sq[:, None] * bank.bsum[None, :]
        den = np.sqrt(np.maximum((n * sqq - sq ** 2)[:, None] * (n * bank.bsq - bank.bsum ** 2)[None, :], 1e-12))
        out["ncc"][ti] = (num / den).max(0)
    return out, best_shift


def stats(v):
    v = np.asarray(v, float)
    return {"n": int(v.size), "min": round(float(v.min()), 4), "p10": round(float(np.percentile(v, 10)), 4),
            "q1": round(float(np.percentile(v, 25)), 4), "median": round(float(np.median(v)), 4),
            "q3": round(float(np.percentile(v, 75)), 4), "p90": round(float(np.percentile(v, 90)), 4),
            "max": round(float(v.max()), 4), "mean": round(float(v.mean()), 4)}


def pct_rank(dist, x):
    """Share of existing glyphs whose own nearest-neighbour score is <= x (0-100)."""
    return round(100.0 * float(np.mean(np.asarray(dist) <= x + 1e-12)), 1)


# ── the analysis for one renderer ────────────────────────────────────────────
def analyse(existing_masks, cand_masks, sizes, disp):
    """existing_masks[size][key] and cand_masks[size][set][anchor]: binary, centred."""
    res = {"calibration": {}, "existing_nn": {}, "candidates": {}, "internal": {}, "_raw": {}}
    for n in sizes:
        names = sorted(existing_masks[n], key=lambda k: disp[k])
        K = blur_matrix(canvas_size(n), BLUR_SIGMA)
        bank = Bank(names, existing_masks[n], K)
        kN = len(names)
        S = {m: np.zeros((len(TRANSFORMS), kN, kN)) for m in MEASURES}
        for i, nm in enumerate(names):
            sc, _ = query(existing_masks[n][nm], bank)
            for m in MEASURES:
                S[m][:, i, :] = sc[m]
        twin = np.zeros((kN, kN), bool)
        for a in range(kN):
            for b in range(kN):
                if frozenset({names[a], names[b]}) in DESIGNED_TWINS:
                    twin[a, b] = True
        cal, enn = {}, {}
        for m in MEASURES:
            ident = S[m][0].copy()
            anyT = S[m].max(0)
            anyT_arg = S[m].argmax(0)
            anyT_ex = np.where(twin, ident, anyT)                      # designed transforms exempt
            anyT_ex_arg = np.where(twin, 0, anyT_arg)
            for arr in (ident, anyT, anyT_ex):
                np.fill_diagonal(arr, -np.inf)
            regimes = {"identity": (ident, np.zeros_like(anyT_arg)), "any_transform": (anyT_ex, anyT_ex_arg),
                       "any_transform_incl_designed_twins": (anyT, anyT_arg)}
            cal[m] = {}
            for rg, (mat, arg) in regimes.items():
                nn = mat.max(1)
                nn_j = mat.argmax(1)
                # closest pairs (symmetrised: the better of the two directions)
                pairs = {}
                for a in range(kN):
                    for b in range(a + 1, kN):
                        if mat[a, b] >= mat[b, a]:
                            sc, t = mat[a, b], TRANSFORMS[arg[a, b]]
                            q, r = names[a], names[b]
                        else:
                            sc, t = mat[b, a], TRANSFORMS[arg[b, a]]
                            q, r = names[b], names[a]
                        pairs[(q, r)] = (sc, t)
                top = sorted(pairs.items(), key=lambda kv: -kv[1][0])[:10]
                if rg == "any_transform":
                    # the closest pair that needs a rotation or mirror (designed twins exempt)
                    nonid = np.where(twin, -np.inf, S[m][1:].max(0))
                    nonid_arg = np.where(twin, 0, S[m][1:].argmax(0) + 1)
                    np.fill_diagonal(nonid, -np.inf)
                    a_, b_ = np.unravel_index(int(np.argmax(nonid)), nonid.shape)
                    rot_pair = {"a": disp[names[a_]], "b": disp[names[b_]], "score": round(float(nonid[a_, b_]), 4),
                                "transform_of_a": TRANSFORMS[int(nonid_arg[a_, b_])]}
                cal[m][rg] = {
                    "nn_distribution": stats(nn),
                    "closest_pair": {"a": disp[top[0][0][0]], "b": disp[top[0][0][1]],
                                     "score": round(float(top[0][1][0]), 4), "transform_of_a": top[0][1][1]},
                    "closest_10_pairs": [{"a": disp[q], "b": disp[r], "score": round(float(sc), 4),
                                          "transform_of_a": t} for (q, r), (sc, t) in top],
                    "_nn": nn,
                }
                if rg == "any_transform":
                    cal[m][rg]["closest_pair_needing_rotation_or_mirror"] = rot_pair
                if rg != "any_transform_incl_designed_twins":
                    for i, nm in enumerate(names):
                        enn.setdefault(disp[nm], {}).setdefault(m, {})[rg] = {
                            "nearest": disp[names[nn_j[i]]], "score": round(float(nn[i]), 4),
                            "transform": TRANSFORMS[arg[i, nn_j[i]]]}
        res["calibration"][n] = cal
        res["existing_nn"][n] = enn

        # candidates
        res["candidates"][n], res["internal"][n] = {}, {}
        res["_raw"][n] = {"names": names, "bank": bank}
        for s in SETS:
            res["candidates"][n][s] = {}
            for a in ANCHORS:
                sc, shift = query(cand_masks[n][s][a], bank)
                entry = {"_scores": sc, "_shift": shift}
                for m in MEASURES:
                    ident = sc[m][0]
                    anyT = sc[m].max(0)
                    anyT_arg = sc[m].argmax(0)
                    e = {}
                    for rg, vec, arg in (("identity", ident, np.zeros(len(names), int)),
                                         ("any_transform", anyT, anyT_arg)):
                        order = np.argsort(-vec)[:5]
                        nnv = float(vec[order[0]])
                        dist = cal[m][rg]["_nn"]
                        e[rg] = {
                            "top5": [{"glyph": disp[names[j]], "score": round(float(vec[j]), 4),
                                      "transform": TRANSFORMS[arg[j]],
                                      "pct_rank_vs_inventory_nn": pct_rank(dist, float(vec[j]))} for j in order],
                            "nearest": disp[names[order[0]]], "score": round(nnv, 4),
                            "transform": TRANSFORMS[arg[order[0]]],
                            "pct_rank_vs_inventory_nn": pct_rank(dist, nnv),
                            "exceeds_inventory_median_nn": bool(nnv > np.median(dist)),
                            "exceeds_inventory_p90_nn": bool(nnv > np.percentile(dist, 90)),
                            "exceeds_closest_existing_pair": bool(nnv > dist.max()),
                        }
                    e["named"] = {}
                    for key in NAMED:
                        if key in names:
                            j = names.index(key)
                            e["named"][disp[key]] = {"identity": round(float(ident[j]), 4),
                                                     "any_transform": round(float(anyT[j]), 4),
                                                     "transform": TRANSFORMS[anyT_arg[j]]}
                    entry[m] = e
                res["candidates"][n][s][a] = entry
            # within the set
            ib = Bank(ANCHORS, cand_masks[n][s], K)
            pairs = []
            for i, a in enumerate(ANCHORS):
                sc, _ = query(cand_masks[n][s][a], ib)
                for j, b in enumerate(ANCHORS):
                    if j <= i:
                        continue
                    row = {"a": a, "b": b}
                    for m in MEASURES:
                        dist_id = cal[m]["identity"]["_nn"]
                        dist_any = cal[m]["any_transform"]["_nn"]
                        sid = float(sc[m][0, j])
                        sany = float(sc[m][:, j].max())
                        row[m] = {"identity": round(sid, 4), "any_transform": round(sany, 4),
                                  "transform": TRANSFORMS[int(sc[m][:, j].argmax())],
                                  "pct_rank_identity": pct_rank(dist_id, sid),
                                  "pct_rank_any_transform": pct_rank(dist_any, sany),
                                  "exceeds_p90_identity": bool(sid > np.percentile(dist_id, 90)),
                                  "exceeds_p90_any": bool(sany > np.percentile(dist_any, 90)),
                                  "exceeds_closest_existing_pair_identity": bool(sid > dist_id.max()),
                                  "exceeds_closest_existing_pair_any": bool(sany > dist_any.max())}
                    pairs.append(row)
            res["internal"][n][s] = pairs
    return res


# ── the picture ──────────────────────────────────────────────────────────────
def mask_img(mask, win, scale, ink=(0, 0, 0)):
    c = mask.shape[0]
    o = (c - win) // 2
    crop = mask[o:o + win, o:o + win]
    rgb = np.full((win, win, 3), 255, np.uint8)
    rgb[crop] = ink
    return Image.fromarray(rgb).resize((win * scale, win * scale), Image.NEAREST)


def overlay_img(qa, nb, win, scale):
    c = qa.shape[0]
    o = (c - win) // 2
    a = qa[o:o + win, o:o + win]
    b = nb[o:o + win, o:o + win]
    rgb = np.full((win, win, 3), 255, np.uint8)
    rgb[a & ~b] = (215, 50, 50)    # candidate only
    rgb[b & ~a] = (40, 110, 220)   # neighbour only
    rgb[a & b] = (0, 0, 0)         # shared ink
    return Image.fromarray(rgb).resize((win * scale, win * scale), Image.NEAREST)


def grey_img(arr, win):
    c = arr.shape[0]
    o = (c - win) // 2
    return Image.fromarray(255 - arr[o:o + win, o:o + win])


def draw_png(res, existing_masks, cand_masks, grey_existing, grey_cand, disp, n=32, scale=3, out=OUT_PNG):
    names = res["_raw"][n]["names"]
    allm = list(existing_masks[n].values()) + [cand_masks[n][s][a] for s in SETS for a in ANCHORS]
    c = canvas_size(n)
    ext = 0
    for mk in allm:
        for t in TRANSFORMS:
            ys, xs = np.nonzero(centre(T_FUNCS[t](mk)))
            ext = max(ext, int(np.abs(ys - (c - 1) / 2).max()), int(np.abs(xs - (c - 1) / 2).max()))
    win = min(c, 2 * ext + 4)
    cell = win * scale
    f = ImageFont.truetype(LABEL_FONT, 13)
    fb_ = ImageFont.truetype(LABEL_FONT, 15)
    ft = ImageFont.truetype(LABEL_FONT, 19)
    gap, ggap = 4, 26
    group_w = 3 * cell + 2 * gap
    left_w = cell + 30
    true_w = 5 * (win + 6) + 10
    W = left_w + 4 * (group_w + ggap) + true_w + 20
    row_h = cell + 44
    cal = res["calibration"][n]
    H = 150 + (cell + 70) + len(SETS) * (36 + len(ANCHORS) * row_h) + 40
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    y = 14
    d.text((20, y), f"Anchor-particle candidates: each beside its three nearest existing glyphs at {n} px "
                    f"(binarised bitmaps, magnified {scale}x; ranked by IoU over all 8 rotations/mirrors)", font=ft, fill=0)
    y += 30
    d.text((20, y), "Each neighbour group: [candidate in the matching transform]  [existing glyph]  [overlay: black = "
                    "shared ink, red = candidate only, blue = neighbour only, at the best +-1 px shift].  "
                    "pN = the share of existing glyphs whose own nearest neighbour is no closer.", font=f, fill=(60, 60, 60))
    y += 20
    ci, ca = cal["iou"]["identity"], cal["iou"]["any_transform"]
    d.text((20, y), f"Calibration at {n} px, IoU: inventory nearest-neighbour median {ci['nn_distribution']['median']:.2f} "
                    f"(as set) / {ca['nn_distribution']['median']:.2f} (any transform); p90 {ci['nn_distribution']['p90']:.2f} / "
                    f"{ca['nn_distribution']['p90']:.2f}; max {ci['nn_distribution']['max']:.2f} / {ca['nn_distribution']['max']:.2f}. "
                    f"Rightmost: true-size {n} px greyscale (candidate, then the three neighbours as set).",
           font=f, fill=(60, 60, 60))
    y += 28
    # calibration exemplars: the closest existing pairs, drawn the same way
    d.text((20, y), "For scale, closest existing pairs: as set; needing a rotation or mirror; and a designed mirror "
                    "twin (exempt from the threshold):", font=fb_, fill=0)
    y += 22
    x = 20
    twin = {"a": "strophe", "b": "anastro"}
    tk = [k for k in names if k in ("strophe", "anastro")]
    if len(tk) == 2:   # same scoring as the calibration: best transform with the +-1 px shift search
        tb = Bank(["anastro"], existing_masks[n], res["_raw"][n]["bank"].K)
        sc, _ = query(existing_masks[n]["strophe"], tb)
        ti = int(sc["iou"][:, 0].argmax())
        twin = {"a": "strophe", "b": "anastro", "score": float(sc["iou"][ti, 0]), "transform_of_a": TRANSFORMS[ti]}
    exemplars = [("as set", ci["closest_pair"]),
                 ("rotation/mirror", ca["closest_pair_needing_rotation_or_mirror"]),
                 ("designed mirror twin, exempt", twin)]
    for label, cp_ in exemplars:
        if "score" not in cp_:
            continue
        ka = [k for k in names if disp[k] == cp_["a"]][0]
        kb = [k for k in names if disp[k] == cp_["b"]][0]
        qa = centre(T_FUNCS[cp_["transform_of_a"]](existing_masks[n][ka]))
        nb = existing_masks[n][kb]
        # best shift for display
        best, bs = -1, (0, 0)
        for dy, dx in SHIFTS:
            q2 = np.roll(np.roll(qa, dy, 0), dx, 1)
            v = (q2 & nb).sum() / max(1, (q2 | nb).sum())
            if v > best:
                best, bs = v, (dy, dx)
        q2 = np.roll(np.roll(qa, bs[0], 0), bs[1], 1)
        img.paste(mask_img(q2, win, scale), (x, y))
        img.paste(mask_img(nb, win, scale), (x + cell + gap, y))
        img.paste(overlay_img(q2, nb, win, scale), (x + 2 * (cell + gap), y))
        d.text((x, y + cell + 4), f"{cp_['a']} ({cp_['transform_of_a']}) ~ {cp_['b']}   IoU {best:.2f}   [{label}]",
               font=f, fill=0)
        x += group_w + ggap + 40
    y += cell + 46
    for s in SETS:
        d.line([(20, y), (W - 20, y)], fill=(180, 180, 180))
        d.text((20, y + 8), f"set {s}", font=ft, fill=0)
        y += 36
        for a in ANCHORS:
            e = res["candidates"][n][s][a]
            sc_iou, sc_ncc, shift = e["_scores"]["iou"], e["_scores"]["ncc"], e["_shift"]
            cm = cand_masks[n][s][a]
            img.paste(mask_img(cm, win, scale), (20, y))
            d.text((20, y + cell + 4), a, font=fb_, fill=0)
            anyv = sc_iou.max(0)
            order = np.argsort(-anyv)[:3]
            x = left_w
            for rank, j in enumerate(order):
                ti = int(sc_iou[:, j].argmax())
                t = TRANSFORMS[ti]
                dy, dx = SHIFTS[shift[ti, j]]
                q = np.roll(np.roll(centre(T_FUNCS[t](cm)), dy, 0), dx, 1)
                nb = existing_masks[n][names[j]]
                img.paste(mask_img(q, win, scale), (x, y))
                img.paste(mask_img(nb, win, scale), (x + cell + gap, y))
                img.paste(overlay_img(q, nb, win, scale), (x + 2 * (cell + gap), y))
                p = pct_rank(cal["iou"]["any_transform"]["_nn"], float(anyv[j]))
                d.text((x, y + cell + 4), f"#{rank + 1} {disp[names[j]]}  IoU {anyv[j]:.2f} (p{p:.0f})  "
                                          f"NCC {sc_ncc[ti, j]:.2f}  {t}", font=f, fill=0)
                x += group_w + ggap
            # nearest sibling in the same set
            sib_best = None
            for b in ANCHORS:
                if b == a:
                    continue
                ib = Bank([b], {b: cand_masks[n][s][b]}, res["_raw"][n]["bank"].K)
                sc, sh = query(cm, ib)
                ti = int(sc["iou"][:, 0].argmax())
                v = float(sc["iou"][ti, 0])
                if sib_best is None or v > sib_best[0]:
                    sib_best = (v, b, ti, int(sh[ti, 0]), float(sc["ncc"][ti, 0]))
            v, b, ti, si, nv = sib_best
            dy, dx = SHIFTS[si]
            q = np.roll(np.roll(centre(T_FUNCS[TRANSFORMS[ti]](cm)), dy, 0), dx, 1)
            nb = cand_masks[n][s][b]
            img.paste(mask_img(q, win, scale), (x, y))
            img.paste(mask_img(nb, win, scale, ink=(90, 60, 140)), (x + cell + gap, y))
            img.paste(overlay_img(q, nb, win, scale), (x + 2 * (cell + gap), y))
            d.text((x, y + cell + 4), f"nearest in set: {b}  IoU {v:.2f}  NCC {nv:.2f}  {TRANSFORMS[ti]}",
                   font=f, fill=(90, 60, 140))
            x += group_w + ggap
            # true-size strip
            xx = x
            img.paste(grey_img(grey_cand[n][s][a], win), (xx, y + 10))
            xx += win + 12
            for j in order:
                img.paste(grey_img(grey_existing[n][names[j]], win), (xx, y + 10))
                xx += win + 6
            y += row_h
    img = img.crop((0, 0, W, y + 10))
    img.save(out)


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    cps, disp = load_morphemes()
    cands = load_candidates()
    composed_cands = {s: {a: compose_candidate(cands[s][a]) for a in ANCHORS} for s in SETS}

    from fontTools.ttLib import TTFont
    shipped_cmap = TTFont(str(SHIPPED_OTF)).getBestCmap()
    existing = [k for k, cp in cps.items() if cp in shipped_cmap and k in gs.GLYPHS]
    assert len(existing) == 93, len(existing)
    for k in ANCHORS:
        assert cps[k] not in shipped_cmap
    for s in SETS:
        for a in ANCHORS:
            disp[f"{s}|{a}"] = f"{s[0]}:{a}"

    # 1. scratch font through R's own builder: the 93 existing specs + the 12 candidates
    BUILD_DIR.mkdir(exist_ok=True)
    cand_cp = {}
    glyphs = {k: gs.GLYPHS[k] for k in existing}
    cmap = {k: cps[k] for k in existing}
    i = 0
    for s in SETS:
        for a in ANCHORS:
            key = f"{s}|{a}"
            glyphs[key] = composed_cands[s][a]
            cmap[key] = SCRATCH_CP0 + i
            cand_cp[(s, a)] = SCRATCH_CP0 + i
            i += 1
    saved = (bf.GLYPHS, bf.load_codepoint_map)
    bf.GLYPHS, bf.load_codepoint_map = glyphs, (lambda: dict(cmap))
    try:
        bf.build_font(SCRATCH_OTF, family="YOUSPEAK anchor audit scratch")
    finally:
        bf.GLYPHS, bf.load_codepoint_map = saved

    all_sizes = SIZES + SUPP_SIZES
    grey = {"font": {"existing": {}, "cand": {}}, "geom": {"existing": {}, "cand": {}}}
    checks = {"scratch_build_vs_shipped_font": {}, "geom_vs_font_binary_pixel_agreement": {},
              "svg_json_vs_composed_specs": {}}
    for n in all_sizes:
        f_ship = ImageFont.truetype(str(SHIPPED_OTF), n)
        f_scr = ImageFont.truetype(str(SCRATCH_OTF), n)
        ge, gc = {}, {s: {} for s in SETS}
        mism = []
        for k in existing:
            a1 = render_font(f_ship, cps[k], n)
            a2 = render_font(f_scr, cps[k], n)
            if not np.array_equal(a1 >= THRESH, a2 >= THRESH):
                mism.append(disp[k])
            ge[k] = a1
        for s in SETS:
            for a in ANCHORS:
                gc[s][a] = render_font(f_scr, cand_cp[(s, a)], n)
        grey["font"]["existing"][n], grey["font"]["cand"][n] = ge, gc
        checks["scratch_build_vs_shipped_font"][n] = {"glyphs_compared": len(existing),
                                                      "glyphs_with_any_binary_pixel_difference": mism}
        # cross-check renderer
        gge = {k: render_geom(contours_of(gs.GLYPHS[k]), n) for k in existing}
        ggc = {s: {a: render_geom(contours_of(composed_cands[s][a]), n) for a in ANCHORS} for s in SETS}
        grey["geom"]["existing"][n], grey["geom"]["cand"][n] = gge, ggc
        agree = []
        for k in existing:
            fa, ga = ge[k] >= THRESH, gge[k] >= THRESH
            u = (fa | ga).sum()
            agree.append(float((fa & ga).sum() / u) if u else 1.0)
        for s in SETS:
            for a in ANCHORS:
                fa, ga = gc[s][a] >= THRESH, ggc[s][a] >= THRESH
                u = (fa | ga).sum()
                agree.append(float((fa & ga).sum() / u) if u else 1.0)
        checks["geom_vs_font_binary_pixel_agreement"][n] = {
            "measure": "IoU between the FreeType and the supersampled-geometry binary renders of the same glyph, uncentred",
            **stats(agree)}

    # svg.json deliverables vs the composed specs (rendered large by the geometry rasteriser)
    for s in SETS:
        sj = json.loads((GLYPHS_ROOT / s / "glyphs.svg.json").read_text())
        checks["svg_json_vs_composed_specs"][s] = {}
        for a in ANCHORS:
            m1 = render_geom(svg_contours(sj[a]), 200, ss=2, c=204) >= THRESH
            m2 = render_geom(contours_of(composed_cands[s][a]), 200, ss=2, c=204) >= THRESH
            checks["svg_json_vs_composed_specs"][s][a] = {"pixels_differing_at_200px": int((m1 ^ m2).sum()),
                                                          "ink_pixels": int(m2.sum())}

    # 2. binarise + centre, then analyse with each renderer
    def prep(g):
        return centre(g >= THRESH)

    results = {}
    masks = {}
    checks["existing_glyphs_with_no_ink_after_binarising"] = {}
    for rname in ("font", "geom"):
        em, empties = {}, {}
        for n in all_sizes:
            em[n] = {}
            for k in existing:
                mk = prep(grey[rname]["existing"][n][k])
                if mk.any():
                    em[n][k] = mk
                else:      # vanishes when binarised: left out of the calibration and of the bank
                    empties.setdefault(n, []).append(disp[k])
        checks["existing_glyphs_with_no_ink_after_binarising"][rname] = empties
        cm = {n: {s: {a: prep(grey[rname]["cand"][n][s][a]) for a in ANCHORS} for s in SETS} for n in all_sizes}
        for n in all_sizes:
            for s in SETS:
                for a in ANCHORS:
                    assert cm[n][s][a].any(), (rname, n, s, a)
        masks[rname] = (em, cm)
        results[rname] = analyse(em, cm, all_sizes, disp)

    # 3. pictures (primary renderer): 32 px as asked, 16 px as a companion
    em, cm = masks["font"]
    draw_png(results["font"], em, cm, grey["font"]["existing"], grey["font"]["cand"], disp, n=32)
    draw_png(results["font"], em, cm, grey["font"]["existing"], grey["font"]["cand"], disp, n=16, scale=5,
             out=HERE / "neighbours_16px.png")

    # 4. JSON
    prim = results["font"]
    table = []
    for n in all_sizes:
        for s in SETS:
            for a in ANCHORS:
                for m in MEASURES:
                    for rg in ("identity", "any_transform"):
                        e = prim["candidates"][n][s][a][m][rg]
                        cal = prim["calibration"][n][m][rg]
                        table.append({
                            "set": s, "candidate": a, "size_px": n, "supplementary_size": n in SUPP_SIZES,
                            "measure": m, "regime": rg,
                            "nearest": e["nearest"], "score": e["score"], "transform": e["transform"],
                            "second": e["top5"][1]["glyph"], "second_score": e["top5"][1]["score"],
                            "third": e["top5"][2]["glyph"], "third_score": e["top5"][2]["score"],
                            "inventory_nn_median": cal["nn_distribution"]["median"],
                            "inventory_nn_p90": cal["nn_distribution"]["p90"],
                            "closest_existing_pair": f"{cal['closest_pair']['a']}~{cal['closest_pair']['b']}",
                            "closest_existing_pair_score": cal["closest_pair"]["score"],
                            "pct_rank_vs_inventory_nn": e["pct_rank_vs_inventory_nn"],
                            "exceeds_median": e["exceeds_inventory_median_nn"],
                            "exceeds_p90": e["exceeds_inventory_p90_nn"],
                            "exceeds_closest_existing_pair": e["exceeds_closest_existing_pair"],
                        })

    internal_table = []
    for n in all_sizes:
        for s in SETS:
            for row in prim["internal"][n][s]:
                for m in MEASURES:
                    r_ = row[m]
                    internal_table.append({
                        "set": s, "a": row["a"], "b": row["b"], "size_px": n, "supplementary_size": n in SUPP_SIZES,
                        "measure": m, "identity": r_["identity"], "any_transform": r_["any_transform"],
                        "transform": r_["transform"], "pct_rank_any_transform": r_["pct_rank_any_transform"],
                        "exceeds_p90_any": r_["exceeds_p90_any"],
                        "exceeds_closest_existing_pair_any": r_["exceeds_closest_existing_pair_any"]})

    def strip(o):
        if isinstance(o, dict):
            return {str(k): strip(v) for k, v in o.items() if not str(k).startswith("_")}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o

    # renderer cross-check summary: does the nearest neighbour / score move?
    xcheck = []
    for n in all_sizes:
        for s in SETS:
            for a in ANCHORS:
                for m in MEASURES:
                    for rg in ("identity", "any_transform"):
                        p = prim["candidates"][n][s][a][m][rg]
                        g = results["geom"]["candidates"][n][s][a][m][rg]
                        xcheck.append({"set": s, "candidate": a, "size_px": n, "measure": m, "regime": rg,
                                       "font_nearest": p["nearest"], "font_score": p["score"],
                                       "font_pct": p["pct_rank_vs_inventory_nn"],
                                       "geom_nearest": g["nearest"], "geom_score": g["score"],
                                       "geom_pct": g["pct_rank_vs_inventory_nn"]})
    geom_cal = {n: {m: {rg: {"nn_distribution": results["geom"]["calibration"][n][m][rg]["nn_distribution"],
                             "closest_pair": results["geom"]["calibration"][n][m][rg]["closest_pair"]}
                        for rg in ("identity", "any_transform")} for m in MEASURES} for n in all_sizes}

    out = {
        "about": "Confusability audit of candidate glyphs for the YOUSPEAK anchor particles mi: yu: yumi: mitakuyame: "
                 "(U+E17C-E17F). Written by an agent (an audit step of a workflow); it is evidence for the language's "
                 "owner, not a decision. Nothing in the repository was changed.",
        "method": {
            "existing_source": str(SHIPPED_OTF) + " via PIL ImageFont (FreeType), codepoints from script/morphemes.json",
            "candidate_source": "each set's specs.py, composed by R's glyph_specs_v1.compose_glyph() (in memory) and "
                                "outlined by R's build_font_v1.build_font() into " + str(SCRATCH_OTF) +
                                " (scratch, never installed), rendered by the same FreeType call",
            "sizes_px_per_em": SIZES, "supplementary_sizes_px_per_em": SUPP_SIZES,
            "canvas": "square of (2 x size + 4) px; em box centred; glyph then re-centred on its ink centroid",
            "binarise": f"grey >= {THRESH} of 255 (50 % coverage)",
            "measures": {
                "iou": "intersection over union of the binary masks",
                "ncc": f"zero-mean normalised cross-correlation (Pearson) of the binary masks after a Gaussian blur "
                       f"sigma {BLUR_SIGMA} px, over the whole fixed canvas (values comparable inside this audit only)",
            },
            "alignment": f"best of the {len(SHIFTS)} integer shifts within +-{SHIFT} px after centroid centring",
            "transforms": TRANSFORMS,
            "regimes": {
                "identity": "candidate as set, no rotation or mirror",
                "any_transform": "best over all 8 symmetries of the square; for existing pairs that are transforms "
                                 "of each other by design (see designed_twins) only their as-set score counts",
            },
            "designed_twins": {" ~ ".join(sorted(k)): v for k, v in DESIGNED_TWINS.items()},
            "pct_rank": "share (0-100) of the 93 existing glyphs whose own nearest-neighbour score, in the same "
                        "measure/regime/size, is <= the candidate's score. 100 = closer than every existing glyph is "
                        "to its own nearest neighbour.",
            "cross_check_renderer": "an independent supersampled (6x6) nonzero-winding rasteriser over the same composed "
                                    "outlines; the whole analysis is repeated with it (renderer_cross_check)",
        },
        "checks": checks,
        "calibration_existing_93": strip(prim["calibration"]),
        "existing_nearest_neighbours": prim["existing_nn"],
        "table": table,
        "internal_table": internal_table,
        "candidates_detail": strip(prim["candidates"]),
        "internal_within_set": prim["internal"],
        "renderer_cross_check": {"calibration_geom": geom_cal, "candidates": xcheck,
                                 "internal_within_set_geom": results["geom"]["internal"]},
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("wrote", OUT_JSON)
    print("wrote", OUT_PNG, "and", HERE / "neighbours_16px.png")

    # console summary
    for n in all_sizes:
        print(f"\n== {n} px ==")
        for m in MEASURES:
            for rg in ("identity", "any_transform"):
                c = prim["calibration"][n][m][rg]
                print(f"  calib {m:3s} {rg:13s} NN median {c['nn_distribution']['median']:.3f} "
                      f"p90 {c['nn_distribution']['p90']:.3f} max {c['nn_distribution']['max']:.3f}  "
                      f"closest {c['closest_pair']['a']}~{c['closest_pair']['b']} {c['closest_pair']['transform_of_a']}")
        for s in SETS:
            for a in ANCHORS:
                parts = []
                for m in MEASURES:
                    for rg in ("identity", "any_transform"):
                        e = prim["candidates"][n][s][a][m][rg]
                        flag = "!!" if e["exceeds_closest_existing_pair"] else ("! " if e["exceeds_inventory_p90_nn"] else "  ")
                        parts.append(f"{m}/{rg[:3]} {e['nearest']}:{e['score']:.2f} p{e['pct_rank_vs_inventory_nn']:.0f}{flag}")
                print(f"  {s[0]} {a:12s} " + " | ".join(parts))
            for row in prim["internal"][n][s]:
                print(f"     {s[0]} internal {row['a']}~{row['b']}: iou id {row['iou']['identity']:.2f} any "
                      f"{row['iou']['any_transform']:.2f} p{row['iou']['pct_rank_any_transform']:.0f}; ncc id "
                      f"{row['ncc']['identity']:.2f} any {row['ncc']['any_transform']:.2f} p{row['ncc']['pct_rank_any_transform']:.0f}")
    print("\nchecks:", json.dumps({k: v for k, v in checks.items() if k != 'geom_vs_font_binary_pixel_agreement'},
                                 ensure_ascii=False)[:1500])
    print("geom vs font:", json.dumps(checks["geom_vs_font_binary_pixel_agreement"]))


if __name__ == "__main__":
    main()
