# Anchor particles — designer C: the bond first

Candidates only. A canonized glyph never changes (`script/philosophy.md:92`),
so these are drawn for the language's owner to choose from, alongside the other
designers' sets. Nothing here was written into the repository.

Files in this folder:

- `specs.py`: `ANCHOR_GLYPHS`, four entries in the exact `CORE_GLYPHS` format.
  A paste into a scratch copy of `glyph_specs_v1.py` imports cleanly, with 97
  glyphs, and every key has its codepoint in `morphemes.json`.
- `render.py`: run it as `/opt/homebrew/bin/python3 -B render.py`. It imports R
  read-only and composes each glyph through R's own `compose_glyph` and
  `build_font_v1.draw_to_pen`. It checks the Visible Constituents law
  mechanically, then draws `sheet.png` and writes `glyphs.svg.json`.
- `sheet.png`: row one is the four anchors at large size plus `O`. Row two is the
  same five at 32 px and 16 px. Below that, the five appear in a line at each
  size, and the 16 px line is repeated with each pixel enlarged 6×.
- `glyphs.svg.json`: the keys are `mi:`, `yu:`, `yumi:`, `mitakuyame:` and `O`.
  Each value is an SVG path `d` for `viewBox="0 0 1000 1000"` with y pointing
  down. It is the composed outline (core, sigil and class mark) exactly as the
  builder emits its contours. Overlapping contours share one orientation, so
  the default `fill-rule="nonzero"` shows their union.

---

## The idea

The idea is to draw **yumi: first, as two people holding each other with a
hook grip**: one hand palm up, one palm down, fingers hooked. Neither hand can
let go alone, and neither hand closes on the other.

- **yu:**, the other, is an upright figure with its floating head-dot. Its foot
  runs out into an **open half-octagon bowl** (the vocabulary of O's mouth-arc,
  turned up into a vessel). The bowl's rim rises toward where the I will be.
- **mi:**, the I, is an upright figure with its head-dot. At shoulder height it
  **reaches over and lets its hand down**.
- **yumi:** hooks the two together. yu's rim rises inside mi's reach, and mi's
  hand hangs inside yu's bowl. No stroke touches another: each person is within
  the other's side, and both stay whole. Between them a white path, the seam,
  runs unbroken from the top-left to the bottom-right of the glyph.
- **mitakuyame:** is the same joining, opened outward. The arm, hand, floor and
  bar meet exactly as in yumi:. But each person's closed outer side (the post
  that shut the bowl or the reach on their own side) is gone. The floor now runs
  out past where yu stood, and the reach runs out past where mi stood. Both heads
  stay exactly where they were. The hold that was closed around two now opens
  toward everything beyond them.

The halves were derived from the bond. They were not designed first. **yu: and
mi: are yumi:'s left and right halves translated whole, point for point.**
`render.py` checks this literally: yu: is yumi: shifted −105, and mi: is yumi:
shifted +137. Each is then optically centred on its own em.

One-sentence keys (`philosophy.md` Part V.1):

- **mi:**: "I stand on my side, and the reach I offer comes down open, an offer
  and not a grip."
- **yu:**: "Your side, as I receive it: a bowl held open, never closed over."
- **yumi:**: "Your bowl rises into my reach, and my hand rests in your bowl: each
  is within the other, touching nowhere."
- **mitakuyame:**: "The same hold with its walls opened: what held two now opens
  to all."

Why a hook: the chapter's name is ἄγκυρα, the anchor, from the PIE root *ank-*,
"to bend". An anchor is a bent thing that holds, and the manifesto calls it "the
relation that holds an utterance in moving talk". A hook that holds without
closing is the anchor reduced to its relational act. It is rung 3: the form
recalls hands and hooks without picturing either.

Why yu: is on the left: Tok Pisin says *yu-mi*, you first. In a left-to-right
line the left is where the utterance starts, so yumi: seats the other at the
speaking origin. The manifesto says "its very first breath already seated the
other party inside the speaking position" (`grammars/ankyrance/manifesto.md:123`).

## How the laws are met (`grammars/ankyrance/manifesto.md`)

1. **Visible Constituents** (lines 61–66): *"yumi contains yu and mi
   unmutilated, as 我 survives inside 我哋 … A we-word that dissolves its members
   is not YOUSPEAK."* This design meets the law in the strictest sense: yumi:
   contains the yu: and mi: polygons unchanged, every point translated (checked
   in `render.py`). The two are hooked and never touch, which is what line 64
   asks for: "maximal depth of relation while preserving distinct identity". The
   donor survey says the same of the Tok Pisin word: "the two pronouns of the
   dyad standing side by side, both fully visible" (`archaeology/tok-pisin/yumi-and-clusivity.md:25`).
   The heads are level, because a we in which the I stands taller would draw a
   domination.
2. **Inclusive Blessing** (line 67): there is a glyph only for the we that
   includes you. Drawing yumi: as the you and the I hooked together makes the
   inclusion structural. No exclusive form (*mipela*) is drawn, and none should be.
3. **One anchor per utterance** (line 71): each anchor is one codepoint and one
   self-contained glyph. Its strokes stay inside x 170–850, with no open stroke at
   the side-bearings, so it sits at the threshold of an utterance and cannot fuse
   with what follows.

## Cohesion and design rules that bind this design

- **Rule 1, invariant weight** (`script/philosophy.md:159`): *"All glyphs use 80
  EM stroke weight on a 1000 EM body. No glyph is heavier; no glyph is
  lighter."* Every stroke here is a mitred 80 EM outline.
  Line 161 also says *"Diagonals use 90 EM … This correction applies
  uniformly"*. The live generator has not implemented it (`glyph_specs_v1.py:24`,
  "not implemented"), and O's chamfers are 80. These chamfers are therefore 80 as
  well, so that they match every other diagonal in the font today. If the
  correction is ever applied across the font, it applies here too.
- **Rule 2, monoline** (`philosophy.md:165`): there is no thick–thin contrast.
  The square head-dots are the font's dot idiom (`dot()`, "dots as squares").
- **Rule 3, zones** (`philosophy.md:171`): *"No glyph rises above 900 EM or
  descends below 100 EM … the class mark occupies 100–200 EM … the main body
  occupies 200–800 EM."* The body sits between y 230 and 680. The head-dots rise
  to 860: under the 900 ceiling but above 800, as dhikr (845), chul (835) and
  sukh (829) already do. They keep 35 EM clear of the top-left sigil zone
  (x 110–190), so a sigil can be added later without redrawing. The lowest
  stroke edge is 230, and mi:'s foot keeps 60 EM above the ◆.
- **Rule 4, shape families** (`philosophy.md:190`): *"A new glyph … must draw its
  core shape from that domain's shape-family."* The domain is
  `relation+position`. The family is relation, "two shapes interacting"
  (`design_philosophy.md:115`), and the reception arc comes from *"Vessels/arcs |
  Reception, carrying | The cup, the hand"* (`philosophy.md:188`). Even mi: and
  yu: alone are relational shapes: each is a person whose reach is half of a
  grip.
- **Rule 5, sigils** (`philosophy.md:196`): *"New donor traditions require new
  sigil assignments before glyph-design begins."* See the sigil proposal below.
- **Rule 6, silhouette** (`philosophy.md:200`): each glyph *"must be
  distinguishable from its five most visually similar neighbors"*. The rotation
  check (`philosophy.md:252`): *"rotate it 90°, 180°, 270°, and mirror it. If any
  … produces a match with another glyph in the inventory, the design needs
  revision."* The mirror-pair rule (`archaeology/script-mechanics/06-cognitive-load.md:84`):
  *"No two YOUSPEAK glyphs should be 90°, 180°, or mirror-reflections of each
  other unless … a diplosemic pair."* This rule shaped the whole design. A hook
  grip between two identical hooks makes mi: and yu: 180° rotations of each
  other, which is the b/d trap. The pair escapes it because both heads sit on
  top (both people stand upright) while one hand reaches from below and the
  other from above. No rotation or mirror maps yu: onto mi:.
- **Compound clarity** (`philosophy.md:262`): *"each glyph's right-edge and
  left-edge be visually closed"*. mitakuyame:'s opened floor and bar stop at
  170 and 830, inside the inventory's own range (haqq's slab runs 150–850).
- **Graceful degradation** (`philosophy.md:258`): *"All meaningful information
  should be in the outline."* The grip is outline, not interior detail. See the
  16 px weakness below.
- **Joints and dots** (`design_philosophy.md:148–149`): mitred at 90°, as the
  S092 corner brackets do with single polygons. The heads are 110 square (dot
  diameter 100; the -si dots are 110–124).
- **Person-marker** (`design_notes_s092.md:106`, `:122`): *"the floating
  head-dot is the family's person-marker, shared with det-rel."* The persons
  here use that marker. They are not borrowed from anywhere else.
- **Kin to O, distinct from O.** O is a half-octagon mouth-arc with a breath
  wedge (`design_notes_s092.md:136`). yu:'s bowl is that half-octagon turned up
  into a vessel. Measured against O: mi: 0.40, yu: 0.45, yumi: 0.48,
  mitakuyame: 0.35.
- **Not the evidential armature.** The evidentials are vertical: a witness
  above, a path, a claim-bar below. The anchors are lateral: persons side by
  side on one ground, with no claim-bar. Measured against -mi: mi: 0.54, yu:
  0.42, yumi: 0.46. Against -chu: mi: 0.52. Against -si: mi: 0.73, the closest
  evidential (see weaknesses).

## Sigil (proposal): none drawn now; tongue recorded truthfully

The entries carry `"tongue": "Tok Pisin"` and `"tongue": "Lakota"`, as
`morphemes.json` and `codepoints.md:142–145` record them. Neither tongue is in
`DONOR_SIGIL`, so `compose_glyph` falls back to no sigil
(`glyph_specs_v1.py:1527`). The metadata stays true, and the corner stays empty
until a sigil is assigned. Reasons:

- Rule 5 asks for an assignment, and an assignment is the owner's decision, not a
  candidate designer's. Tok Pisin is written in Latin letters and has no script
  of its own to trace, so any sigil would be invented. For Lakota, the obvious
  visual sources sit close to ceremonial imagery. That decision should be made
  with Lakota people, not by a type designer (Rejection 2, `philosophy.md`
  Part IV).
- The four must read as one ladder. A Tok Pisin mark on three and a Lakota mark
  on one would divide the family at its only shared corner.
- The anchor system is a native YOUSPEAK grammar assembled from four donors.
  The S092 designers ruled that "native marks go unmarked"
  (`design_notes_s092.md:195`).
- The cost is stated as weakness 9.

## Class mark (proposal): ◆ structural

`mclass: "structural"` composes R's ◆ at bottom-right (`design_philosophy.md:130`).
O- took ◁ because the chapter treats it as **bound**, "prefixed to the addressed
noun" (`design_notes_s092.md:136`). The anchors are explicitly *"free particles
of the address-axis like O-, not bound affixes"*
(`ankyrance/manifesto.md:141–142`). Their codepoints sit in the structural
range, and the worship-grammar precedent [selah] keeps its ◆. The alternative is
◁, read as "begins" because the anchor opens the utterance. ◆ is preferred
because the anchors are not attached to anything.

## Distinctness audit (method and numbers)

Method: every glyph is rasterized at 16 px (and at 24 px) from its composed
outline, then blurred by σ 0.6 px. The score is the normalized correlation
against every one of the 93 existing glyphs, taking the best of the 8
rotations and mirrors. As a baseline, each existing glyph's nearest-neighbour
score has a median of **0.865** (quartiles 0.83–0.92; the highest pairs, such
as strophe/anastro and mia/ence, reach 0.967).

| candidate | nearest five at 16 px (score, transform) |
|---|---|
| mi: | kin 0.80 (rot180) · 」 0.75 · si 0.73 · gloria 0.69 · en 0.69 |
| yu: | 「 0.73 · kin 0.68 · jamal 0.65 · morphe 0.65 · hesych 0.64 |
| yumi: | sukh 0.72 · kavod 0.66 · kairos 0.66 · phanes 0.65 · brahman 0.62 |
| mitakuyame: | mushin 0.69 · parallax 0.65 · me 0.65 · si 0.64 · qing 0.63 |

Within the family: mi:~yu: 0.66 · mi:~yumi: 0.52 · mi:~mitakuyame: 0.54 ·
yu:~yumi: 0.51 · yu:~mitakuyame: 0.42 · yumi:~mitakuyame: 0.73.

All four, and every pair within the family, score below the inventory's median
nearest-neighbour score. The metric is crude. It is evidence that no candidate
duplicates an existing silhouette, not a reading test.

## Revisions made (each after looking at the rendered sheet)

Exploration rejected these forms before the first sheet:

- Point-symmetric hook pairs: yu: and mi: became 180° rotations of each other.
- Bare ∪ and ∩ halves: mi: scored 0.85–0.92 against stasis and diplos.
- A version where mi:'s head stood 165 EM above yu:'s, drawing a hierarchy into
  yumi:.
- For mitakuyame:: a closed loop of two hooks (it reads as a hoop, too near
  the Sacred Hoop described in the Lakota survey, lines 70–81). Keeping mi:
  whole with the you opened (0.86 to yumi:). A doorway-gap version (0.88). The
  two figures side by side and turned outward. That last one has no interlock,
  so it reads as mi: and yu: typed next to each other, which is a real
  ambiguity in running text.

1. **Revision 1** (first sheet):
   - mi:'s foot stood 40 EM above yu:'s floor. It now shares the ground line.
   - yu:'s head was 5 EM from the sigil zone. Both heads moved 35 EM inward.
   - The floor centreline went from 200 to 270, so its edge clears the class-mark
     band and mi:'s foot clears the ◆ by 60 EM.
2. **Revision 2** (FreeType rendering of a throwaway font built with R's
   builder into a scratch folder, magnified):
   - At 16 px the 45 EM head gaps closed, yu: read as "ı", and yumi:'s inner
     channels (90–110 EM) went grey.
   - Head gap raised to 70 EM.
   - The grip's uprights moved to 230/430/610/810, giving channels of
     120/100/120 EM.
   - Heads set 50 EM inward. Each person now leans slightly toward the other,
     and the sigil zone is cleared by 35 EM.
3. **Revision 3**:
   - yu: and mi: sat 51 and 34 EM off centre by ink. Each is now shifted halfway
     to its centroid (optical centring), still a pure translation of yumi:'s
     halves.
   - The sheet gained a 6× pixel view of the 16 px line, so small-size
     legibility can be judged from the sheet itself.

## Known weaknesses

1. **mitakuyame: is where the idea strains.** Opening the joining outward costs
   each person the post that was their body. Both heads stay where they stood,
   and the grip is identical, but the persons are no longer drawn whole. That is
   a real tension with Law 1, which applies to "any union-form", and the widest
   we is one. It sits against the Lakota teaching that you *are* your relations.
   I chose to show the tension rather than hide it. This is the best honest
   version I found of "the same joining opened outward" that keeps the interlock
   and both persons and stays legible at 16 px.
2. mitakuyame: shows "all" by **openness**, not by plurality. A reader has to
   learn that the opened holds mean the unbounded web. With the posts removed,
   the two level heads over the open grip can read as a face.
3. Two pairs are the closest in the set: mitakuyame:~yumi: (0.73) and mi:'s
   nearest existing neighbour (kin, 0.80 rotated 180°). mi: also sits 0.73 from
   the evidential -si. That is under the median, but -si is one of the glyphs
   the brief warns about, and an owner should look at the two side by side.
4. **At 16 px the seam is the first thing lost.** yumi:'s channels render near
   1.6 px and turn grey, so at that size yumi: reads as "two persons with a dense
   middle". The bond itself survives only at 24 px and up.
5. The head-dots rise to 860, making these the tallest marks in the font, and
   above the 800 main-body line. They are within the 900 ceiling.
6. yu: and mi: alone are asymmetric figures (one post on one side). They are
   balanced dynamically and optically centred, not symmetric. At small sizes
   they can recall letters: mi: like "ṅ", yu: like "ὐ".
7. mi:'s hand descends from shoulder height into yu:'s bowl. Level heads and a
   shared ground answer it, but a reader may still see an "offer from above".
8. The head-dot persons push the forms toward rung 2 (a simplified picture), not
   rung 3. The precedent is .PER and .REL.
9. **Sigil absence reads as "English"** under the v1 rule (absence-is-English).
   That is half-true for yu: and mi: (Tok Pisin *yu*/*mi* come from English
   *you*/*me*) and false for mitakuyame: (Lakota plus Sumerian -me). The owner
   may prefer to assign sigils. The corner is kept clear for that.
10. The 90 EM diagonal correction from Rule 1 is not applied, matching the live
    font rather than the rule's text.
11. Placing yu: on the left (the other at the speaking origin) is deliberate,
    but readers who expect self-first may misread yumi: at first.
12. No human reading test was done. The distinctness numbers come from a
    correlation metric only.
