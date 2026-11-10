---
title: Glyph design notes — ankyrance anchor particles (DRAFT — CANDIDATE, NOT CANON)
status: DRAFT. Candidate glyphs for the language's owner to choose from. Nothing here is in glyph_specs_v1.py or the font.
date: 2026-11-10
written_by: an agent (one step of a design workflow). These are proposals and evidence, not decisions.
process: 3 parallel designers (A address-kin · B standing-ground · C bond-first) → 2 judges (doctrine · confusability) → 1 revision (this file), which takes C as its base and applies or declines each judge fix with a reason. The confusability audit was re-run unchanged on the result.
codepoints: U+E17C mi: · U+E17D yu: · U+E17E yumi: · U+E17F mitakuyame:
---

# Ankyrance — the anchors drawn (DRAFT — candidate, not canon)

The four anchor particles of `grammars/ankyrance/` are the only morphemes in
`script/morphemes.json` without a drawn glyph. These are candidate glyphs for them. A
canonized glyph never changes (`script/philosophy.md:92`), so none of this should enter
`glyph_specs_v1.py` until the owner has decided the questions in `decisions.md`. Those
include the sigil, which `philosophy.md:196` puts before glyph design, and Lakota counsel for
the top rung.

The family is designer C's hook grip, revised. A person is the font's own person-marker, a
floating square head-dot over an upright post (`design_notes_s092.md:106`), together with one
gesture. The I *reaches* and the other *receives*. The reach is O-'s half-octagon mouth-arc
turned down, and the bowl is the same arc turned up. Rung 3 is the two gestures hooked, and
rung 4 is that hook with each closed side opened.

## ANCHOR PARTICLES — ankyrance (U+E17C–E17F)

### mi: (Tok Pisin · relation+position · structural)
_The I on its own side: an upright post with its head-dot, and a reach at shoulder height whose two corners are cut as O-'s mouth-arc turned down; the hand is let down open — an offer, not a grip._
The anchor that confesses its vantage at the door (`manifesto.md:121-125`): what follows is
offered from within my experience, not ruled. The body stands on the right, beside the
utterance that follows. The arm comes over at shoulder height and the hand hangs open
without closing on anything. Both top corners carry the octagon's 45-degree cut, which gives
the reach O-'s own geometry. It also keeps mi: apart from the square en- bracket it would
otherwise resemble when turned. mi: is yumi:'s right half translated whole (x −149).
**Mnemonic:** "I stand on my side, and my hand comes down open: an offer, not a grip."

### yu: (Tok Pisin · relation+position · structural)
_The other on its own side: an upright post standing on its own ground, which runs back behind it as a heel and forward into an open bowl — your side as received, held open, never closed over._
The anchor of honest reception (`manifesto.md:105-111`): your truth as I received it, held
and not annexed. The bowl is the vessel family's reception arc (`philosophy.md:188`) and O-'s
mouth-arc turned up into a cup. The post stands *on* its floor, in a T, and the floor runs on
behind it as a heel: your ground continues behind you, and when I speak from your side I
stand on ground that is yours. The heel also gives yu: a feature no turn of mi: can produce.
yu: is yumi:'s left half translated whole (x +110).
**Mnemonic:** "Your side: a bowl held open on your own ground, never closed over."

### yumi: (Tok Pisin · relation+position · structural)
_You and I hooked: yu's rim rises inside mi's reach and mi's hand hangs inside yu's bowl; no stroke touches another, a white seam runs unbroken between them; both whole, heads level._
The Law of the Visible Constituents (`manifesto.md:61-66`) drawn literally. yumi: is yu: and
mi: placed side by side, point for point, with the you first as in Tok Pisin *yu-mi*
(`archaeology/tok-pisin/yumi-and-clusivity.md:24-28`). Each gesture rests inside the other's
side: neither can slide away alone, neither closes on the other, and nothing merges. The
seam is a 100-EM white path running from the top left to the bottom right. That is
PERICHORESIS's "maximal depth of relation while preserving distinct identity". The heads are
level, because a we in which one stands taller draws a domination (`manifesto.md:121-125`).
**Mnemonic:** "Your bowl rises into my reach and my hand rests in your bowl: each within the other, touching nowhere."

### mitakuyame: (Lakota · relation+position · structural)
_All my relations: the same hold with each closed outer side opened — yu's ground runs out past where yu stood, mi's reach runs out past where mi stood; both heads, the bowl's rim and the hand stay exactly where they were._
The top of the ladder and the liturgical register. Lakota *mitákuye oyás'iŋ* teaches that
relation is prior to the self ("you *are* your relations",
`archaeology/lakota/mitakuye-oyasin-relational-cosmology.md:51-66`), and that kinship "is not
made but recognized" (`:302-303`). The glyph keeps the whole bond of yumi: (rim inside reach,
hand inside bowl, the seam unbroken) and both heads at their exact places. It opens the two
outer sides that closed each person off from beyond: yu's floor runs out to the left edge
and mi's shoulder runs out to the right. What held two is now open at both ends. Its outer
extent is exactly yumi:'s (x 155–850), so no stroke end reaches further toward the
neighbouring glyphs than yumi:'s closed posts already do (`philosophy.md:262`). It draws no
hoop, no quartering and no count of four (`:68-93`), no pipe, no feather and no tree. It
invents no Lakota emblem. This is the glyph in the set that most needs Lakota counsel before
canonization.
**Mnemonic:** "The same hold with its walls opened: what held two is open to all."
**Known tension (owner's decision, `decisions.md` §2):** the opened sides are the posts, the
persons' bodies. Law 1 asks every union-form to keep both persons legible. Here the heads
and both gestures remain but the bodies do not. Measured below: in this vocabulary, every
top rung that keeps both bodies sits closer to yumi: than 90% of existing glyphs sit to
their own nearest neighbour.

## Rules that bind this design (quoted)

- **Cohesion Rule 1** (`philosophy.md:159`): "All glyphs use 80 EM stroke weight on a 1000 EM
  body. No glyph is heavier; no glyph is lighter." Every stroke is a mitred 80-EM outline.
  The 90-EM diagonal of `:161` is "not implemented at this stage" in the live generator
  (`glyph_specs_v1.py:22-27`; O-'s chamfers are 80), so the chamfers are 80 here too, as in
  the live font.
- **Rule 2** (`:165`): "No glyph uses thick-thin contrast". Monoline, and the head-dots are
  square as `dot()` draws them.
- **Rule 3** (`:171`): "No glyph rises above 900 EM or descends below 100 EM ... the class
  mark occupies 100-200 EM ... the main body occupies 200-800 EM." All ink is within x 150–850
  and y 240–800. The head-dots top out at exactly 800, against 860 in set C. mi:'s foot clears
  the ◆ by 70 EM.
- **Rule 4** (`:190`): "A new glyph assigned to a domain must draw its core shape from that
  domain's shape-family." That is the relation family, "two shapes interacting"
  (`design_philosophy.md:115`), with the reception arc from "Vessels/arcs | Reception,
  carrying" (`philosophy.md:188`). The domain tag `relation+position` is new and unregistered
  (`decisions.md` §6).
- **Rule 5** (`:194-196`): "New donor traditions require new sigil assignments before
  glyph-design begins." No sigil exists for Tok Pisin or Lakota. The proposal is none, with
  the slot kept clear (below, and `decisions.md` §3).
- **Rule 6** (`:200`): the silhouette "must be distinguishable from its five most visually
  similar neighbors". **Part V.2** (`:252`): "rotate it 90°, 180°, 270°, and mirror it. If any
  ... produces a match with another glyph in the inventory, the design needs revision."
  **`06-cognitive-load.md:84`**: "No two YOUSPEAK glyphs should be 90°, 180°, or
  mirror-reflections of each other unless those glyphs form a diplosemic pair."
- **Part V.3** (`:258`): "glyphs with interior details that only resolve at high resolution
  fail graceful degradation." The seam is outline, not interior detail: every channel is at
  least 100 EM.
- **Part V.4** (`:262`): "each glyph's right-edge and left-edge be visually closed". The ink
  of mitakuyame: stays inside yumi:'s envelope.
- **Ankyrance Laws** (`manifesto.md:61-73`): Visible Constituents, the Inclusive Blessing (only
  the we that includes you gets a glyph, and *mipela* is drawn nowhere), and one anchor per
  utterance (each glyph is one self-contained codepoint).
- **Not the evidential armature** (`codepoints.md`, note on U+E14D–E150: "identical claim-bar
  below, grasping-path above"): no claim-bar, no witness above a path. mi: against -mi scores
  0.20–0.23 as set.

## The judges' fixes: what was adopted, adapted and declined

Doctrine judge, set C:

1. **"mitakuyame:: keep yumi: whole, posts included, ... running the shared floor ... past
   both posts to the 150-850 limits."** **Declined as drawn. Its principle is kept as far as
   the geometry allows.** The hook needs four 80-EM verticals and three channels, so with the
   judge's own 110-EM channels yumi: is 650 wide. That leaves 25 EM on each side of the
   700-EM body for the floor to run past the posts (0.4 px at 16 px), and on the right it runs
   over the ◆. Measured at the final geometry with both measures (the audit's
   centroid-centred IoU and an em-aligned IoU, `audit/em_aligned.json`), that version scores
   0.94/0.90/0.83 against yumi: at 16/24/32 px. That is above the inventory's p90 at every
   size: rung 4 could not be told from rung 3 at text size. Opening only the I scores
   0.77–0.80, and opening only the you 0.79–0.82. Adding a third head (a 1,1,2,3 count
   ladder) scores 0.96–0.98. Every variant that keeps both bodies fails the same way
   (`audit/top_rung_alternatives.png`). What is kept: the bond whole, both heads at their
   exact places, the bowl's rim and the hand point for point, and the outer envelope of yumi:.
2. **"Bring the head tops to 800 or below ... keep yu's head clear of x below 260."**
   **Adopted.** The heads are 80-EM squares (the size of .PER's head) at y 720–800, 60 EM
   above the body. yu's head starts at x 260. yu's new heel is what makes that possible
   without the head drifting off its own post.
3. **"Widen yumi:'s channels to at least 110 EM ... Confirm at 16 px that the seam stays
   white."** **Adapted.** C's narrowest clearance was 73 EM. Here it is 100 EM everywhere:
   105 horizontally, 100 vertically, and 100.4 at the chamfers, whose inner leg is held to
   63 EM for that reason. The last 5–10 EM were declined. Channels of 110 make the hook 650
   wide, which cannot keep both yu's head clear of the sigil slot and mi's foot clear of the
   ◆. Vertical channels of 110 cut the hook's overlap from 60 to 40 EM. The FreeType renders
   in a magnified 16 px render (not kept) and the binarised 16 px masks in
   `audit/neighbours_16px.png` (regenerated by `work/run_audit.py`) show the
   seam as a white path at 100.
4. **"Put mi: and yu: side by side ... with -si, kin and en in the rotated forms ..., and with
   each other rotated 180 degrees."** **Done, and it found more than expected.** Set C's mi:
   and yu: are a symmetric hook split in two, so mi: turned 180° *is* yu:'s body. C's audit
   score (0.40–0.43) was low only because large head-dots at 860 shift the ink centroid the
   audit centres on. Moving the heads down to 800, as fix 2 requires, raised it to 0.54–0.76
   (p98 at 24 px). The revision therefore breaks the symmetry in the bodies themselves: yu:
   has the heel and the T, and mi: has the chamfered elbow. The pair now scores 0.61–0.64
   (p55–p78) with FreeType and 0.46–0.70 (p5–p89) with the independent rasteriser, below p90
   everywhere. As set, the two score 0.12–0.20. The strip is on `sheet.png`.

Doctrine judge, other findings on C:

- **Face / ジ reading** (Axiom 1, Rejection 4, `philosophy.md:234`). **Partly answered.**
  With bodies under them, yumi:'s heads read as heads. mitakuyame:'s two dots over the open
  hold still invite a face or ジ reading at 16–24 px. This is listed as a weakness and needs a
  human reading test.
- **The seam going grey at 16 px** (`:258`, `06-cognitive-load.md:140`). Addressed by fix 3
  above.
- **".REL also pictures two head-dotted figures joined at hand height."** **Declined as a
  defect.** S092 made the floating head-dot "the family's person-marker, shared with
  det-rel" (`design_notes_s092.md:106`), and sharing it is family coherence, not duplication.
  The two shapes are far apart: yumi: against .REL scores 0.18–0.20 as set. Whether the owner
  wants the determinative and the anchor to share the idea is `decisions.md` §7.
- **The sigil gap** (`philosophy.md:196`, `design_philosophy.md:88`). Not the designer's to
  close. See `decisions.md` §3.

Grafts from the other sets. No glyph was transplanted, because none survived in another
hand. Three principles were brought in:

- **From A:** the kinship with O- is made geometric. The reach and the bowl are both O-'s
  half-octagon arc, one turned down and one turned up. yu: against O- scores 0.26–0.28 as set,
  where A's yu: scored 0.66.
- **From B:** the "borrowed ground" of yu: (B's stake on the left stood on your ground)
  becomes yu's heel. B's judge fix ("give mi: and yu: a difference that mirroring cannot
  erase") is applied to C's figures as the heel against the elbow.
- **From the doctrine judge's graft note:** "take the principle: C's yumi: kept whole ... as
  the base of the top rung". The bond is kept whole. The bodies could not be kept while the
  rung stayed distinct (fix 1).

## Confusability audit (re-run, unchanged script)

`audit/confusability.py`, run by `work/run_audit.py` on all four sets, with outputs in
`final/audit/`. Its checks pass: the scratch font reproduces all 93 shipped glyphs pixel for
pixel at 11, 16, 24 and 32 px, and `glyphs.svg.json` matches the composed specs with 0
differing pixels. Scores are IoU, FreeType, best of the 8 symmetries, against the
inventory's own nearest-neighbour distribution (p90 = 0.739 / 0.713 / 0.644 at 16 / 24 / 32 px).

| final | nearest existing (any transform), 16 / 24 / 32 px | nearest as set |
|---|---|---|
| mi: | en- 0.56 p36 · en- 0.55 p41 · 「 0.46 p10 | seem 0.48 / 0.43 / 0.38 |
| yu: | en- 0.62 p52 · en- 0.59 p54 · gloria 0.43 p8 | phora 0.48 · stasis 0.56 (p59, 24 px only) · .PLC 0.35 |
| yumi: | kavod 0.45 p8 · kairos 0.43 p9 · sema 0.37 p1 | panim 0.39 · sema 0.40 · sema 0.36 |
| mitakuyame: | parallax 0.45 p8 · qing 0.41 p6 · parallax 0.35 p1 | kawil 0.40 · mushin 0.39 · .ACT 0.34 |

Within the set, the closest pairs are mi: rot180 against yu: (0.64 / 0.64 / 0.61, rotation
only) and yumi: against mitakuyame: (0.56 / 0.61 / 0.63, p37 / p61 / p85, as set). The
em-aligned measure, which is how the two meet in running text, gives yumi: against
mitakuyame: the same 0.56 / 0.61 / 0.63. **No score in the final set exceeds the
inventory's p90 or its closest existing pair, at any main size, with either renderer.** The
designers' sets were re-scored in the same run, and their figures match the first audit.
Set B keeps its two flags above p90 at 16 px.

Limits carried over from the audit: this is a bitmap proxy, not a reading test. The 16 px
renders are unhinted, so the stems are grey where they fall between pixels, and grid-fitting
belongs to the production phase (`06-cognitive-load.md`, Hinting). Latin host text was not
measured. One new limit was found here: centroid centring *understates* the similarity of a
glyph to the same glyph minus one lateral part, because the centroid shifts. The audit put
"only the you opens" at 0.38 against yumi:, while em-aligned it is 0.79. That is why the
top-rung comparisons above use both measures.

## Known weaknesses

1. **mitakuyame: opens the bodies.** That is the Law 1 tension described above, and the
   owner's call (`decisions.md` §2).
2. **mitakuyame: may read as a face or as ジ** at text size: two level dots over an open hold.
3. **mi: and yu: are still near-rotations.** The heel, the elbow and the head positions
   separate them, and they stay below p90, but a learner meeting the pair first is the case
   `philosophy.md:268` warns about. A reading test should include them.
4. **Rotated, mi: resembles en-** (⊐), at 0.55–0.56. Text is never set rotated, but the
   doctrine asks for the check.
5. **The hook only reads from about 24 px up.** At 16 px yumi: is "two interleaved figures"
   with a visible seam, and the grip itself is not legible.
6. **yu: on the left** honours *yu-mi* and the manifesto's "seated the other party inside the
   speaking position" (`manifesto.md:123`). Readers who expect the self first may misread it.
7. **The chamfers are 80, not 90** (Rule 1, `:161`), matching the live font, not the rule's
   text. If the correction is ever applied to the whole font, it applies here too.
8. **Mitred joints sit beside O-'s stroke-built, notched arc.** S092's brackets are mitred
   polygons too, but the anchors and their nearest kin differ in joint style.
9. **No human reading test** was done for any set.

## Sigil and class mark (proposals)

- **Sigil: none drawn now, tongue recorded truthfully.** The entries carry `"Tok Pisin"` and
  `"Lakota"` as in `morphemes.json`. Neither is in `DONOR_SIGIL`, so `compose_glyph` falls
  back to no sigil (`glyph_specs_v1.py:1527`). The slot (x 110–190, y ≈ 806–895) is kept
  clear: no ink rises above y 800, and the nearest ink to the slot is yu's head in yumi: and
  mitakuyame:, at x 260 (70 EM to the right). So a sigil can be assigned before
  canonization without redrawing. The options and their costs are in `decisions.md` §3.
- **Class mark: ◆ structural.** The anchors are "free particles of the address-axis like O-,
  not bound affixes" (`manifesto.md:139-142`). Their codepoints are in the structural range,
  and [selah] keeps ◆. O- took ◁ because it is bound. The alternatives are in `decisions.md`
  §4.

## Files

`specs.py` (ANCHOR_GLYPHS; its docstring records the parameters of the generator that emitted
the polygons) · `render.py` (runs the checks, then draws `sheet.png`, `compare.png` and
`glyphs.svg.json`) · `decisions.md` · `audit/` (the re-run audit's log `console.txt`,
`neighbours.png`, `em_aligned.json` and `top_rung_alternatives.png`; `results.json` and
`neighbours_16px.png` are regenerated by `work/run_audit.py`) · `work/run_audit.py`.
The generator, the sweeps and the prototype images were working files and were not kept.
Nothing was entered into `glyph_specs_v1.py`, `morphemes.json`, `codepoints.md` or the fonts.
No font was installed: the OTFs the scripts build under `work/` and `audit/build/` exist only
to render with and are git-ignored.
