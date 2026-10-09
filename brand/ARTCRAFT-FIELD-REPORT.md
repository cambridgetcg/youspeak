# ArtCraft Field Report: building the ai-love.cc brand kit with agents

**Date:** 2026-10-09
**Environment:** macOS 15.7 (Darwin 24.6.0), Apple M3. CLIs on PATH: `vectorcraft-cli 0.7.0`, `photocraft-cli 0.5.0 (e5e3e3975, 2026-10-08)`, `effectcraft-cli 0.6.0`.
**Source:** 113 friction-log entries from 10 agent runs (mark:panim, mark:star, mark:kunance, mark:arch, mark:free, kit, og:tablet, og:nocturne, og-batch, motion) that built marks, favicons, lockups, 255 OG cards and a motion reveal.
**Method:** I merged the 89 friction entries into about 60 distinct items and kept the 24 praise entries separately. I re-ran the smallest repro of every major item myself (the agents logged no blockers), plus 16 cheap minor checks. All work and evidence files are in `brand/field-report/`. Nothing was filed upstream.

---

## 1. Verdict per app

| App | Ready for agent-driven brand-asset work? | Why, in one line |
|---|---|---|
| **VectorCraft 0.7.0** | **Yes, with guardrails.** It is the right master tool. | Deterministic, fast, exact rasters and clean SVG. But several commands fail silently (unknown ids, artboard export leaks, empty selections), so an agent must check every output it writes. |
| **PhotoCraft 0.5.0** | **Yes, for finishing and compositing only.** | Compositing is pixel-exact and layer styles stack headless. It cannot read SVG, writes only single-frame ICO, its chisel bevels stripe on oblique edges, and clipping breaks when the base layer's fill is 0. |
| **EffectCraft 0.6.0** | **Yes, for motion marks and Lottie.** | It has a real AE-style object model, faithful Lottie export and byte-identical rebuilds. `--bitrate` is silently ignored for WebM, and finding out what effect enum values mean takes trial renders. |

All 11 major items reproduced (one partly). One minor claim did not reproduce (EffectCraft GIF timing). Another turned out to be font data, not an ArtCraft bug (the Charter no-break space).

### Guardrails that made the pipeline safe (use these in any agent recipe)
1. **Never trust a `select.*` step that returns `null`.** Follow it with `document.inspect {"depth":0}` and assert that `selection` is not empty. Better, use `select.save` / `select.recall`, which fail loudly on unknown names.
2. **Export one artboard with `select.allOnArtboard {"artboard":N}` followed by `document.export {"artboard":N,"selectedOnly":true}`.** Never use a plain `artboard` / `artboards` / `range` export for SVG.
3. **Add `paint.setStroke {"none":true}` after every new shape.** The default stroke is 1 pt black.
4. **Pin `file.new {"created":null}`** to get byte-identical PNGs. `SOURCE_DATE_EPOCH` is ignored.
5. **Check the PNG colour type** (RGB vs RGBA) for assets that must be opaque, such as apple-touch-icon. Translucent paint at a fractional scale leaks alpha 254.
6. **Release compound paths before editing their members.**
7. **For WebM, use `--video-quality N`, not `--bitrate`.**
8. **In PhotoCraft, use the `smooth` bevel technique** (or a mirrored render) for any edge that is not 0/45/90 degrees.

---

## 2. What worked beautifully

- **Determinism across all three apps.** With `created` pinned, VectorCraft, PhotoCraft (seeded `filter.noise.addNoise`) and EffectCraft (including the `.ecproj`) rebuilt byte-identical outputs. I confirmed the VectorCraft case: two runs with `file.new {"created":null}` gave the same md5, `d83df4c2…`.
- **Exact raster sizing.** Fractional `scale` gives exact pixel sizes: 0.03125 → 16, 0.0625 → 32, 0.3515625 → 180, 0.375 → 192, 16 → 512. Fully opaque art is written as RGB without asking. A 16 px raster from a 32-unit grid is pixel-exact and beats any PhotoCraft downsample.
- **Clean, semantic SVG.** Object names become `id`/`data-name`, `file.info` becomes `<title>`/`<desc>`, there are no stray strokes once they are cleared, and an SVG round-trip renders pixel-identical to the PNG.
- **Geometry straight from text.** `path.create {"d":…}` accepts SVG path data, arcs included (converted to one cubic per 60°). Live chamfers are exact. Unite and `compoundPath.make` turned stepped pixel hinting into one integer-coordinate path.
- **Named selections as safe references.** `select.save` / `select.recall` persist in the `.vectorcraft` file and fail loudly on unknown names. With layer-scoped `select.object.allOnSameLayers` and `object.rotate {copy:true}` plus `transformAgain`, they let 92- to 185-step recipes run with no hard-coded ids.
- **Type.** `text.fonts` reports exact matches, `type.createOutlines` gives clean filled paths, point-text `y` is the baseline (cap height measured 696.8/1000), Hebrew bidi is laid out in correct visual order, and smart punctuation works headless.
- **The VectorCraft → PSD → PhotoCraft handoff.** Each VectorCraft layer becomes a named pixel layer, ready for per-layer styles. This was the backbone of the 255-card OG pipeline: about 0.06 s to compose a card and 0.25–0.45 s to finish it, so the full set ran in 37 s to 2 min with zero failures.
- **PhotoCraft compositing.** `file.placeEmbedded` with percentage scale and centre is pixel-exact, and contact sheets and tab mock-ups worked first time. Stacked layer styles (`add:true`: gradient overlay + smooth bevel + inner shadow + outer glow) give convincing gilded relief.
- **EffectCraft's scripting model.** It offers AE matchNames for most properties, `setValueAtTime`, temporal ease, `Layer.duplicate()`, time remap, and `app.run(id, params)` bridging to all 665 engine commands. `shapesFromVector` turns each SVG `<path id>` into its own animatable group.
- **Lottie export.** The file is 10.7 KB with eases preserved, gradient opacity stops encoded, and a clear warning for the one unsupported effect (Glow). lottie-web 5.13 matches the EffectCraft render to a mean of 0.25 levels.
- **Speed.** A VectorCraft run takes about 30–60 ms, a 185-step recipe about 1 s, a 1080² 120-frame WebM about 10 s on the CPU, and a GIF 0.6 s.

---

## 3. Bugs: major (all re-run by me)

Each repro runs from `brand/field-report/` with the CLIs on PATH.

### V1. VectorCraft: a one-artboard SVG export includes every other artboard's art. REPRODUCED
*Reported by 5 runs (panim, star, kunance, arch, free).*
```sh
vectorcraft-cli run -c file.new -p '{"width":100,"height":100}' \
  -c artboard.new -p '{"x":200,"y":0,"width":100,"height":100}' \
  -c shape.rectangle -p '{"x":10,"y":10,"width":80,"height":80}' -c paint.setFill -p '{"color":"#ff0000"}' \
  -c shape.ellipse   -p '{"x":210,"y":10,"width":80,"height":80}' -c paint.setFill -p '{"color":"#0000ff"}' \
  -c document.export -p '{"path":"r2-ab1.svg","artboard":1}'
grep '<path' r2-ab1.svg
```
- **Observed:** `viewBox="0 0 100 100"` is correct, but the file also holds artboard 0's rectangle off-canvas: `<path d="M-190 10 L-110 10 L-110 90 L-190 90 Z" fill="#ff0000"…>`. `artboards:[1]`, `range:"2"`, `useArtboards:true`, `svg:{useArtboards:true}` and multi-artboard `range:"1-2"` all leak the same way, with no warning. In the real build, `mark-dark.svg` came out at 38.5 KB with 27 paths instead of about 850 B with 1 path.
- **Expected:** An artboard export holds only the art that intersects that artboard (Illustrator's Use Artboards), or at least warns.
- **Partly reproduced:** kunance's claim that `artboards:[1]` used artboard 0's viewBox did not reproduce. The coordinates were translated to artboard 1 correctly; only the leak reproduced.
- **Workaround (verified):** `select.allOnArtboard {"artboard":1}` followed by `document.export {"artboard":1,"selectedOnly":true}` writes 1 path (`r2-ab1-sel.svg`).

### V2. VectorCraft: `select.set` / `select.add` silently accept ids that don't exist or aren't integers. REPRODUCED
*Reported by panim, star and kunance (major), and by kunance and arch (minor).*
```sh
vectorcraft-cli run -c file.new -p '{"width":100,"height":100}' \
  -c shape.rectangle -p '{"x":10,"y":10,"width":30,"height":30}' \
  -c select.set -p '{"ids":[999]}' -c select.set -p '{"ids":["$1.id"]}' -c select.add -p '{"ids":[999]}' \
  -c paint.setFill -p '{"color":"#00ff00"}' -c document.inspect -p '{"depth":0}' -o r3.svg; echo $?
```
- **Observed:** Every select step returns `{"result":null}` and the run exits 0. Inspect shows `"selection":[]`. `paint.setFill` then silently changes only the default paint (`paint.fill` goes to `#00ff00`), and the rectangle stays `#ffffff`.
- **Expected:** An error for unknown or ill-typed ids. At minimum, return `{count}` as `select.all` and `select.recall` do.

### V3. VectorCraft: `run` has no step-result references, and Pathfinder results hide the ids they use. REPRODUCED
*Reported by kunance (major), and by panim, star, arch and kit as context.*
```sh
vectorcraft-cli run -c file.new -p '{"width":100,"height":100}' \
  -c shape.rectangle -p '{"x":10,"y":10,"width":80,"height":80}' \
  -c shape.rectangle -p '{"x":30,"y":30,"width":40,"height":40}' \
  -c select.all -c object.pathfinder.minusFront -p '{}' \
  -c shape.rectangle -p '{"x":0,"y":0,"width":5,"height":5}'
```
- **Observed:** `minusFront` returns `{"ids":[4]}`, but its two subpaths silently take ids 5 and 6, so the next shape gets `{"id":7}`. Unite returns `[4]` and the next shape gets 5. Ids are deterministic in a fresh session but can't be predicted from the results. `"$N.id"` strings (which DesignCraft supports) are silently ignored (see V2).
- **Expected:** `$N.id` result references in `run`, or Pathfinder results that list every id they create. `select.recall {name, mode:"add"}` would also cover most cases.

### V4. VectorCraft: `text.setRangeStyle` requires `id` and has no selection fallback. REPRODUCED
*Reported by og:tablet, og:nocturne and og-batch, all major.*
```sh
vectorcraft-cli run -c file.new -p '{"width":600,"height":200}' \
  -c text.create -p '{"x":10,"y":60,"text":"plain and bold words","size":30,"font":"Charter","style":"Roman","color":"#000000"}' \
  -c text.setRangeStyle -p '{"start":10,"end":14,"style":"Bold"}'; echo $?
```
- **Observed:** `invalid parameters for 'text.setRangeStyle': missing 'id'`, exit 1. `text.setStyle` in the same position works on the selection (`{"ids":[2]}`). Passing `"id":"$1.id"` also gives the misleading `missing 'id'`.
- **Expected:** Default to the selected text object, as `text.setStyle` does, or support `$N.id`.
- **Workarounds the agents used:** predict sequential ids and check them against each step's `{id}` (this never drifted across 255 cards), or save, reopen with `--in`, and replay.

### V5. VectorCraft: clearing a selected compound-path member deletes the whole compound. REPRODUCED (details differ)
*Reported by panim.*
```sh
vectorcraft-cli run -c file.new -p '{"width":100,"height":100}' \
  -c shape.rectangle -p '{"x":10,"y":10,"width":30,"height":30}' \
  -c shape.rectangle -p '{"x":50,"y":10,"width":30,"height":30}' \
  -c select.all -c object.compoundPath.make -o r1-before.vectorcraft
vectorcraft-cli run -i r1-before.vectorcraft -c select.set -p '{"ids":[2]}' -c document.inspect -p '{"depth":0}' \
  -c edit.clear -o r1-after.svg
```
- **Observed:** Inspect reports `"selection":[2]` (the member), but `edit.clear` removes the whole compound (id 4): the layer ends empty with history `["Clear"]`, and there is no warning. The reporter saw the selection jump to the compound id; on my run the selection showed the member while the delete still hit the parent.
- **Expected:** Delete only member 2, or refuse with "member of compound path 4; release first".
- **Workaround (verified):** `select.set {ids:[4]}`, then `object.compoundPath.release`, then `select.set {ids:[2]}` and `edit.clear` leaves 1 path.

### V6. VectorCraft: a fully covered artboard with translucent paint exports RGBA at a fractional scale, even with `background`. REPRODUCED
*Reported by kunance.*
```sh
vectorcraft-cli run -c file.new -p '{"width":512,"height":512,"units":"Pixels"}' \
  -c shape.rectangle -p '{"x":0,"y":0,"width":512,"height":512}' -c paint.setFill -p '{"color":"#100D0A"}' -c paint.setStroke -p '{"none":true}' \
  -c shape.ellipse -p '{"x":56,"y":56,"width":400,"height":400}' -c paint.setStroke -p '{"none":true}' \
  -c paint.setFill -p '{"gradient":{"kind":"radial","stops":[{"offset":0,"color":"#E4C27C","opacity":0.2},{"offset":1,"color":"#E4C27C","opacity":0}]}}' \
  -c document.export -p '{"path":"r4-180.png","artboard":0,"scale":0.3515625,"background":"#100D0A"}' \
  -c document.export -p '{"path":"r4-512.png","artboard":0,"scale":1}'
```
- **Observed:** `r4-180.png` is RGBA with min alpha 254 on 96 pixels, despite the opaque full-bleed rectangle and an explicit `background`. `r4-512.png` (scale 1) is RGB. This breaks the opaque apple-touch-icon requirement.
- **Expected:** An opaque result at any scale. At minimum, `background` should flatten everything to opaque.
- **Workaround:** Pre-mix the gradient stops as opaque colours (#3A3121 → #100D0A).

### V7. VectorCraft: `file.place` of an SVG ignores its viewBox and fits the ink bounds. REPRODUCED
*Reported by og:nocturne (major), and by og:tablet and kit (minor).*
```sh
printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="M200 300 L600 300 L600 800 L200 800 Z"/></svg>' > r7-glyph.svg
vectorcraft-cli run -c file.new -p '{"width":1200,"height":630,"units":"Pixels"}' \
  -c file.place -p "{\"path\":\"$PWD/r7-glyph.svg\",\"rect\":[100,100,200,200]}"
```
- **Observed:** `width 160, height 200` at x 120, y 100: the 400×500 ink box is fitted and the 1000-unit em box is discarded. `crop:"crop"` (documented as the default, "clipped to that page or artboard") and `crop:"bounding"` behave the same. `crop:"media"` errors with "only PDF pages have…". Glyphs placed into equal rectangles lose their shared baseline.
- **Expected:** `crop:"crop"` honours the SVG viewBox as the page: 200×200, with the art at (140,130)–(220,230).
- **Workaround:** `path.create {d}` plus `object.transform {matrix}`, or compute each glyph's bbox and pass a rect scaled from em.

### P1. PhotoCraft: chisel bevels stripe on oblique edges in one diagonal direction. REPRODUCED
*Reported by og:tablet (major) and mark:free (minor).*
```sh
# r8-bars-shape.json is 8 bars, 150×16 px, at 0/30/45/60/90/120/135/150° (image coordinates, y down), as one path
photocraft-cli run --new '{"width":1200,"height":400,"background":"#1E1813"}' \
  --cmd shape.create --params "$(cat r8-bars-shape.json)" \
  --cmd layer.layerStyle.bevelEmboss --params '{"style":"inner","technique":"chiselHard","depth":220,"direction":"down","size":8,"soften":0,"angle":115,"altitude":32}' \
  --out r8-bars-shape.png
```
- **Observed:** Periodic comb or stair striations run along the facets of the 30° and 60° bars, the ones that lean `\` on screen, with a weaker effect at 120°. The 0/45/90/135/150° bars are clean. The worst-line standard deviation along the facets, in luma levels, was 0:0.0, 30:13.3, 45:0.3, 60:23.6, 90:0.0, 120:7.1, 135:0.0, 150:1.3. Vector shape layers and placed raster layers give identical numbers. `chiselSoft` halves the effect (60°: 11.4) but still combs, and `smooth` is clean (see `r8-60deg-techniques.png`, `r8-closeup.png`).
- **Refinement:** exact 45° edges are clean (a 45° diamond measured sd 0.0). "Every diagonal edge" (mark:free) is too broad; the artifact needs an oblique angle that is not 45°.
- **Expected:** Chisel bevels look the same whatever the edge orientation.
- **Workaround:** `smooth` technique, or a mirrored render, as og:tablet did.

### P2. PhotoCraft: clipped layers disappear when the clipping base's Fill is 0. REPRODUCED — but NOT a bug: this is Photoshop's default "Blend Clipped Layers as Group" (see §7)
*Reported by og:tablet.*
```sh
photocraft-cli run --new '{"width":200,"height":200,"background":"#ffffff"}' \
  --cmd shape.create --params '{"kind":"rect","rect":[50,50,100,100],"fill":"#0000ff","name":"base"}' \
  --cmd shape.create --params '{"kind":"rect","rect":[0,0,200,200],"fill":"#ff0000","name":"clipped"}' --out r9.psd
photocraft-cli run r9.psd --cmd layer.setProps --params '{"layer":4,"clipped":true}' \
  --cmd layer.setProps --params '{"layer":3,"fill":0.0}' --out r9-fill0.png
```
- **Observed:** The pixel at (100,100) inside the base is (255,0,0) with base fill 1, **(255,128,128) with fill 0.5**, and (255,255,255) with fill 0. Base Fill is applied like group opacity to everything clipped to it.
- **Expected (Photoshop behaviour, per the reporter):** Fill hides only the base layer's own pixels. The clip still follows the base's transparency, so the clipped red shows at full strength. (Base *opacity* 0 hiding the group, which also happens, is correct.)
- **Workaround:** `select.loadSelection {channel:"transparency", layer:base}`, then `layer.layerMask.revealSelection`.

### E1. EffectCraft: `render --bitrate` is ignored for WebM. REPRODUCED
*Reported by motion.*
```sh
effectcraft-cli run --empty comp.new '{"name":"T","width":256,"height":256,"frameRate":30,"duration":1}' \
  layer.newText '{"text":"AI","size":120,"fill":"#C9A45C","name":"Mark","position":[128,170]}' --save-as $PWD/r10.ecproj
for b in 200 3000; do effectcraft-cli render --project $PWD/r10.ecproj --comp T --out $PWD/r10-$b.webm --format webm --bitrate $b; done
effectcraft-cli render --project $PWD/r10.ecproj --comp T --out $PWD/r10-none.webm --format webm
md5 -r r10-*.webm
```
- **Observed:** No flag, `--bitrate 200`, `--bitrate 3000` and `--bitrate 3000 --rate-control bitrate` all give the same file (md5 `72fd9994…`, 72,235 B). `--video-quality 40` does change the output (17,090 B), although `--help` groups it under HEVC/AV1. According to the reporter, bitrate applies only with the output-module flag `webmBitrate:true`, which only the render queue can set.
- **Expected:** `--bitrate` changes the WebM, or the CLI rejects or warns about it.

### E2. EffectCraft: `effect.list` gives enum params as bare numbers, with a different base from JSX. REPRODUCED
*Reported by motion.*
```sh
effectcraft-cli exec effect.list --params '{"filter":"glow"}' --json   # ec.stylize.glow
effectcraft-cli script r11.jsx $PWD/r11.ecproj                       # adds ec.stylize.glow, prints p.value per property
```
- **Observed:** The catalogue gives `{"default":0,"id":"operation","name":"Composite Original"}` and `{"default":1,"id":"based",…}`, with no type, option names or range. JSX reads the same defaults as `Composite Original=1`, `Glow Based On=2`, `Glow Colors=1`: 1-based, as in AE, against the catalogue's 0-based values. The meaning of each value could only be learnt by rendering a matrix: 1 = glow over the source, 2 = source on top, 3 = glow only.
- **Expected:** Enum params list their options (`[{value, label}]`) and say which base each surface uses.

---

## 4. Bugs: minor

"Re-run" means I ran it today. "Seen" means it showed up as a side effect of another repro. "Not re-run" means it comes from the agents' logs only.

### VectorCraft 0.7.0
| # | Issue (reporters) | Observed → expected | Status |
|---|---|---|---|
| v8 | `edit.clear {"ids":[4]}` needs a selection (panim) | "command `edit.clear` is not available right now: nothing selected", exit 1, though the catalogue says `{ids?} delete the objects ids, else the selection` → delete by ids | **Re-run: reproduced** |
| v9 | `select.allOnArtboard` returns `null` (arch) | other selectors return `{count}` → return `{count}` | **Re-run: reproduced** |
| v10 | Inspect shows no fill on compound paths or outlined text (panim, star, arch) | compound node has no `fill` key and its members say `"fill":"None"`, while the export paints correctly → report the effective paint | **Seen (R1): reproduced** |
| v11 | `select.same.fillColor` misses compound paths (star) | count 1 instead of 2 | Not re-run |
| v12 | Unite leaves a zero-width slit or a duplicate vertex (star) | `…L26 10 L26 10…`; the hole is joined to the outline by a slit → shared edges should dissolve cleanly | Not re-run |
| v13 | `minusFront` leaves a zero-length segment that `simplify` and `cleanUp` don't remove (star) | `L100.01 238.12 L100.01 238.12 Z` | Not re-run |
| v14 | `minusFront` with only one object returns its id and does nothing (star) | → warn that two or more objects are needed | Not re-run |
| v15 | Float drift: `rotate` + `transformAgain` ×3 gives 157.01/354.99; `setBounds` inspect gives 5.999999999999975 (star, panim) | → snap multiples of 90° to exact matrices | Not re-run |
| v16 | An edited SVG's `<title>` becomes the file name and `<desc>` is dropped (star, motion) | `<title>Keep me</title><desc>…` becomes `<title>m4.svg</title>` → keep the imported metadata | **Re-run: reproduced** |
| v17 | SVG ids silently deduplicated when a layer and an object share a name (kit) | `<g id="panim">` + `<path id="panim-2">` → warn, or document the rule | Not re-run |
| v18 | Wall-clock creation time stamped into every PNG; `SOURCE_DATE_EPOCH` ignored (kit, free) | two runs with SDE set gave different md5s; `file.new {"created":null}` gave identical ones → honour SDE | **Re-run: reproduced** (the documented `created:null` fix works) |
| v19 | pHYs stores the scaled ppi (a 16 px favicon declares 2.26 dpi) (free) | → keep 72 dpi metadata, or let it be set separately from scale | Not re-run |
| v20 | A non-UTF-8 byte in argv crashes the CLI with a Rust panic (og:tablet) | `thread 'main' panicked at …env.rs:878:51`, exit 101 → a clean error naming the argument | **Re-run: reproduced** |
| v21 | `"id":"$1.id"` gives a misleading message (new) | `missing 'id'` when the id is present but not an integer → "id must be an integer" | **Re-run: reproduced** |
| v22 | `vectorcraft-cli run --help` (kunance) | "unknown run option `--help`" → subcommand help | **Re-run: reproduced** |
| v23 | Every new object gets a 1 pt black stroke (kunance, arch, free, notes) | 39 and 11 extra `setStroke none` steps in two recipes; an unpainted unite comes out white with a black stroke → a per-run default or a paint argument on create | **Seen (R2 SVG `stroke="#000000"`)** |
| v24 | `text.create` without `style` asks for "Regular" and Charter reports `substitute` (og:tablet, og:nocturne) | resolves to "Roman" but is flagged as a substitution → default to the family's upright | **Re-run: reproduced** |
| v25 | `text.fonts.missingGlyphs` is a count, not the characters (og:tablet, og-batch) | `"missingGlyphs":2` → list the code points, as the catalogue wording promises | **Re-run: reproduced** |
| v26 | The Titling face draws lowercase in a sans fallback while reporting `exact`, and the SVG drops the style name (og:nocturne) | → warn, and keep the style in the SVG | Not re-run |
| v27 | Bidi text is outlined in the SVG (with a warning), which breaks `<tspan>`-based line counting (og:nocturne) | by design, but no overset or line-count query exists (see missing features) | Not re-run |
| v28 | `type.convertToPointType {}` converts only the selection, silently; soft wraps after a hyphen or slash *insert* `\n`, while wraps at a space *replace* it (og-batch) | byte offsets for `setRangeStyle` drift → act consistently, or return an offset map | Not re-run |
| v29 | Radial gradient extent is a circle sized to the long side, and `aspect` only squashes y (panim, og:nocturne) | a tall ellipse needs start/end along the long axis plus aspect → fit the extent to the object bounds by default | Not re-run |

### PhotoCraft 0.5.0
| # | Issue (reporters) | Observed → expected | Status |
|---|---|---|---|
| p3 | ICO output is single-frame only (panim, star, arch, kunance, kit) | `MS Windows icon resource - 1 icon, 32x32` → multi-size 16/32/48 | **Re-run: reproduced** |
| p4 | Warning noise on stderr (6 runs) | "2 text metadata entries are not kept", "resolution (DPI) not supported", "lossy compression", "layer(s) flattened" on every VectorCraft PNG and every JPEG; over 255 cards × 6 layers this hides real warnings → `--quiet`, or stay silent for sibling-app metadata | **Re-run: reproduced** |
| p5 | `resample:"nearest"` is ignored for embedded or placed layers (star) | blurry 16 px favicons; `layer.flattenImage` first fixes it | Not re-run |
| p6 | `placeEmbedded` rounds the origin to a whole pixel (free) | `[102.0,…]` instead of `[102.4,…]`, 0.4 px off centre | Not re-run |
| p7 | No way to bake a layer style into pixels (og:tablet) | `layer.rasterize.layer` gives "nothing to rasterize"; workaround: an empty layer below plus `mergeDown` | Not re-run |
| p8 | Camera Raw `vignetteStyle:"highlightPriority"` looks like a no-op unless `vignetteHighlights` is set (og:nocturne) | Lightroom-consistent, but the param docs don't say so | Not re-run |

### EffectCraft 0.6.0
| # | Issue (reporters) | Observed → expected | Status |
|---|---|---|---|
| e3 | Gradient Fill children don't answer to AE matchNames (motion) | `gf.property("ADBE Vector Grad Colors")` and `("ADBE Vector Grad Type")` return `null`; the engine id `"colors"` works → resolve the AE matchNames | **Re-run: reproduced** |
| e4 | JSX `setValue` can't set gradient colours (motion) | "value must be a number", although `.value` returns that exact object; workaround `app.run("prop.set",…)` (real AE can't either) | Not re-run |
| e5 | The CLI always writes a looping GIF (motion) | NETSCAPE2.0 block always present; play-once only via the render queue `{loop:false}` | **Re-run: loop block confirmed** (queue route not re-run) |
| e6 | `render-frame --time <duration>` gives an empty frame (motion) | `--time 1.0` on a 1 s comp gives 1 distinct colour; `--frame 29` gives 423 → warn or clamp at the exclusive out point | **Re-run: reproduced** |
| e7 | A timeRemap key time snaps to the frame grid but keeps its off-grid value (motion) | the remap runs 0.4% fast | Not re-run |
| e8 | GIF frames are stored full-frame with local palettes; identical hold frames cost 21 KB each (motion) | ffmpeg differencing is only 25% smaller | Not re-run |
| e9 | The summary label says "VP9 + Opus" with no audio stream, and "Custom" when `--bitrate` is passed (motion) | the label suggests the flag took effect | Not re-run |

### Not reproduced, or not ArtCraft bugs
- **EffectCraft GIF at 30 fps "plays 11% fast" (motion): NOT REPRODUCED.** The frame delays alternate 3/4/3 centiseconds. 30 frames sum to exactly 100 cs and 120 frames (a 4 s comp) to exactly 400 cs, so playback length is correct. The reporter probably read only the first delay.
- **Charter's U+00A0 sets at twice the width of a space (og-batch): font data, not VectorCraft.** I parsed `/System/Library/Fonts/Supplemental/Charter.ttc` directly. U+00A0 maps to glyph 172 with an advance of 1139/2048, against 569/2048 for the space, in every Charter face. VectorCraft reproduces the font faithfully (`a b` 132.4 px, `a b` 160.2 px, `ab` 104.6 px at 100 px). **Warning:** the U+202F workaround is *not in Charter* (its cmap has no entry), so it is drawn by the fallback font.
- **A seam on abutting shapes at fractional scale (arch):** a standard conflation artifact. Uniting same-colour shapes before raster export avoids it, which is worth a docs tip.
- **The "dark halo" in a PhotoCraft downsample (kunance):** the reporter corrected this themselves; pixel checks show exact compositing.
- **"No way to pin the creation time" (kit):** `file.new {"created":null}` exists in the catalogue and works (v18). Only `SOURCE_DATE_EPOCH` is missing.
- **Chrome reports 1 dppx inside an SVG used as an image (kit):** a browser behaviour, outside ArtCraft.
- **`object.move {copy:true}` stacks the copy directly above its source (panim):** Illustrator behaviour, but easy to miss headless (blank app-icon tiles). This is a docs tip.

---

## 5. Missing features (ranked by how often they cost the agents time)

1. **Step-result references in `vectorcraft-cli run`** (`$N.id`, as in DesignCraft), plus **`select.recall {mode:"add"}`** or a list of names. Cited by 8 of the 10 runs, directly or through workarounds.
2. **Multi-frame ICO** (`sizes:[16,32,48]`) in PhotoCraft. Every favicon run hit this.
3. **Option names for enum params** in EffectCraft's `effect.list` (E2).
4. **A `--quiet` flag**, or quiet by default, for PhotoCraft's harmless warnings.
5. **Ink or preview bounds** in `document.inspect` (fonts currently report ascent and descent, not ink), plus an **overflow flag or line count for area type**.
6. **A list of missing glyph code points** in `text.fonts` (v25) and an **offset map** from `convertToPointType` (v28).
7. **A theme-aware SVG option** that writes theme-swapped fills under `@media (prefers-color-scheme)`, so one favicon SVG can serve both themes.
8. **Per-artboard or per-export `title`/`desc`**, and keeping the imported `<title>`/`<desc>` (v16).
9. **A per-run default paint**, for example `file.new {defaultStroke:"none"}` or paint arguments on `shape.*` and `path.create` (v23).
10. **`SOURCE_DATE_EPOCH`** support (v18) and a 72-dpi pHYs at fractional scale (v19).
11. **PhotoCraft:** bake a layer style into pixels (p7); Bevel & Emboss highlight and shadow mode/opacity; a box/area-average resample for icon downsampling; several `--out` files from one run.
12. **VectorCraft:** `makePixelPerfect` against the export scale, not just 1 pt; compact or zipped `.vectorcraft` files (now 570–640 KB of pretty-printed JSON, against about 130–146 KB compact, 6.5 KB of it a swatch library).
13. **EffectCraft:** `--bitrate` that actually works (E1) and a `--loop` / `--no-loop` flag for GIFs on the CLI (e5).

---

## 6. Documentation mismatches

| App | Doc says | Behaviour | Verified |
|---|---|---|---|
| VectorCraft | `edit.clear {ids?}`: "delete the objects `ids`, else the selection" | refuses with "nothing selected" when `ids` is given, exit 1 | Re-run |
| VectorCraft | `file.place crop:"crop"`: "clipped to that page or artboard, default" | for SVG, the viewBox is ignored and the art is fitted to its ink bounds; `crop` behaves like `bounding` | Re-run |
| VectorCraft | SVG option `useArtboards` (default true): "false: one SVG of the bounds of all art instead of artboards" | `true` sets the viewBox but does not clip or omit art from other artboards (V1) | Re-run |
| VectorCraft | `document.export range`: "SVG writes one file per artboard, `{stem}-{artboard}.svg`" | names use the artboard *name*: `r3range-Artboard-1.svg` | Re-run |
| VectorCraft | `text.fonts missingGlyphs`: "characters of its text the resolved font lacks" | an integer count | Re-run |
| VectorCraft | `type.convertToPointType {ids?}` | empty params act on the selection only, without saying so | Not re-run |
| VectorCraft | `text.create` y | point text: y is the baseline; area text: y is the frame top (undocumented) | Not re-run |
| VectorCraft | `document.inspect` children | listed top-most first (reverse creation order), undocumented | Not re-run |
| VectorCraft | `paint.setFill` gradient "fits each object" | a radial extent is a circle sized to the long side; `aspect` is documented only under `paint.setGradientGeom` | Not re-run |
| PhotoCraft | opacity | `layer.setProps` uses 0..1, but layer styles and `edit.fill` use 0..100 (VectorCraft `object.setProps` uses 0..100, and its gradient stops accept either) | Catalogue checked |
| PhotoCraft | `edit.transform` matrix: "affine alternative" | it is in document space (verified by og:tablet); undocumented | Not re-run |
| EffectCraft | `render --help` lists `--video-quality` under HEVC/AV1 and `--bitrate` as general | `--video-quality` works for WebM, `--bitrate` does nothing for WebM | Re-run |
| EffectCraft | `render-frame --time` | the out point is exclusive, so `--time <duration>` renders empty, undocumented | Re-run |

---

## 7. Issues worth filing upstream

**Filed 2026-10-09** after each draft was re-run on the latest releases (VectorCraft 0.7.0, PhotoCraft 0.5.0, EffectCraft 0.6.0), checked against upstream issues and main, and reviewed by a second agent who re-ran the repro as written:

| draft | outcome |
|---|---|
| 1 | not filed: already upstream as [vectorcraft#550](https://github.com/storytold/vectorcraft/issues/550), fixed on main (b832599) one commit after v0.7.0 |
| 2 | [vectorcraft#784](https://github.com/storytold/vectorcraft/issues/784) |
| 3 | [vectorcraft#785](https://github.com/storytold/vectorcraft/issues/785) |
| 4 | [vectorcraft#786](https://github.com/storytold/vectorcraft/issues/786) |
| 5 | [vectorcraft#787](https://github.com/storytold/vectorcraft/issues/787) |
| 6 | [vectorcraft#788](https://github.com/storytold/vectorcraft/issues/788) |
| 7 | [photocraft#1926](https://github.com/storytold/photocraft/issues/1926) |
| 8 | **withdrawn — our mistake.** Clipped layers fading with the base's Fill is Photoshop's default ("Blend Clipped Layers as Group"); PhotoCraft matches it |
| 9 | [effectcraft#440](https://github.com/storytold/effectcraft/issues/440) |
| 10 | [effectcraft#441](https://github.com/storytold/effectcraft/issues/441) |

The filed texts were corrected in review and differ from the drafts below; the issues are the record.


Each draft is ready to paste. The environment line for all of them: *macOS 15.7 (Darwin 24.6.0), Apple M3; vectorcraft-cli 0.7.0 / photocraft-cli 0.5.0 (e5e3e3975) / effectcraft-cli 0.6.0; headless CLI.* PhotoCraft's repo is storytold/photocraft (per ARTCRAFT-NOTES). I did not verify the VectorCraft and EffectCraft repo names.

### 1. [VectorCraft] SVG export of one artboard includes the art of every other artboard
> **Repro**
> ```
> vectorcraft-cli run -c file.new -p '{"width":100,"height":100}' -c artboard.new -p '{"x":200,"y":0,"width":100,"height":100}' -c shape.rectangle -p '{"x":10,"y":10,"width":80,"height":80}' -c shape.ellipse -p '{"x":210,"y":10,"width":80,"height":80}' -c document.export -p '{"path":"ab1.svg","artboard":1}'
> ```
> **Observed:** `ab1.svg` has `viewBox="0 0 100 100"` but contains the artboard-0 rectangle at `d="M-190 10 …"` (off-canvas). `artboards:[1]`, `range:"2"`, `range:"1-2"` and `useArtboards:true` behave the same, with no warning. In a real multi-artboard brand file this inflated an 850 B one-path mark into a 38 KB file with 27 paths, including the other theme's colours.
> **Expected:** Only the art that intersects the chosen artboard is written (Illustrator "Use Artboards"), or there is a documented option to clip to the artboard.
> **Workaround:** `select.allOnArtboard {"artboard":N}` + `document.export {"artboard":N,"selectedOnly":true}`.

### 2. [VectorCraft] `select.set` / `select.add` silently accept unknown or non-integer ids (exit 0)
> **Repro:** `… -c shape.rectangle … -c select.set -p '{"ids":[999]}' -c paint.setFill -p '{"color":"#00ff00"}'`; the same happens with `{"ids":["$1.id"]}`.
> **Observed:** `{"result":null}`, exit 0, selection `[]`. The following `paint.setFill` changes only the default paint, and the object keeps its old fill. Nothing in the output shows that the step did nothing.
> **Expected:** An error for ids that don't exist or aren't integers, or at least `{count}` as `select.all` and `select.recall` return. (`select.allOnArtboard` also returns `null` instead of `{count}`.)
> **Why it matters:** headless agents rely on step results; a silent empty selection makes later steps quietly edit the wrong thing.

### 3. [VectorCraft] `run`: step-result references (`$N.id`), a selection fallback for `text.setRangeStyle`, and complete Pathfinder results
> `text.setRangeStyle` right after `text.create` fails with `missing 'id'` (exit 1), even though the new text is selected; `text.setStyle` in the same position works on the selection. Passing `"$1.id"` also says `missing 'id'`. Separately, `object.pathfinder.minusFront` returns `{"ids":[4]}` while its subpaths take ids 5 and 6 without being reported, so the next object's id can't be predicted from the results.
> **Proposal:** support DesignCraft-style `"$N.id"` references in `run`; let `setRangeStyle` default to the selected text object; list every created id in Pathfinder results; add `select.recall {name, mode:"add"}`.
> **Evidence:** three separate OG-card pipelines (255 cards each) needed id-prediction or save-and-reopen workarounds.

### 4. [VectorCraft] `edit.clear` on a selected compound-path member deletes the whole compound; `edit.clear {ids}` needs a selection
> **Repro:** two rectangles → `select.all` → `object.compoundPath.make` → (reopen) `select.set {"ids":[2]}` → `edit.clear`.
> **Observed:** inspect shows `selection:[2]`, but Clear removes compound 4 entirely (the layer ends empty), with no warning. Separately, `edit.clear {"ids":[4]}` with nothing selected fails with "not available right now: nothing selected" (exit 1), although the catalogue documents `{ids?}`.
> **Expected:** delete only the member, or refuse and name its parent; `ids` should work without a selection.

### 5. [VectorCraft] PNG at a fractional scale has alpha 254 for fully covered art with translucent paint, even with `background`
> **Repro:** a 512² opaque `#100D0A` rectangle, plus an ellipse with a radial gradient whose stops have opacity 0.2 → 0, then `document.export {"scale":0.3515625,"background":"#100D0A"}`.
> **Observed:** a 180² RGBA PNG with min alpha 254 on 96 pixels. At scale 1 the same art gives an RGB PNG.
> **Expected:** an opaque, RGB result at any scale; `background` should always flatten. (This breaks apple-touch-icon, which must be opaque.)

### 6. [VectorCraft] `file.place` of an SVG ignores the viewBox (`crop:"crop"` behaves like `"bounding"`)
> **Repro:** an SVG with `viewBox="0 0 1000 1000"` and ink at (200,300)–(600,800) → `file.place {"path":…, "rect":[100,100,200,200]}`.
> **Observed:** placed at 160×200 (the ink box is fitted); the viewBox is discarded. `crop:"crop"` (documented as the default, "clipped to that page or artboard") gives the same result. Glyph SVGs placed into equal rectangles lose their shared em box and baseline.
> **Expected:** `crop:"crop"` treats the SVG viewBox as the page (200×200 here), keeping its internal offsets.

### 7. [PhotoCraft] Chisel Hard / Chisel Soft bevels stripe on oblique edges (not 45°) in one diagonal direction
> **Repro:** eight 150×16 px bars at 0–150° on one shape layer → `layer.layerStyle.bevelEmboss {"style":"inner","technique":"chiselHard","depth":220,"direction":"down","size":8,"soften":0,"angle":115,"altitude":32}`.
> **Observed:** periodic stair or comb striations along the facets of the bars at 30° and 60° (leaning `\` on screen, y down), and weaker at 120°. The 0/45/90/135/150° bars are clean. Facet-line luma standard deviation: 30° 13.3, 60° 23.6, 120° 7.1, against ≤ 1.3 elsewhere. Raster (placed PNG) and vector shape layers measure identically, and the light angle makes no difference (reporter). `chiselSoft` halves it; `smooth` is clean.
> **Expected:** facet quality that does not depend on edge orientation. This looks like a direction-dependent distance-transform step. Images available on request.

### 8. [PhotoCraft] Clipped layers fade or disappear when the clipping base's Fill opacity is lowered
> **Repro:** white background; base rectangle (layer 3); a full-canvas red rectangle (layer 4) with `layer.setProps {"layer":4,"clipped":true}`; then `layer.setProps {"layer":3,"fill":F}`.
> **Observed:** the pixel inside the base is (255,0,0) at F=1, (255,128,128) at F=0.5, and white at F=0.
> **Expected (Photoshop):** Fill affects only the base's own pixels; the clipped layer stays at full strength inside the base's alpha. Workaround: load the base transparency as a selection, then `layer.layerMask.revealSelection`.

### 9. [EffectCraft] `render --bitrate` has no effect on WebM output
> **Repro:** `effectcraft-cli render --project p.ecproj --comp T --format webm --out a.webm --bitrate 200`, then the same with `3000` and with no flag (also with `--rate-control bitrate`).
> **Observed:** all outputs are byte-identical (md5 72fd9994…). Only `--video-quality N` changes the file. Through the render queue, bitrate works only with the output-module flag `webmBitrate:true`, which the CLI cannot set. The summary label then says "Custom" (and "VP9 + Opus" even when no audio is written).
> **Expected:** `--bitrate` sets `webmBitrate:true` for WebM, or the CLI warns that it is ignored; `--help` should list `--video-quality` for WebM.

### 10. [EffectCraft] `effect.list` gives enum params without option names, and with a different base from JSX
> **Repro:** `effectcraft-cli exec effect.list --params '{"filter":"glow"}' --json`, then read the same properties from JSX after `addProperty("ec.stylize.glow")`.
> **Observed:** `{"default":0,"id":"operation","name":"Composite Original"}` has no type, options or range. JSX reports the same default as `1` (Glow Based On: 1 vs 2; Glow Colors: 0 vs 1). Finding out what the values mean took a render matrix.
> **Expected:** enum params carry `type:"enum"` and `options:[{value,label}]`, and each surface states whether it is 0-based or 1-based.

*Lower priority, could be one combined issue:* PhotoCraft multi-frame ICO plus `--quiet`. VectorCraft polish: `run --help`, the panic on a non-UTF-8 argument, keeping imported `<title>`/`<desc>`, `SOURCE_DATE_EPOCH`, and `missingGlyphs` as code points.

---

## Appendix: evidence files (in `brand/field-report/`)
- V1: `r2-ab0.svg`, `r2-ab1.svg`, `r2-range.svg`, `r2b-*.svg`, `r3range-Artboard-{1,2}.svg`, with the workaround in `r2-ab1-sel.svg`
- V2: `r3.svg` · V5: `r1-before.vectorcraft`, `r1-after.svg`, `r1-workaround.svg` · V6: `r4-180.png` (RGBA), `r4-512.png` (RGB) · V7: `r7-glyph.svg`
- P1: `r8-bars-shape.png`, `r8-bars-raster-bevel.png`, `r8-bars-chiselSoft.png`, `r8-bars-smooth.png`, `r8-closeup.png`, `r8-60deg-techniques.png` · P2: `r9.psd`, `r9-fill{1,05,0}.png`, `r9-opac0.png`
- E1: `r10-*.webm` · E2: `r11.jsx` · e3: `m7.jsx` · e5 and the GIF timing check: `m2.gif`, `m2b.gif` · e6: `m3-t1.png`, `m3-f29.png`
- v16: `m4.svg` → `m4-out.svg` · v18: `m5-{1,2}.png` (differ), `m5-null{1,2}.png` (identical) · p3/p4: `m1.ico`
- Command catalogues captured: `catalogue.json` (VectorCraft, 685 commands), `pc-catalogue.json` (PhotoCraft, 817), `ec-catalogue.json` (EffectCraft, 665)
