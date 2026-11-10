"""YOUSPEAK anchor particles (U+E17C-E17F): the recommended CANDIDATE set.

CANDIDATE, NOT CANON. Nothing here is entered in glyph_specs_v1.py; the language's
owner chooses. Built on designer C's set (bond first), revised after the two judges.
See design_notes.md and decisions.md beside this file.

Format: the exact CORE_GLYPHS entry format of script/glyphs/glyph_specs_v1.py; the
dict can be pasted into CORE_GLYPHS unchanged. Font units on the 1000-unit em, y up.
Primitives: filled polygons only (mitred 80-EM monoline outlines, as the S092 corner
brackets use, and square head-dots as dot() draws them). Every polygon is
counter-clockwise like stroke_to_polygon output, and no two polygons touch.

Parameters of the generator that emitted these polygons (a working file, not kept): {'xheel': 155, 'heel': 60, 'y0': 240, 'top': 660, 'ch': 105, 'cv': 100, 'h': 80, 'hg': 60, 'dx_yu': 45, 'dx_mi': 45}
Derived: inner chamfer 63, outer chamfer 110, hook overlap 60,
head tops 800, yumi: spans x 155-850.

tongue "Tok Pisin" / "Lakota" is truthful metadata (as in morphemes.json); neither is in
DONOR_SIGIL, so compose_glyph draws no sigil (the proposal). mclass "structural" draws
the small diamond class mark (the proposal).
"""

ANCHOR_GLYPHS = {

    "mi:": {  # The I on its own side: an upright post with its floating head-dot and a reach at shoulder height, both corners cut as O's mouth-arc turned down, the hand let down open - an offer, not a grip; yumi:'s right half, translated whole.
        "core": {
            "polygons": [
                [(251, 420), (331, 420), (331, 517), (394, 580), (558, 580), (621, 517), (621, 240), (701, 240), (701, 550), (591, 660), (361, 660), (251, 550)],  # mi: hand, shoulder bar and post - O's half-octagon turned down
                [(576, 720), (656, 720), (656, 800), (576, 800)],  # mi: head-dot (the family's person-marker)
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yu:": {  # The other on its own side: an upright post standing on its own ground, which runs back behind it as a heel and forward into an open bowl - your side, borrowed ground, held open and never closed over; yumi:'s left half, translated whole.
        "core": {
            "polygons": [
                [(265, 240), (665, 240), (775, 350), (775, 480), (695, 480), (695, 383), (632, 320), (468, 320), (405, 383), (405, 660), (325, 660), (325, 320), (265, 320)],  # yu: heel, post, floor and rim - the bowl is O's mouth-arc turned up
                [(370, 720), (450, 720), (450, 800), (370, 800)],  # yu: head-dot
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yumi:": {  # You and I hooked: yu's rim rises inside mi's reach and mi's hand hangs inside yu's bowl; no stroke touches another, a white seam runs unbroken between them; both whole, heads level.
        "core": {
            "polygons": [
                [(155, 240), (555, 240), (665, 350), (665, 480), (585, 480), (585, 383), (522, 320), (358, 320), (295, 383), (295, 660), (215, 660), (215, 320), (155, 320)],  # yu: body = yu: part 0 shifted x-110
                [(400, 420), (480, 420), (480, 517), (543, 580), (707, 580), (770, 517), (770, 240), (850, 240), (850, 550), (740, 660), (510, 660), (400, 550)],  # mi: body = mi: part 0 shifted x+149
                [(260, 720), (340, 720), (340, 800), (260, 800)],  # yu: head = yu: part 1 shifted x-110
                [(725, 720), (805, 720), (805, 800), (725, 800)],  # mi: head = mi: part 1 shifted x+149
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "mitakuyame:": {  # All my relations: the same hold with each closed outer side opened - yu's ground runs out past where yu stood, mi's reach runs out past where mi stood; both heads, the bowl's rim and the hand stay exactly where they were; the relation is whole and open at both ends.
        "core": {
            "polygons": [
                [(155, 240), (555, 240), (665, 350), (665, 480), (585, 480), (585, 383), (522, 320), (155, 320)],  # yu's ground opened: floor runs out to the left edge, rim rises inside mi's reach
                [(400, 420), (480, 420), (480, 517), (543, 580), (850, 580), (850, 660), (510, 660), (400, 550)],  # mi's reach opened: hand hangs inside yu's bowl, shoulder bar runs out to the right edge
                [(260, 720), (340, 720), (340, 800), (260, 800)],  # yu: head-dot, where it stood in yumi:
                [(725, 720), (805, 720), (805, 800), (725, 800)],  # mi: head-dot, where it stood in yumi:
            ],
        },
        "tongue": "Lakota", "domain": "relation+position", "mclass": "structural",
    },
}
