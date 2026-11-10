"""YOUSPEAK anchor particles - designer C (bond-first) candidates.

ANCHOR_GLYPHS uses the exact entry format of CORE_GLYPHS in
script/glyphs/glyph_specs_v1.py and can be pasted into that dict unchanged.
Coordinates: 1000-unit em, y up (font convention), as in CORE_GLYPHS.
Primitives: filled polygons only (mitred 80-EM monoline outlines, as the S092
corner brackets use for clean joins; square head-dots identical to dot()).
Every polygon is counter-clockwise, matching stroke_to_polygon, so nonzero
filling unions them; no two polygons touch.

yu: and mi: are yumi:'s two halves translated whole:
  yu: = yumi: parts 0 and 2 shifted x+105;  mi: = parts 1 and 3 shifted x-137.

tongue 'Tok Pisin' / 'Lakota' is truthful metadata; neither is in DONOR_SIGIL,
so compose_glyph falls back to no sigil (the proposal - see rationale.md).
mclass 'structural' gives the ◆ class mark (the proposal - see rationale.md).

"""

ANCHOR_GLYPHS = {

    "mi:": {  # The I standing on its own side: an upright post with its floating head-dot, reaching over at shoulder height and letting its hand down - an offer, not a grip; the right half of yumi:, translated whole.
        "core": {
            "polygons": [
                [(333, 400), (333, 600), (546, 600), (633, 513), (633, 230), (713, 230), (713, 547), (580, 680), (253, 680), (253, 400)],  # mi: reach - leg, bar, shoulder, post
                [(568, 750), (678, 750), (678, 860), (568, 860)],  # mi: head-dot
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yu:": {  # The other standing on its own side: an upright post with its head-dot, its foot running out as an open half-octagon bowl - your ground, as received, held open and never closed over; the left half of yumi:, translated whole.
        "core": {
            "polygons": [
                [(295, 680), (295, 363), (428, 230), (622, 230), (755, 363), (755, 510), (675, 510), (675, 397), (588, 310), (462, 310), (375, 397), (375, 680)],  # yu: post, half-octagon floor, rising rim
                [(330, 750), (440, 750), (440, 860), (330, 860)],  # yu: head-dot
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yumi:": {  # You and I hooked: yu's bowl rises inside mi's reach, mi's hand hangs inside yu's bowl, and no stroke touches another - each within the other's side, both whole, the seam a white path running unbroken between them; heads level.
        "core": {
            "polygons": [
                [(190, 680), (190, 363), (323, 230), (517, 230), (650, 363), (650, 510), (570, 510), (570, 397), (483, 310), (357, 310), (270, 397), (270, 680)],  # yu: post, floor, rim = yu: part 0 shifted x-105
                [(470, 400), (470, 600), (683, 600), (770, 513), (770, 230), (850, 230), (850, 547), (717, 680), (390, 680), (390, 400)],  # mi: leg, bar, shoulder, post = mi: part 0 shifted x+137
                [(225, 750), (335, 750), (335, 860), (225, 860)],  # yu: head-dot = yu: part 1 shifted x-105
                [(705, 750), (815, 750), (815, 860), (705, 860)],  # mi: head-dot = mi: part 1 shifted x+137
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "mitakuyame:": {  # All my relations: the same joining, its two closed outer sides opened - the floor runs out past where yu stood, the reach runs out past where mi stood; both persons kept where they were; the hold now opens to every side beyond the pair.
        "core": {
            "polygons": [
                [(170, 230), (517, 230), (650, 363), (650, 510), (570, 510), (570, 397), (483, 310), (170, 310)],  # yu's hold opened: floor runs out left, rim rises into mi's reach
                [(470, 400), (470, 600), (830, 600), (830, 680), (390, 680), (390, 400)],  # mi's hold opened: hand hangs into yu's floor, bar runs out right
                [(225, 750), (335, 750), (335, 860), (225, 860)],  # yu: head-dot (where yu stood in yumi:)
                [(705, 750), (815, 750), (815, 860), (705, 860)],  # mi: head-dot (where mi stood in yumi:)
            ],
        },
        "tongue": "Lakota", "domain": "relation+position", "mclass": "structural",
    },
}
