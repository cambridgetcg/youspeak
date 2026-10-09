"""extract_glyphs.py — lay the 93 stones out as SVG files for the brand recipes.

Reads home/data/morphemes.min.json (baked by home/bake.py — never edit it) and
writes brand/glyphs/<latin>.svg (viewBox 0 0 1000 1000, y-down, exactly the
font's svg_path) plus brand/glyphs/index.json with each stone's meaning,
iconography and rationale. The output is derived and git-ignored.
"""
import json
import re
from pathlib import Path

BRAND = Path(__file__).resolve().parent
SRC = BRAND.parent / "home/data/morphemes.min.json"
OUT = BRAND / "glyphs"
OUT.mkdir(exist_ok=True)

index = []
for m in json.loads(SRC.read_text())["morphemes"]:
    slug = re.sub(r"[^a-z0-9]+", "_", m["latin"].lower()).strip("_") or "cp_" + m["codepoint"][2:]
    (OUT / f"{slug}.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">'
        f'<path fill="#000" fill-rule="nonzero" d="{m["svg_path"]}"/></svg>')
    index.append({k: m.get(k, "") for k in ("latin", "tongue", "meaning", "mclass", "iconography", "rationale")}
                 | {"file": f"glyphs/{slug}.svg"})
(OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
print(f"brand/glyphs/  {len(index)} stones")
