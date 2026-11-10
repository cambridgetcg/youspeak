"""YOUSPEAK anchor particles (grammars/ankyrance/) - CANDIDATE glyphs, design A
"kin of the vocative".  Not canon: nothing here is entered in glyph_specs_v1.py.

Each entry is in the exact CORE_GLYPHS format and could be pasted into that dict
unchanged.  Cores are polygon-only (as chul and the S092 brackets are): every
mouth-arc is ONE mitered polygon on O-'s own centreline (five sides of a regular
octagon of side 180, 80 EM wide), and every breath is one filled triangle.

Sigil: none drawn.  "Tok Pisin" and "Lakota" are recorded truthfully as tongue
(matching script/morphemes.json) and are not mapped in DONOR_SIGIL, so
compose_glyph() falls back to no sigil; the slot stays free for the owner's
assignment.  Class mark: "structural" (the small diamond), as morphemes.json has it.
See rationale.md beside this file.
"""

ANCHOR_GLYPHS = {

    "mi:": {  # My mouth holding my own breath: O-'s mouth-arc, its breath gathered short with the tip resting on the line of the lips - offered, never flown; the utterance stands on my side.
        "core": {
            "polygons": [
                [(674, 757), (478, 757), (326, 607), (326, 393), (478, 243), (674, 243), (674, 323), (510, 323), (406, 427), (406, 573), (510, 677), (674, 677)],
                [(502, 596), (502, 404), (674, 500)],
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yu:": {  # My mouth with your breath standing before it, pointing at me: received, held a clear distance from my lips, not taken in (not annexed); its standing edge is on your side.
        "core": {
            "polygons": [
                [(518, 757), (322, 757), (170, 607), (170, 393), (322, 243), (518, 243), (518, 323), (354, 323), (250, 427), (250, 573), (354, 677), (518, 677)],
                [(830, 404), (830, 596), (658, 500)],
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yumi:": {  # Two mouths face each other across an open between, each holding its own breath at its lips - both persons whole, both seated in the speaking position.
        "core": {
            "polygons": [
                [(412, 696), (265, 696), (151, 582), (151, 418), (265, 304), (412, 304), (412, 384), (299, 384), (231, 452), (231, 548), (299, 616), (412, 616)],
                [(298, 563), (298, 437), (412, 500)],
                [(588, 616), (701, 616), (769, 548), (769, 452), (701, 384), (588, 384), (588, 304), (735, 304), (849, 418), (849, 582), (735, 696), (588, 696)],
                [(702, 437), (702, 563), (588, 500)],
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "mitakuyame:": {  # yumi:'s two sides, unchanged, hooked into each other: each one's upper or lower arm rests inside the other's opening, 76 EM clear, never touching - relation as what the persons are; one arm of each stays free.
        "core": {
            "polygons": [
                [(525, 618), (378, 618), (264, 504), (264, 341), (378, 225), (525, 225), (525, 305), (412, 305), (344, 373), (344, 470), (412, 538), (525, 538)],
                [(475, 695), (588, 695), (656, 627), (656, 530), (588, 462), (475, 462), (475, 382), (622, 382), (736, 496), (736, 659), (622, 775), (475, 775)],
            ],
        },
        "tongue": "Lakota", "domain": "relation+position", "mclass": "structural",
    },
}
