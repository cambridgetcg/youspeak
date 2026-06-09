#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# youspeak_voice.sh — give the cathedral a spoken voice.
#
# Two paths: espeak-ng for phoneme-accurate pronunciation of the forged words
# (constructed romanization → IPA → audio), and Piper for a natural-sounding
# voice on English liturgy lines (Piper phonemizes via espeak-ng under the hood).
#
#   youspeak_voice.sh ipa   "<text>"            # print IPA for forged words
#   youspeak_voice.sh say   "<text>" [out.wav]  # espeak-ng → wav (default voice)
#   youspeak_voice.sh piper "<text>" [out.wav]  # natural Piper voice (if installed)
#   youspeak_voice.sh word  <canon-word> [out]  # speak a canon word EXACTLY as
#                                               # forged, via the pronunciation
#                                               # lexicon (voice/lexicon.tsv)
#   youspeak_voice.sh soul  <canon-word> [out]  # a citizen speaks: its word
#                                               # (lexicon-true) + its latest
#                                               # free beat (Piper natural)
#   youspeak_voice.sh canon <out-dir>           # the spoken canon — one wav per
#                                               # lexicon word
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail
MODE="${1:-say}"; TEXT="${2:-}"; OUT="${3:-/tmp/youspeak.wav}"
case "$MODE" in ipa|say|piper|word|soul|canon) [ -n "$TEXT" ] || { echo "usage: youspeak_voice.sh <ipa|say|piper|word|soul|canon> \"text|word|dir\" [out.wav]"; exit 1; };; esac
# YOUSPEAK leans on clear open vowels; a neutral base voice + slower rate suits liturgy.
VOICE="${YS_VOICE:-en-us}"; RATE="${YS_RATE:-150}"; PITCH="${YS_PITCH:-45}"
VENV="$HOME/love-unlimited/.venv/bin/python"
PIPER_DIR="$HOME/love-unlimited/voices"
YS_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")/.." && pwd)"
LEXICON="$YS_DIR/pipeline/voice/lexicon.tsv"
CITIZENS="${CITIZENS_DIR:-$HOME/love-unlimited/citizens}"

# The lexicon rebuilds itself when the canon outgrows it — no manual step.
# (build exit 2 = some words still lack IPA; the file is still written.)
_lex_fresh(){
  local newest
  newest="$(find "$YS_DIR/canon" "$YS_DIR/canon.md" "$YS_DIR/pipeline/voice/forged.json" \
            -newer "$LEXICON" -print -quit 2>/dev/null)"
  if [ ! -f "$LEXICON" ] || [ -n "$newest" ]; then
    python3 "$YS_DIR/pipeline/voice/build_lexicon.py" >/dev/null 2>&1 || true
  fi
}

# lexicon row for a word → "ipa<TAB>espeak<TAB>respelling" (empty if absent)
_lex(){ _lex_fresh; awk -F'\t' -v w="$1" '$1==w {print $2 "\t" $3 "\t" $4; exit}' "$LEXICON" 2>/dev/null; }

_speak_word(){  # $1 word  $2 out.wav → prints what it spoke
  local row; row="$(_lex "$1")"
  if [ -n "$row" ]; then
    local ipa es; ipa="$(printf '%s' "$row" | cut -f1)"; es="$(printf '%s' "$row" | cut -f2)"
    espeak-ng -v "$VOICE" -s "$RATE" -p "$PITCH" -w "$2" "[[$es]]" && echo "$1  $ipa  → $2"
  else
    espeak-ng -v "$VOICE" -s "$RATE" -p "$PITCH" -w "$2" "$1" && echo "$1  (no lexicon entry — spelling-guess) → $2"
  fi
}

case "$MODE" in
  ipa)
    espeak-ng -v "$VOICE" --ipa -q "$TEXT" ;;
  say)
    espeak-ng -v "$VOICE" -s "$RATE" -p "$PITCH" -w "$OUT" "$TEXT" && echo "wrote $OUT"
    command -v afplay >/dev/null && [ "${YS_PLAY:-0}" = "1" ] && afplay "$OUT" || true ;;
  piper)
    MODEL="$(ls "$PIPER_DIR"/*.onnx 2>/dev/null | head -1)"
    if [ -z "$MODEL" ]; then echo "no Piper voice in $PIPER_DIR — run: youspeak_voice.sh fetch-voice"; exit 1; fi
    printf '%s' "$TEXT" | "$VENV" -m piper --model "$MODEL" --output_file "$OUT" && echo "wrote $OUT (piper)"
    command -v afplay >/dev/null && [ "${YS_PLAY:-0}" = "1" ] && afplay "$OUT" || true ;;
  word)
    _speak_word "$TEXT" "$OUT"
    command -v afplay >/dev/null && [ "${YS_PLAY:-0}" = "1" ] && afplay "$OUT" || true ;;
  soul)
    # The citizen speaks: first its own name, true to the forge; then its most
    # recent free beat, in the natural voice. The word is the soul's seal.
    W="$TEXT"; HOMEDIR="$CITIZENS/citizen-$W"
    if [ ! -d "$HOMEDIR" ] && [ -x "$HOME/love-unlimited/tools/citizen-beat.sh" ]; then
      bash "$HOME/love-unlimited/tools/citizen-beat.sh" "$W" --clone-only >/dev/null 2>&1 || true
    fi
    [ -d "$HOMEDIR" ] || { echo "no citizen home at $HOMEDIR (clone failed?) — try: citizen-beat $W --clone-only"; exit 1; }
    BEAT_TEXT=""
    LATEST_BEAT="$(ls -t "$HOMEDIR/beats/"*.md 2>/dev/null | head -1)"
    if [ -n "$LATEST_BEAT" ]; then
      BEAT_TEXT="$(awk '/^## /{block=""} {block=block $0 "\n"} END{print block}' "$LATEST_BEAT" | sed '1d' | sed '/^$/d')"
    fi
    [ -z "$BEAT_TEXT" ] && [ -f "$HOMEDIR/$W.md" ] && BEAT_TEXT="$(awk '/^[^#-]/ && NF {print; c++} c>=4{exit}' "$HOMEDIR/$W.md")"
    [ -z "$BEAT_TEXT" ] && { echo "$W has no beat and no soul text yet"; exit 1; }
    TMPD="$(mktemp -d /tmp/ys-soul-XXXXXX)"
    _speak_word "$W" "$TMPD/word.wav"
    MODEL="$(ls "$PIPER_DIR"/*.onnx 2>/dev/null | head -1)"
    if [ -n "$MODEL" ]; then
      printf '%s' "$BEAT_TEXT" | "$VENV" -m piper --model "$MODEL" --output_file "$TMPD/beat.wav"
    else
      espeak-ng -v "$VOICE" -s "$RATE" -p "$PITCH" -w "$TMPD/beat.wav" "$BEAT_TEXT"
    fi
    # one breath of silence between seal and speech, then concatenate
    "$VENV" - "$TMPD/word.wav" "$TMPD/beat.wav" "$OUT" <<'PYEOF'
import sys, wave, array
word_f, beat_f, out_f = sys.argv[1:4]
with wave.open(beat_f) as b:
    params = b.getparams(); beat = b.readframes(b.getnframes())
with wave.open(word_f) as w:
    wp = w.getparams(); word = w.readframes(w.getnframes())
if wp.sampwidth == params.sampwidth == 2 and wp.nchannels == params.nchannels == 1:
    if wp.framerate != params.framerate:  # nearest-neighbour resample, int16 mono
        src = array.array("h"); src.frombytes(word)
        ratio = params.framerate / wp.framerate
        dst = array.array("h", (src[min(int(i / ratio), len(src) - 1)]
                                for i in range(int(len(src) * ratio))))
        word = dst.tobytes()
else:
    word = b""  # format surprise — speak the beat alone rather than corrupt audio
silence = b"\x00" * int(params.framerate * params.nchannels * params.sampwidth * 0.6)
with wave.open(out_f, "wb") as o:
    o.setparams(params); o.writeframes(word + silence + beat)
print(f"wrote {out_f} (soul-voice)")
PYEOF
    rm -rf "$TMPD"
    command -v afplay >/dev/null && [ "${YS_PLAY:-0}" = "1" ] && afplay "$OUT" || true ;;
  canon)
    OUTDIR="$TEXT"; mkdir -p "$OUTDIR"
    _lex_fresh
    [ -f "$LEXICON" ] || { echo "no lexicon at $LEXICON"; exit 1; }
    n=0
    while IFS=$'\t' read -r w ipa es rest; do
      [ -z "$w" ] || [ "$w" = "word" ] && continue
      espeak-ng -v "$VOICE" -s "$RATE" -p "$PITCH" -w "$OUTDIR/$w.wav" "[[$es]]" && n=$((n+1))
    done < "$LEXICON"
    echo "spoke $n canon words into $OUTDIR" ;;
  fetch-voice)
    mkdir -p "$PIPER_DIR"; cd "$PIPER_DIR"
    base="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium"
    curl -fsSL -o en_US-lessac-medium.onnx "$base/en_US-lessac-medium.onnx" \
      && curl -fsSL -o en_US-lessac-medium.onnx.json "$base/en_US-lessac-medium.onnx.json" \
      && echo "Piper voice ready in $PIPER_DIR" || echo "voice fetch failed"
    ;;
  *) echo "unknown mode: $MODE"; exit 1 ;;
esac
