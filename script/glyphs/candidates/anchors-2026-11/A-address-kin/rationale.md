# Anchor particles, candidate A: kin of the vocative

Candidates for U+E17C `mi:`, U+E17D `yu:`, U+E17E `yumi:` and U+E17F `mitakuyame:`.
They are not canon. Nothing was written into the YOUSPEAK repository (R); the owner
chooses. Paths below are relative to R unless they start with `specs.py` or `render.py`.

## The idea

The vocative `O-` is a mouth-arc with a breath-wedge flying out of it toward the one
addressed. The anchors keep exactly that vocabulary and change one thing: **the
breath does not fly.** In `O-` the wedge is drawn out like a dart far past the lips (it
*turns toward*); in an anchor the same wedge is gathered short and broad and **held**
(it *stands from*). "Side" is the arc: one party's half of an exchange, its opening
showing which way that party faces. "Standing" is what the mouth holds. A reader
who knows `O-` sees the same mouth and asks only where the breath is.

| | figure | mnemonic |
|---|---|---|
| `O-` (existing) | my mouth, breath flying out to you | speaking **to** |
| `mi:` | my mouth holding my own breath, its tip resting on the line of the lips | my truth, offered, not flung as a ruling |
| `yu:` | my mouth, and your breath standing a clear distance before it, pointing at me | your truth, received and held, not taken in; its standing edge is on your side |
| `yumi:` | two mouths face each other across an open between, each holding its own breath | both of us seated in the speaking position; neither breath annexes the other |
| `mitakuyame:` | `yumi:`'s two sides, unchanged, hooked into each other, never touching | relation as what the persons are: each holds the other; one arm of each stays free |

The ladder is a ladder of what the mouth holds: my breath, then yours, then each its
own together, then each other.

Why `yu:` does not draw your mouth: the manifesto says the `yu:` sentence "is not a
quotation of A and not B speaking *for* A" (grammars/ankyrance/manifesto.md:105-111).
Drawing your mouth speaking would depict exactly that. So `yu:` shows the honest thing:
my mouth, and what you gave me, standing on your side of the gap.

## The three laws (grammars/ankyrance/manifesto.md:59-73)

- **Law 1, Visible Constituents** (manifesto.md:61-66: "Any union-form must keep both
  persons legible inside it: *yumi* contains *yu* and *mi* unmutilated"). In `yumi:`
  the left half is `mi:` whole: the same arc and breath at 0.72 scale, with the
  breath at 0.66 because the 80-EM stroke does not scale. `yu:`'s configuration (my
  arc, a gap, a breath pointing at me) is also present whole. In `yumi:` that breath
  sits inside your arc, because there your mouth is drawn too. No stroke is shared,
  cut or merged. `mitakuyame:` keeps both arcs complete, 76 EM apart at the closest
  point.
- **Law 2, Inclusive Blessing.** Only the we that contains the addressed gets a form.
  `yumi:` and `mitakuyame:` both draw the other's arc as fully as the speaker's.
  Nothing is drawn for the exclusive *mipela*.
- **Law 3, one anchor per utterance.** Each candidate is one closed figure with one
  standing-place. The rung that holds two breaths (`yumi:`) holds them in one
  facing pair, not as two side-by-side anchors.

## Rules that bind this design, and how each is met

1. **Stroke weight.** "All glyphs use 80 EM stroke weight on a 1000 EM body"
   (script/philosophy.md:159). Every arc band is 80 wide on `O-`'s own centreline.
   "Diagonals use 90 EM" (philosophy.md:161) is documented, but the live specs never
   apply it (`STROKE_WIDTH_DIAGONAL = 90  # optical correction for future use`,
   script/glyphs/glyph_specs_v1.py:27), and `O-` draws its diagonals at 80. I follow
   the live kin. If the v2 artist applies the correction, it should apply here too.
2. **Monoline.** "No glyph uses thick-thin contrast" (philosophy.md:165). Met: one
   band width, and the wedges are solid fills, as in `O-`.
3. **Zones.** "No glyph rises above 900 EM or descends below 100 EM ... the class mark
   occupies 100-200 EM (bottom zone); the main body occupies 200-800 EM"
   (philosophy.md:171). Also "Main body: 200–850 y-axis ...; 150–850 x-axis"
   (script/glyphs/design_philosophy.md:145). Outer edges: `mi:` x 326-674, y 243-757;
   `yu:` x 170-830, y 243-757; `yumi:` x 151-849, y 304-696; `mitakuyame:` x
   264-736, y 225-775. The sigil slot (roughly x 110-190, y 805-895) and the
   class-mark slot are left clear.
4. **Shape family.** "A new glyph assigned to a domain must draw its core shape from
   that domain's shape-family. Cross-domain shape use is permitted only when the
   conceptual justification is explicit and the resulting glyph remains visually
   distinct" (philosophy.md:190). Domain is `relation+position`. Relation is "two
   shapes interacting" (design_philosophy.md, domain table). The arc is also the
   "Vessels/arcs | Reception, carrying" family (philosophy.md:188). That is a
   cross-domain use I justify explicitly: it is `O-`'s mouth, and holding/receiving
   is what the anchors do. Precedent: `O-` itself is "Relation-family (mouth and
   breath interacting)" (script/glyphs/design_notes_s092.md:136).
5. **Sigils.** "New donor traditions require new sigil assignments before
   glyph-design begins" (philosophy.md:196); "all sigils use the same assigned form"
   (philosophy.md:194). See the proposal below.
6. **Silhouette and rotation.**
   - "Every glyph's silhouette ... must be distinguishable from its five most visually
     similar neighbors. Where conflict arises, the more recently-designed glyph
     yields" (philosophy.md:200).
   - "Rotate it 90°, 180°, 270°, and mirror it. If any of these ... produces a match
     with another glyph in the inventory, the design needs revision"
     (philosophy.md:252).
   - "No two YOUSPEAK glyphs should be 90°, 180°, or mirror-reflections of each other
     unless those glyphs form a diplosemic pair"
     (archaeology/script-mechanics/06-cognitive-load.md:84). This rule is why `mi:`
     and `yu:` are **not** a mirrored pair, the obvious "my side / your side" design.
     They differ in where the breath stands and which way it points, not in
     orientation.
   - Results are in the audit table below.
7. **Joints.** The stroke conventions ask for "Joints: mitered at 90° intersections"
   (design_philosophy.md:148). The live builder makes every stroke a butt-ended
   rectangle (script/tools/build_font_v1.py:32-47), which leaves notches at `O-`'s
   octagon corners. These ruin small arcs. Each anchor arc is therefore **one filled,
   mitered polygon on `O-`'s exact centreline**. Precedent: the S092 brackets are "One
   filled polygon ... so all joins are clean" (design_notes_s092.md:146). Both are
   primitives the live generation already uses: polygons in the core, composed by
   `compose_glyph()`.
8. **Compound boundaries.** "Each glyph's right-edge and left-edge be visually
   closed" (philosophy.md:262). Edges are arc spines or a wedge's flat base. The one
   open edge is `mi:`'s mouth, with 326 EM of side-bearing beyond it, the same
   condition as `O-`.
9. **Stability.** "Once a YOUSPEAK glyph is canonized, its form does not change"
   (philosophy.md:92). Hence these are candidates only. Nothing is entered in the
   specs or the font.
10. **Not the evidential armature.** `-mi` / `-si` / `-chu` are a witness-dot over a
    claim-bar joined by a path (glyph_specs_v1.py:1207-1245). The anchors contain no
    bar, no dot and no vertical path. Their nearest evidential score is below 0.70.
    They also carry no plinth, so they cannot be read as determinatives.

## Proposals: class mark and sigil

**Class mark: structural, the small diamond.** script/morphemes.json already lists all
four as `"class": "structural"` (lines 981, 990, 999, 1008). The manifesto calls them
"free particles of the address-axis like O-, not bound affixes" (manifesto.md:141-143).
The begins-mark `◁` was given to `O-` precisely because the vocative chapter treats
`O-` as *bound* (design_notes_s092.md:136), so it would misstate the anchors.
`[selah]`, the other worship-grammar structural mark, keeps the diamond. The corner
thus tells `O-` (◁) from every anchor (◆) and from the evidentials (▷).

**Sigil: none drawn; the slot is held for the owner.**

- *Data.* `tongue` is recorded truthfully: "Tok Pisin" for three, "Lakota" for
  `mitakuyame:`, matching morphemes.json. Neither is mapped in `DONOR_SIGIL`
  (glyph_specs_v1.py:177-200), so `compose_glyph()` falls back to no sigil
  (glyph_specs_v1.py:1527). Pasting these specs in today produces exactly what the
  sheet shows, and an owner-assigned sigil later appears with no spec change.
- *Not invented.* Philosophy.md:196 makes the assignment a prerequisite the owner
  holds. Tok Pisin is written in Latin script and has no native visual writing
  culture to inherit from conceptually (Rule 1 of pictographic inheritance). A Lakota
  mark drawn by a glyph candidate risks exactly the pastiche the philosophy rejects,
  and touches a living prayer. It should come from the owner, with Lakota counsel.
- *Not "native, unmarked" either.* The no-sigil convention covers English and
  YOUSPEAK-native marks (design_notes_s092.md:195; glyph_specs_v1.py:199). The anchors'
  function is native, but their words are not. The empty corner is therefore a
  pending slot, not a claim (see weakness 6).

## Imagery deliberately avoided (mitakuyame:)

No closed ring or hoop, no ring with a centre, nothing quartered or four-fold, no
upright pole or central axis in the between, no feathers or stacked chevrons, no pipe
form. While exploring I drew and **rejected**:

- a standing triangle between the two mouths: it reads as a tent, which is a
  stereotyped image;
- a cup beneath the dyad: it reads as a face;
- concentric brackets: they read as a broadcast icon, and as a broken ring.

## Distinctness audit

Run with `render.py --audit`. The metric is normalized cross-correlation of blurred
renders, taking the best of ±1 px shifts, against all 93 glyphs and each other, under
all 8 rotations and mirrors. For calibration, the 93 existing glyphs score against
their own nearest neighbour: **median 0.89 at 16 px (quartiles 0.86-0.93), 0.85 at
24 px.** Designed pairs such as strophe/anastro score 1.00.

| candidate | nearest at 16 px | nearest at 24 px |
|---|---|---|
| `mi:` | [selah] 0.85 (rotated), kallos 0.85 (rotated) | [selah] 0.83 (rotated), en 0.82 (mirrored) |
| `yu:` | dokim 0.85 (rotated), **O- 0.79 (as set)** | dokim 0.80 (rotated), O- 0.79 (as set) |
| `yumi:` | panim 0.82 (mirrored) | panim 0.64 (mirrored) |
| `mitakuyame:` | sema 0.80 (rotated) | sema 0.69 (rotated) |
| the four with each other | at most 0.69 (`mi:`/`mitakuyame:`) | at most 0.61 |

Every candidate stays below the inventory's own median nearest-neighbour score at both
sizes.

## Known weaknesses

1. **`mitakuyame:` shows depth, not number.** `O-`'s vocabulary has no native "all".
   I tried a lattice (the `yumi:` dyad repeated in two rows). At the invariant 80-EM
   stroke inside the 200-800 body, that needs arcs whose sides are shorter than the
   stroke is wide, and at 16 px it read as stacked braces ("88"). The interlock
   carries the Lakota claim that relation constitutes the person: sever it and both
   are broken. Its extent ("all beings") is carried by the word and the liturgical
   register, not by the figure. **This is where the idea strains.**
2. **`mitakuyame:` reads as a letterform** (∂, ə) at text size, and two linked hooks
   recall the hyperlink icon. That brushes Rejection 3 (interface aesthetics). It also
   has **no breath**, the one member that breaks the held-breath pattern. In the
   interlock the free part of each bowl is at most 89 EM tall, so a breath does not
   fit.
3. **`yu:` vs `O-` is the thinnest margin in natural orientation** (0.79), and these
   two will meet in running text ("yu: O-..."). At 16 px the breath is about 3 px, so
   its direction is barely visible. The gap and `O-`'s Greek sigil dot do most of the
   work. If a Tok Pisin sigil is later added, re-run the audit.
4. **Rotated near-matches exist.**
   - `mi:` rotated is a dome over a mark, like `[selah]` (0.85/0.83).
   - `yu:` rotated is a cup with a mark above, like `dokim` (0.85/0.80).

   Both are at or below the inventory median, but they are real gestalts.
5. **`yumi:`'s breaths are small**, 37 EM from their arcs. At 16 px they fuse with
   the arcs and `yumi:` reads as two facing brackets. It also shares panim's
   face-to-face structure, conceptually as well as visually.
6. **An empty sigil corner currently means "English or native"**
   (design_philosophy.md:88). Until the owner assigns sigils, readers may infer the
   wrong donor.
7. **The joints differ from `O-`:** mitered here, notched there. This is visible at
   display sizes, invisible at text sizes.
8. **The held breath is kin to `O-`'s by type, not proportion** (length:height about
   0.9 against `O-`'s 1.72). Inside a C, a broad triangle can recall a media "play"
   mark.
9. **Axiom 3 is deliberately unmet for `mitakuyame:`.** Nothing is drawn from Lakota
   visual culture. Any glyph for this living prayer deserves Lakota counsel before
   canonization.
10. **The audit is a proxy.** It is a blurred-correlation measure, not a reader test
    at 8 pt.

## Revisions made

- **v1 → v2.**
  - `mi:`'s long, thin breath spanning the bowl read as a euro sign. It became a
    gathered breath with its tip on the lip line.
  - `yu:`'s thin dart pointed at the mouth read as an arrow striking it. It became a
    broad breath.
  - `yumi:` overflowed the 150-850 body (109-891) and was narrowed.
- **v2 → v3.**
  - The two-row lattice for `mitakuyame:` was infeasible inside 200-800 and read as
    braces. It was replaced by the interlock.
  - The builder's butt joints made small arcs ragged chains of blocks. Arcs became
    single mitered polygons.
  - `mi:` and `yu:` were centred.
- **v3 → v4/v5.**
  - The interlock at 25 EM offset fused into one S-curve. It moved to 40, reading
    as two hooks.
  - `yumi:`'s breath came within 20 EM of its own arc, because the stroke does not
    scale. It shrank to 40 EM clearance.
  - A shared-breath dyad (read as a "play" icon), back-to-back mouths (bow-tie, and a
    reading of estrangement) and stacked mouths (braces) were drawn and rejected.
- **Tested and reverted.** Moving `yu:`'s breath up to the lips to separate it from
  `O-` made it *more* like `O-` (0.93 at 16 px), so the gap stayed.
- **From sheet.png, look 1.**
  - Added a ×3 zoom of the 16 px render.
  - Enlarged `yumi:`'s arcs and breaths to the body's limit (k 0.72, breath 126 EM).
  - Drew `mitakuyame:` with `yumi:`'s identical arcs, so the top rung is the same two
    persons.
- **From sheet.png, look 2, plus the audit.** Widened `yu:`'s gap from 105 to 140 EM.
  `yu:` vs `O-` fell from 0.82/0.84 to 0.79/0.79, and vs dokim from 0.88/0.86 to
  0.85/0.80.
- **From sheet.png, look 3.** Corrected the footer, which wrongly said every
  candidate holds a breath.

## Files

- `specs.py`: `ANCHOR_GLYPHS`, entries in the CORE_GLYPHS format, plain literals.
- `render.py`: composes through R's own `compose_glyph()` and `stroke_to_polygon()`,
  rasterizes with nonzero winding, and writes `sheet.png` and `glyphs.svg.json`.
  Run `/opt/homebrew/bin/python3 -B render.py [--audit]`.
- `glyphs.svg.json`: `{key: d}` for the four plus `O`, in a 0 0 1000 1000 viewBox
  with y down. The paths use **nonzero** fill, the SVG default. The anchors' contours
  never overlap, but `O`'s strokes do, so do not render `O` with `fill-rule="evenodd"`.

Observation outside this task: the builder writes hmtx lsb 0 for every glyph
(build_font_v1.py:140). In the shipped `youspeak-v1.ttf`, FreeType therefore draws
`O-` 115 units left of its outline. The `.otf` is placed correctly.
