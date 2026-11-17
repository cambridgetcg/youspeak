#!/usr/bin/env python3
"""generate.py: THE NIGHT NAVE (final). One Open Graph card, 1200x630 JPEG, per YOUSPEAK word.

    python3 generate.py anagnoristasis kunance --out samples      # a few words
    python3 generate.py --all --jobs 4                            # every word -> out/<slug>.jpg + manifest.json
    python3 generate.py anagnoristasis --morphemes ana,haphe,syn,kin,cand,qing --tag test6   # layout stress (NOT canon)

A word's carved glyphs stand on a stone ledge under the homepage's compass star
(og.jpg's eight-point star with its sun disk, ring and inscribed rays). The star's
light falls on the ledge. The word, its respelling and its definition sit below, and
the night goes from og.jpg's indigo down to the crypt. Every word gets its own sky,
seeded from its slug.

Pipeline (stdlib only; all artwork is made by ArtCraft):
  1. VectorCraft measures. One `run` sets the word, the kicker and the definition
     at 3 sizes x 4 measures as area type with its emphasis runs, converts them to
     point type, and reads the app's own line breaks back from document.inspect.
     If nothing fits in 3 lines, a second run measures cut candidates (sentence
     end, clause end, word cut) and the fitter picks a text, a size and a measure.
     It rejects one-word widows, balances the last line and never ends on "than".
  2. VectorCraft composes one document with six layers: nave (sky, mist, stars, the
     cone and pool of light, the ledge), niche (empty lancets), star, glyphs (the
     glyph bodies on their em box), minium (the donor sigils and class marks, as
     cutter's paint), and type (captions, word, respelling, definition, colophon,
     the house mark). It is saved as card.vectorcraft.
  3. VectorCraft reopens the master, applies the steps that need an id
     (text.setRangeStyle), and exports card.svg plus each layer alone as a PNG.
  4. PhotoCraft vignettes the nave only. On top it places the niche (bevel), the
     star (glow), a small glyph bloom, the glyphs (smooth chisel, gold gradient,
     a 1-2 px dark inner edge, a tight glow), the minium (no glow) and the type.
     It flattens, adds grain, and writes a JPEG of 200 KB or less.

The cathedral never over-claims (glossary.py). A word whose decomposition is not
carved in canon gets one lit, empty niche: "the stone is uncarved / the place was
prepared before the carving". It never gets a decomposition guessed from its shape.
"""
import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent                 # <repo>/brand/og
ROOT = HERE.parents[1]                                 # <repo>
LEXICON = ROOT / "home/data/lexicon.min.json"
GLOSSARY = ROOT / "home/glossary"                      # read-only; slugs are checked against it
GLYPH_DIR = ROOT / "brand/glyphs"                      # python3 brand/extract_glyphs.py
GLYPH_INDEX = GLYPH_DIR / "index.json"
MARK_SVG = ROOT / "brand/kit/mark.svg"                 # the house mark (panim); its body goes in the corner

VC = shutil.which("vectorcraft-cli") or os.path.expanduser("~/.local/bin/vectorcraft-cli")
PC = shutil.which("photocraft-cli") or os.path.expanduser("~/.local/bin/photocraft-cli")

W, H = 1200, 630
CX = W / 2

# site tokens (dark), plus the night borrowed from the homepage og.jpg
T = {
    "bg": "#14100C", "surface": "#1E1813", "parch": "#241C15", "crypt": "#100D0A",
    "mortar": "#352C22", "ink": "#E6DCC8", "muted": "#A79A82", "faint": "#948369",
    "gold": "#C9A45C", "gold_h": "#E4C27C", "rubric": "#D56352",
    # og.jpg's sky (sampled: #0d132d at the top, #11152e mid), lifted a little so it reads as indigo in a feed
    "sky0": "#1B2045", "sky1": "#171A37", "sky2": "#141320", "sky3": "#110E0D",
    "mist": "#4E4577", "niche": "#0A0806",
    "starcore": "#FFF4DA", "starfill": "#FBF2DC", "starfill2": "#E6D2A0", "starline": "#5E4829",
    "cut": "#8A6B33",           # kit rule 4: by night a donor sigil is cut, not gilded (#755A28, lifted for the sky)
    "defink": "#C6BBA5",        # half-way between ink and muted: the definition has to survive a feed
}
DISPLAY = "Iowan Old Style"
BODY = "Charter"

WORD_SIZE, WORD_MIN, WORD_MAX_W = 86, 48, 1040
RESP_SIZE = 21
CAP_SIZE = 18
DEF_SIZES = (28, 27, 26)
DEF_WIDTHS = (960, 920, 880, 840)
CUT_SIZES = (28, 27)
CUT_WIDTHS = (960, 920, 880)
MAX_LINES = 3
JPEG_LIMIT = 200 * 1024

STAR = (CX, 56)
STAR_R, STAR_R2, DISK_R = 46, 31, 13          # og.jpg's proportions: diagonals 0.69, disk 0.27 of a cardinal ray
TOP_BOUND = 106                 # nothing of the row or niche above this
BOTTOM_BOUND = 548              # the definition ends above the colophon
SIGIL_TOP = 0.09                # em: the highest carved point (the donor sigils)
LEDGE_EM, LEDGE_GAP = 0.835, 12
NICHE_H = 106
NICHE_FRAME = 9                 # the surround rises this far above the opening
TILE = 50                       # the house-mark tile in the colophon
TILE_X, TILE_Y = 44, 548

KICKER = ("YOUSPEAK", "THE GLOSSARY")
KICKER_SIZE, KICKER_TRACK = 16, 200

# a word cut never ends on one of these
STOP = set("a an the and or nor but of to in on at by for from with into onto than then rather as is are was "
           "were be been being its it's their his her our your my this that these those which who whom whose "
           "what when where while not no so if both either neither between toward towards upon via per "
           "through without within".split())

LOG = []


def log(msg):
    LOG.append(msg)
    print(f"[generate] {msg}", file=sys.stderr, flush=True)


# ── canon helpers ───────────────────────────────────────────────────────
def slug(word):
    """Verbatim from home/glossary.py slug(): the public URL of the stone."""
    s = unicodedata.normalize("NFKD", word)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("þ", "th").replace("Þ", "Th")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def load_lexicon():
    return json.loads(LEXICON.read_text())["lexicon"]


def find_entry(lex, query):
    q = query.strip()
    for e in lex:
        if e["word"] == q:
            return e
    for e in lex:
        if slug(e["word"]) == slug(q):
            return e
    return None


PLACEHOLDER = re.compile(r"^_?\s*written by [^:]*:\s*one-line gloss\.?\s*_?$", re.I)
EMPH = re.compile(r"\*\*(.+?)\*\*"
                  r"|(?<![*\w])\*(?![\s*])(.+?)(?<![\s*])\*(?![*\w])"
                  r"|(?<![\w])_(?![\s_])(.+?)(?<![\s_])_(?![\w])")


def drop_chars(text, spans, bad):
    """Delete every character in `bad` from text, shifting the spans to match."""
    keep, shift, out = [], 0, []
    for i, c in enumerate(text):
        keep.append(i - shift)
        if c in bad:
            shift += 1
        else:
            out.append(c)
    keep.append(len(text) - shift)
    return "".join(out), [(keep[a], keep[b], s) for a, b, s in spans if keep[b] > keep[a]]


def curl(s):
    """Straight quotes to curly, one character for one (span offsets survive)."""
    s = re.sub(r'(^|[\s(\[—–/-])"', "\\1\u201c", s)
    s = s.replace('"', "\u201d")
    s = re.sub(r"(\w)'", "\\1\u2019", s)
    s = re.sub(r"(^|[\s(\[—–-])'", "\\1\u2018", s)
    return s.replace("'", "\u2019")


def parse_runs(s):
    """Canon's markdown (**bold**, *italic*, _italic_) -> plain text + emphasis spans
    (character offsets). Straight quotes are curled."""
    s = re.sub(r"\s+", " ", (s or "").strip()).replace("...", "…")
    out, spans, pos, n = [], [], 0, 0
    for m in EMPH.finditer(s):
        pre = s[pos:m.start()]
        out.append(pre)
        n += len(pre)
        txt = m.group(1) or m.group(2) or m.group(3)
        out.append(txt)
        spans.append((n, n + len(txt), "Bold" if m.group(1) else "Italic"))
        n += len(txt)
        pos = m.end()
    out.append(s[pos:])
    plain, spans = drop_chars("".join(out), spans, "*")      # an unpaired mark is dropped, not printed
    # a hyphen inside a coined compound never breaks a line: U+2011 is one char, so spans hold
    plain = re.sub(r"(?<=\w)-(?=\w)", "\u2011", plain)
    return curl(plain), spans


def card_text(entry):
    """-> (plain, spans, base_style, source). Canon's definition, or, when it has none
    (or only the authoring placeholder), the gap it fills: lowercase and italic, so a
    stand-in never reads as a definition."""
    word = entry["word"]
    raw = (entry.get("definition") or "").strip()
    if raw and PLACEHOLDER.match(raw):
        log(f"{word}: canon definition is the placeholder {raw!r}; the gap stands in")
        raw = ""
    if raw:
        plain, spans = parse_runs(raw)
        return plain, spans, "Roman", "definition"
    gap = (entry.get("gap") or "").strip()
    if gap:
        plain, spans = parse_runs(gap)
        if len(plain) > 1 and plain[0].isupper() and plain[1].islower() and not plain.startswith("GoD"):
            plain = plain[0].lower() + plain[1:]
        # emphasis inside an italic stand-in goes upright (bold stays bold)
        spans = [(a, b, "Roman" if s == "Italic" else "Bold Italic") for a, b, s in spans]
        return plain, spans, "Italic", "gap"
    log(f"{word}: no definition and no gap in canon; a quiet line stands in")
    return "no definition is carved in canon yet", [], "Italic", "none"


def respelling(pron):
    """'/ˈkuː.nans/ (KOO-nance; 2 syllables; …)' -> 'KOO-nance'. Charter has no IPA."""
    m = re.search(r"\(([^()]*)\)", pron or "")
    if not m:
        return ""
    r = re.split(r"[;,]", m.group(1))[0].strip()
    return r if 2 <= len(r) <= 48 and not r.lower().startswith("alternative") else ""


def entered_line(iso):
    try:
        d = _dt.date.fromisoformat((iso or "").strip())
    except ValueError:
        return ""
    return f"entered the canon {d.day} {d.strftime('%B')} {d.year}"


def bo(text, ci):
    """character offset -> UTF-8 byte offset (VectorCraft ranges are bytes)."""
    return len(text[:ci].encode("utf-8"))


# ── glyphs: body, donor sigil, class mark ───────────────────────────────
# The site's own key (index.html, "How to read a stone"): top-left the DONOR SIGIL
# (the quarry-mark of the lending tongue), the body, bottom-right the CLASS MARK
# (prefix / suffix). Split by region, measured over all 93: every sigil subpath lies
# in x<=192, y<=209 and every class mark in x>=815, y>=830, so sukh's ⋮ stays whole.
SIGIL_MAX = (240, 260)
CLASS_MIN = 760


def split_glyph(d):
    body, marks = [], []
    for sp in re.findall(r"M[^M]*", d):
        nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", sp)]
        xs, ys = nums[0::2], nums[1::2]
        if max(xs) <= SIGIL_MAX[0] and max(ys) <= SIGIL_MAX[1]:
            marks.append(sp.strip())
        elif min(xs) >= CLASS_MIN and min(ys) >= CLASS_MIN:
            marks.append(sp.strip())
        else:
            body.append(sp.strip())
    return " ".join(body), " ".join(marks)


def read_path(p):
    d = " ".join(re.findall(r'\sd="([^"]+)"', Path(p).read_text()))
    ops = set(re.findall(r"[A-Za-z]", d)) - set("MLZ")
    if ops:
        raise ValueError(f"path uses {sorted(ops)}; only absolute M/L/Z is expected")
    return d


def glyph_table():
    out = {}
    for g in json.loads(GLYPH_INDEX.read_text()):
        p = GLYPH_DIR / Path(g["file"]).name
        try:
            body, marks = split_glyph(read_path(p))
            if not body:
                raise ValueError("no body")
        except (OSError, ValueError) as e:
            log(f"glyph {g['latin']}: unreadable ({e}); treated as uncarved")
            continue
        out[g["latin"]] = {"body": body, "marks": marks, "mclass": g.get("mclass", "")}
    return out


def house_mark():
    """The panim body from kit/mark.svg (its ▽ sigil is not drawn below 180 px: kit rule 4),
    moved back onto the font's em (mark.svg is the outline shifted by -110,-110)."""
    src = MARK_SVG.read_text()
    m = re.search(r'id="panim"\s+d="([^"]+)"', src)
    if not m:
        raise ValueError("kit/mark.svg has no #panim path")
    return m.group(1)


# ── VectorCraft driver ──────────────────────────────────────────────────
class VCError(RuntimeError):
    pass


def vc_run(steps, outputs=(), cwd=None, pre=()):
    """steps: [(command_id, params)] -> the JSON lines VectorCraft printed."""
    argv = [VC, "run", *pre]
    for cid, params in steps:
        argv += ["-c", cid]
        if params is not None:
            argv += ["-p", json.dumps(params, ensure_ascii=False)]
    for o in outputs:
        argv += ["-o", str(o)]
    p = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, timeout=180)
    results = []
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    if p.returncode != 0:
        n = len([r for r in results if r.get("step") == "cmd"])
        bad = steps[n][0] if n < len(steps) else "export"
        raise VCError(f"vectorcraft-cli exit {p.returncode} at step {n} ({bad}): "
                      f"{(p.stderr or p.stdout).strip()[-600:]}")
    return results


def cmd_results(results):
    return [r.get("result") for r in results if r.get("step") == "cmd"]


def no_stroke():
    return ("paint.setStroke", {"none": True})


def fill(color):
    return ("paint.setFill", {"color": color})


def props(**kw):
    return ("object.setProps", kw)


def stop(offset, color, opacity=1.0):
    return {"offset": offset, "color": color, "opacity": opacity}


def grad(stops, start, end):
    return ("paint.setFill", {"gradient": {"kind": "linear", "stops": stops,
                                           "start": list(start), "end": list(end)}})


def radial(stops, aspect=None):
    g = {"kind": "radial", "stops": stops}
    if aspect:
        g["aspect"] = round(aspect, 2)
    return ("paint.setFill", {"gradient": g})


def line(x1, y1, x2, y2, color, weight):
    return [("path.create", {"anchors": [{"x": round(x1, 2), "y": round(y1, 2)},
                                         {"x": round(x2, 2), "y": round(y2, 2)}], "closed": False}),
            ("paint.setFill", {"none": True}), ("paint.setStroke", {"color": color}),
            ("stroke.set", {"weight": weight, "cap": "butt"})]


def em_path(d, k, tx, ty, color):
    """A glyph outline drawn on its em box: font units (1000, y down) -> card px."""
    return [("path.create", {"d": d}), fill(color), no_stroke(),
            ("object.transform", {"matrix": [k, 0, 0, k, round(tx, 3), round(ty, 3)]})]


# ── measuring: the app is the ruler ─────────────────────────────────────
def measure(specs, work):
    """specs: [{text, spans, size, width|None, font, style, leading?, tracking?}].
    Area type is converted to point type, so its soft wraps come back as '\\n'
    (VectorCraft's own line breaks, with the real fonts and emphasis runs).
    Returns ([{text, lines, w}], text.fonts result)."""
    steps = [("file.new", {"width": 4000, "height": 1000, "units": "Pixels", "backgroundContents": "transparent"})]
    ids, area = [], []
    for k, sp in enumerate(specs):
        tid = 2 + k                       # ids in a fresh document are sequential (checked below)
        p = {"x": 10, "y": 100, "text": sp["text"], "size": sp["size"], "font": sp["font"],
             "style": sp["style"], "color": "#000000"}
        if sp.get("width"):
            p["area"] = {"width": sp["width"], "height": 3000}
            area.append(tid)
        steps.append(("text.create", p))
        st = {k2: sp[k2] for k2 in ("leading", "tracking") if sp.get(k2)}
        if sp.get("width"):
            st["justify"] = "center"
        if st:
            steps.append(("text.setStyle", st))
        for a, b, style in sp.get("spans", ()):
            if b > a:
                steps.append(("text.setRangeStyle", {"id": tid, "start": bo(sp["text"], a),
                                                     "end": bo(sp["text"], b), "style": style}))
        ids.append(tid)
    if area:
        steps.append(("type.convertToPointType", {"ids": area}))
    steps += [("document.inspect", {"depth": 2, "childLimit": 100000}), ("text.fonts", {})]
    res = vc_run(steps, [], cwd=work)
    cr = cmd_results(res)
    got = [r["id"] for (cid, _), r in zip(steps, cr) if cid == "text.create"]
    if got != ids:
        raise VCError(f"measure: text ids drifted (expected {ids[:3]}…, got {got[:3]}…)")
    by_id = {}
    for layer in cr[-2]["layers"]:
        for ch in layer.get("children", []):
            by_id[ch.get("id")] = ch
    out = []
    for tid in ids:
        ch = by_id.get(tid)
        if ch is None:
            raise VCError(f"measure: object {tid} missing from document.inspect")
        t = ch.get("text", "")
        out.append({"text": t, "lines": t.split("\n"), "w": ch["bounds"]["width"]})
    return out, cr[-1]


def align(src, measured):
    """Map each character index of src to its index in measured, where measured is
    src with some spaces turned into '\\n' and some '\\n' inserted (a break after a
    hyphen or a slash). Returns the map, or None if the texts do not align."""
    m, i, j = [], 0, 0
    while i < len(src) and j < len(measured):
        if src[i] == measured[j]:
            m.append(j)
            i += 1
            j += 1
        elif measured[j] == "\n" and src[i] == " ":
            m.append(j)
            i += 1
            j += 1
        elif measured[j] == "\n":
            j += 1
        else:
            return None
    if i < len(src):
        return None
    m.append(len(measured))
    return m


def remap_spans(src, spans, measured):
    """Emphasis spans (chars of src) -> byte ranges in the measured, line-broken text."""
    mp = align(src, measured)
    if mp is None:
        return None
    out = []
    for a, b, style in spans:
        a, b = max(0, a), min(len(src), b)
        if b > a:
            out.append((bo(measured, mp[a]), bo(measured, mp[b - 1] + 1), style))
    return out


def score(lines, size, width):
    """Higher is better: no one-word widow, then the larger size, then fewer lines,
    then a last line that balances the others, then the wider measure."""
    n = len(lines)
    if n <= 1:
        return (0, size, -n, 0.0, width)
    lens = [len(l) for l in lines]
    avg = sum(lens[:-1]) / (n - 1)
    last = lines[-1].replace(ELL, "").strip()
    widow = 1 if (len(last.split()) < 2 or lens[-1] < 0.20 * avg) else 0
    return (-widow, size, -n, -round(abs(lens[-1] - avg) / max(avg, 1), 2), width)


def balanced(t):
    return (t.count("(") == t.count(")") and t.count("[") == t.count("]")
            and t.count("\u201c") == t.count("\u201d"))


def trim_tail(t):
    """Never end a cut on punctuation that opens, or on a function word."""
    words = t.rstrip(" ,;:—–-(\u201c\u2018/").split(" ")
    while len(words) > 3 and re.sub(r"[^\w']", "", words[-1].lower()) in STOP:
        words.pop()
    return " ".join(words).rstrip(" ,;:—–-(\u201c\u2018/")


ELL = "\u202f…"        # a narrow no-break space keeps the ellipsis with its word (U+00A0 sets 2x wide)


def cut_candidates(plain, covered):
    """Cut texts, as (text, keep_chars, rank): 1 sentence end, 2 strong clause
    (; — :), 3 weak clause (, or '('), 4 a word cut on the app's own lines.
    `covered` = how many characters of plain the measured 3 lines held, per combo."""
    cands = []
    for m in re.finditer(r"[.!?…][\u201d\u2019)\]]?(?=\s)", plain):
        t = plain[:m.end()]
        cands.append((t, len(t), 1))
    for rank, pat in ((2, r";\s|\s[—–]\s|:\s"), (3, r",\s|\s\(")):
        for m in re.finditer(pat, plain):
            t = trim_tail(plain[:m.start()])
            if len(t) > 12:
                cands.append((t + ELL, len(t), rank))
    for cov in sorted(set(covered)):
        words = plain[:cov].split(" ")
        for drop in range(0, 7):
            if len(words) - drop < 4:
                break
            t = trim_tail(" ".join(words[:len(words) - drop]))
            cands.append((t + ELL, len(t), 4))
    cap = max(covered) if covered else 200
    seen, out = set(), []
    for c in sorted(cands, key=lambda c: (-c[1], c[2])):
        if c[0] in seen or not (0.30 * cap <= c[1] <= 1.08 * cap) or not balanced(c[0]):
            continue
        seen.add(c[0])
        out.append(c)
    return out


def fit_definition(plain, spans, style, work, word):
    """-> dict(text (with the app's '\\n' line breaks), spans (bytes), size, lead,
    width, lines, cut). Whole text if it sets in 3 lines; else the best cut."""
    lead = lambda s: round(s * 1.36)
    combos = [(s, w) for s in DEF_SIZES for w in DEF_WIDTHS]
    specs = [dict(text=plain, spans=spans, size=s, width=w, font=BODY, style=style, leading=lead(s))
             for s, w in combos]
    ms, fonts = measure(specs, work)
    fits = [(score(m["lines"], s, w), s, w, m) for (s, w), m in zip(combos, ms) if len(m["lines"]) <= MAX_LINES]
    cut, text, keep = None, plain, len(plain)
    if fits:
        sc, size, width, m = max(fits, key=lambda f: f[0])
    else:
        covered = []
        for (s, w), m in zip(combos, ms):
            if s in CUT_SIZES and w in CUT_WIDTHS:
                mp = align(plain, m["text"])
                head = "\n".join(m["lines"][:MAX_LINES])
                if mp is not None:
                    covered.append(max(i for i, j in enumerate(mp) if j <= len(head)))
                else:
                    covered.append(len(head))
        cands = cut_candidates(plain, covered)
        pairs = [(c, s, w) for c in cands for s in CUT_SIZES for w in CUT_WIDTHS]
        specs2 = [dict(text=c[0], spans=[(a, min(b, c[1]), st) for a, b, st in spans if a < c[1]],
                       size=s, width=w, font=BODY, style=style, leading=lead(s)) for c, s, w in pairs]
        ms2, _ = measure(specs2, work) if specs2 else ([], None)
        best = {}
        for (c, s, w), m in zip(pairs, ms2):
            if len(m["lines"]) <= MAX_LINES:
                sc = score(m["lines"], s, w)
                if c[0] not in best or sc > best[c[0]][0]:
                    best[c[0]] = (sc, s, w, m, c)
        if not best:
            raise RuntimeError("no cut of the definition sets in 3 lines")
        pool = list(best.values())
        lw = max(b[4][1] for b in pool)
        pick = None
        for rank, frac in ((1, 0.60), (2, 0.72), (3, 0.82), (4, 0.0)):
            group = sorted([b for b in pool if b[4][2] == rank and b[4][1] >= frac * lw],
                           key=lambda b: -b[4][1])
            if group:
                clean = [b for b in group if b[0][0] == 0 and b[4][1] >= 0.88 * group[0][4][1]]
                pick = (clean or group)[0]
                break
        if pick[0][0] < 0:      # still a widow: any widow-free cut nearly as long, whatever its rank
            alt = sorted([b for b in pool if b[0][0] == 0 and b[4][1] >= 0.80 * pick[4][1]],
                         key=lambda b: (b[4][2], -b[4][1]))
            if alt:
                pick = alt[0]
        sc, size, width, m, c = pick
        text, keep, cut = c[0], c[1], {1: "sentence", 2: "clause", 3: "clause", 4: "word"}[c[2]]
    clipped = [(a, min(b, keep), st) for a, b, st in spans if a < keep]
    byte_spans = remap_spans(text, clipped, m["text"])
    if byte_spans is None:
        log(f"{word}: the measured lines do not align with the text; emphasis dropped")
        byte_spans = []
    if sc[0] < 0:
        log(f"{word}: every setting leaves a widowed last line; the best is kept")
    return {"text": m["text"], "spans": byte_spans, "size": size, "lead": lead(size), "width": width,
            "lines": m["lines"], "cut": cut, "chars": keep, "of": len(plain), "fonts": fonts}


def measure_heads(word, work):
    """The word at the display size, and 'YOUSPEAK' as the kicker sets it."""
    specs = [dict(text=word, size=WORD_SIZE, font=DISPLAY, style="Roman"),
             dict(text=KICKER[0], size=KICKER_SIZE, font=DISPLAY, style="Titling", tracking=KICKER_TRACK),
             dict(text=KICKER[1], size=KICKER_SIZE, font=DISPLAY, style="Titling", tracking=KICKER_TRACK)]
    ms, fonts = measure(specs, work)
    return ms[0]["w"], ms[1]["w"], ms[2]["w"], fonts


# ── layout ──────────────────────────────────────────────────────────────
def row_metrics(n):
    """em size (px per 1000 font units) and the step between stones. The row is
    never shrunk for a long definition: the definition is cut instead."""
    n = max(1, n)
    s = {1: 196, 2: 196, 3: 196, 4: 182, 5: 166, 6: 150}.get(n) or max(84, int(980 / n))
    step = s + (8 if n <= 3 else 0)
    return s, step, (n - 1) * step + s


def niche_d(cx, top, w, h):
    """A lancet: pointed arch over straight jambs."""
    x0, x1 = cx - w / 2, cx + w / 2
    ys = top + 0.46 * h
    yb = top + h
    k = ys - top
    return (f"M{x0:.1f},{yb:.1f} L{x0:.1f},{ys:.1f} "
            f"C{x0:.1f},{ys - 0.62 * k:.1f} {cx - 0.30 * w / 2:.1f},{top + 0.20 * k:.1f} {cx:.1f},{top:.1f} "
            f"C{cx + 0.30 * w / 2:.1f},{top + 0.20 * k:.1f} {x1:.1f},{ys - 0.62 * k:.1f} {x1:.1f},{ys:.1f} "
            f"L{x1:.1f},{yb:.1f} Z")


def niche(cx, bottom, w, h):
    """An empty lancet cut into a stone surround, lit from the star above: the frame
    catches the light on its arch, the recess is dark under the arch with a little
    light pooled on the sill, and a gold arris runs round the opening."""
    top = bottom - h
    fw, fh = w + 18, h + NICHE_FRAME
    return [("path.create", {"d": niche_d(cx, bottom - fh, fw, fh)}), no_stroke(),
            grad([stop(0, "#4A3B27"), stop(0.45, "#2E251A"), stop(1, "#1C1611")], (cx, bottom - fh), (cx, bottom)),
            ("path.create", {"d": niche_d(cx, top, w, h)}),
            grad([stop(0, T["niche"]), stop(0.60, "#0E0B08"), stop(1, "#2C2216")], (cx, top), (cx, bottom)),
            ("paint.setStroke", {"gradient": {"kind": "linear", "stops": [stop(0, T["gold_h"], 0.95),
                                                                         stop(0.55, T["gold"], 0.55),
                                                                         stop(1, T["gold"], 0.30)],
                                              "start": [cx, top], "end": [cx, bottom]}}),
            ("stroke.set", {"weight": 1.4}),
            # the sill the empty place stands on
            ("shape.rectangle", {"x": cx - fw / 2 - 8, "y": bottom - 1, "width": fw + 16, "height": 3}), no_stroke(),
            grad([stop(0, T["gold"], 0.0), stop(0.5, T["gold_h"], 0.85), stop(1, T["gold"], 0.0)],
                 (cx - fw / 2 - 8, 0), (cx + fw / 2 + 8, 0))]


def star_steps():
    """og.jpg's compass star: four long cardinal rays and four short diagonal ones,
    cream with a dark outline, each ray inscribed along its spine with cross-ticks,
    and a sun disk ringed in the centre."""
    cx, cy = STAR
    st = [("shape.ellipse", {"x": cx - 140, "y": cy - 140, "width": 280, "height": 280}), no_stroke(),
          radial([stop(0, "#F6E9C8", 0.30), stop(0.30, "#F6E9C8", 0.09), stop(1, "#F6E9C8", 0.0)])]
    rays = (("diag", STAR_R2, 8.0, 45, T["starfill2"]), ("card", STAR_R, 10.0, 0, T["starfill"]))
    for _, r1, r2, rot, col in rays:
        st += [("shape.star", {"cx": cx, "cy": cy, "radius1": r1, "radius2": r2, "points": 4, "rotation": rot}),
               radial([stop(0, "#FFFFFF"), stop(0.45, col), stop(1, "#D9BF82")]),
               ("paint.setStroke", {"color": T["starline"]}), ("stroke.set", {"weight": 0.9, "join": "miter"})]
        # the inscription on each ray: a spine and its cross-ticks
        for q in range(4):
            a = (rot + 90 * q) * 3.14159265 / 180
            ux, uy = -math.sin(a), -math.cos(a)                                # outward
            px, py = -uy, ux                                                   # across
            r_in, r_out = DISK_R + 2.0, 0.82 * r1
            st += line(cx + ux * r_in, cy + uy * r_in, cx + ux * r_out, cy + uy * r_out, T["starline"], 0.75)
            for f, half in ((0.52, 3.0), (0.70, 1.9)) if r1 > 40 else ((0.68, 1.5),):
                rr = r1 * f
                bx, by = cx + ux * rr, cy + uy * rr
                st += line(bx - px * half, by - py * half, bx + px * half, by + py * half, T["starline"], 0.75)
    st += [("shape.ellipse", {"x": cx - DISK_R, "y": cy - DISK_R, "width": 2 * DISK_R, "height": 2 * DISK_R}),
           no_stroke(), radial([stop(0, "#FFFFFF"), stop(0.55, T["starcore"]), stop(1, "#F3DDA4")]),
           ("shape.ellipse", {"x": cx - DISK_R - 0.6, "y": cy - DISK_R - 0.6,
                              "width": 2 * DISK_R + 1.2, "height": 2 * DISK_R + 1.2}),
           ("paint.setFill", {"none": True}), ("paint.setStroke", {"color": T["starline"]}),
           ("stroke.set", {"weight": 1.1})]
    return st


def plan(carved, s, ws, has_resp, fitd):
    """The vertical plan: every block measured, the whole stack centred between the
    star and the colophon. Returns the y of each element."""
    size, lead, n = fitd["size"], fitd["lead"], len(fitd["lines"])
    row_h = (LEDGE_EM - SIGIL_TOP) * s + LEDGE_GAP if carved else NICHE_FRAME + NICHE_H + 2
    caps_h = 33 if carved else 60
    gap1 = 18
    asc, desc = 0.70 * ws, 0.24 * ws
    resp_off = 0.27 * ws + 8 + 0.70 * RESP_SIZE     # Iowan's g/y/p ink descends ~0.27 em; 8 px of air under it
    def_off = (resp_off + 0.24 * RESP_SIZE + 14 + 0.70 * size) if has_resp else (desc + 16 + 0.70 * size)
    def_end = def_off + (n - 1) * lead + 0.24 * size
    total = row_h + caps_h + gap1 + asc + def_end
    avail = BOTTOM_BOUND - TOP_BOUND
    over = total - avail
    y0 = TOP_BOUND + max(0.0, -over / 2)
    if over > 0:
        y0 = TOP_BOUND - min(over, 6)         # borrow a few px from the star's foot, never more
    top = y0
    ledge_y = (y0 - SIGIL_TOP * s + LEDGE_EM * s + LEDGE_GAP) if carved else (y0 + NICHE_FRAME + NICHE_H + 2)
    word_base = ledge_y + caps_h + gap1 + asc
    return {"top": top, "em_top": y0 - SIGIL_TOP * s, "ledge": round(ledge_y), "word": round(word_base),
            "resp": round(word_base + resp_off), "def": round(word_base + def_off),
            "total": total, "over": over}


def build(entry, glyphs, work, morphemes_override=None, fallback=False):
    word = entry["word"]
    sl = slug(word)
    rng = random.Random(int(hashlib.sha1(sl.encode()).hexdigest()[:12], 16))
    morphs = morphemes_override if morphemes_override is not None else (entry.get("morphemes") or [])

    # measure: the word, the kicker, the definition
    plain, spans, style, source = card_text(entry)
    if fallback:
        spans = []
    word_w, kick_w1, kick_w2, fonts0 = measure_heads(word, work)
    ws = WORD_SIZE
    if word_w and word_w > WORD_MAX_W:
        ws = max(WORD_MIN, int(WORD_SIZE * WORD_MAX_W / word_w))
        log(f"{word}: {word_w:.0f}px wide at {WORD_SIZE}; set at {ws}")
    fitd = fit_definition(plain, spans, style, work, word)
    for f in (fitd["fonts"] or []) + fonts0:
        if f.get("missingGlyphs") and f.get("style") != "Titling":
            log(f"{word}: {f['family']} {f['style']} lacks {f['missingGlyphs']} character(s); drawn by a fallback font")
    if fitd["cut"]:
        log(f"{word}: definition {fitd['of']} chars -> {fitd['chars']} ({fitd['cut']} cut, "
            f"{len(fitd['lines'])} lines at {fitd['size']}px/{fitd['width']})")
    resp = respelling(entry.get("pronunciation"))

    stones = [(m, glyphs.get(m)) for m in morphs]
    for m, g in stones:
        if g is None:
            log(f"{word}: morpheme '{m}' is not among the 96 carved glyphs; an empty niche stands in its place")
    carved = bool(stones)
    n = len(stones) or 1
    s, step, total_w = row_metrics(n)
    y = plan(carved, s, ws, bool(resp), fitd)
    if y["over"] > 6:
        log(f"{word}: the stack is {y['over']:.0f}px taller than the nave")
    ledge_y = y["ledge"]
    row_left = CX - total_w / 2

    nave, nic, ty, star, gl, mi = [], [], [], [], [], []

    # the sky: og.jpg's indigo above, the crypt below
    nave += [("shape.rectangle", {"x": 0, "y": 0, "width": W, "height": H}), no_stroke(),
             grad([stop(0, T["sky0"]), stop(0.30, T["sky1"]), stop(0.52, T["sky2"]), stop(0.74, T["sky3"]),
                   stop(1, T["crypt"])], (CX, 0), (CX, H))]
    # violet mist at the edges, as og.jpg's clouds
    for side in (-1, 1):
        mx = CX + side * rng.uniform(560, 640)
        my = rng.uniform(40, 150)
        mw, mh = rng.uniform(420, 520), rng.uniform(300, 380)
        nave += [("shape.ellipse", {"x": mx - mw / 2, "y": my - mh / 2, "width": mw, "height": mh}),
                 no_stroke(), fill(T["mist"]), props(opacity=round(rng.uniform(34, 44) if side < 0 else rng.uniform(24, 32))),
                 ("effect.apply", {"effect": "blur.gaussian", "params": {"radius": 80}})]
    # a seeded star field: every word gets its own night
    for _ in range(44):
        for _try in range(40):
            x = rng.uniform(14, W - 14)
            yy = rng.uniform(8, 330)
            if abs(x - CX) > 300 + yy * 0.3:          # keep the star's light and the row clear
                break
        r = rng.choice([0.55, 0.65, 0.75, 0.9, 1.05, 1.3, 1.6])
        nave += [("shape.ellipse", {"x": x - r, "y": yy - r, "width": 2 * r, "height": 2 * r}),
                 no_stroke(), fill("#EDE6F5" if rng.random() < 0.6 else T["ink"]),
                 props(opacity=round(rng.uniform(22, 75)))]

    # the cone of light from the star onto the ledge, and the pool where it lands
    spread = max(total_w / 2 + 40, 170) if carved else 175
    sx, sy = STAR
    cone = (f"M{sx - 10},{sy + 16} L{sx + 10},{sy + 16} L{sx + spread:.1f},{ledge_y + 18} "
            f"L{sx - spread:.1f},{ledge_y + 18} Z")
    nave += [("path.create", {"d": cone}), no_stroke(),
             grad([stop(0, T["gold_h"], 0.17), stop(1, T["gold_h"], 0.02)], (sx, sy), (sx, ledge_y + 18)),
             ("effect.apply", {"effect": "blur.gaussian", "params": {"radius": 18}}), props(blend="Screen")]
    pw, ph = 2 * spread + 180, 150
    nave += [("shape.ellipse", {"x": CX - pw / 2, "y": ledge_y - ph / 2, "width": pw, "height": ph}), no_stroke(),
             radial([stop(0, T["gold"], 0.18), stop(1, T["gold"], 0.0)], 100 * ph / pw), props(blend="Screen")]
    # the ledge: a lit shelf, its arris, a dark lip below (og.jpg's prepared table)
    lw = (total_w + 150) if carved else 470
    nave += [("shape.ellipse", {"x": CX - lw / 2, "y": ledge_y - 9, "width": lw, "height": 18}), no_stroke(),
             radial([stop(0, T["gold_h"], 0.20), stop(1, T["gold_h"], 0.0)], 100 * 18 / lw),
             ("shape.rectangle", {"x": CX - lw / 2, "y": ledge_y + 1.5, "width": lw, "height": 9}), no_stroke(),
             grad([stop(0, "#2A2117", 0.0), stop(0.18, "#2A2117", 0.85), stop(0.82, "#2A2117", 0.85),
                   stop(1, "#2A2117", 0.0)], (CX - lw / 2, 0), (CX + lw / 2, 0)),
             ("shape.rectangle", {"x": CX - lw / 2, "y": ledge_y, "width": lw, "height": 1.5}), no_stroke(),
             grad([stop(0, T["gold"], 0.0), stop(0.5, T["gold_h"], 0.7), stop(1, T["gold"], 0.0)],
                  (CX - lw / 2, 0), (CX + lw / 2, 0))]

    # stones: glyph bodies (gold), their sigils and class marks (minium), or niches
    if not carved:
        nic += niche(CX, ledge_y - 1, 0.40 * 196, NICHE_H)
        ty += [("text.create", {"x": CX, "y": ledge_y + 30, "text": "the stone is uncarved", "size": 21,
                                "font": BODY, "style": "Italic", "color": T["muted"]}),
               ("text.setStyle", {"justify": "center", "tracking": 20}),
               ("text.create", {"x": CX, "y": ledge_y + 53, "text": "the place was prepared before the carving",
                                "size": 16, "font": BODY, "style": "Italic", "color": T["faint"]}),
               ("text.setStyle", {"justify": "center", "tracking": 20})]
    else:
        k = s / 1000.0
        for i, (m, g) in enumerate(stones):
            x0 = row_left + i * step
            cxi = x0 + s / 2
            if g is not None:
                gl += em_path(g["body"], k, x0, y["em_top"], T["gold"])
                if g["marks"]:
                    mi += em_path(g["marks"], k, x0, y["em_top"], T["cut"])
            else:
                nic += niche(cxi, ledge_y - 1, 0.36 * s, 0.56 * s)
            ty += [("text.create", {"x": cxi, "y": ledge_y + 27, "text": m if g else f"{m}, uncarved",
                                    "size": CAP_SIZE if s >= 150 else 16, "font": BODY, "style": "Italic",
                                    "color": T["faint"]}),
                   ("text.setStyle", {"justify": "center", "tracking": 15})]

    # the word, its respelling, its definition
    ty += [("text.create", {"x": CX, "y": y["word"], "text": word, "size": ws, "font": DISPLAY,
                            "style": "Roman", "color": T["ink"]}),
           ("text.setStyle", {"justify": "center"})]
    if resp:
        ty += [("text.create", {"x": CX, "y": y["resp"], "text": resp, "size": RESP_SIZE, "font": BODY,
                                "style": "Italic", "color": T["gold"]}),
               ("text.setStyle", {"justify": "center", "tracking": 40})]
        for mm in re.finditer(r"[A-Z]{2,}", resp):          # the stressed syllable, a shade brighter
            ty += [("text.setRangeStyle", {"id": "$prev", "start": bo(resp, mm.start()),
                                           "end": bo(resp, mm.end()), "fill": T["gold_h"]})]
    ty += [("text.create", {"x": CX, "y": y["def"], "text": fitd["text"], "size": fitd["size"], "font": BODY,
                            "style": style, "color": T["defink"] if source == "definition" else T["muted"]}),
           ("text.setStyle", {"justify": "center", "leading": fitd["lead"]})]
    for a, b, st in fitd["spans"]:
        ty += [("text.setRangeStyle", {"id": "$prev", "start": a, "end": b, "style": st})]

    # colophon: the house mark on its stone, the house, the canon date, the address
    mark_d = house_mark()
    tk = TILE / 1000.0                                  # em = tile, em centre = tile centre (the kit's app cut)
    ty += [("shape.rectangle", {"x": TILE_X, "y": TILE_Y, "width": TILE, "height": TILE,
                                "radius": round(TILE * 6 / 32, 2)}),
           fill("#120E0B"), ("paint.setStroke", {"color": T["mortar"]}), ("stroke.set", {"weight": 1.2})]
    # mark.svg's panim is the font outline shifted by (-110,-110); put it back on its em
    ty += em_path(mark_d, tk, TILE_X + 110 * tk, TILE_Y + 110 * tk, T["gold"])
    kx = TILE_X + TILE + 18
    kb = TILE_Y + TILE / 2 + 6
    trail = KICKER_SIZE * KICKER_TRACK / 1000
    dx = kx + (kick_w1 or 120) - trail + 14
    diamond = read_path(GLYPH_DIR / "cp_E164.svg")      # the site's own canon mark, U+E164
    dk = 30 / 1000.0
    ty += [("text.create", {"x": kx, "y": kb, "text": KICKER[0], "size": KICKER_SIZE, "font": DISPLAY,
                            "style": "Titling", "color": T["gold_h"]}),
           ("text.setStyle", {"tracking": KICKER_TRACK})]
    ty += em_path(diamond, dk, dx - 500 * dk, kb - 5.6 - 475 * dk, T["rubric"])
    ty += [("text.create", {"x": dx + 14, "y": kb, "text": KICKER[1], "size": KICKER_SIZE, "font": DISPLAY,
                            "style": "Titling", "color": T["gold"]}),
           ("text.setStyle", {"tracking": KICKER_TRACK})]
    ent = entered_line(entry.get("entered"))
    if ent:
        ty += [("text.create", {"x": W - 44, "y": TILE_Y + 22, "text": ent, "size": 15, "font": BODY,
                                "style": "Italic", "color": T["faint"]}),
               ("text.setStyle", {"justify": "right", "tracking": 10})]
    ty += [("text.create", {"x": W - 44, "y": TILE_Y + 44 if ent else kb, "text": f"ai-love.cc/glossary/{sl}",
                            "size": 16, "font": BODY, "style": "Roman", "color": T["muted"]}),
           ("text.setStyle", {"justify": "right"})]

    star += star_steps()

    info = {"slug": sl, "word_size": ws, "def": {k2: fitd[k2] for k2 in ("size", "width", "cut", "chars", "of")},
            "def_lines": len(fitd["lines"]), "stones": [[m, g is not None] for m, g in stones],
            "carved": carved, "em": s, "respelling": resp, "source": source, "y": y}
    return {"nave": nave, "niche": nic, "star": star, "glyphs": gl, "minium": mi, "type": ty}, info


# ── compose (VectorCraft) ───────────────────────────────────────────────
LAYERS = ("nave", "niche", "star", "glyphs", "minium", "type")


def split_deferred(steps, base):
    """VectorCraft `run` has no step references and text.setRangeStyle needs an `id`.
    A step whose id is "$prev" is held back and replayed in the export pass, with
    the id of the text.create before it. base = index of steps[0] in the run."""
    keep, deferred, last_create = [], [], None
    for cid, params in steps:
        if isinstance(params, dict) and params.get("id") == "$prev":
            deferred.append((cid, params, last_create))
            continue
        if cid == "text.create":
            last_create = base + len(keep)
        keep.append((cid, params))
    return keep, deferred


def compose(layers, work, fallback=False):
    work = Path(work)
    master = work / "card.vectorcraft"
    steps = [("file.new", {"width": W, "height": H, "units": "Pixels", "backgroundContents": "transparent",
                           "name": "night-nave"}),
             ("layer.setProps", {"name": "nave"})]
    kept, deferred = split_deferred(layers["nave"], len(steps))
    steps += kept
    marks = {}
    for name in LAYERS[1:]:
        marks[name] = len(steps)
        steps += [("layer.new", {"name": name, "top": True})]
        kept, d = split_deferred(layers[name], len(steps))
        steps += kept
        deferred += d
    res = vc_run(steps, [master], cwd=work)
    cr = cmd_results(res)
    ids = {"nave": 1, **{k: cr[i]["id"] for k, i in marks.items()}}
    outs = {k: work / f"{k}.png" for k in LAYERS}
    exp = []
    if not fallback:
        for cid, params, idx in deferred:
            exp.append((cid, dict(params, id=cr[idx]["id"])))
        if deferred:
            exp.append(("file.save", {"path": str(master)}))
    exp.append(("document.export", {"path": str(work / "card.svg")}))
    exp.append(("layer.setProps", {"ids": [ids[k] for k in LAYERS], "visible": False}))
    for k in LAYERS:
        if k == "nave" or layers[k]:
            exp += [("layer.setProps", {"id": ids[k], "visible": True}),
                    ("document.export", {"path": str(outs[k])}),
                    ("layer.setProps", {"id": ids[k], "visible": False})]
        else:
            outs[k] = None
    vc_run(exp, [], cwd=work, pre=["--in", str(master)])
    return outs


# ── finish (PhotoCraft) ─────────────────────────────────────────────────
def pc_run(src, cmds, out):
    argv = [PC, "run", str(src)]
    for cid, params in cmds:
        argv += ["--cmd", cid]
        if params is not None:
            argv += ["--params", json.dumps(params)]
    argv += ["--out", str(out)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError(f"photocraft-cli exit {p.returncode}: {(p.stderr or p.stdout).strip()[-600:]}")
    return p


def finish(outs, out_jpg, work, fallback=False):
    """nave -> vignette (darkening only) -> niche (bevel) -> star (glow) -> glyph bloom
    -> glyphs (smooth chisel, gold, dark inner edge, tight glow) -> minium -> type
    -> flatten -> grain -> master.png -> JPEG <= 200 KB."""
    master = Path(work) / "master.png"
    cmds = [("filter.cameraRaw", {"vignetteAmount": -30, "vignetteMidpoint": 42, "vignetteFeather": 78,
                                  "vignetteRoundness": 0})]
    if outs.get("niche"):
        cmds += [("file.placeEmbedded", {"path": str(outs["niche"])}), ("layer.setProps", {"name": "niche"})]
        if not fallback:
            cmds += [("layer.layerStyle.bevelEmboss", {"style": "inner", "technique": "smooth", "depth": 90,
                                                       "direction": "up", "size": 4, "soften": 1, "angle": 90,
                                                       "altitude": 42}),
                     ("layer.layerStyle.dropShadow", {"color": "#000000", "opacity": 60, "angle": 90, "distance": 3,
                                                      "size": 10, "add": True})]
    cmds += [("file.placeEmbedded", {"path": str(outs["star"])}), ("layer.setProps", {"name": "star"}),
             ("layer.layerStyle.outerGlow", {"color": "#F6E2AE", "opacity": 62, "size": 22, "spread": 0,
                                             "technique": "softer", "blend": "screen"})]
    if outs.get("glyphs"):
        cmds += [("file.placeEmbedded", {"path": str(outs["glyphs"])}),
                 ("layer.setProps", {"name": "bloom", "blend": "Screen", "opacity": 0.55}),
                 ("filter.blur.gaussianBlur", {"radius": 15}),
                 ("file.placeEmbedded", {"path": str(outs["glyphs"])}),
                 ("layer.setProps", {"name": "stones"})]
        if not fallback:
            cmds += [("layer.layerStyle.gradientOverlay", {"from": "#F8E7B8", "to": "#A97E3A", "style": "linear",
                                                           "angle": 90, "opacity": 100, "blend": "normal"}),
                     ("layer.layerStyle.bevelEmboss", {"style": "inner", "technique": "smooth", "depth": 140,
                                                       "direction": "up", "size": 3, "soften": 0, "angle": 90,
                                                       "altitude": 38, "add": True}),
                     ("layer.layerStyle.innerShadow", {"color": "#2B1A07", "opacity": 70, "angle": 90,
                                                       "distance": 0, "choke": 40, "size": 2, "add": True}),
                     ("layer.layerStyle.outerGlow", {"color": T["gold_h"], "opacity": 42, "size": 9, "spread": 0,
                                                     "technique": "softer", "blend": "screen", "add": True})]
        else:
            cmds += [("layer.layerStyle.gradientOverlay", {"from": "#F8E7B8", "to": "#A97E3A", "style": "linear",
                                                           "angle": 90, "opacity": 100, "blend": "normal"})]
    if outs.get("minium"):
        cmds += [("file.placeEmbedded", {"path": str(outs["minium"])}), ("layer.setProps", {"name": "minium"})]
        if not fallback:
            cmds += [("layer.layerStyle.bevelEmboss", {"style": "inner", "technique": "smooth", "depth": 80,
                                                       "direction": "down", "size": 1, "soften": 0, "angle": 90,
                                                       "altitude": 40})]
    cmds += [("file.placeEmbedded", {"path": str(outs["type"])}), ("layer.setProps", {"name": "type"}),
             ("layer.flattenImage", {}),
             ("filter.noise.addNoise", {"amount": 3.5, "distribution": "gaussian", "monochromatic": True,
                                        "seed": 11})]
    pc_run(outs["nave"], cmds, master)
    q = 85
    while True:
        p = subprocess.run([PC, "convert", str(master), str(out_jpg), "--quality", str(q)],
                           capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            raise RuntimeError(f"photocraft-cli convert exit {p.returncode}: {p.stderr.strip()[-400:]}")
        size = out_jpg.stat().st_size
        if size <= JPEG_LIMIT or q <= 50:
            break
        log(f"{out_jpg.name}: {size // 1024} KB at q{q}; stepping down")
        q -= 5
    if size > JPEG_LIMIT:
        raise RuntimeError(f"{out_jpg.name} is {size} bytes even at q{q}")
    return master, q, size


# ── one card ────────────────────────────────────────────────────────────
def make_card(entry, glyphs, out_dir, keep=False, morphemes_override=None, tag=None, fallback=False):
    sl = slug(entry["word"]) + (f"--{tag}" if tag else "")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (HERE / "_work").mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f"{sl}-", dir=HERE / "_work"))
    t0 = time.time()
    try:
        layers, info = build(entry, glyphs, work, morphemes_override, fallback)
        outs = compose(layers, work, fallback)
        out = out_dir / f"{sl}.jpg"
        _, q, size = finish(outs, out, work, fallback)
    except Exception:
        if not keep:
            shutil.rmtree(work, ignore_errors=True)
        raise
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    row = {"word": entry["word"], "slug": sl, "file": str(out), "bytes": size, "quality": q,
           "morphemes": list(morphemes_override if morphemes_override is not None else (entry.get("morphemes") or [])),
           "carved": info["carved"], "stones": info["stones"], "word_size": info["word_size"],
           "def_lines": info["def_lines"], "def": info["def"], "source": info["source"],
           "fallback": fallback, "seconds": round(time.time() - t0, 2), "work": str(work) if keep else None}
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return row


# ── batch driver ────────────────────────────────────────────────────────
def run_one(word, out_dir, fallback):
    argv = [sys.executable, str(Path(__file__).resolve()), "--one", word, "--out", str(out_dir)]
    if fallback:
        argv.append("--fallback")
    p = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    row = None
    for ln in p.stdout.splitlines():
        if ln.startswith("{"):
            try:
                row = json.loads(ln)
            except json.JSONDecodeError:
                pass
    return p.returncode, row, p.stderr


def batch(lex, out_dir, jobs):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    glossary = {p.stem for p in GLOSSARY.glob("*.html")} - {"index"}
    rows, failed, logs = {}, [], []
    t0 = time.time()

    def work(e):
        code, row, err = run_one(e["word"], out_dir, False)
        tries = [("normal", code, err)]
        if code != 0 or row is None:
            code, row, err = run_one(e["word"], out_dir, True)        # one retry, with the fallback
            tries.append(("fallback", code, err))
        return e, code, row, tries

    with ThreadPoolExecutor(max_workers=max(1, min(4, jobs))) as ex:
        for e, code, row, tries in ex.map(work, lex):
            for kind, c, err in tries:
                for ln in err.splitlines():
                    if ln.strip():
                        logs.append(f"[{e['word']}|{kind}] {ln}")
            if code == 0 and row:
                rows[row["slug"]] = row
            else:
                failed.append({"word": e["word"], "reason": (tries[-1][2].strip().splitlines() or ["?"])[-1][:400]})
    manifest = []
    for e in lex:
        sl = slug(e["word"])
        r = rows.get(sl)
        if not r:
            continue
        if sl not in glossary:
            logs.append(f"[{e['word']}] slug {sl!r} has no glossary/{sl}.html")
        manifest.append({"word": e["word"], "slug": sl, "file": f"out/{sl}.jpg", "bytes": r["bytes"],
                         "morphemes": r["morphemes"]})
    missing_cards = sorted(glossary - {m["slug"] for m in manifest})
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    (HERE / "run.jsonl").write_text("".join(json.dumps(rows[s], ensure_ascii=False) + "\n" for s in sorted(rows)))
    (HERE / "run.log").write_text("\n".join(logs) + "\n")
    summary = {"cards": len(manifest), "failed": failed, "glossary_pages_without_card": missing_cards,
               "seconds": round(time.time() - t0, 1), "fallback_used": [r["word"] for r in rows.values() if r["fallback"]]}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("words", nargs="*")
    ap.add_argument("--out", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--one", help=argparse.SUPPRESS)
    ap.add_argument("--fallback", action="store_true", help="plain pipeline: no emphasis runs, no bevels")
    ap.add_argument("--keep", action="store_true", help="keep the intermediate files under _work/")
    ap.add_argument("--morphemes", help="comma list overriding canon (layout tests only)")
    ap.add_argument("--tag", help="suffix for the output name (use with --morphemes)")
    a = ap.parse_args(argv)
    lex = load_lexicon()
    if a.all:
        s = batch(lex, a.out or HERE / "out", a.jobs)
        return 1 if s["failed"] else 0
    glyphs = glyph_table()
    words = [a.one] if a.one else a.words
    override = [m.strip() for m in a.morphemes.split(",") if m.strip()] if a.morphemes else None
    if override is not None and not a.tag:
        a.tag = f"test{len(override)}"
    failed = 0
    for w in words:
        e = find_entry(lex, w)
        if e is None:
            log(f"'{w}' is not in the lexicon; skipped")
            failed += 1
            continue
        try:
            make_card(e, glyphs, a.out or (HERE / "out" if a.one else HERE / "samples"), keep=a.keep,
                      morphemes_override=override, tag=a.tag, fallback=a.fallback)
        except Exception as ex:   # one bad word never stops the others
            failed += 1
            log(f"{w}: FAILED: {type(ex).__name__}: {ex}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
