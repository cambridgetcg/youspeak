"""Candidate glyphs for the four ankyrance anchor particles (U+E17C-E17F).

Designer B, starting idea STANDING GROUND. CANDIDATES ONLY: nothing here is
canonical until the language's owner chooses.

The four entries below are in the exact format of CORE_GLYPHS in
script/glyphs/glyph_specs_v1.py (literal coordinates, no helper calls), so
they can be pasted into that dict unchanged. Coordinates are font units on
the 1000-unit em, y pointing UP, exactly as in CORE_GLYPHS.

Composition by the live builder (compose_glyph):
  - tongue "Tok Pisin" / "Lakota" are the donors recorded in
    script/morphemes.json. Neither is in DONOR_SIGIL, so compose_glyph falls
    back to sigil_english() and draws no sigil. That is the proposal (see
    rationale.md): no sigil, pending the owner's decision.
  - mclass "structural" adds the small diamond class mark at bottom-right.
"""

ANCHOR_GLYPHS = {
    "mi:": {  # One stake driven through a shared ground on its right side, leaning back to hold what follows - I stand on my side; the open ground behind me is room left for you.
        "core": {
            "strokes": [
                (150, 315, 800, 315),
                (682, 210, 570, 745, 90),
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yu:": {  # The same stake on the left of the same ground - the stance is taken on your side, on borrowed ground; the bare ground between it and the words is the distance they were carried.
        "core": {
            "strokes": [
                (150, 315, 800, 315),
                (347, 210, 235, 745, 90),
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "yumi:": {  # Both stakes, whole and in their own places, in one ground - yu then mi as the word is spoken; parallel, so they correspond and never merge.
        "core": {
            "strokes": [
                (150, 315, 800, 315),
                (347, 210, 235, 745, 90),
                (682, 210, 570, 745, 90),
            ],
        },
        "tongue": "Tok Pisin", "domain": "relation+position", "mclass": "structural",
    },
    "mitakuyame:": {  # The ground held everywhere: three equal stakes evenly spread (the script's plural) - you and I lose our privileged places and stand among kin; no one higher, no one outside.
        "core": {
            "strokes": [
                (150, 315, 800, 315),
                (312, 210, 200, 745, 90),
                (522, 210, 410, 745, 90),
                (732, 210, 620, 745, 90),
            ],
        },
        "tongue": "Lakota", "domain": "relation+position", "mclass": "structural",
    },
}
