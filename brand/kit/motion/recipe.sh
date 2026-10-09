#!/bin/bash
# recipe.sh: rebuilds the panim reveal (ai-love.cc / YOUSPEAK animated mark) from ../mark.svg.
# ArtCraft only: vectorcraft-cli 0.7.0 splits the mark, effectcraft-cli 0.6.0 animates and exports.
# Outside ArtCraft, only to CHECK the outputs: ffprobe, sips, file, and (if present) lottie-web in
# headless Chrome via work/lottie-check/shoot.sh.
#
#   bash recipe.sh            rebuild everything + verify
#   bash recipe.sh --frames   also render the review strip frames into work/frames/
set -euo pipefail
M="$(cd "$(dirname "$0")" && pwd)"          # kit/motion
K="$(dirname "$M")"                         # kit (mark.svg lives here; READ ONLY)
W="$M/work"; mkdir -p "$W"
VC=vectorcraft-cli; EC=effectcraft-cli
say() { printf '\n== %s\n' "$*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }

say "versions"
$VC --version 2>/dev/null || true
$EC --version
[ -f "$K/mark.svg" ] || fail "no $K/mark.svg"

# 1. VectorCraft: release the compound panim path into seven named stones (ids 2-7 and 9 are
#    asserted by name below, so a changed mark.svg fails loudly instead of animating the wrong piece).
say "1. VectorCraft: split mark.svg into named stones → stones.svg"
$VC run --in "$K/mark.svg" \
  --cmd select.set --params '{"ids":[8]}' --cmd object.compoundPath.release \
  --cmd object.setProps --params '{"id":2,"name":"stave-l"}' \
  --cmd object.setProps --params '{"id":3,"name":"stave-r"}' \
  --cmd object.setProps --params '{"id":4,"name":"face-l"}' \
  --cmd object.setProps --params '{"id":5,"name":"face-r"}' \
  --cmd object.setProps --params '{"id":6,"name":"eye-l"}' \
  --cmd object.setProps --params '{"id":7,"name":"eye-r"}' \
  --cmd select.set --params '{"ids":[9]}' --cmd paint.setFill --params '{"color":"#755A28"}' \
  --cmd select.none \
  --export "$M/stones.svg" > "$W/vectorcraft-split.log"
for id in stave-l stave-r face-l face-r eye-l eye-r sigil-hebrew; do
  grep -q "id=\"$id\"" "$M/stones.svg" || fail "stones.svg lacks $id"
done
echo "stones.svg: 7 named paths ($(grep -c '<path' "$M/stones.svg") <path>)"

# 2. EffectCraft: comp + import + shapesFromVector; edit.clear drops the hidden SVG footage layer,
#    which would otherwise ride into the Lottie as a mislabelled image asset (ARTCRAFT-NOTES).
say "2. EffectCraft: import stones.svg as shape layers → work/import.ecproj"
rm -f "$W/import.ecproj"
$EC run --empty \
  comp.new '{"name":"Panim","width":1080,"height":1080,"frameRate":30,"duration":4,"background":"#14100C"}' \
  file.import '{"paths":["'"$M"'/stones.svg"],"addToComp":true}' \
  --save-as "$W/import.ecproj" --json > "$W/effectcraft-import.log"
$EC run "$W/import.ecproj" comp.open '{"comp":"Panim"}' \
  layer.create '{"op":"shapesFromVector","layers":["#1"]}' edit.clear '{"layers":["#2"]}' \
  --save --json >> "$W/effectcraft-import.log"

# 3. choreography (build.jsx), the 512 GIF comp + its render-queue item (gif.jsx), proofs (verify.jsx)
say "3. EffectCraft JSX: build.jsx → panim-reveal.ecproj; gif.jsx; verify.jsx"
cp "$W/import.ecproj" "$M/panim-reveal.ecproj"
$EC script "$M/build.jsx"  "$M/panim-reveal.ecproj"
$EC script "$M/gif.jsx"    "$M/panim-reveal.ecproj"
$EC script "$M/verify.jsx" "$M/panim-reveal.ecproj"

# 4. renders. Absolute --out paths: v0.6.0 resolves relative ones against the project folder.
say "4. renders"
rm -f "$M/mark-reveal.webm" "$M/mark-reveal.mp4" "$M/mark-reveal-512.gif" "$M/poster.png" "$M/mark-reveal.json"
# WebM at the encoder default (quality 90, ~250 KB). Note: --bitrate is ignored for WebM in v0.6.0.
$EC render --project "$M/panim-reveal.ecproj" --comp Panim --out "$M/mark-reveal.webm" --format webm --channels rgb
# H.264 for Safari, whose WebM support is patchy (added at publish; --bitrate is honoured for h264, not webm)
$EC render --project "$M/panim-reveal.ecproj" --comp Panim --out "$M/mark-reveal.mp4" --format h264 --bitrate 700
# GIF from the queue item gif.jsx saved (512 px, 20 fps, loop off; the CLI has no --loop flag)
$EC render --queue --project "$M/panim-reveal.ecproj"
# poster = the last frame (frame 119 = 3.9667 s; --time 4.0 is the out point and renders empty)
$EC render-frame --project "$M/panim-reveal.ecproj" --comp Panim --frame 119 --out "$M/poster.png"
# Lottie: shapes only; the glow is the one thing it cannot carry (expected warning)
$EC exec file.exportLottie --params '{"comp":"Panim","path":"'"$M"'/mark-reveal.json","textAsShapes":true}' \
  --project "$M/panim-reveal.ecproj" --json | tee "$W/lottie-export.log"
echo

# 5. checks
say "5. checks"
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size \
  -of default=nw=1 "$M/mark-reveal.webm" | tee "$W/webm-probe.txt"
grep -q "width=1080" "$W/webm-probe.txt" && grep -q "height=1080" "$W/webm-probe.txt" || fail "webm not 1080x1080"
grep -q "duration=4.0" "$W/webm-probe.txt" || fail "webm not 4.0 s"
sips -g pixelWidth -g pixelHeight "$M/poster.png" | tail -2
file "$M/mark-reveal-512.gif"
file "$M/mark-reveal-512.gif" | grep -q "512 x 512" || fail "gif not 512x512"
if grep -q NETSCAPE2.0 "$M/mark-reveal-512.gif"; then fail "gif loops (expected play-once)"; else echo "gif: plays once (no NETSCAPE loop block), ends on the still mark"; fi
grep -q '"warnings":\["panim ▸ breath glow: effect not supported by Lottie (skipped)"\]' "$W/lottie-export.log" \
  || fail "unexpected Lottie warnings (only the glow should be skipped)"
grep -q '"assets":\[\]' "$M/mark-reveal.json" && echo "lottie: 0 assets (no stray SVG footage)" || fail "lottie carries assets"
for f in mark-reveal.webm mark-reveal-512.gif mark-reveal.json poster.png panim-reveal.ecproj stones.svg; do
  printf '%-22s %8d bytes\n' "$f" "$(stat -f %z "$M/$f")"
done

# 6. optional: play the Lottie in a real web player (lottie-web 5.13, SVG renderer) if the harness is here
if [ -x "$W/lottie-check/shoot.sh" ] && [ -f "$W/lottie-check/lottie.min.js" ]; then
  say "6. lottie-web check (headless Chrome)"
  "$W/lottie-check/shoot.sh" "$M/mark-reveal.json" final svg 15 30 45 60 81 119 && ls "$W/lottie-check"/final_svg_*.png | wc -l | xargs echo "frames shot:"
fi

if [ "${1:-}" = "--frames" ]; then
  say "review frames → work/frames/"
  mkdir -p "$W/frames"
  for fr in 6 12 18 24 30 36 42 45 48 54 60 66 72 81 90 105 119; do
    $EC render-frame --project "$M/panim-reveal.ecproj" --comp Panim --frame $fr --max-side 360 \
      --out "$W/frames/f$(printf %03d $fr).png" > /dev/null
  done
fi
say "done"
