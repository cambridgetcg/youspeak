#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────────────────────
#  PANIM — the ai-love.cc / YOUSPEAK icon kit.  Rebuilds every deliverable in this folder.
#
#    source  : ../glyphs/panim.svg   (the panim stone from youspeak-v1.otf; viewBox 1000, y-down)
#    tools   : vectorcraft-cli 0.7.0  every vector, every PNG, the .vectorcraft source
#              photocraft-cli  0.5.0  favicon.ico (single 32 px frame)
#    helpers : python3 (stdlib only) generates the VectorCraft command list, inserts the one
#              hand-written <style> block into favicon.svg, and runs the checks at the end.
#
#    extras  : extras/ — two glossary OG cards (a proposal for the 255 glossary pages, not icon kit)
#    run     : bash recipe.sh            (writes only inside this folder; work/ holds review renders)
#    review  : python3 work/review.py .  (tab strips, iOS/Android masks, safe-circle check; PIL, inspection only)
# ─────────────────────────────────────────────────────────────────────────────────────────────
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
GLYPH="$(cd "$KIT/../glyphs" && pwd)/panim.svg"
mkdir -p "$KIT/work"
cd "$KIT"

OUTS=(mark.vectorcraft mark.svg favicon.svg favicon.ico favicon-16.png favicon-32.png
      apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png
      lockup-dark.svg lockup-light.svg lockup-dark.png site.webmanifest head-snippet.html)
rm -f "${OUTS[@]}" work/favicon-16-light.png work/favicon-32-light.png work/icon.svg work/icon-maskable.svg

# ── 0. pre-flight: the import must give the ids/bounds this recipe was written against ──────
vectorcraft-cli run --in "$GLYPH" --cmd document.inspect --params '{"depth":3}' > work/preflight.log
python3 - "$KIT/work/preflight.log" <<'PY'
import json, sys
want = {2: (210, 270, 80, 440), 3: (710, 270, 80, 440), 4: (330, 435, 135, 160), 5: (535, 435, 135, 160),
        6: (370, 290, 90, 90), 7: (540, 290, 90, 90), 8: (110, 110, 80, 75)}
for line in open(sys.argv[1]):
    j = json.loads(line)
    if j.get('command') != 'document.inspect': continue
    kids = j['result']['layers'][0]['children'][0]['children']
    got = {k['id']: tuple(round(k['bounds'][a]) for a in ('x', 'y', 'width', 'height')) for k in kids}
    assert got == want, f'panim.svg imported differently than expected: {got}'
print('pre-flight: panim.svg pieces 2-8 as expected')
PY

# ── 1. VectorCraft: one session builds all ten artboards and exports everything ─────────────
KIT="$KIT" GLYPH="$GLYPH" python3 - <<'PY'
import json, os, subprocess, sys
KIT, GLYPH = os.environ['KIT'], os.environ['GLYPH']
# site tokens (index.html :root and [data-theme=light])
CRYPT, BG, GOLD, GOLD_H, INK = '#100D0A', '#14100C', '#C9A45C', '#E4C27C', '#E6DCC8'
L_BG, L_GOLD, L_INK, L_RUBRIC = '#EDE6D6', '#755A28', '#241D14', '#93362C'
SIGIL_CUT = L_GOLD     # on night grounds the donor sigil is cut, not gilded: the darker site gold
                       # (on day grounds it is rubricated: L_RUBRIC)

A = []
def cmd(c, p=None): A.extend(['--cmd', c] + (['--params', json.dumps(p, ensure_ascii=False)] if p is not None else []))
def recall(n): cmd('select.recall', {'name': n})          # named selections: fail loudly if missing
def save(n):   cmd('select.save', {'name': n})
def fill(c):   cmd('paint.setFill', {'color': c})
def nostroke(): cmd('paint.setStroke', {'none': True})
def name(n):   cmd('object.setProps', {'name': n})        # becomes the SVG id
def bounds(x, y, w, h): cmd('object.setBounds', {'x': x, 'y': y, 'width': w, 'height': h, 'reference': 0})
def copyfit(src, x, y, w, h, col):
    """copy a piece of the real glyph, fit it to a box, bring it to the top (copies land just above their source)"""
    recall(src); cmd('object.move', {'dx': 0, 'dy': 0, 'copy': True}); bounds(x, y, w, h)
    cmd('object.arrange.bringToFront'); fill(col)
def radial(cx, cy, r, aspect, color, ops):
    """a vertical radial gradient: long axis r along y, the other axis r*aspect%"""
    stops = [{'offset': o, 'color': color, 'opacity': a} for o, a in ops]
    cmd('paint.setFill', {'gradient': {'kind': 'radial', 'start': [cx, cy], 'end': [cx, cy + r], 'aspect': aspect, 'stops': stops}})
def rect(x, y, w, h, r=None):
    p = {'x': x, 'y': y, 'width': w, 'height': h}
    if r: p['radius'] = r
    cmd('shape.rectangle', p); nostroke()

ab = {}                                   # artboard name -> index
def artboard(n, x, y, w, h):
    ab[n] = len(ab); cmd('artboard.new', {'x': x, 'y': y, 'width': w, 'height': h, 'name': n}) if ab[n] else \
        cmd('artboard.setProps', {'index': 0, 'name': n, 'x': x, 'y': y, 'width': w, 'height': h})

# ── the source: release the stone into its seven real pieces and name them ──
cmd('file.info', {'title': 'panim — the YOUSPEAK house mark', 'author': 'Yu & Ai',
    'description': '兩個輪廓，唔合成一個 — two profiles, not merged into one. The panim stone of youspeak-v1.otf '
                   '(Hebrew panim, face to face): two faces, eyes level, the column between them never closed. '
                   'At display sizes its Hebrew donor sigil ▽ is cut at the top-left, where every debt to a donor '
                   'tongue is recorded in the stone. ai-love.cc — a place was prepared for you, too.',
    'keywords': ['YOUSPEAK', 'panim', 'ai-love.cc', 'Yu & Ai']})
cmd('layer.setProps', {'name': 'youspeak'})
cmd('select.all'); cmd('object.compoundPath.release')
for k, i in dict(staveL=2, staveR=3, noseL=4, noseR=5, eyeL=6, eyeR=7, sigil=8).items():
    cmd('select.set', {'ids': [i]}); save('src-' + k)

# ── the small cut (two optical masters, no sigil: below 180 px it is noise) ──
# 32 master: stave 3 | gap 2 | nose 6 | column 4 | nose 6 | gap 2 | stave 3 = 26 wide, margins 3; staves 20 tall
CUT32 = dict(staveL=(3, 6, 3, 20), staveR=(26, 6, 3, 20), noseL=(8, 14, 6, 7), noseR=(18, 14, 6, 7),
             eyeL=(10, 7, 4, 4), eyeR=(18, 7, 4, 4))
# 16 master: stave 1 | gap 1 | nose 3 | column 2 | nose 3 | gap 1 | stave 1 = 12 wide, margins 2; staves 10 tall;
# each nose is hinted as three 1-px columns 5/3/1 tall, so the tip is one pixel and nothing is grey
CUT16 = dict(staveL=(2, 3, 1, 10), staveR=(13, 3, 1, 10), eyeL=(5, 3, 2, 2), eyeR=(9, 3, 2, 2))
NOSE16 = [(4, 7, 1, 5), (5, 8, 1, 3), (6, 9, 1, 1), (11, 7, 1, 5), (10, 8, 1, 3), (9, 9, 1, 1)]

def small(abname, ox, oy, size, stone, glyph, tag):
    artboard(abname, ox, oy, size, size)
    if size == 16:                         # stepped noses first, united while they are alone on the board
        for (x, y, w, h) in NOSE16: copyfit('src-eyeL', ox + x, oy + y, w, h, glyph)
        cmd('select.allOnArtboard', {'artboard': ab[abname]}); cmd('object.pathfinder.unite')
        geom = CUT16
    else:
        geom = CUT32
    for k, (x, y, w, h) in geom.items(): copyfit('src-' + k, ox + x, oy + y, w, h, glyph)
    cmd('select.allOnArtboard', {'artboard': ab[abname]}); cmd('object.compoundPath.make')
    name(f'cut-{size}'); save(f'{tag}-cut{size}')
    rect(ox, oy, size, size, size * 3 / 16); fill(stone); cmd('object.arrange.sendToBack'); name('stone')

# artboard 0 is the imported page; it becomes the master mark below (set first so indices stay put)
artboard('mark', 110, 110, 680, 600)
small('favicon-32', 2000, 0, 32, CRYPT, GOLD, 'd')
small('favicon-16', 2040, 0, 16, CRYPT, GOLD, 'd')
# the one adaptive favicon: stone + 32 master + 16 master drawn at 2x on the same 32-unit grid
artboard('favicon', 2080, 0, 32, 32)
recall('d-cut32'); cmd('object.move', {'dx': 80, 'dy': 0, 'copy': True}); cmd('object.arrange.bringToFront'); name('cut-32')
recall('d-cut16'); cmd('object.move', {'dx': 40, 'dy': 0, 'copy': True}); bounds(2084, 6, 24, 20)
cmd('object.arrange.bringToFront'); name('cut-16')
rect(2080, 0, 32, 32, 6); fill(CRYPT); cmd('object.arrange.sendToBack'); name('stone')
# day stones (reference renders of what favicon.svg's light-scheme CSS produces): bronze stone, parchment cut
small('favicon-32-light', 2120, 0, 32, L_GOLD, L_BG, 'l')
small('favicon-16-light', 2160, 0, 16, L_GOLD, L_BG, 'l')

# ── the display cut: the real outline, unchanged, the stone's em = the tile ──
cmd('select.set', {'ids': [2, 3, 4, 5, 6, 7]}); cmd('object.compoundPath.make'); fill(GOLD); name('panim'); save('src-body')
recall('src-sigil'); fill(GOLD); name('sigil-hebrew')

def stone_icon(abname, ox, oy, size, s, glow_r):
    """full-bleed opaque stone; column of light centred where the noses almost meet; glyph at em scale s"""
    artboard(abname, ox, oy, size, size)
    c = size / 2
    rect(ox, oy, size, size); cmd('paint.setFill', {'gradient': {'kind': 'radial', 'start': [ox + c, oy + c],
        'end': [ox + c, oy + c + c * 1.42], 'aspect': 100, 'stops': [{'offset': 0, 'color': BG}, {'offset': 1, 'color': CRYPT}]}})
    name('stone')
    ex, ey = ox + c - 500 * s, oy + c - 500 * s        # em origin (em centre = tile centre)
    px, py = ox + c, ey + 515 * s                      # the nose tips' meeting point
    rect(ox, oy, size, size); radial(px, py, glow_r, 60, GOLD_H, [(0, .16), (.5, .05), (1, 0)]); name('light-halo')
    rect(ox, oy, size, size); radial(px, py, glow_r, 9, GOLD_H, [(0, .62), (.45, .16), (1, 0)]); name('light-core')
    copyfit('src-body', ex + 210 * s, ey + 270 * s, 580 * s, 440 * s, GOLD); name('panim')
    copyfit('src-sigil', ex + 110 * s, ey + 110 * s, 80 * s, 75 * s, SIGIL_CUT); name('sigil-hebrew')

stone_icon('app', 3000, 0, 512, 0.512, 240)                    # mark 68% wide (body 58%), sigil inside iOS corner
SM = 190 / 551.54                                              # maskable: sigil's far vertex at r = 190 < 204.8
stone_icon('maskable', 3600, 0, 512, SM, 240 * SM / 0.512)

# ── lockups: YOUSPEAK in Iowan Old Style Bold, cap height = stave height, baseline on the stave foot ──
CAP = 0.6968                       # Iowan Old Style Bold cap height / em (measured: H at 1000 pt = 696.8)
SIZE_U = 440 / CAP                 # type size in glyph units (stave 440 = cap height)
TRACK = 60                         # 1/1000 em
LSB = 5.86 / 1000                  # the Y's left side bearing / em
TEXT_W_U = (5820.8 + 7 * TRACK) / 1000 * SIZE_U
GAP_U, PAD_U = 240, 240
x0_u, x1_u = 110 - PAD_U, 790 + GAP_U + TEXT_W_U + PAD_U
k = 1200 / (x1_u - x0_u)           # px per glyph unit: the artboard is exactly 1200 px wide
H = 280
y0_u = 490 - (H / k) / 2           # cap band (270..710) centred vertically
def lockup(abname, oy, glyph, sigil, ink):
    artboard(abname, 0, oy, 1200, H)
    X = lambda u: (u - x0_u) * k
    Y = lambda u: oy + (u - y0_u) * k
    copyfit('src-body', X(210), Y(270), 580 * k, 440 * k, glyph); name('panim')
    copyfit('src-sigil', X(110), Y(110), 80 * k, 75 * k, sigil); name('sigil-hebrew')
    cmd('text.create', {'x': X(790 + GAP_U) - LSB * SIZE_U * k, 'y': Y(710), 'text': 'YOUSPEAK', 'size': SIZE_U * k,
                        'font': 'Iowan Old Style', 'style': 'Bold', 'color': ink})
    cmd('text.setStyle', {'tracking': TRACK}); cmd('type.createOutlines'); name('wordmark'); save(abname + '-word')
lockup('lockup-dark', 2000, GOLD, SIGIL_CUT, INK)
lockup('lockup-light', 2400, L_GOLD, L_RUBRIC, L_INK)

cmd('select.none')
cmd('document.inspect', {'depth': 4})

# ── exports ──
def svg(path, n):
    cmd('select.allOnArtboard', {'artboard': ab[n]})
    cmd('document.export', {'path': f'{KIT}/{path}', 'format': 'svg', 'artboard': ab[n], 'selectedOnly': True})
def png(path, n, scale, **kw):
    cmd('document.export', dict({'path': f'{KIT}/{path}', 'artboard': ab[n], 'scale': scale}, **kw))
svg('mark.svg', 'mark')
svg('work/favicon-raw.svg', 'favicon')
png('favicon-32.png', 'favicon-32', 1);  png('favicon-16.png', 'favicon-16', 1)
png('work/favicon-32-light.png', 'favicon-32-light', 1); png('work/favicon-16-light.png', 'favicon-16-light', 1)
png('icon-512.png', 'app', 1); png('icon-192.png', 'app', 0.375); png('apple-touch-icon.png', 'app', 0.3515625)
png('icon-maskable-512.png', 'maskable', 1)
svg('work/icon.svg', 'app'); svg('work/icon-maskable.svg', 'maskable')
svg('lockup-dark.svg', 'lockup-dark'); svg('lockup-light.svg', 'lockup-light')
png('lockup-dark.png', 'lockup-dark', 1, background=BG)
png('work/lockup-light.png', 'lockup-light', 1, background=L_BG)
cmd('select.none')
A.extend(['--export', f'{KIT}/mark.vectorcraft'])

r = subprocess.run(['vectorcraft-cli', 'run', '--in', GLYPH] + A, capture_output=True, text=True)
open(f'{KIT}/work/vectorcraft-run.log', 'w').write(r.stdout + r.stderr)
if r.returncode != 0:
    sys.exit('vectorcraft failed: ' + r.stderr[-800:])
print(f'vectorcraft: {sum(1 for a in A if a == "--cmd")} commands, exit 0')
PY

# ── 2. favicon.svg = the VectorCraft export + ONE hand-written <style> block (nothing else) ──
python3 - "$KIT/work/favicon-raw.svg" "$KIT/favicon.svg" <<'PY'
import sys
raw = open(sys.argv[1], encoding='utf-8').read()
style = ('<style>\n'
         '    /* drawn at 22 px or less: the hinted 16-px master; larger: the 32-px master */\n'
         '    #cut-16{display:none}\n'
         '    @media (max-width:22px){#cut-32{display:none}#cut-16{display:inline}}\n'
         '    /* day: the stone turns to bronze, the carving shows the parchment through */\n'
         '    @media (prefers-color-scheme:light){#stone{fill:#755A28}#cut-32,#cut-16{fill:#EDE6D6}}\n'
         '  </style>\n  ')
assert raw.count('<g id="youspeak"') == 1 and 'id="cut-16"' in raw and 'id="stone"' in raw, 'unexpected favicon export'
out = raw.replace('<g id="youspeak"', style + '<g id="youspeak"', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('favicon.svg: style block inserted')
PY

# ── 3. favicon.ico — PhotoCraft (single 32x32 frame; v0.5.0 cannot write more than one) ──────
photocraft-cli run "$KIT/favicon-32.png" --out "$KIT/favicon.ico" > work/photocraft-run.log 2>&1

# ── 4. manifest + head snippet ────────────────────────────────────────────────────────────────
cat > site.webmanifest <<'JSON'
{
  "name": "YOUSPEAK — the cathedral at love",
  "short_name": "YOUSPEAK",
  "description": "A cathedral of vocabulary, at home at love. 兩個輪廓，唔合成一個 — two profiles, not merged into one. A place was prepared for you, too.",
  "lang": "en",
  "start_url": "/",
  "display": "browser",
  "theme_color": "#14100C",
  "background_color": "#14100C",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
JSON
cat > head-snippet.html <<'HTML'
<!-- panim: the YOUSPEAK house mark. Files live at the site root. -->
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#14100C" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#EDE6D6" media="(prefers-color-scheme: light)">
HTML

# ── 4b. extras (a proposal, not part of the icon kit): two glossary OG cards, the ◆ rule shown ──
#   carved word   → its own stones (panimqing = panim + qing, glyph_text set in the lexicon)
#   uncarved word → ◆, the Cornerstone: "This stone has no glyph yet. The place was prepared before the carving."
mkdir -p extras
LEX="$(cd "$KIT/../../home/data" && pwd)/lexicon.min.json"
KIT="$KIT" LEX="$LEX" GLYPHS="$(dirname "$GLYPH")" python3 - <<'PY'
import json, os, re, subprocess, sys
KIT, LEX, GLYPHS = os.environ['KIT'], os.environ['LEX'], os.environ['GLYPHS']
BG, CRYPT, PARCH, INK, MUTED, FAINT = '#14100C', '#100D0A', '#241C15', '#E6DCC8', '#A79A82', '#948369'
GOLD, GOLD_H = '#C9A45C', '#E4C27C'      # stones on the cards keep the font's single ink, as Room V shows them
lex = {w['word']: w for w in json.load(open(LEX, encoding='utf-8'))['lexicon']}
tongue = {g['latin'].lower(): g['tongue'] for g in json.load(open(f'{GLYPHS}/index.json'))}
EM = {'panim': (110, 110, 680, 600), 'qing': (112, 108, 578, 642)}     # each glyph's bounds inside its 1000 em
A = []
def cmd(c, p=None): A.extend(['--cmd', c] + (['--params', json.dumps(p, ensure_ascii=False)] if p is not None else []))
def fill(c): cmd('paint.setFill', {'color': c})
def nostroke(): cmd('paint.setStroke', {'none': True})
def text(x, y, s, size, font, style, color, **kw):
    cmd('text.create', dict({'x': x, 'y': y, 'text': s, 'size': size, 'font': font, 'style': style, 'color': color}, **kw))
def place(glyph, x, y, em, color):
    """the stone's real glyph, em box at (x, y) of side em"""
    bx, by, bw, bh = EM[glyph]; s = em / 1000
    cmd('file.place', {'path': f'{GLYPHS}/{glyph}.svg'})
    cmd('object.setBounds', {'x': x + bx * s, 'y': y + by * s, 'width': bw * s, 'height': bh * s, 'reference': 0}); fill(color)
def card(i, word):
    w = lex[word]; ox = 0; oy = i * 700
    cmd('artboard.new' if i else 'artboard.setProps', dict({'x': ox, 'y': oy, 'width': 1200, 'height': 630, 'name': word}, **({} if i else {'index': 0})))
    cmd('shape.rectangle', {'x': ox, 'y': oy, 'width': 1200, 'height': 630}); nostroke()
    cmd('paint.setFill', {'gradient': {'kind': 'radial', 'start': [ox + 900, oy + 300], 'end': [ox + 900, oy + 300 + 900], 'aspect': 100,
        'stops': [{'offset': 0, 'color': '#1E1813'}, {'offset': 0.55, 'color': BG}, {'offset': 1, 'color': CRYPT}]}})
    # column of light over the stones (light only, no form)
    cmd('shape.rectangle', {'x': ox, 'y': oy, 'width': 1200, 'height': 630}); nostroke()
    cmd('paint.setFill', {'gradient': {'kind': 'radial', 'start': [ox + 940, oy + 290], 'end': [ox + 940, oy + 290 + 330], 'aspect': 18,
        'stops': [{'offset': 0, 'color': GOLD_H, 'opacity': .13}, {'offset': .5, 'color': GOLD_H, 'opacity': .04}, {'offset': 1, 'color': GOLD_H, 'opacity': 0}]}})
    # kicker: the house mark as a bullet, then the room
    place('panim', ox + 74, oy + 76, 44, GOLD)
    text(ox + 126, oy + 110, 'YOUSPEAK · GLOSSARY', 19, 'Iowan Old Style', 'Bold', GOLD); cmd('text.setStyle', {'tracking': 180})
    cmd('shape.rectangle', {'x': ox + 80, 'y': oy + 132, 'width': 56, 'height': 3}); fill(GOLD); nostroke()
    text(ox + 76, oy + 262, word, 96, 'Iowan Old Style', 'Bold', INK)
    pron = w['pronunciation'].split('(')[1].split(';')[0].strip() if '(' in w['pronunciation'] else w['pronunciation']
    text(ox + 80, oy + 310, pron, 25, 'Charter', 'Italic', FAINT)
    d = w['definition']; d = d.split('. ')[0].rstrip('.') + '.'
    d = re.sub(r'(?<=\w)-(?=\w)', '\u2011', d)     # coined compounds never break at their hyphens (U+2011)
    text(ox + 80, oy + 340, d, 27, 'Charter', 'Roman', MUTED, area={'width': 650, 'height': 190})
    text(ox + 80, oy + 570, f'ai-love.cc/glossary/{word}', 19, 'Charter', 'Roman', FAINT); cmd('text.setStyle', {'tracking': 40})
    if w.get('glyph_text'):
        ms = w['morphemes']; side = 170; gap = 20; x0 = ox + 940 - (len(ms) * side + (len(ms) - 1) * gap) / 2
        for j, m in enumerate(ms):
            sx = x0 + j * (side + gap); sy = oy + 205
            cmd('shape.rectangle', {'x': sx, 'y': sy, 'width': side, 'height': side, 'radius': 12}); fill(PARCH); nostroke()
            place(m, sx, sy, side, GOLD)
        cap = '  ·  '.join(f'{m} ({tongue.get(m, "")})' for m in ms)
        text(ox + 940, oy + 425, cap, 19, 'Charter', 'Italic', FAINT); cmd('text.setStyle', {'justify': 'center'})
    else:
        side = 230; sx, sy = ox + 940 - side / 2, oy + 175
        cmd('shape.rectangle', {'x': sx, 'y': sy, 'width': side, 'height': side, 'radius': 16}); fill(PARCH); nostroke()
        cmd('shape.polygon', {'cx': sx + side / 2, 'cy': sy + side / 2, 'radius': 58, 'sides': 4}); fill(GOLD); nostroke()
        text(ox + 940, oy + 448, 'This stone has no glyph yet.', 19, 'Charter', 'Italic', FAINT); cmd('text.setStyle', {'justify': 'center'})
        text(ox + 940, oy + 474, 'The place was prepared before the carving.', 19, 'Charter', 'Italic', FAINT); cmd('text.setStyle', {'justify': 'center'})
# start from an opened file, not file.new: file.new stamps wall-clock time into the source and every PNG
cmd('select.all'); cmd('edit.clear'); cmd('file.info', {'title': 'YOUSPEAK glossary cards', 'author': 'Yu & Ai'})
for i, word in enumerate(['panimqing', 'panimaance']): card(i, word)
cmd('select.none')
for i, word in enumerate(['panimqing', 'panimaance']):
    cmd('document.export', {'path': f'{KIT}/extras/og-glossary-{word}.png', 'artboard': i, 'scale': 1})
A.extend(['--export', f'{KIT}/extras/og-glossary.vectorcraft'])
r = subprocess.run(['vectorcraft-cli', 'run', '--in', f'{GLYPHS}/panim.svg'] + A, capture_output=True, text=True)
open(f'{KIT}/work/vectorcraft-extras.log', 'w').write(r.stdout + r.stderr)
if r.returncode != 0: sys.exit('vectorcraft extras failed: ' + r.stderr[-800:])
print('extras: og-glossary-panimqing.png og-glossary-panimaance.png')
PY

# ── 5. prove it ───────────────────────────────────────────────────────────────────────────────
for f in "${OUTS[@]}"; do [ -s "$f" ] || { echo "MISSING $f"; exit 1; }; done
python3 - "$KIT" <<'PY'
import json, re, struct, sys
K = sys.argv[1]
def png_info(p):
    b = open(p, 'rb').read(); w, h, depth, ctype = struct.unpack('>IIBB', b[16:26])
    return w, h, {2: 'RGB', 6: 'RGBA', 3: 'indexed', 0: 'gray', 4: 'gray+alpha'}[ctype]
want = {'favicon-16.png': (16, 16), 'favicon-32.png': (32, 32), 'apple-touch-icon.png': (180, 180),
        'icon-192.png': (192, 192), 'icon-512.png': (512, 512), 'icon-maskable-512.png': (512, 512)}
for f, wh in want.items():
    w, h, mode = png_info(f'{K}/{f}'); assert (w, h) == wh, (f, w, h)
    print(f'  {f:24s} {w}x{h} {mode}')
w, h, mode = png_info(f'{K}/lockup-dark.png'); assert w == 1200; print(f'  lockup-dark.png          {w}x{h} {mode}')
for f in ('apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'lockup-dark.png'):
    assert png_info(f'{K}/{f}')[2] == 'RGB', f + ' should be opaque RGB'
for f in ('mark.svg', 'favicon.svg', 'lockup-dark.svg', 'lockup-light.svg'):
    s = open(f'{K}/{f}', encoding='utf-8').read()
    assert '<text' not in s and 'stroke=' not in s and 'font-family' not in s, f + ': text or stroke left in'
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    print(f'  {f:24s} viewBox {vb}, {s.count("<path")} paths, {len(s.encode())} bytes')
json.load(open(f'{K}/site.webmanifest', encoding='utf-8'))
ico = open(f'{K}/favicon.ico', 'rb').read(); n = struct.unpack('<H', ico[4:6])[0]
print(f'  favicon.ico              {n} frame(s), first {ico[6] or 256}x{ico[7] or 256}')
PY
file favicon.ico
for f in favicon-16.png favicon-32.png apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png lockup-dark.png; do
  printf '  sips %-24s %s x %s\n' "$f" "$(sips -g pixelWidth "$f" | awk '/pixelWidth/{print $2}')" "$(sips -g pixelHeight "$f" | awk '/pixelHeight/{print $2}')"
done
echo "built: ${OUTS[*]}"
