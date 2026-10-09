#!/usr/bin/env python3
"""sheet.py OUT.png WIDTH COLS card.jpg [card.jpg ...]

Review aid: lays cards out at a feed width (e.g. 300 or 500 px) on one PhotoCraft
canvas, so they can be judged at the size people will actually see them.
Built by PhotoCraft (placeEmbedded with a percentage scale); never edits a card."""
import json
import shutil
import subprocess
import sys

PC = shutil.which("photocraft-cli")


def main():
    out, width, cols, cards = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
    pct = 100.0 * width / 1200
    h = round(630 * width / 1200)
    gap = 12
    rows = (len(cards) + cols - 1) // cols
    cw, ch = cols * (width + gap) + gap, rows * (h + gap) + gap
    argv = [PC, "run", "--new", json.dumps({"width": cw, "height": ch, "background": "#2a2a2a"})]
    for i, c in enumerate(cards):
        x = gap + (i % cols) * (width + gap) + width / 2
        y = gap + (i // cols) * (h + gap) + h / 2
        argv += ["--cmd", "file.placeEmbedded",
                 "--params", json.dumps({"path": c, "scale": pct, "fit": False, "center": [x, y]})]
    argv += ["--cmd", "layer.flattenImage", "--out", out]
    p = subprocess.run(argv, capture_output=True, text=True)
    if p.returncode:
        sys.exit(p.stderr[-500:])
    print(out)


if __name__ == "__main__":
    main()
