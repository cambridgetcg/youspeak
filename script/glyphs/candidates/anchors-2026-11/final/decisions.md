# Anchor glyphs — decisions that belong to the language's owner

_Written by an agent (one step of a design workflow), 2026-11-10. Each item gives the
options and what each one costs. "Recommended" means this step's proposal, not a decision.
Nothing here is decided until the owner says so. A canonized glyph never changes
(`script/philosophy.md:92`), so the items marked **before canon** must be settled first._

Evidence for every number: `audit/results.json` (the confusability audit re-run unchanged),
`audit/em_aligned.json`, `audit/top_rung_alternatives.png`, `sheet.png`, `compare.png`.

---

## 1. Which set

| option | what you get | what it costs |
|---|---|---|
| **Final (C revised)**, recommended | C's hook: two different figures (a reach and a bowl) that hold each other without touching, with yumi: containing both point for point. Rule 3 zones met (heads at 800, against 860 in C). Every seam is at least 100 EM. The rotation trap in C's bodies is fixed (heel and elbow). The reach and the bowl are O-'s arc turned down and up. Nothing in the set exceeds the inventory's p90 at 16, 24 or 32 px. | The top rung opens the persons' bodies (§2). mi: and yu: are still near-rotations of each other (0.61–0.64, below p90). At 16 px the grip reads only as "two interleaved figures". |
| C as designed | The same idea, with larger heads and channels of 73–120 EM. | Heads at 860 (Rule 3). Seams as narrow as 73 EM go grey at 16 px. mi: turned 180° is yu:'s body, and only the head placement hides it from the audit. Same top-rung tension. |
| B (standing ground), with the judge's fixes applied | The only strictly nested ladder (1, 1, 2, 3 stakes). Law 1 can hold at every rung. Simplest to cut. | The judge rated its beauty 3 and its kinship with O- 2. It reads as tally marks in running text (Rejection 3, `philosophy.md:224`). Its mi:/yu: are a near-mirror pair until redrawn, and yumi: resembles stasis. The fixes are untested: nobody has drawn them yet. |
| A (address kin) | The closest kinship with O-. | Fails Law 1 at yumi: (its halves are rescaled, not contained). yu: sits beside O- at 0.66 (p87) in exactly the sequence the manifesto writes (`yumi: O-…`). |

## 2. The top rung and Law 1 (the question the judges could not settle) — before canon

Law 1 (`grammars/ankyrance/manifesto.md:61-66`): "Any union-form must keep both persons
legible inside it ... A we-word that dissolves its members is not YOUSPEAK."

The finding: in the hook vocabulary, yumi: uses 620–650 of the body's 700 EM of width, and
its heads reach the 800 ceiling. A top rung that **adds** to yumi: has nowhere to put what it
adds. A top rung that **keeps both bodies** can only differ by a small part. Measured at the
final geometry, em-aligned IoU against yumi: at 16 / 24 / 32 px, where the inventory's p90
is 0.73 / 0.66 / 0.65:

| top rung | vs yumi: | keeps both bodies? | readable as a different word at text size? |
|---|---|---|---|
| **both closed sides open (in specs.py)** | 0.56 / 0.61 / 0.63 | no: heads, rim and hand stay; the posts open | yes |
| yumi: + floor run out past both posts (the doctrine judge's fix) | 0.94 / 0.90 / 0.83 | yes | no. The run-out is 25 EM per side, and it sits on the ◆. |
| only the I opens, the you whole (*mi*-tákuye: "my relatives") | 0.77 / 0.79 / 0.80 | the you only | no |
| only the you opens, the I whole | 0.79 / 0.82 / 0.82 | the I only | no |
| yumi: + a third head (a 1,1,2,3 count) | 0.98 / 0.96 / 0.96 | yes | no |

Options:

- **(a) Accept the opened top rung** (recommended within this set). It holds that "legible"
  is met by two distinct heads and two distinct, still non-touching gestures: no merger,
  which is what PERICHORESIS forbids. This matches the Lakota teaching that "you are your
  relations". *Cost:* a strict reader of Law 1 will say the bodies are dissolved. The doctrine
  judge already has. And two dots over an open hold may read as a face or as ジ.
- **(b) Hold Law 1 strictly for bodies too, and keep this family.** mitakuyame: would then be
  one of the near-copies in the table. *Cost:* rung 4 cannot be told from rung 3 at text size,
  against Cohesion Rule 6 (`philosophy.md:200`).
- **(c) Hold Law 1 strictly and change families.** Take set B with the judge's fixes, the only
  vocabulary whose persons are thin enough to nest. *Cost:* the beauty and kinship losses in
  §1, and a new round of drawing and auditing.
- **(d) Rule that Law 1 governs yumi: only.** The manifesto's own example is "*yumi* contains
  *yu* and *mi*". The top rung is then judged on Lakota fidelity, not on containment.
  *Cost:* a doctrine reading only the owner can make.

## 3. Sigil — before canon (`philosophy.md:196`: "New donor traditions require new sigil assignments before glyph-design begins")

The slot (x 110–190, y ≈ 806–895) is kept clear in all four glyphs, so any option below needs
no redrawing.

| option | cost |
|---|---|
| **None drawn, tongue recorded truthfully** (recommended for now; all three designers proposed it) | Under `design_philosophy.md:88` an empty corner reads as English. That is half-true for yu:/mi: (Tok Pisin *yu*/*mi* come from English *you*/*me*) and false for mitakuyame:. It also leaves Rule 5 unmet. |
| A new Tok Pisin sigil on three glyphs and a new Lakota sigil on mitakuyame: | Meets Rule 5. But the family's one shared corner is split, and the ladder's top rung is marked off from the rest. Tok Pisin is written in Latin letters, so its sigil would be invented. A Lakota sigil should come from Lakota people: the obvious sources are close to ceremonial imagery. |
| One new sigil for all four, for the ankyrance chapter as a whole | Keeps the family whole. Credits no donor exactly. |
| The reserved YOUSPEAK saltire (`glyph_specs_v1.py:163-174`) | Treats the anchor system as a native grammar assembled from four donors. Goes against the S092 ruling that "native marks go unmarked" (`design_notes_s092.md:195`). |

## 4. Class mark

| option | cost |
|---|---|
| **◆ structural** (recommended) | Matches the codepoint range, the manifesto ("free particles of the address-axis like O-, not bound affixes", `manifesto.md:139-142`), and [selah]. The anchors then carry a different mark from O- (◁), their nearest kin. |
| ◁ prefix, like O- | Reads as "begins", and the anchors do open the utterance. But they are not bound to a following word, and S092 gave ◁ to O- for being bound (`design_notes_s092.md:136`). |
| Suppressed, like the determinatives | Frees the corner. But it reads as a content morpheme, which the anchors are not. |

## 5. mi: and yu: as a near-rotation pair

mi: turned 180° against yu: scores 0.61–0.64 (FreeType) and 0.46–0.70 (the independent
rasteriser): below the inventory's p90 everywhere, but the closest pair in the set. As set,
they score 0.12–0.20. Options:

- **(a) Accept, and run a reading test** with first-time readers (recommended).
- **(b) Declare them a designed reversal pair** (offer and receive). `06-cognitive-load.md:84`
  permits rotations between intentionally reversed glyphs. *Cost:* `philosophy.md:268` asks
  that the most frequent glyphs be the most distinct.
- **(c) Redraw for more asymmetry.** *Cost:* either width the hook does not have, or the
  heads above 800.

## 6. The domain tag

All three designers and this revision use `relation+position`, which no shape-family table
names (`philosophy.md:179-188`, `design_philosophy.md:108-121`). Options: **register
"position"** (standing-place) as a domain under the relation family; or use the existing
`relation+between` (as .REL, -mi, -si do) or `relation+act` (as O- does). The tag is metadata
only and does not change the drawing.

## 7. Sharing the person-marker with .REL

The anchors' persons use the floating head-dot that S092 made "the family's person-marker,
shared with det-rel" (`design_notes_s092.md:106`). The doctrine judge counted the shared idea
as a fault, because .REL is "two head-dotted figures ... joined at hand height". The shapes are
far apart: yumi: against .REL scores 0.18–0.20. Options: accept the shared marker as family
coherence (recommended), or ask for persons without head-dots. *Cost:* without head-dots,
mi: and yu: fall back toward plain brackets (en-, phora, 「」). The heads are also part of
what separates them under rotation.

## 8. Order inside yumi:

**yu: on the left** (recommended) follows Tok Pisin *yu-mi* and the manifesto's "its very
first breath already seated the other party inside the speaking position" (`manifesto.md:123`).
The alternative is mi: on the left, self first. That mirrors yumi: and moves the heel and
elbow features, so the glyphs would need to be redrawn and re-audited.

## 9. Before canonization, whatever is chosen

- **Lakota counsel** for mitakuyame:. This step drew nothing ceremonial: no hoop, no
  quartering, no four, no pipe, no feather, no tree. It cannot judge how Lakota people would
  receive a glyph for words from a living prayer.
- **A human reading test** at 8–12 pt and in running English host text: the anchor pairs, the
  ジ/face reading of mitakuyame:, and mi:/yu: rotated. No set has had one.
- **Production hinting.** The 16 px renders are unhinted, so the seams depend on stem
  placement (`06-cognitive-load.md`, Hinting).
- **Two smaller consistency questions.** The chamfers are 80 EM, matching the live font, not
  Rule 1's unimplemented 90 EM diagonal (`philosophy.md:161`; `glyph_specs_v1.py:22-27`). And
  the anchors' joints are mitred, while O-'s arc is stroke-built with notched joints.
