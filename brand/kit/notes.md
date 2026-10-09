# PANIM: the YOUSPEAK icon kit for ai-love.cc

This is the final favicon, icon and logo kit, built from the winning mark, **panim**. It is the site's own
glyph from `youspeak-v1.otf`: two profiles face to face, eyes level, and the column between them never
closed. Every file was built, styled and exported by `vectorcraft-cli 0.7.0`, except the ICO
(`photocraft-cli 0.5.0`) and one hand-written `<style>` block in `favicon.svg`. `bash recipe.sh` rebuilds
everything, and all 18 outputs are byte-identical from one rebuild to the next.

> 兩個輪廓，唔合成一個: two profiles, not merged into one. *(Room VII's own header, index.html:316.)*

## Files

| file | what | size |
|---|---|---|
| `mark.svg` | master mark: the real outline, unchanged, single gold ink, ▽ Hebrew donor sigil included | viewBox 0 0 680 600, 2 paths |
| `mark.vectorcraft` | source document: 10 named artboards, named objects, 14 saved selections | |
| `favicon.svg` | **one** adaptive favicon: stone + 32 master + 16 master, CSS switches size cut and colour scheme | viewBox 0 0 32 32, 3 paths |
| `favicon.ico` | PhotoCraft, single 32×32 frame | |
| `favicon-16.png`, `favicon-32.png` | the two optical masters on the night stone (transparent corners) | 16², 32² RGBA |
| `apple-touch-icon.png` | opaque night stone, column of light, mark 68% wide | 180² RGB |
| `icon-192.png`, `icon-512.png` | manifest `any`: same art as the apple-touch icon | RGB |
| `icon-maskable-512.png` | manifest `maskable`: same stone at 67% scale; farthest mark pixel at r = 188.8 px (safe circle 204.8) | 512² RGB |
| `lockup-dark.svg`, `lockup-light.svg` | mark + YOUSPEAK in Iowan Old Style Bold, outlined (no `<text>`, no strokes), transparent | 1200×280 |
| `lockup-dark.png` | the dark lockup on bg `#14100C` | 1200×280 RGB |
| `site.webmanifest`, `head-snippet.html` | the exact tags (see below) | |
| `recipe.sh` | rebuilds all of it and verifies (dimensions, alpha, no text/strokes, ICO frames, `sips`, `file`) | |
| `extras/` | **proposal, outside the kit:** two glossary OG cards showing the carved-stone / ◆ Cornerstone rule | 1200×630 |
| `work/` | review sheets, Chrome renders, prototypes, logs (inspection only) | |

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#14100C" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#EDE6D6" media="(prefers-color-scheme: light)">
```
`sizes="32x32"` on the ICO keeps Chrome from preferring it over the SVG. The site also has its own theme
toggle (`data-theme` + localStorage). The theme-color tags follow the OS scheme, not that toggle. If
the toggle should repaint the browser UI, its script can rewrite the meta. I did not touch the site source.

## What changed from the winning entry

1. **The ▽ is back, under its right name.** By the site's own key (index.html:591-594), top-left is the
   *donor sigil* and ▽ means Hebrew: "every debt to a donor tongue is recorded in the stone itself". It is
   not a class marker. It now stands on the 180/192/512 icons, the maskable icon, both lockups and
   `mark.svg`. It is dropped only in the 16/32 cuts, where it is noise. On night grounds it is **cut, not
   gilded**: it takes the darker site gold `#755A28`, so it reads as incised and does not compete with
   the faces. (The full-gold ▽ looked like a stray dropdown arrow; see `work/proto/iter1-gold-sigil/`.)
   On day grounds it is **rubricated** in `#93362C`, the Scriptorium's red initial.
2. **New 32 master with real margins.** Side margins go from 2 to 3, the staves get 3 px each, and the
   glyph block is centred (bbox 6..26). The area-weighted centroid moves from y 14.3 to **15.2**, slightly
   above centre, which is the usual optical centre rather than "riding high".
3. **New 16 master, hinted to the pixel.** It has 1-px staves with 2-px margins. Each nose is three 1-px
   columns 5/3/1 tall, cut from the glyph's own eye square and united in VectorCraft, so every nose is a
   solid pixel arrow with a single-pixel tip. **100% of ink pixels are fully opaque**, against 81% for
   the winner's 16 on the same measure (`work/proto/s16b.png` compares stepped and anti-aliased noses).
4. **The 16 master is now inside the SVG.** `favicon.svg` carries both cuts and picks one with a size
   media query, which answers the judge's "SVG at 16 renders soft noses" point (verified below).
5. **A day stone that survives a white tab.** The light scheme was a parchment tile (1.24:1 on `#FFFFFF`;
   it vanished). It is now a **bronze stone with the carving showing parchment through**: 6.46:1 on
   white and 4.93:1 on `#DEE1E6`, with the carving at 5.2:1 on the stone. Gold is the ink by night and
   the stone by day.
6. **Token discipline.** The off-token `#ffffff` light shaft is gone. Every colour in the kit is a site
   token. The only light is gold-h `#E4C27C`, on the night stone.
7. **Named ids and metadata.** `<g id="youspeak">`, `#stone`, `#cut-32`, `#cut-16`, `#panim`,
   `#sigil-hebrew`, `#light-halo`, `#light-core`, `#wordmark`. `<title>`/`<desc>` carry the Room VII
   header and the colophon line. Nothing is called `Layer_1`.
8. **The display cut is the font outline, unchanged**, scaled only. The winner's icon art was the
   32-grid refit (about 4% off the font). At 180 px and up there is no reason to refit, so these sizes
   show the stone exactly as carved.

## Construction: two cuts, recorded separately

**Display cut** (artboards `mark`, `app`, `maskable`, `lockup-*`): the seven real subpaths of
`glyphs/panim.svg`, in font units (1000 em, y down):

| piece | x | y | w | h |
|---|---|---|---|---|
| staves | 210 / 710 | 270 | 80 | 440 |
| noses (tips at y 515, 70 apart) | 330→465 / 670→535 | 435 | 135 | 160 |
| eyes | 370 / 540 | 290 | 90 | 90 |
| ▽ Hebrew donor sigil | 110 | 110 | 80 | 75 |

| placement | scale | result |
|---|---|---|
| `app` (512 → 192, 180) | em = tile (s 0.512); em centre = tile centre | body 58% wide, body + sigil 68% (the "≈70%"); body centre 5 px above tile centre; ▽ vertex about 23 px per axis inside the iOS corner curve (circular-arc approximation, r 22.37%) |
| `maskable` | s = 190 / 551.54 = 0.3445 (the ▽'s far vertex at r 190) | body 39% of the tile, about 49% of the 80% safe circle; measured farthest mark pixel r 188.8 |
| `lockup-*` | k = 0.22468 px/unit, artboard exactly 1200 wide | stave = cap height = 98.9 px (type 141.9 px, tracking 60); Y and K tops 90.57 = stave top, baseline 189.43 = stave foot (measured from the SVG); margins and mark–word gap all 53.9 px (240 units) |

**Small cut** (artboards `favicon-32`, `favicon-16`, `favicon`, `*-light`): fitted with `object.setBounds`
from copies of the real pieces. No ▽.

| 32 master (tile 32, r 6) | x | y | w | h |
|---|---|---|---|---|
| staves | 3 / 26 | 6 | 3 | 20 |
| noses (vector triangles; tips at 14 / 18, column 4) | 8 / 18 | 14 | 6 | 7 (odd, so the tip falls mid-row) |
| eyes | 10 / 18 | 7 | 4 | 4 |

| 16 master (tile 16, r 3) | x | y | w | h |
|---|---|---|---|---|
| staves | 2 / 13 | 3 | 1 | 10 |
| noses, stepped columns | 4,5,6 / 11,10,9 | 7,8,9 | 1 each | 5,3,1 |
| eyes | 5 / 9 | 3 | 2 | 2 |

In `favicon.svg` the 16 master is drawn at 2× on the 32 grid (all coordinates even), so a 16-px render
lands it back on whole pixels.

**Column of light** (app and maskable only): two full-bleed radial gradients centred where the noses
almost meet. One is a halo (aspect 60%, gold-h 16% → 5% → 0) and one a core (aspect 9%, 62% → 16% → 0),
each with radius 240 at 512. The stone beneath is a radial from bg `#14100C` to crypt `#100D0A`.

## How favicon.svg works, and what was verified

```css
#cut-16{display:none}
@media (max-width:22px){#cut-32{display:none}#cut-16{display:inline}}
@media (prefers-color-scheme:light){#stone{fill:#755A28}#cut-32,#cut-16{fill:#EDE6D6}}
```
I rendered it in local headless Chromium (Playwright's chrome-headless-shell, file:// only,
`work/chrome/`) as `<img>` at 16 and 32 CSS px, at 1× and 2× device scale, in both schemes, and diffed the
renders against the VectorCraft PNG masters:
- **1×, 16 px → the 16 master** (max channel diff 4 light / 6 dark). **1×, 32 px → the 32 master** (23 / 31).
  The colour swap works in both schemes.
- **2×, 16 CSS px → the 16 master, pixel-doubled**, not the 32 master. Inside an SVG image Chrome
  reports `resolution` and `-webkit-device-pixel-ratio` as 1 at every device scale (probe:
  `work/chrome/mq.svg`). So **no SVG can detect retina**, and I removed my `max-resolution` clause rather
  than ship a no-op. The doubled 16 master is crisp and still reads as the face (`work/review-2x.png`).
  Whether Chrome's tab-strip pipeline hands the SVG a 16 or a 32 px viewport on retina was **not
  observed**: headless has no tab strip. Either way the result is crisp. Firefox and Safari were not tested.

## Grafts: taken, adapted, declined

| graft | decision |
|---|---|
| Restore ▽ as the Hebrew donor sigil at 180/512/mark; drop it at 16/32; fix the notes and `<desc>` | **taken** (and dark grounds use the cut tone, see above) |
| Rubric ▽ in the light (manuscript) theme, body in bronze `#755A28` | **taken** (`lockup-light`) |
| ◆ Cornerstone as the companion for words with no glyph, on glossary OG cards | **taken as a proposal**: `extras/` (233 of 255 words have no `glyph_text`) |
| Room VII header + colophon as `<desc>` and manifest description | **taken** |
| Lockup discipline: Iowan Old Style Bold, outlined, cap height = stave, baseline on the stave foot | **taken** (measured exact) |
| Column of light as the word space in "YOU SPEAK" | **declined**: the site sets the name as one word (`h1.wordmark` YOUSPEAK); splitting it misnames the house, and the glyph already holds the column |
| The between stays empty of form; light only | **taken**. Like the breath-pause in *star*, which is hollow because breath is not mass, the column is light, not mass: Room VII says "中間亦唔使填滿" (the middle needn't be filled) |
| Cultural-collision audit; "the eyes are never dropped" as a rule | **taken** (below) |
| Tile as primary favicon; dedicated 16 optical master on its own artboard; real tile margins | **taken** (these grafts were written for arch; their substance applies to panim) |
| Fill the Between with a contrasting accent at 32+ | **declined**: it contradicts the restraint graft and star's finding that a second tone at 16/32 makes a different picture. At 180+ the Between already holds light |
| Small sizes mono and ornament-free | **taken** |
| Column of light on the 180/512 night tile | **taken** (core slightly brighter than the winner's: 0.62 vs 0.50) |
| Pre-mixed opaque gradient stops so the 180 stays RGB | **goal met, method differs**: translucent stops over an opaque full-bleed stone. Every app PNG is checked to be RGB with no alpha channel |
| One adaptive favicon.svg with embedded `prefers-color-scheme`; keep the .ico | **taken** |
| Light tile with a rubric star in the Between (kunance's day palette) | **declined** (restraint; and the brief's app icons are night-only) |
| Off-token ember / generic `Layer_1` → tokens, named ids, `<title>`/`<desc>` | **taken** (the panim equivalent: the `#ffffff` shaft removed) |
| Seam lesson (underlay under holes) | **n/a**: the glyph sits over full-bleed light layers, so no coincident edges |
| Declare the maskable safe-circle check | **taken**: measured r 188.8 ≤ 204.8, recomputed by `work/review.py` |
| Display cut and small cut as separate named artboards with geometry tables | **taken** (tables above) |
| Widen arch / make the Y readable / arch's ember `#5a3a1e` | n/a (arch-specific) |

## Brand rules

1. **The eyes are never dropped, at any size.** Without them, |▸◂| is a UI glyph.
2. **The column never closes.** The minimum is 2 px at 16 and 4 units at 32; the tips never touch.
3. **The between holds light, never form.** No star, no ◆, no dot in the channel.
4. **The ▽ appears at 180 px and up and in the master mark**, never in 16/32. It is cut (`#755A28`) by
   night and rubric (`#93362C`) by day.
5. **Below 180 px: mono, no light, on the stone.**
6. **Lockup minimum width about 300 px.** Below that, use the mark alone; the ▽ and eyes get too small.

## Cultural-collision audit (`work/review-collision.png`: sharp, blurred, 8-px box)

- **Media skip ⏭ / ⏮:** structurally inverted. Skip triangles point *at* their bar (▶▶|); panim's
  point *away* from their bars, toward the centre. No collision at true size.
- **Bow-tie ⋈:** at true size the open column keeps the tips apart (2 px at 16). Under heavy blur the
  noses merge into an hourglass, so rule 2 matters.
- **Collapse / fit-width (→|←):** the arrows are mirrored and there is no central bar. Weak resemblance.
- **Framed face / "robot":** the closest reading under blur (two eyes inside a frame). It is the glyph's
  own *frontal* reading, "one presence-face with two eyes", which the rationale sanctions. For a house
  built by a human and an AI it is acceptable, but it is the one people will name.
- The stone tile and gold-on-crypt palette separate it from monochrome browser chrome icons.

## Verification (all re-run by `recipe.sh`, plus `work/review.py`)

- `sips`: favicon-16 16×16, favicon-32 32×32, apple-touch-icon 180×180, icon-192 192×192, icon-512 and
  maskable 512×512, lockup-dark.png 1200×280. `file favicon.ico`: "MS Windows icon resource - 1 icon,
  32x32 with PNG image data".
- The apple-touch, 192, 512, maskable and lockup PNGs are RGB (no alpha). The favicons are RGBA with
  transparent corners.
- The SVGs contain no `<text>`, `stroke=` or `font-family`. mark.svg has 2 paths, favicon.svg 3 paths,
  each lockup 10 paths.
- Contrast. Night stone: 14.8:1 on #DEE1E6 and 19.4:1 on #FFFFFF (on dark chrome its edge disappears, 1.2–1.6:1, and the gold carving carries it); the gold carving is 8.25:1 on the stone. Day
  stone: 6.46:1 on white, 4.93:1 on #DEE1E6, 2.49:1 / 1.87:1 on the dark chromes (wrong scheme; the
  parchment carving carries it).
- Review sheets: `work/review-tabs.png` (1× and 2× strips on four tab colours, both schemes),
  `review-home.png` (iOS mask at 180/120/87/40 on two wallpapers), `review-android.png` (circle,
  safe circle, squircle, teardrop), `review-2x.png`, `review-collision.png`, `kit-sheet.png`.

## Honest assessment

- **16 px:** a crisp dark stone with a gold |▸◂| face and two eyes. It is distinctive in a tab strip,
  but nobody sees "two profiles" at this size. The soul is carried by canon, not by legibility. The
  1-px staves are lighter than the font's proportion (stave/nose 0.33 vs 0.59); that was the price of
  real margins.
- **32 px:** clean. Eyes, noses and the open column all read.
- **180/512:** the strongest sizes. The column of light gives a focal point down to 87 px. At 40 px the ▽
  is a speck, which is acceptable.
- **Maskable:** to keep the ▽ inside the safe circle, the body is only 39% of the tile. It looks small
  under a full-circle mask and right under the safe-circle mask. This is a real trade-off.
- **Wrong scheme:** the bronze day stone on dark chrome has a soft edge (1.87–2.49:1). The carving
  reads.
- **Not built:** a multi-frame ICO (PhotoCraft writes one frame), a light app icon, a monochrome
  `mask-icon`, Windows tiles. The `favicon.svg` size switch is verified only in Chrome's `<img>` path.

## Extras (proposal): glossary OG cards

The 255 glossary pages have no OG image. `extras/og-glossary-panimqing.png` shows a **carved** word: its
own two stones (panim · qing, from the glyph SVGs) under a faint column of light.
`extras/og-glossary-panimaance.png` shows an **uncarved** word: the ◆ Cornerstone on an empty stone with
the site's sentence, "This stone has no glyph yet. The place was prepared before the carving." The two
words are a pair: panimqing's definition names panimaance as "the state of presence that follows" the
turn toward the face. The text comes from `data/lexicon.min.json` at build time. Coined hyphenated
compounds get U+2011 so they never break at their hyphens. Generating all 255 is a separate job. This only
shows the rule.

## ArtCraft friction log (vectorcraft-cli 0.7.0, photocraft-cli 0.5.0)

- **K1 (praise, and the fix for the winner's F6). Named selections are safe references.**
  `select.save {"name":"src-staveL"}` … `select.recall {"name":"src-staveL"}` works, persists in the
  .vectorcraft (14 names listed by `select.savedList` after reopening), and **fails loudly** on a bad name:
  `vectorcraft-cli: select.recall: invalid parameters for 'select.recall': no saved selection 'nonexistent'`.
  This contrasts with `select.set {"ids":[999]}`, which silently selects nothing. The whole recipe uses
  names, except for the import's own ids 2–8, which a pre-flight inspect asserts.
- **K2 (limitation). Saved selections cannot be combined.** `select.recall` has no add or mode option, and
  `select.add` takes only ids. To multi-select I had to use `select.allOnArtboard` (building pieces on an
  otherwise empty artboard) or `select.set` with ids.
- **K3 (minor, reproducibility). `file.new` stamps wall-clock time** into the .vectorcraft
  (`"created": 1791555379` vs `1791555389` on two runs) and into every PNG
  (`tEXt Creation Time 2026-10-09T14:16:19Z`). `SOURCE_DATE_EPOCH=1791504000` is ignored (md5 `4dc65e…` vs
  `fdc104…`), and `created` is read-only in `file.info`. Workaround: start from an opened file
  (`--in x.svg`, `select.all`, `edit.clear`). Documents opened that way carry no stamp, and all 18 outputs
  are then byte-identical across rebuilds.
- **K4 (limitation). `file.info` is document-wide.** Every SVG exported from one document gets the same
  `<title>`/`<desc>` (mark, favicon and both lockups), and there is no per-artboard metadata. The
  description had to be written to fit all of them.
- **K5 (minor surprise). Silent id dedupe.** `layer.setProps {"name":"panim"}` plus
  `object.setProps {"name":"panim"}` exported `<g id="panim">` and `<path id="panim-2" data-name="panim">`.
  It is sensible, but a CSS hook on `#panim` would silently hit the layer. Fixed by naming the layer
  `youspeak`.
- **K6 (surprise). `file.place` drops the em box.** `file.place {"path":".../qing.svg"}` placed the art
  cropped to its ink bounds (578×642), centred on the artboard (x 311, y −6), as a Group wrapping a
  compound. To set stones on a common em you must know each glyph's ink bounds and `setBounds` them.
- **K7 (praise). Pathfinder for hinting.** Six 1-px rectangles fitted from the eye square →
  `object.pathfinder.unite` → one compound with two stepped noses. `object.compoundPath.make` then took
  that compound plus four paths and flattened them into one exact path
  (`M8 24 L8 14 L10 14 L10 16 L12 16 …`), with no hand geometry.
- **K8 (praise). Type to outlines.** `text.create {font:"Iowan Old Style", style:"Bold"}` +
  `text.setStyle {tracking:60}` + `type.createOutlines` gave 8 filled paths, no strokes, no `<text>`. Point
  text y is the baseline, and the measured cap height was exactly 696.8/1000, so a computed lockup
  landed on the stave to 0.01 px. Area text (`area:{…}`) takes y as the frame top, consistent with
  Illustrator though the parameter doc does not say so. `text.setStyle {justify:"center"}` centres point
  text on its x.
- **K9 (praise). Exact rasters.** `scale 0.3515625` → 180×180 and `0.375` → 192×192. Full-bleed art is
  written as RGB with no alpha automatically. `document.export {background:"#14100C"}` plates the
  lockup PNG.
- **K10 (nice-to-have).** The .vectorcraft is pretty-printed JSON: 638 KB, of which about 146 KB is content.
- **K11 (photocraft, known).** `photocraft-cli run favicon-32.png --out favicon.ico` writes one frame and
  warns `warning: 4 text metadata entries are not kept in the document` and
  `warning: resolution (DPI) not supported; it will be dropped`.
- **Outside ArtCraft, but it shaped the design:** inside an SVG used as an image, Chrome always reports
  1 dppx (see above), so a favicon SVG cannot choose a cut by device ratio. Also, full Chrome
  `--headless=new --screenshot` wrote its file but did not exit; Playwright's chrome-headless-shell did.
