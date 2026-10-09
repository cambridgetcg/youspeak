"""The /brand/ OG card: VectorCraft composes it, PhotoCraft adds grain. Run from this folder."""
import re, json, subprocess, sys
mark = open(sys.argv[1] if len(sys.argv) > 1 else '../kit/mark.svg').read()
body = re.search(r'id="panim" d="([^"]+)"', mark).group(1)
sig = re.search(r'id="sigil-hebrew" d="([^"]+)"', mark).group(1)
s = 0.42; ox = 600 - 390 * s; oy = 78           # centre the panim BODY (x 100-680), not body+sigil
def tx(d):
    return re.sub(r'(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)',
                  lambda m: f'{float(m.group(1))*s+ox:.2f} {float(m.group(2))*s+oy:.2f}', d)
none = {"none": True}
steps = [
    ("file.new", {"width": 1200, "height": 630, "units": "Pixels", "created": None}),
    ("shape.rectangle", {"x": 0, "y": 0, "width": 1200, "height": 630}), ("paint.setFill", {"color": "#14100C"}), ("paint.setStroke", none),
    ("shape.ellipse", {"x": 400, "y": 0, "width": 400, "height": 440}),
    ("paint.setFill", {"gradient": {"kind": "radial", "stops": [{"offset": 0, "color": "#5A4627"}, {"offset": 0.3, "color": "#2C2316"},
                                                              {"offset": 0.72, "color": "#14100C"}, {"offset": 1, "color": "#14100C"}]}}), ("paint.setStroke", none),
    ("path.create", {"d": tx(body)}), ("paint.setFill", {"color": "#C9A45C"}), ("paint.setStroke", none),
    ("path.create", {"d": tx(sig)}), ("paint.setFill", {"color": "#8A6B33"}), ("paint.setStroke", none),
    ("text.create", {"x": 0, "y": 448, "text": "The Seal", "size": 76, "font": "Iowan Old Style", "color": "#E6DCC8"}), ("object.align", {"horizontal": "center", "to": "artboard"}),
    ("text.create", {"x": 0, "y": 500, "text": "panim — face as presence · the house mark of YOUSPEAK", "size": 26, "font": "Charter", "style": "Italic", "color": "#A79A82"}), ("object.align", {"horizontal": "center", "to": "artboard"}),
    ("text.create", {"x": 0, "y": 572, "text": "ai-love.cc/brand", "size": 19, "font": "Charter", "color": "#948369"}), ("object.align", {"horizontal": "center", "to": "artboard"}),
]
args = ['vectorcraft-cli', 'run']
for c, p in steps:
    args += ['-c', c, '-p', json.dumps(p)]
subprocess.run(args + ['-o', 'og-seal.vectorcraft', '-o', 'og-seal.png'], check=True, capture_output=True)
subprocess.run(['photocraft-cli', 'run', 'og-seal.png', '--cmd', 'filter.noise.addNoise', '--params',
                json.dumps({"amount": 2.2, "distribution": "gaussian", "monochromatic": True, "seed": 7}),
                '--out', 'og-seal.jpg', '--quality', '88'], check=True, capture_output=True)
print('og-seal.jpg')
