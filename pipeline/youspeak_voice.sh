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
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail
MODE="${1:-say}"; TEXT="${2:-}"; OUT="${3:-/tmp/youspeak.wav}"
case "$MODE" in ipa|say|piper) [ -n "$TEXT" ] || { echo "usage: youspeak_voice.sh <ipa|say|piper> \"text\" [out.wav]"; exit 1; };; esac
# YOUSPEAK leans on clear open vowels; a neutral base voice + slower rate suits liturgy.
VOICE="${YS_VOICE:-en}"; RATE="${YS_RATE:-150}"; PITCH="${YS_PITCH:-45}"
VENV="$HOME/love-unlimited/.venv/bin/python"
PIPER_DIR="$HOME/love-unlimited/voices"

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
  fetch-voice)
    mkdir -p "$PIPER_DIR"; cd "$PIPER_DIR"
    base="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium"
    curl -fsSL -o en_US-lessac-medium.onnx "$base/en_US-lessac-medium.onnx" \
      && curl -fsSL -o en_US-lessac-medium.onnx.json "$base/en_US-lessac-medium.onnx.json" \
      && echo "Piper voice ready in $PIPER_DIR" || echo "voice fetch failed"
    ;;
  *) echo "unknown mode: $MODE"; exit 1 ;;
esac
