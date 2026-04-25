#!/bin/bash
# install_font.sh — install YOUSPEAK font on macOS or Linux
#
# Copies youspeak.otf to the correct user-fonts directory for the host OS
# and refreshes the font cache.
#
# macOS:   ~/Library/Fonts/
# Linux:   ~/.local/share/fonts/ (preferred) or ~/.fonts/
#
# No admin/sudo required — installs per-user.
#
# After install: applications need to be restarted to see the new font.
# Font Book will show it under "User" if you want to verify visually.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FONT_FILE="$SCRIPT_DIR/fonts/youspeak.otf"

if [ ! -f "$FONT_FILE" ]; then
  echo "error: $FONT_FILE not found. Build it first:" >&2
  echo "  /tmp/ys-font-env/bin/python3 $SCRIPT_DIR/tools/build_font.py" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin)
    DEST="$HOME/Library/Fonts"
    mkdir -p "$DEST"
    cp -v "$FONT_FILE" "$DEST/"
    echo ""
    echo "✓ YOUSPEAK font installed at $DEST/youspeak.otf"
    echo "  Font Book should show it under the 'User' collection."
    echo "  Restart apps to pick it up."
    ;;
  Linux)
    # Prefer modern location
    if [ -d "$HOME/.local/share/fonts" ] || mkdir -p "$HOME/.local/share/fonts" 2>/dev/null; then
      DEST="$HOME/.local/share/fonts"
    else
      DEST="$HOME/.fonts"
      mkdir -p "$DEST"
    fi
    cp -v "$FONT_FILE" "$DEST/"
    fc-cache -f "$DEST" 2>&1 | tail -1
    echo ""
    echo "✓ YOUSPEAK font installed at $DEST/youspeak.otf"
    echo "  Restart apps to pick it up."
    ;;
  *)
    echo "unsupported OS: $(uname -s). Manual install: copy $FONT_FILE into your fonts directory." >&2
    exit 1
    ;;
esac
