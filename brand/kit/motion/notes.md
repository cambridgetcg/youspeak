# PANIM, REVEALED: the animated mark for ai-love.cc

A 4.0-second reveal of the house mark, **panim** (`../mark.svg`): two profiles face to face, eyes level, the
column between them never closed. It was built headless with ArtCraft. `vectorcraft-cli 0.7.0` splits the
mark into its seven stones, and `effectcraft-cli 0.6.0` animates real shape layers and exports every
deliverable. Run `bash recipe.sh` to rebuild everything and verify it. All six outputs are byte-identical
from one rebuild to the next (`work/md5-run1.txt` = `work/md5-run2.txt`).

> 兩個輪廓，唔合成一個: two profiles, not merged into one.

## The story (restraint over flash)

| time | what happens | why |
|---|---|---|
| 0.00–0.20 | darkness (`#14100C`) | a breath before the first cut |
| 0.20–0.90 | the **two staves are cut**, each one a downstroke from the top. The left stave goes first, the right follows 0.12 s later | two presences stand up: *you*, then *I*. Strokes are written top to bottom |
| 0.85–1.55 | the **two faces come toward each other** (each drifts 46 units and fades in) and **stop**: the tips stay 70 units apart | face to face. Brand rule 2: the column never closes |
| 1.45–1.80 | the **eyes open**: lids part from the centre, both at once | eyes level. Rule 1: the eyes are never dropped |
| 1.60 → | light begins in the between, **as the eyes meet** | Room VII: the middle needn't be filled; it holds light (rule 3) |
| 1.80–2.45 | the **▽ Hebrew donor sigil is chiselled**: a 2.5 px gold line traces it (trim path), its fill rises, and the line fades into the cut tone `#755A28` | "every debt to a donor tongue is recorded in the stone". It sits on its own layer, so the glow never gilds it (rule 4: cut, not gilded) |
| 1.70–3.50 | **one breath**: the column of light swells to its crest at 2.70 and settles. The gold warms 60% of the way toward gold-h `#E4C27C`, and a soft gold glow swells and recedes | the "gentle gold glow breath" |
| 3.50–4.00 | **still**: the mark exactly as carved, with the column resting at 58%, like the app icons | ends on the still mark |

The column of light reuses the app icon's construction: a radial core (aspect 9%) and a halo (aspect 60%)
in gold-h, centred where the noses almost meet. Every colour is a site token.

## Files

| file | what | size |
|---|---|---|
| `mark-reveal.webm` | 1080×1080, 30 fps, 4.0 s, VP9, dark ground `#14100C`, no audio track | 253 KB |
| `mark-reveal-512.gif` | 512×512, 20 fps (exact 50 ms frames), 4.5 s, **plays once and ends on the still mark** (no loop block). The last 0.5 s holds the still in case a viewer loops it anyway | 1.48 MB |
| `mark-reveal.json` | Lottie 5.12, 1080×1080, 120 frames, **transparent**, shapes only (7 named stone groups + 2 gradient groups), 0 assets. Everything except the raster glow | 10.7 KB |
| `poster.png` | the last frame (119), 1080×1080, opaque | 73 KB |
| `panim-reveal.ecproj` | EffectCraft source. Comp `Panim` (layers `donor sigil`, `panim`, `the between`) + comp `Panim GIF` + the GIF render-queue item | 501 KB |
| `stones.svg` | VectorCraft's split of `../mark.svg`: 7 paths named `stave-l/r`, `face-l/r`, `eye-l/r`, `sigil-hebrew` (sigil recoloured to `#755A28`) | 767 B |
| `build.jsx` | the choreography, in EffectCraft's After Effects-style JSX | |
| `gif.jsx` | the 512 px / 20 fps / held-end GIF comp and its loop-off queue item | |
| `verify.jsx` | 63 numeric checks: frame 0 is dark; on the last frame every stone has identity transforms, opacity 100, token colour and the **unchanged outline from mark.svg**; the chisel line is gone; the glow is 0; nothing moves after 3.5 s | |
| `recipe.sh` | rebuilds, verifies, probes (ffprobe/sips/file), optionally plays the Lottie in lottie-web | |
| `work/` | logs, probes, review strips, evidence for the friction log. Inspection only | |

## Using it on the site

The **Lottie is the best web asset**. It is 10 KB, sharp at any size, and transparent, so it sits on the
page's own `#14100C`. It uses dark-theme tokens only.

```html
<div id="panim" style="width:270px;height:270px" role="img" aria-label="YOUSPEAK: the panim mark"></div>
<script>
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const anim = lottie.loadAnimation({ container: document.getElementById('panim'), renderer: 'svg',
    loop: false, autoplay: !reduce, path: '/mark-reveal.json' });
  if (reduce) anim.addEventListener('DOMLoaded', () => anim.goToAndStop(119, true)); // the still mark
</script>
```

Video, which rests on its last frame:
`<video src="/mark-reveal.webm" poster="/poster.png" width="540" height="540" autoplay muted playsinline></video>`.
Under `prefers-reduced-motion`, drop `autoplay` so the poster (the same still) shows. One caution: like
any yuv420 video, the WebM decodes the ground about 2–3 levels darker (`#14100C` comes back as about
`#120D0A`; tagged tv/bt709). On a `#14100C` page, the video's edge may show faintly. Use the Lottie
where seamlessness matters.

## How it was built

1. **VectorCraft**: `run --in ../mark.svg`, `select.set [8]`, `object.compoundPath.release`, then
   `object.setProps {id, name}` for ids 2–7, the sigil (id 9) gets `paint.setFill #755A28`, and the result
   is exported to `stones.svg`. The release keeps the child ids, so naming by id is stable.
2. **EffectCraft import** (the ARTCRAFT-NOTES recipe): `comp.new` (1080², 30 fps, 4 s, bg `#14100C`),
   `file.import {addToComp}`, `layer.create {op:"shapesFromVector"}`, then `edit.clear` on the hidden SVG
   footage layer. Each SVG `<path id>` becomes a shape **group with that name**, which is what makes
   per-stone animation possible.
3. **build.jsx** (`effectcraft-cli script build.jsx panim-reveal.ecproj`): the layer is placed at em-centre
   (390,390) → comp centre at 0.88 px/unit. It is duplicated so the sigil gets its own layer, and the groups
   are pivoted (stave tops, eye centres, face bases). Keys are set with `setValueAtTime`, and each segment
   is eased with a CSS cubic-bezier converted to `KeyframeEase` speed/influence (outExpo for the cuts,
   outQuint for the faces and eyes, inOutSine for the breath). It adds the chisel stroke and trim path,
   the Glow effect, and the `the between` layer with two radial gradient fills.
4. **gif.jsx**: comp `Panim GIF` (512², 20 fps, 4.5 s) nests `Panim` with collapse transformations (the
   shapes are rasterised at 512, not shrunk from 1080). Time remap holds the last frame, and a queue item
   is added with `loop:false`.
5. **Renders**: `render --format webm`, `render --queue` (the GIF), `render-frame --frame 119` (the poster),
   and `exec file.exportLottie {textAsShapes:true}`.

## Verified

- `verify.jsx`: **63/63 pass**. The end frame is the still mark, with the outlines byte-for-byte those of
  `mark.svg` (`stave-l` = `[[100,160],[100,600],[180,600],[180,160]]` …), and frame 0 is dark.
- ffprobe: vp9, 1080×1080, 30/1, 4.000 s. sips: poster 1080×1080. `file`: GIF 512×512. No `NETSCAPE2.0`
  block, so the GIF plays once.
- Lottie export warnings: exactly one, `panim ▸ breath glow: effect not supported by Lottie (skipped)`.
  The JSON has 0 assets.
- **Lottie in a real player**: lottie-web 5.13.0 (SVG renderer) in headless chrome-headless-shell
  (`work/lottie-check/`). The staves, faces, opening eyes, chisel, column, warmth and rest all play. At
  the end frame, the mean difference from EffectCraft's own render is **0.25 levels** (the max of 45 is on
  anti-aliased edges). `work/lottie-vs-ec.png`.
- WebM quality: PSNR against EffectCraft's PNG renders is 39.8–39.9 dB at frames 66/81/119. That is the
  yuv420 ceiling (quality 95 gave 40.0 dB at 1.75× the size), so the default stays.
- Looked at: `work/review-strip.png` (17 frames), `poster.png`, `work/gif-final-strip.png`,
  `work/webm-crest*.png` (decoded crest, normal and 4× boosted).

## Honest shortfalls

- **The glow exists only in the raster outputs** (WebM, GIF, poster). Lottie has no Glow. Its breath is
  carried by the column of light and the warming fill alone, which is softer but still reads.
- **The GIF is 1.48 MB, not small.** The soft gradients and glow dither on every breath frame (20–33 KB
  each), and the v0.6.0 writer stores every frame whole. A diff-rectangle re-encode of the same GIF
  (ffmpeg, measurement only: `work/measure-only_ffmpeg-diffrect.gif`) was only 25% smaller, so most of
  the weight is the content itself. A no-glow GIF cut would be lighter; it was not made.
- **The halo's outer edge** still shows as a very faint oval on the resting frame. These are 8-bit steps
  of about 1 level at the halo rim. The first cut (stops 0/.45/1) showed it clearly; the bell-shaped
  stops reduced it, but EffectCraft has no gradient dithering to remove it.
- **The WebM ground decodes about 2–3 levels dark** (see above).
- **Dark theme only.** A light-theme reveal (bronze `#755A28` stones, rubric `#93362C` ▽ on parchment) was
  not built. The ending rests on the night palette.
- I watched no real-time playback. Motion was judged from 17 sampled frames, the eases' sampled curves,
  and lottie-web frames. Timing feel (for example whether the faces' 0.7 s approach is too slow) deserves
  a human eye.
- `../mark.svg` and the rest of the kit were not touched. Everything lives in `motion/`.

## ArtCraft friction log (effectcraft-cli 0.6.0, vectorcraft-cli 0.7.0)

**EC1 (praise). SVG ids become shape-group names.** `layer.create {"op":"shapesFromVector","layers":["#1"]}`
on the imported `stones.svg` gave one layer with a group per `<path>`, named `stave-l` … `sigil-hebrew`,
each with its own Transform. Per-piece animation of a real SVG needed no hand-built geometry. (The
original `mark.svg` imports as 2 groups because panim is one compound path, so the VectorCraft split
step matters.)

**EC2 (praise). The JSX engine is a real After Effects object model.**
`effectcraft-cli script build.jsx project.ecproj` supports `addProperty("ADBE Vector Group" | "… Stroke" |
"… Filter - Trim" | "ADBE Glo2")`, `setValueAtTime`, `setTemporalEaseAtKey` with `KeyframeEase` (sampled:
outExpo gives 0 → 47.9 → 73.5 → … → 100), `isSpatial`, `Layer.duplicate()`, `PropertyGroup.remove()`,
`timeRemapEnabled`, `collapseTransformation`, `app.project.save()`, and `app.project.file.parent`. Above
all there is **`app.run(id, params)`**, which reaches every one of the 665 engine commands from JSX
(`String(app.run)` = `function (id, params) { return __call(String(id), params || {}); }`).

**EC3 (inconsistency). Gradient Fill children ignore AE matchNames.** Fill, Stroke and Trim children
answer to `ADBE Vector Fill Color`, `ADBE Vector Stroke Width`, `ADBE Vector Trim End` and so on, but the
G-Fill's children are engine ids:
`gf.property("ADBE Vector Grad Colors")` → `null` (likewise `… Grad Type`, `… Grad Start Pt`, `… Grad End Pt`);
`gf.property("colors")` → `Colors`. AE scripts that touch gradients break silently (null, then a TypeError).

**EC4 (limitation). Gradient colours cannot be set from JSX, though they can be read.**
`gf.property("colors").setValue({t:"Gradient",v:{colors:[…],opacities:[…]}})` → `Error: value must be a number`;
the AE flat-array form gives `Error: value must be a number, not an array`. Reading `.value` returns that
very object. (Real AE cannot script gradient colours either, so this is faithful, but the engine can.)
Workaround used: `app.run("prop.set",{layer:col.id, path:"contents/halo/contents/gfill/colors", value:{…}})`.
Group-name paths work even though `props --flat` prints kind paths (`contents/group#2/…`).

**EC5 (surprise). Enum values are unlabeled and indexed differently per surface.**
`exec effect.list --params '{"filter":"glow"}'` gives `{"default":0,"id":"operation","name":"Composite Original"}`
with no option names. The JSX value for the same parameter reads `1`, and the gradient `Type` reads `1` in
JSX but `type enum 0` in `props`. I had to render a 3×2 matrix (`work/glow-composite-matrix.png`) to
learn that Composite Original **1 lays the glow over the source** (it bleached `#C9A45C` to cream:
`work/iter1-glow-bleached.png`), **2 keeps the source on top**, and 3 is glow-only. Glow Colors 2 = A & B.
Ask: put the option names in `effect.list` and `describe_command`.

**EC6 (bug). `render --bitrate` is silently ignored for WebM.**
`render … --format webm` at default, `--bitrate 1200` and `--bitrate 2500` → three identical files
(md5 `3a9f3540e71ee8f2fa77d6ae004b8c35`, 253,040 B). The only hint is the summary label switching from
`WebM (VP9 + Opus) · RGB` to `Custom`. Bitrate takes effect only with the output-module flag
`webmBitrate:true`, which the CLI cannot set: queue `{webmBitrate:true, bitrate:3000}` → 1,155,222 B.
`--video-quality 40` **does** work for WebM (59,038 B, md5 `924084fa…`), although `--help` lists it under
"HEVC / AV1". The label "VP9 + Opus" is printed even though no audio stream is written (ffprobe shows
one vp9 stream). That's the right output, but a misleading label.

**EC7 (limitation). A 30 fps GIF plays 11% fast.** `render --format gif` on the 30 fps comp wrote
`'duration': 30` ms per frame (GIF counts in 1/100 s), so 120 frames last 3.6 s instead of 4.0 s, with no
warning. Workaround: a 20 fps GIF comp (exact 50 ms).

**EC8 (limitation). GIF looping: no CLI flag; the queue works.** `render --format gif` always writes
`NETSCAPE2.0` loop 0 (forever). `app.run("renderQueue.add",{…,format:"gif",loop:false})` followed by
`render --queue --project …` writes no loop block (`gif_loop:false`), so the GIF plays once.

**EC9 (limitation). The GIF writer stores every frame whole.** Parsing the blocks shows every frame is a
full 512×512 rectangle with a local palette. Identical hold frames are not merged or diffed: 30 held
frames cost 21,287 B each. I cut the hold from 1.5 s to 0.5 s. Compared with a diff-rectangle re-encode
this costs only about 25% (1,478,277 → 1,121,855 B), so it's minor.

**EC10 (surprise). `render-frame --time 4.0` on a 4.0 s comp renders an empty frame,** silently (the out
point is exclusive: `work/iter1-glow-bleached.png`, last tile). The poster uses `--frame 119`. A warning
for a time at or after the comp's end would help.

**EC11 (minor). Key times snap to the comp frame grid while keeping the value.** In the 20 fps GIF comp,
`tr.setValueAtTime(3.9667, 3.9667)` made a key at **3.95** with value 3.9667, so time ran 0.4% fast
(`t(3.0)=3.0127`). Workaround: key on the grid (3.95 → 3.95), which gives `t(3.0)=3`.

**EC12 (praise). The Lottie export is faithful and lean.** 10.7 KB. Eases survive (outExpo
[0.16,1,0.3,1] comes out as `o:{x:.16,y:.977} i:{x:.3,y:1}`), the gradient opacity stops are encoded,
and there's one clear warning for the one unsupported thing (the glow). Thanks to the notes' `edit.clear`
it has 0 assets. lottie-web 5.13 matches EffectCraft to a mean of 0.25 levels.

**EC13 (praise). Fast and deterministic.** The 1080² 120-frame WebM renders in about 10 s on the CPU, the
GIF in 0.6 s, and a render-frame in about 13 ms. All six outputs, **including the .ecproj**, are
byte-identical across rebuilds. (Compare the VectorCraft kit's K3, where `file.new` stamps wall-clock
time.)

**EC14 (praise). `--resolution 0.4740741` gave exactly 512×512,** and `collapseTransformation` on the
nested comp rasterises the vectors at the target size.

**VC1 (praise). `object.compoundPath.release` keeps the child ids** (2–7), so naming by id afterwards is
safe. `document.inspect` shows the tree with ids and bounds.

**VC2 (minor). An SVG round-trip drops metadata.** `../mark.svg` carries `<title>panim — the YOUSPEAK
house mark</title>` and a `<desc>`. VectorCraft's re-export of it is titled `mark.svg` and has no
`<desc>`. Harmless here (stones.svg is an intermediate), but a pass-through edit loses the mark's
documentation.

Not ArtCraft: zsh does not word-split `$extra`, so my first `--bitrate` loop passed `"--bitrate 1200"` as
one argument and "failed". That was my error, not the CLI's.
