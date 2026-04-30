"""YOUSPEAK glyph specifications — v1 with feature-encoding.

Each morpheme has:
  - core: the iconographic shape (list of strokes + polygons)
  - tongue: donor-tongue (adds top-left sigil automatically)
  - domain: semantic domain (body-shape follows domain's shape-family)
  - mclass: content | prefix | suffix | structural (adds bottom-right class-mark)

The sigil and class-mark are COMPOSED with the core shape by the font-builder,
so the spec itself declares only the iconographic core + metadata. This keeps
the spec declarative and lets all glyphs share consistent sigil/class-mark
drawing without per-glyph duplication.

Design rationale: see script/glyphs/design_philosophy.md
"""

from __future__ import annotations

import json
from pathlib import Path

# Stroke-width: heavier than v0 (60 → 80) for body-text legibility at 10-12pt.
# Correcting-factor for diagonals: a 45° line appears ~10% thinner than a
# horizontal of the same width. v1 uses conditional weighting (not implemented
# at this stage; flagged for the v2 font artist).
STROKE_WIDTH = 80
STROKE_WIDTH_DIAGONAL = 90  # optical correction for future use
DOT_SIZE = 100
EM = 1000


def dot(x: int, y: int, size: int = DOT_SIZE) -> list[tuple[int, int]]:
    """Square dot (4 corners) centred at (x, y)."""
    h = size // 2
    return [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)]


# ────────────────────────────────────────────────────────────────────────
# DONOR-TONGUE SIGILS — top-left corner, 80 EM region centered at (150, 850)
# ────────────────────────────────────────────────────────────────────────

def sigil_greek() -> dict:
    """● filled dot — Greek (classical alpha of marks)."""
    return {"polygons": [dot(150, 850, 70)]}

def sigil_latin() -> dict:
    """■ filled square — Latin (Roman orthogonality)."""
    h = 35
    return {"polygons": [[(150 - h, 850 - h), (150 + h, 850 - h),
                          (150 + h, 850 + h), (150 - h, 850 + h)]]}

def sigil_hebrew() -> dict:
    """▽ downward triangle — Hebrew (kavod descent)."""
    return {"polygons": [[(110, 890), (190, 890), (150, 815)]]}

def sigil_arabic() -> dict:
    """○ open circle (ring) — Arabic (tawhid)."""
    # Drawn as two concentric polygons (outer - inner) approximation
    # For simplicity, use a ring as a thick stroke on an octagon
    r_outer = 40
    r_inner = 25
    # 8-sided approximation
    import math
    outer = [(150 + int(r_outer * math.cos(i * math.pi / 4)),
              850 + int(r_outer * math.sin(i * math.pi / 4))) for i in range(8)]
    inner = [(150 + int(r_inner * math.cos(-i * math.pi / 4)),
              850 + int(r_inner * math.sin(-i * math.pi / 4))) for i in range(8)]
    # Single contour that traces outer then jumps to inner (approximated as strokes)
    # Simpler: just render as small ring using 8 short arc strokes
    strokes = []
    import math as _m
    for i in range(8):
        a1 = i * _m.pi / 4
        a2 = (i + 1) * _m.pi / 4
        x1 = 150 + int((r_outer + r_inner) / 2 * _m.cos(a1))
        y1 = 850 + int((r_outer + r_inner) / 2 * _m.sin(a1))
        x2 = 150 + int((r_outer + r_inner) / 2 * _m.cos(a2))
        y2 = 850 + int((r_outer + r_inner) / 2 * _m.sin(a2))
        strokes.append((x1, y1, x2, y2))
    return {"strokes": strokes, "stroke_width": 12}

def sigil_sanskrit() -> dict:
    """⋮ three vertical dots — Sanskrit (Trimurti)."""
    return {"polygons": [
        dot(150, 895, 28),
        dot(150, 850, 28),
        dot(150, 805, 28),
    ]}

def sigil_egyptian() -> dict:
    """□ empty square outline — Egyptian (Ma'at's precision)."""
    return {"strokes": [
        (115, 885, 185, 885),
        (185, 885, 185, 815),
        (185, 815, 115, 815),
        (115, 815, 115, 885),
    ], "stroke_width": 14}

def sigil_pie() -> dict:
    """≡ three horizontal lines — PIE (grandmother root)."""
    return {"strokes": [
        (115, 885, 185, 885),
        (115, 850, 185, 850),
        (115, 815, 185, 815),
    ], "stroke_width": 14}


def sigil_sumerian() -> dict:
    """⊻ wedge-pair — Sumerian (cuneiform horizontal wedge, source of me)."""
    # Two short horizontal strokes stacked — approximating the cuneiform
    # horizontal wedge-marks used to write 'me' in Sumerian clay tablets.
    return {"strokes": [
        (115, 870, 185, 850),   # upper wedge stroke
        (115, 835, 185, 815),   # lower wedge stroke
    ], "stroke_width": 14}

def sigil_english() -> dict:
    """(no sigil) — English (default; absence-is-English)."""
    return {}

DONOR_SIGIL = {
    "Greek":    sigil_greek,
    "Latin":    sigil_latin,
    "Hebrew":   sigil_hebrew,
    "Arabic":   sigil_arabic,
    "Sanskrit": sigil_sanskrit,
    "Egyptian": sigil_egyptian,
    "PIE":      sigil_pie,
    "English":  sigil_english,
    "Gr/En":    sigil_greek,   # hybrid: primary donor shown
    "Sumerian": sigil_sumerian,
    "Lat/Gr":   sigil_latin,
}


# ────────────────────────────────────────────────────────────────────────
# CLASS MARKS — bottom-right corner, ~60 EM region centered at (850, 140)
# ────────────────────────────────────────────────────────────────────────

def mark_content() -> dict:
    """(no mark) — content morpheme; the default."""
    return {}

def mark_prefix() -> dict:
    """◁ left-pointing triangle — prefix (begins)."""
    return {"polygons": [[(880, 170), (880, 110), (815, 140)]]}

def mark_suffix() -> dict:
    """▷ right-pointing triangle — suffix (ends)."""
    return {"polygons": [[(815, 170), (815, 110), (880, 140)]]}

def mark_structural() -> dict:
    """◆ small diamond — structural mark (mark-of-marks)."""
    return {"polygons": [[(850, 170), (880, 140), (850, 110), (820, 140)]]}

CLASS_MARK = {
    "content":    mark_content,
    "prefix":     mark_prefix,
    "suffix":     mark_suffix,
    "structural": mark_structural,
}


# ────────────────────────────────────────────────────────────────────────
# CORE GLYPHS — iconographic shapes, shape-family per semantic domain
# ────────────────────────────────────────────────────────────────────────

# Each core-shape respects the domain's shape-language (see design_philosophy.md):
#
#   beauty         → curves opening upward (wings, petals)
#   rightness/truth→ balanced symmetric axes
#   appearing/light→ radiating from centre
#   ache/pressure  → bent line with stress-point
#   act/event      → directional wedge
#   relation       → two interacting shapes
#   space/enclose  → closed form
#   time/process   → spiral / flowing
#   wonder/recog.  → eye-symmetric
#   testing        → vessel
#   deception      → crossed / doubled
#   structure(meta)→ centred contained
#   hidden         → dashed / partial
#   weight/glory   → heavy-bottomed

CORE_GLYPHS = {

    # ── CONTENT MORPHEMES ──────────────────────────────────────────────

    "doxa": {  # weight + appearing-light (doxa's dual nature)
        "core": {
            "strokes": [
                (200, 680, 800, 680),   # upper bar (heavy-top)
                (800, 680, 500, 230),   # right diagonal to point
                (500, 230, 200, 680),   # left diagonal
                # plus three inward-radiating strokes (light-in-weight)
                (500, 600, 500, 300),   # central ray
                (350, 590, 500, 350),   # left inward-ray
                (650, 590, 500, 350),   # right inward-ray
            ],
        },
        "tongue": "Greek", "domain": "weight+light", "mclass": "content",
    },

    "kallos": {  # beauty — wings opening upward
        "core": {
            "strokes": [
                (500, 200, 500, 680),   # central stem
                (500, 680, 280, 480),   # left wing (curving down-out)
                (500, 680, 720, 480),   # right wing
                # small secondary curves (adding the opening-upward gesture)
                (280, 480, 220, 300),
                (720, 480, 780, 300),
            ],
        },
        "tongue": "Greek", "domain": "beauty", "mclass": "content",
    },

    "ortho": {  # rightness — balanced cross
        "core": {
            "strokes": [
                (500, 250, 500, 750),   # vertical
                (280, 680, 720, 680),   # upper horizontal (near top)
                (250, 400, 750, 400),   # lower horizontal (near middle)
            ],
        },
        "tongue": "Greek", "domain": "rightness", "mclass": "content",
    },

    "phanes": {  # appearing — radiating rays from centre
        "core": {
            "strokes": [
                (500, 280, 220, 680),
                (500, 280, 360, 710),
                (500, 280, 500, 740),
                (500, 280, 640, 710),
                (500, 280, 780, 680),
                (500, 280, 200, 440),
                (500, 280, 800, 440),
            ],
        },
        "tongue": "Greek", "domain": "appearing", "mclass": "content",
    },

    "algia": {  # ache — bent line with pressure-point
        "core": {
            "strokes": [
                (400, 730, 400, 480),
                (400, 480, 680, 230),
            ],
            "polygons": [dot(400, 480, 140)],
        },
        "tongue": "Greek", "domain": "ache", "mclass": "content",
    },

    "anagno": {  # recognition — eye-symmetric (the pattern-match)
        "core": {
            "strokes": [
                (230, 720, 770, 720),   # top parallel
                (230, 280, 770, 280),   # bottom parallel
                (500, 720, 500, 280),   # connector
                # horizontal eye-line suggestion
                (370, 500, 630, 500),
            ],
        },
        "tongue": "Greek", "domain": "wonder+recognition", "mclass": "content",
    },

    "stasis": {  # standing — two verticals on horizontal anchor
        "core": {
            "strokes": [
                (350, 220, 350, 720),
                (650, 220, 650, 720),
                (220, 220, 780, 220),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "meta": {  # after — leftward directional wedge
        "core": {
            "strokes": [
                (250, 480, 800, 480),
                (250, 480, 470, 680),
                (250, 480, 470, 280),
            ],
        },
        "tongue": "Greek", "domain": "act+event", "mclass": "content",
    },

    "strophe": {  # turning — spiral
        "core": {
            "strokes": [
                (800, 480, 750, 720),
                (750, 720, 500, 780),
                (500, 780, 250, 720),
                (250, 720, 200, 480),
                (200, 480, 250, 280),
                (250, 280, 500, 220),
                (500, 220, 700, 280),
                (700, 280, 700, 440),
            ],
        },
        "tongue": "Greek", "domain": "time+process", "mclass": "content",
    },

    "thauma": {  # wonder — eye
        "core": {
            "strokes": [
                (200, 480, 400, 620),
                (400, 620, 600, 620),
                (600, 620, 800, 480),
                (800, 480, 600, 340),
                (600, 340, 400, 340),
                (400, 340, 200, 480),
            ],
            "polygons": [dot(500, 480, 180)],
        },
        "tongue": "Greek", "domain": "wonder+recognition", "mclass": "content",
    },

    "syn": {  # together — converging inverted V (two-into-one)
        "core": {
            "strokes": [
                (220, 720, 500, 220),
                (780, 720, 500, 220),
                # horizontal meeting-line (the 'together')
                (380, 470, 620, 470),
            ],
        },
        "tongue": "Greek", "domain": "relation+between", "mclass": "content",
    },

    "phora": {  # carrying — L-shape (bracket)
        "core": {
            "strokes": [
                (220, 420, 720, 420),
                (720, 420, 720, 670),
            ],
        },
        "tongue": "Greek", "domain": "act+event", "mclass": "content",
    },

    "cand": {  # warm clarity — soft radiance (appearing-family, warm register)
        "core": {
            "strokes": [
                # radiating but softer, with small dots at tips
                (400, 700, 350, 800),
                (500, 730, 500, 830),
                (600, 700, 650, 800),
                # circle body (octagon)
                (350, 450, 430, 600),
                (430, 600, 570, 600),
                (570, 600, 650, 450),
                (650, 450, 570, 300),
                (570, 300, 430, 300),
                (430, 300, 350, 450),
            ],
            "polygons": [
                dot(350, 800, 60),
                dot(500, 830, 60),
                dot(650, 800, 60),
            ],
        },
        "tongue": "Latin", "domain": "appearing+warm", "mclass": "content",
    },

    "dokim": {  # testing — crucible (vessel with flame)
        "core": {
            "strokes": [
                (270, 500, 320, 250),
                (320, 250, 680, 250),
                (680, 250, 730, 500),
                # flame
                (500, 540, 500, 760),
                (470, 700, 500, 760),
                (530, 700, 500, 760),
            ],
        },
        "tongue": "Greek", "domain": "testing+forging", "mclass": "content",
    },

    "arti": {  # skilled-making (PIE *h2ert-) — pentagon (five-pre-domain)
        "core": {
            "strokes": [
                (500, 770, 800, 570),
                (800, 570, 680, 240),
                (680, 240, 320, 240),
                (320, 240, 200, 570),
                (200, 570, 500, 770),
            ],
        },
        "tongue": "PIE", "domain": "rightness", "mclass": "content",
    },

    "veri": {  # truth — balanced cross (rightness-family)
        "core": {
            "strokes": [
                (500, 220, 500, 780),
                (220, 500, 780, 500),
            ],
        },
        "tongue": "Latin", "domain": "rightness", "mclass": "content",
    },

    "compler": {  # filling-together — two opposing curves (relation-family)
        "core": {
            "strokes": [
                (270, 670, 470, 670),
                (470, 670, 470, 330),
                (470, 330, 270, 330),
                (730, 670, 530, 670),
                (530, 670, 530, 330),
                (530, 330, 730, 330),
            ],
        },
        "tongue": "Latin", "domain": "relation+between", "mclass": "content",
    },

    "diplos": {  # twofold — two parallel verticals (structure-family, multiplicity)
        "core": {
            "strokes": [
                (350, 220, 350, 780),
                (650, 220, 650, 780),
            ],
        },
        "tongue": "Greek", "domain": "structure+multiplicity", "mclass": "content",
    },

    "sema": {  # sign — square with centre-dot (structure+signification)
        "core": {
            "strokes": [
                (300, 320, 700, 320),
                (700, 320, 700, 680),
                (700, 680, 300, 680),
                (300, 680, 300, 320),
            ],
            "polygons": [dot(500, 500, 160)],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "anastro": {  # inversion — reverse spiral
        "core": {
            "strokes": [
                (200, 480, 250, 720),
                (250, 720, 500, 780),
                (500, 780, 750, 720),
                (750, 720, 800, 480),
                (800, 480, 750, 280),
                (750, 280, 500, 220),
                (500, 220, 300, 280),
                (300, 280, 300, 440),
            ],
        },
        "tongue": "Greek", "domain": "time+process", "mclass": "content",
    },

    "kalypt": {  # enclosure — box with interior mark
        "core": {
            "strokes": [
                (260, 280, 740, 280),
                (740, 280, 740, 720),
                (740, 720, 260, 720),
                (260, 720, 260, 280),
            ],
            "polygons": [dot(500, 500, 140)],
        },
        "tongue": "Greek", "domain": "space+enclosure", "mclass": "content",
    },

    "haphe": {  # touching — two fingertips meeting
        "core": {
            "strokes": [
                (300, 250, 460, 500),
                (460, 500, 500, 620),
                (700, 250, 540, 500),
                (540, 500, 500, 620),
            ],
        },
        "tongue": "Greek", "domain": "relation+between", "mclass": "content",
    },

    "allos": {  # other — bifurcating Y
        "core": {
            "strokes": [
                (500, 220, 500, 500),
                (500, 500, 280, 760),
                (500, 500, 720, 760),
            ],
        },
        "tongue": "Greek", "domain": "structure+multiplicity", "mclass": "content",
    },

    "parallax": {  # parallel-shift — two parallels + offset indicator
        "core": {
            "strokes": [
                (220, 640, 780, 640),
                (220, 320, 780, 320),
                (420, 480, 580, 480),
                (500, 540, 580, 480),
                (500, 420, 580, 480),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "hypo": {  # under — horizontal with descending vertical
        "core": {
            "strokes": [
                (220, 570, 780, 570),
                (500, 570, 500, 230),
            ],
        },
        "tongue": "Greek", "domain": "space+position", "mclass": "content",
    },

    "stix": {  # punctuation — dot
        "core": {
            "strokes": [],
            "polygons": [dot(500, 500, 200)],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "kairos": {  # time-layer — hourglass
        "core": {
            "strokes": [
                (220, 720, 780, 720),
                (780, 720, 220, 220),
                (220, 220, 780, 220),
                (780, 220, 220, 720),
            ],
        },
        "tongue": "Greek", "domain": "time+process", "mclass": "content",
    },

    "morphe": {  # form — irregular closed shape
        "core": {
            "strokes": [
                (310, 720, 560, 760),
                (560, 760, 760, 510),
                (760, 510, 710, 260),
                (710, 260, 410, 220),
                (410, 220, 260, 410),
                (260, 410, 310, 720),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "klimax": {  # scale — staircase
        "core": {
            "strokes": [
                (220, 280, 410, 280),
                (410, 280, 410, 420),
                (410, 420, 600, 420),
                (600, 420, 600, 570),
                (600, 570, 780, 570),
                (780, 570, 780, 720),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "content",
    },

    "lanthes": {  # hidden — dashed outline
        "core": {
            "strokes": [
                (260, 720, 410, 720),
                (510, 720, 660, 720),
                (760, 720, 760, 570),
                (760, 470, 760, 320),
                (760, 270, 610, 270),
                (510, 270, 360, 270),
                (260, 270, 260, 420),
                (260, 520, 260, 670),
            ],
        },
        "tongue": "Greek", "domain": "hidden", "mclass": "content",
    },

    "sleight": {  # deception-skill — crossed diagonals
        "core": {
            "strokes": [
                (260, 260, 740, 720),
                (740, 260, 260, 720),
            ],
        },
        "tongue": "English", "domain": "deception", "mclass": "content",
    },

    "seem": {  # appear-as — lenticular lens
        "core": {
            "strokes": [
                (260, 480, 410, 620),
                (410, 620, 590, 620),
                (590, 620, 740, 480),
                (740, 480, 590, 340),
                (590, 340, 410, 340),
                (410, 340, 260, 480),
            ],
        },
        "tongue": "English", "domain": "deception", "mclass": "content",
    },

    "gloria": {  # creature-scale glory — downward triangle (lighter than doxa)
        "core": {
            "strokes": [
                (230, 680, 770, 680),
                (770, 680, 500, 260),
                (500, 260, 230, 680),
            ],
        },
        "tongue": "Latin", "domain": "weight+light", "mclass": "content",
    },

    "andros": {  # of-a-person — stylized figure (standing human shape)
        "core": {
            "strokes": [
                (500, 220, 500, 500),   # body
                (500, 500, 320, 680),   # left leg
                (500, 500, 680, 680),   # right leg
                (350, 540, 650, 540),   # arms
            ],
            "polygons": [dot(500, 700, 160)],  # head (top)
        },
        "tongue": "Greek", "domain": "relation+between", "mclass": "content",
    },

    "vide": {  # seeing — open eye (wonder-family variant)
        "core": {
            "strokes": [
                (240, 500, 500, 640),
                (500, 640, 760, 500),
                (760, 500, 500, 360),
                (500, 360, 240, 500),
            ],
            "polygons": [dot(500, 500, 120)],
        },
        "tongue": "Latin", "domain": "wonder+recognition", "mclass": "content",
    },

    "cede": {  # yielding — stepping-back wedge (directional-backward)
        "core": {
            "strokes": [
                (750, 480, 250, 480),   # horizontal pointing-left
                (250, 480, 420, 620),
                (250, 480, 420, 340),
                # plus a small "step back" mark
                (500, 720, 600, 660),
            ],
        },
        "tongue": "Latin", "domain": "act+event", "mclass": "content",
    },

    "choro": {  # gathered-chorus — multi-radial (gathering)
        "core": {
            "strokes": [
                (500, 500, 200, 500),
                (500, 500, 800, 500),
                (500, 500, 500, 230),
                (500, 500, 500, 770),
                (500, 500, 290, 290),
                (500, 500, 710, 290),
                (500, 500, 290, 710),
                (500, 500, 710, 710),
            ],
            "polygons": [dot(500, 500, 160)],
        },
        "tongue": "Greek", "domain": "relation+between", "mclass": "content",
    },

    # Core Canon morphemes (v2, post-Constitution)
    "ki": {  # Japanese 気 — gathered life-attention-presence (appearing + centered)
        "core": {
            "strokes": [
                # a small gathered radiance inside a centered anchor
                (400, 300, 600, 300),    # anchor base horizontal
                (500, 300, 500, 600),    # upward stem
                (500, 600, 380, 720),    # left radiant
                (500, 600, 620, 720),    # right radiant
                (500, 600, 500, 780),    # central ray
            ],
            "polygons": [dot(500, 600, 80)],  # the gathered-point
        },
        "tongue": "Japanese", "domain": "appearing+warm", "mclass": "content",
    },

    "qing": {  # Mandarin 情 — deep emotional bond (relation + structural weight)
        "core": {
            "strokes": [
                # bonded double vertical with connecting curves (bond structure)
                (350, 250, 350, 720),   # left vertical
                (650, 250, 650, 720),   # right vertical
                (350, 500, 650, 500),   # middle connector (bond horizontal)
                # small inward markings (the earnest regard between)
                (430, 420, 570, 420),
                (430, 580, 570, 580),
            ],
            "polygons": [dot(500, 500, 60)],  # the bond-point
        },
        "tongue": "Mandarin", "domain": "relation+between", "mclass": "content",
    },

    "kin": {  # English/PIE — kinship, chosen-relation
        "core": {
            "strokes": [
                # two figures joined by a shared root-line
                (300, 720, 300, 400),   # left figure vertical
                (700, 720, 700, 400),   # right figure vertical
                (200, 400, 800, 400),   # shared root
                (300, 400, 700, 250),   # binding diagonal
                (700, 400, 300, 250),   # binding diagonal (cross)
            ],
        },
        "tongue": "English", "domain": "relation+between", "mclass": "content",
    },

    "tacit": {  # Latin — silent, wordless
        "core": {
            "strokes": [
                # a horizontal with a missing middle (silence)
                (220, 500, 400, 500),   # left segment
                (600, 500, 780, 500),   # right segment (gap in middle = silence)
                # small vertical above the gap (acknowledged-presence-of-silence)
                (500, 600, 500, 700),
            ],
            "polygons": [dot(500, 650, 50)],
        },
        "tongue": "Latin", "domain": "hidden", "mclass": "content",
    },

    "mushin": {  # Japanese 無心 — no-mind
        "core": {
            "strokes": [
                # circle (the held form) with slash (the absence-of-deliberation)
                (300, 480, 400, 620),
                (400, 620, 600, 620),
                (600, 620, 700, 480),
                (700, 480, 600, 340),
                (600, 340, 400, 340),
                (400, 340, 300, 480),
                # absence-slash (diagonal striking through)
                (250, 260, 750, 720),
            ],
        },
        "tongue": "Japanese", "domain": "act+event", "mclass": "content",
    },

    # ── GRAMMATICAL MORPHEMES ─────────────────────────────────────────

    "a": {  # privative — circle with slash
        "core": {
            "strokes": [
                (350, 500, 450, 620),
                (450, 620, 550, 620),
                (550, 620, 650, 500),
                (650, 500, 550, 380),
                (550, 380, 450, 380),
                (450, 380, 350, 500),
                (260, 280, 740, 680),
            ],
        },
        "tongue": "Greek", "domain": "hidden", "mclass": "prefix",
    },

    "sis": {  # state-suffix — short vertical with terminal bar
        "core": {
            "strokes": [
                (500, 320, 500, 680),
                (400, 320, 600, 320),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "suffix",
    },

    "ance": {  # quality-state-suffix — hook
        "core": {
            "strokes": [
                (400, 580, 400, 320),
                (400, 320, 600, 180),
            ],
        },
        "tongue": "Latin", "domain": "structure", "mclass": "suffix",
    },

    "mance": {  # quality-mode — hook + dot (variant)
        "core": {
            "strokes": [
                (400, 580, 400, 320),
                (400, 320, 600, 180),
            ],
            "polygons": [dot(600, 500, 80)],
        },
        "tongue": "Gr/En", "domain": "structure", "mclass": "suffix",
    },

    "ence": {  # quality-state parallel — softer hook
        "core": {
            "strokes": [
                (400, 520, 400, 320),
                (400, 320, 570, 220),
            ],
        },
        "tongue": "Latin", "domain": "structure", "mclass": "suffix",
    },

    "ma": {  # result-of-action — small closed curl
        "core": {
            "strokes": [
                (400, 480, 450, 570),
                (450, 570, 550, 570),
                (550, 570, 600, 480),
                (600, 480, 550, 390),
                (550, 390, 450, 390),
                (450, 390, 400, 480),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "suffix",
    },

    "iance": {  # luminous-quality — hook with upward ray
        "core": {
            "strokes": [
                (400, 520, 400, 320),
                (400, 320, 600, 180),
                (500, 580, 500, 800),
            ],
        },
        "tongue": "Latin", "domain": "appearing+warm", "mclass": "suffix",
    },

    "escence": {  # becoming — open-ended hook
        "core": {
            "strokes": [
                (400, 520, 400, 320),
                (400, 320, 720, 260),
            ],
        },
        "tongue": "Latin", "domain": "time+process", "mclass": "suffix",
    },

    "mia": {  # state-suffix variant — short form
        "core": {
            "strokes": [
                (400, 520, 400, 320),
                (400, 320, 500, 220),
                (500, 220, 600, 320),
            ],
        },
        "tongue": "Greek", "domain": "structure", "mclass": "suffix",
    },

    "ana": {  # up/back — upward arrow
        "core": {
            "strokes": [
                (500, 270, 500, 670),
                (500, 670, 390, 570),
                (500, 670, 610, 570),
            ],
        },
        "tongue": "Greek", "domain": "act+event", "mclass": "prefix",
    },

    "en": {  # in/within — inward bracket
        "core": {
            "strokes": [
                (300, 670, 570, 670),
                (570, 670, 570, 270),
                (570, 270, 300, 270),
            ],
        },
        "tongue": "Greek", "domain": "space+enclosure", "mclass": "prefix",
    },

    "com": {  # together — joining marks
        "core": {
            "strokes": [
                (260, 270, 420, 470),
                (420, 470, 260, 670),
                (740, 270, 580, 470),
                (580, 470, 740, 670),
            ],
        },
        "tongue": "Latin", "domain": "relation+between", "mclass": "prefix",
    },


    "me": {  # -me suffix — Sumerian 'me' (divine-ordinances-as-gifts)
        # Design: descent-into-reception
        # A downward-pointing triangle (the ordinance descends from above)
        # sitting in / resting on an upward-opening arc (the human vessel receives)
        # Together: divine gift arrives and is held.
        #
        # Visual rhyme with doxa (also downward-triangle) — distinction:
        #   doxa has a crossbar (manifestation / glory-that-shows)
        #   -me has an arc-base (reception / ordinance-that-lands)
        #
        # Lighter than doxa (4 strokes vs 6) — correct for a suffix.
        # Codepoint: U+E12A (reserved in codepoints.md).
        # Research basis: archaeology/script-mechanics/ (S075, all 7 chapters).
        "core": {
            "strokes": [
                # Triangle (downward-pointing): bar at top, apex at bottom
                (340, 650, 660, 650),   # horizontal bar (top of triangle)
                (340, 650, 500, 430),   # left diagonal to apex
                (660, 650, 500, 430),   # right diagonal to apex
                # Arc (upward-opening cup below the apex): 2-segment approximation
                (300, 420, 500, 240),   # left arc-stroke (down to nadir)
                (500, 240, 700, 420),   # right arc-stroke (back up)
            ],
        },
        "tongue": "Sumerian", "domain": "weight+light", "mclass": "suffix",
    },

    "y": {  # noun-abstract suffix
        "core": {
            "strokes": [
                (400, 720, 500, 500),
                (600, 720, 500, 500),
                (500, 500, 500, 300),
            ],
        },
        "tongue": "Gr/En", "domain": "structure", "mclass": "suffix",
    },
}


def compose_glyph(latin: str) -> dict:
    """Compose a final glyph for a morpheme: core + sigil + class-mark.

    Returns a dict with 'strokes' and 'polygons' suitable for font-building.
    Handles variable stroke-widths if present in the sigil/mark components.
    """
    spec = CORE_GLYPHS.get(latin)
    if not spec:
        return {}

    core = spec.get("core", {})
    tongue = spec.get("tongue", "English")
    mclass = spec.get("mclass", "content")

    strokes: list = list(core.get("strokes", []))
    polygons: list = list(core.get("polygons", []))

    # Add donor-tongue sigil
    sigil = DONOR_SIGIL.get(tongue, sigil_english)()
    if "strokes" in sigil:
        # Sigil may have its own stroke-width; for v1 we use primary width.
        # The stroke width parameter is used in font-builder.
        strokes.extend(sigil["strokes"])
    if "polygons" in sigil:
        polygons.extend(sigil["polygons"])

    # Add class mark
    mark = CLASS_MARK.get(mclass, mark_content)()
    if "polygons" in mark:
        polygons.extend(mark["polygons"])

    return {"strokes": strokes, "polygons": polygons}


def load_codepoint_map() -> dict[str, int]:
    """Load {latin: codepoint_int} from morphemes.json."""
    morphemes_path = Path(__file__).resolve().parent.parent / "morphemes.json"
    with morphemes_path.open() as f:
        data = json.load(f)
    out: dict[str, int] = {}
    for m in data["morphemes"]:
        latin = m["latin"].strip("-")
        cp_str = m["codepoint"].replace("U+", "")
        out[latin] = int(cp_str, 16)
    return out


# GLYPHS-compatible export: each glyph is {strokes, polygons} after composition
GLYPHS = {latin: compose_glyph(latin) for latin in CORE_GLYPHS}

# Also export metadata for LLM dataset preparation
METADATA = {
    latin: {
        "tongue": spec.get("tongue", "English"),
        "domain": spec.get("domain", "unspecified"),
        "mclass": spec.get("mclass", "content"),
    }
    for latin, spec in CORE_GLYPHS.items()
}
