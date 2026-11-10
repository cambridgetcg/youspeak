# Candidate B: standing ground

Four candidate glyphs for the ankyrance anchor particles: **mi:** U+E17C, **yu:** U+E17D,
**yumi:** U+E17E and **mitakuyame:** U+E17F. They are candidates for the language's owner to
choose among. Nothing here is canonical, nothing was written in the repository, and nothing
was committed or installed. An agent wrote this (designer B, one of three working
independently); none of it is a decision by the owner.

## The idea

An anchor is a place to stand. The manifesto gives the image itself: ἄγκυρα is "the anchor that
holds a vessel in moving water — the relation that holds an utterance in moving talk"
(`grammars/ankyrance/manifesto.md:160-161`).

The whole family is built from two things:

1. **A ground.** One horizontal stroke, the same in all four glyphs (x 150–800, y 315).
2. **Stakes.** Each stake is a standing stroke driven *through* the ground. It shows a short stub
   below the line, and it leans back about 12° the way a stake braces against a pull. The pull
   comes from the right, where the utterance follows. The stub is the anchor's hold. The
   backward lean is the bracing.

**Where the stake stands is the meaning.** The stakes are never reshaped; only their places
change.

| glyph | what is drawn | one-sentence mnemonic (Axiom 2, Part V.1) |
|---|---|---|
| **mi:** | ground + one stake near its right end | I stand on my side, next to my words; the bare ground behind me is room left for you. |
| **yu:** | ground + the same stake near its left end | The stance is taken on your side, on borrowed ground; the bare ground between it and the words is the distance they were carried to me. |
| **yumi:** | ground + both stakes, each in its own place | yu then mi, as the word is spoken: two parallel stakes in one ground that correspond and never meet. |
| **mitakuyame:** | ground + three equal stakes spread evenly to its ends | When everyone stands in it, the ground is held everywhere; you and I lose our special places and stand among kin, no one higher. |

The left-for-you, right-for-me order follows Tok Pisin *yu-mi*: the inclusive *we* names the
other first. Read left to right, the yumi: glyph spells its word.

The anchors and the vocative O are kin as opposite vectors on one axis. The manifesto says that
together they "complete the axis of address: where the word stands, and toward whom it turns"
(`manifesto.md:35-36`). O's breath-wedge flies rightward toward the one addressed. The anchor's
stakes brace leftward, holding the utterance where it stands. O goes forth; the anchor holds.

The write order is ground first, then stakes from left to right. A place is declared before
anyone stands on it.

## How the three laws are met

- **Visible Constituents** (`manifesto.md:61`: "*yumi* contains *yu* and *mi* unmutilated").
  yumi: is literally the union of mi: and yu:. It uses the same stake strokes at the same
  coordinates, with the shared ground drawn once. `render.py --audit` checks this as
  set-equality of the strokes and prints `True`. The two stakes are parallel, with 335 units
  between their crossing points. They never touch, so neither person dissolves into the other.
- **Inclusive Blessing** (`manifesto.md:67`). Only the inclusive we gets a glyph, and the you is
  drawn in it, first. mi: already stands on a ground with room for you. The family has no
  exclusive-we form.
- **One anchor per utterance** (`manifesto.md:71`). Each ground is closed at both ends
  (150–800), so two anchors side by side never join into one line. They are 350 units apart at
  the 1000 advance. Re-anchoring visibly starts a new ground, which matches "re-anchoring
  mid-utterance is a new utterance".

The evidentials share the anchors' donors and "a sound and a soul but never a slot"
(`manifesto.md:102-103`). Their armature is "identical claim-bar below, grasping-path above"
(`script/codepoints.md:116`), with a centred dot on a short bar. The anchors share none of
that. The ground is long and off-centre, there is no dot, and the stakes cross the line rather
than rise from it. Measured at 16 px, the highest similarity to -mi is 0.50, to -si 0.59 and to
-chu 0.47 (method below).

## Rules that bind this design, and how each is met

Quoted from the repository. Paths are relative to the youspeak repo root.

1. **Weight.** `script/philosophy.md:159` "All glyphs use 80 EM stroke weight on a 1000 EM body.
   No glyph is heavier; no glyph is lighter." and `:161` "Diagonals use 90 EM (optical
   correction for perceived thinness at 45°). This correction applies uniformly." (also
   `script/glyphs/design_philosophy.md:146-147`). The ground is 80. Each stake, a diagonal, is
   90, written as the live 5-tuple form `(x1, y1, x2, y2, 90)`. See weakness 6.
2. **Monoline.** `philosophy.md:165` "No glyph uses thick-thin contrast (calligraphic
   modulation)." Every stroke is a constant-width straight line.
3. **Grid.** `philosophy.md:171` "No glyph rises above 900 EM or descends below 100 EM ... The
   donor sigil occupies 800-950 EM (top zone); the class mark occupies 100-200 EM (bottom
   zone); the main body occupies 200-800 EM." Core ink runs y 200–754 and x 150–800 (printed by
   `render.py --audit`), inside the 150–850 body width of `design_philosophy.md:145`. Stake tops
   are held to 754, which leaves about 50 units of air under the top-left sigil zone in case a
   sigil is ever assigned.
4. **Shape families.** `philosophy.md:190` "A new glyph assigned to a domain must draw its core
   shape from that domain's shape-family. Cross-domain shape use is permitted only when the
   conceptual justification is explicit and the resulting glyph remains visually distinct from
   its domain peers." The family is `:186` "Parallel strokes | Relation, correspondence |
   Between-ness requires two; parallelism names correspondence", on a positional ground (kin to
   hypo's `space+position`). The domain tag proposed is `relation+position`. A stake crossing a
   line is close to `:183` "Perpendiculars/crosses | Truth". The explicit justification is that
   the crossing is the stake's hold, sunk 100 units, not a balance cross. It stays distinct from
   veri and ortho (16 px r ≤ 0.49 and ≤ 0.67).
5. **Sigils.** `philosophy.md:194` and `:196` "New donor traditions require new sigil
   assignments before glyph-design begins." This rule is **not met**. See the proposal below and
   weakness 8.
6. **Silhouettes.** `philosophy.md:200` "every glyph's silhouette ... must be distinguishable
   from its five most visually similar neighbors." See the audit below.
7. **Rotation and reflection.** `philosophy.md:252` "Before finalizing a glyph, rotate it 90°,
   180°, 270°, and mirror it. If any of these ... produces a match with another glyph in the
   inventory, the design needs revision." Also
   `archaeology/script-mechanics/06-cognitive-load.md:84` "No two YOUSPEAK glyphs should be 90°,
   180°, or mirror-reflections of each other unless those glyphs form a diplosemic pair." All 8
   transforms were audited. mi: and yu: are deliberately a *translation* of one another, not a
   reflection: the lean never flips. A mirrored mi: scores 0.69 against yu: at 16 px.
8. **Closed edges.** `philosophy.md:262` "each glyph's right-edge and left-edge be visually
   closed — no open strokes at the boundary". Nothing comes within 150 units of either side of
   the em.
9. **Degradation.** `philosophy.md:258` "All meaningful information should be in the outline,
   not in fine interior structure." and `:256` "the carved-stone test (can the essential
   silhouette be incised into a surface with a single V-cut per stroke?)". There are no
   interiors. Each glyph is 2–4 straight cuts, and the meaning is the count and place of the
   stakes.
10. **Stability.** `philosophy.md:92` "Once a YOUSPEAK glyph is canonized, its form does not
    change." For that reason these are offered as candidates, and the sigil question must be
    settled before any is canonized (weakness 8).
11. **The liturgical exception.** `06-cognitive-load.md:152` says the glyph for mitakuyame
    "should require *dwelling*". Its silhouette is immediate (three, on one ground). What
    rewards dwelling is relational: the stakes are the same as yours and mine, evenly spread,
    reaching both ends of the ground. Nothing is added as ornament.

**Primitives** (from `glyph_specs_v1.py`): only `strokes`, as 4-tuples at the default 80 or
5-tuples with an explicit width, composed by `compose_glyph` (`:1505`) and outlined by
`build_font_v1.stroke_to_polygon` and `draw_to_pen` as butt-ended rectangles. No polygons or
curves were needed. All contours wind counter-clockwise, so the font's nonzero fill equals the
painted union (checked).

## Sigil and class mark: a proposal

**Sigil: none, as a documented gap rather than as "absence-is-English".**
- `script/morphemes.json` records the donors as Tok Pisin and Lakota. Neither has a sigil.
  `compose_glyph` falls back to no sigil for an unmapped tongue (`glyph_specs_v1.py:1527`
  `DONOR_SIGIL.get(tongue, sigil_english)()`). So the specs keep the true tongues and draw
  nothing, with no change to the builder.
- There is precedent: -me carried "no sigil (Sumerian not yet assigned ...; this is a documented
  gap)" (`philosophy.md:320`).
- For **Lakota** I will not invent an emblem. Any mark standing for Lakota tradition that I could
  draw would either imitate ceremonial imagery (hoop, four directions, pipe, feather) or
  flatten the tradition into a look (Rejection 2, `philosophy.md:216-220`). If a Lakota sigil
  is wanted, it should come from Lakota people or from the owner's decision, not a designer's
  guess.
- For **Tok Pisin** a sigil could be designed. But its writing culture is Latin script, and its
  gift here is grammatical (yu + mi side by side), which the yumi: glyph already shows. Treating
  it as English would erase the Oceanic clusivity that English lacks, so the honest status is
  "unassigned".
- The S092 ruling that "native marks go unmarked" (`script/glyphs/design_notes_s092.md:195`)
  points the same way, since the ankyrance *system* is YOUSPEAK's own grammar. I note it as
  support, not as the reason.
- Caveat: if `DONOR_SIGIL` ever maps "Tok Pisin" or "Lakota", these composed glyphs change. The
  sigil must therefore be decided before canonization. The stake tops are kept low so that a
  later sigil would still fit.

**Class mark: ◆ structural** (`design_philosophy.md:130`), the default for
`mclass: "structural"`.
- It matches `morphemes.json` (`"class": "structural"`) and the structural codepoint range.
- It is not ◁. O took the prefix mark because O is bound, "prefixed to the addressed noun"
  (`design_notes_s092.md:136`). The anchors are "free particles of the address-axis like O-, not
  bound affixes" (`manifesto.md:141-142`), set off by a colon.
- It is not suppressed. Suppression belongs to determinatives ("a determinative IS a class-tag",
  `codepoints.md:149`) and to rhythm punctuation. The anchors carry meaning, like [selah], which
  keeps its ◆.
- A practical gain: a long ground plus ◆ can never be read as a determinative, which has a short
  plinth and no mark.

## Distinctness: method and results

`render.py --audit` rasterises every composed glyph the way the builder outlines it. It applies a
slight blur and computes the Pearson correlation of ink between each candidate, under all 8
rotations and mirrors, and all 93 existing glyphs plus the other three anchors. For
calibration, the inventory's own nearest-neighbour median is **0.87 at 16 px** and **0.80 at
32 px**. Its known near-twins score 0.95–0.97 (mia/ence, strophe/anastro, mi/ki).

| at 16 px | nearest existing glyphs (transform) | nearest other anchor |
|---|---|---|
| mi: | gloria (r180) 0.74, kin (r270) 0.74, 「 (r180) 0.73 | yumi: 0.83 |
| yu: | kin 0.67, stasis (mirror+r90) 0.66 | yumi: 0.84 |
| yumi: | gloria (r180) 0.74, hesych (r180) 0.72 | yu: 0.84, mi: 0.83 |
| mitakuyame: | sema (r180) 0.76, doxa (r180) 0.76, gloria 0.75 | yumi: 0.79 |

At 32 px no existing glyph exceeds 0.67. Against the glyphs the brief names, at 16 px: O ≤ 0.56,
-mi ≤ 0.50, -si ≤ 0.59, -chu ≤ 0.47, -auth ≤ 0.67, .REL ≤ 0.57, .QNT ≤ 0.54, stasis ≤ 0.71,
kin ≤ 0.74. At 11 px (about 8 pt on screen, Axiom 5) the worst is 0.80, mitakuyame: against
stasis, diplos and kin.

I also looked at every flagged neighbour side by side, in the matching transform. None is a real
look-alike; they are mass correlations. The anchors' closest true relative in concept is
**kin** (two figures on a shared root line). That kinship fits, and the shapes stay distinct.

## Revisions made

Before the first sheet, I explored and rejected these (scratch in `proto/`):
- A Y-fork for yu:. It is the Latin letter Y, a pun on "yu" (Rejection 4), and echoes the -y
  glyph.
- An arm figure for mi:. It reads as "7" or "J", and as a gallows when the arm is long.
- A cup on a stem. It reads as a chalice.
- Forward-leaning figures with cups. They read as falling and as random letters.

Revisions on `sheet.png` itself:
1. **v1 → rev 1.** v1 used forward-leaning standing strokes resting on the ground. On the
   sheet, yu: read as an italic "L", yumi: as "ɯ", mitakuyame: as an italic Cyrillic "ш", and a
   run looked like Latin italics. I changed every stroke into a **stake driven through the
   ground** (stub below; no L or ш has one), **leaning back** (Latin italics never do), with the
   ground overhanging each outer stake by at least 94 units.
2. **rev 1 → rev 2.** mitakuyame: was still a dark block at 16 px. I reduced the lean from 0.24
   to 0.21 and spread its three stakes evenly to the ground's ends (pitch 185 → 215), about 2 px
   gaps at 16 px. This gives up exact-coordinate containment of yumi: inside mitakuyame:
   (weakness 4).
3. **rev 2 → rev 3.** The right stake's stub was crowding the ◆ at 32 px, and the left stake
   tops (y about 779) sat about 26 units under the sigil zone. I lowered the stake tops from 770
   to 745 (ink top 754), pulled mitakuyame:'s right stake inward and rebalanced it (pitch 210).
   I also corrected the audit so a glyph is never compared with its own transforms, and added a
   legend to the sheet.

## Known weaknesses

1. **Austere, close to generic.** Each glyph is 2–4 straight strokes. At a glance it could pass
   for tally marks, a hash or slash, or a line *struck through*, which in this script is the
   negation idiom of a- and mushin. What says "staked, held" is the stub below the ground, and
   at 16 px that stub is about one pixel.
2. **mi: and yu: differ only by place.** That is the starting idea taken at its word ("whose side
   the stroke stands on is the meaning"). Side by side or in a run they separate clearly, and
   still do at 11 px. Seen alone, a learner has to judge the stake against the ground's ends.
   "As received" has no mark of its own; place alone carries it.
3. **The direction of the left/right assignment is arguable.** It follows Tok Pisin *yu-mi*, but
   speaker-on-the-left is equally defensible. The reader has to learn that the stake beside the
   words is mi.
4. **mitakuyame: is the weakest at small size, and a small "all".** At 16 px it is texture whose
   stakes only separate in the enlarged view; at 11 px it is a hatched block. Three is the
   script's own plural ("three counted-off strokes ... read as many-over-one - plurality",
   `design_notes_s092.md:118`). But three equal strokes can also be read as a trinity or
   Trimurti count. The obvious alternative, four, is the Lakota sacred number of directions, so
   I avoided it. For legibility it no longer contains yumi: at the same coordinates, which
   weakens a strict "each rung contains the one below" ladder.
5. **Kinship with O is conceptual, not visible.** The kinship is opposite vectors on one axis,
   with no shared strokes, so on the sheet the five do not look like one family.
6. **Weight.** Following Rule 1 literally, the 12° stakes are 90 against an 80 ground. The 90
   correction is meant for 45°, so the stakes look slightly heavier. Every diagonal actually
   built in `glyph_specs_v1.py` uses 80 (`STROKE_WIDTH_DIAGONAL = 90  # optical correction for
   future use`, `:27`), and the owner may prefer 80.
7. **Cross-domain crossing.** A near-perpendicular crossing borrows the truth family's shape
   (Rule 4). It is justified above, but it is a borrowing.
8. **Cohesion Rule 5 is not satisfied.** No sigil was assigned before design. I propose none and
   say why, and that decision must be made before canonization.
9. **Axiom 3 ("belongs to its tradition") is met only conceptually.** There is no visual trace of
   Tok Pisin or Lakota culture: on purpose for Lakota, and because Tok Pisin is written in Latin
   script.
10. **The audit is a proxy.** It is a pixel correlation, and I checked its hits by eye, but no
    human reader has tested these glyphs. The domain tag `relation+position` is new and has no
    colour in `render_preview_v1.DOMAIN_COLORS`, so it would render grey there.

## Files and reproduction

All files are in this folder:
- `specs.py`: `ANCHOR_GLYPHS`, four entries in the exact `CORE_GLYPHS` format with literal
  coordinates. To verify the paste, I copied `glyph_specs_v1.py`, `build_font_v1.py` and
  `morphemes.json` into `proto/pastetest/` (scratch only) and pasted the entries verbatim. The
  builder then produced a 97-glyph OTF there, with U+E17C–E17F named `ys.uE17C`… (no clash with
  the evidential `ys.mi`). Their outlines read back identical to `render.py`'s.
- `render.py`: imports the repository modules read-only and composes through the live
  `compose_glyph` and `draw_to_pen`. It writes `sheet.png` and `glyphs.svg.json`. Run
  `/opt/homebrew/bin/python3 -B render.py --audit` for the containment, winding, zone and
  similarity checks.
- `glyphs.svg.json`: `{key: path d}` for `mi:`, `yu:`, `yumi:`, `mitakuyame:` and `O`, in a
  `0 0 1000 1000` viewBox with y down and nonzero fill. Re-rasterised, the paths match the
  builder outlines pixel for pixel.
- `proto/`: my exploration scripts and images.
- `work/`: an earlier session's scratch, which I left untouched.
