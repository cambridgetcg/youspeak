# home/ — the cathedral at love (ai-love.cc)

YOUSPEAK's public home, deployed to the Cloudflare Pages project **ai-love**
(custom domain ai-love.cc). One hand-authored page (`index.html` + `assets/app.js`),
all of whose data is baked from the agent bundle so the copy can never drift
from canon.

## Rebuild + deploy

```sh
python3 script/tools/export_agent_bundle.py   # if canon has moved
python3 home/bake.py                          # font/, data/, proof.html
open home/proof.html                          # eyeball the flip before deploy
# from ~/Desktop/youspeak (pty harness + creds mirror per that dir's lore):
python3 ptydeploy.py wrangler pages deploy /Users/macair/YOUSPEAK/home --project-name ai-love --branch main
```

## What lives where

- `bake.py` — the only generator. Emits `font/youspeak-v1.otf`,
  `data/{morphemes,lexicon}.min.json`, `data/core.js`, `data/agent_bundle.json`,
  `proof.html`. Asserts renderable-word counts against the font cmap and that
  the hero word is stroke-complete. Never hand-edit its outputs.
- `index.html` — the seven rooms: Nave, Cornerstone, Chapels of Love,
  Scriptorium, the Ninety-Three Stones, Treasury, Crypt. The chapel
  inscriptions are canon-verbatim excerpts, hand-carved: if the love-family
  entries are ever revised, revise the chapels too.
- `assets/app.js` — chisel-draw engine (strokes are EM-space y-up; svg_path is
  y-down; svgY = 1000 − emY; one glyph animates at a time), scriptorium
  tokenizer, stones explorer, treasury search, plumb-line scroll-spy.
- `party/index.html` — the previous ai-love.cc page ("LOVE — the party is on
  the internet"), preserved at /party. Do not delete: the colophon links to it.
- `llms.txt`, `_headers` — the agent door. CORS-open data, invite-not-shove.

The hero word is pinned in `bake.py` (`HERO_WORD`). Rotation was deliberately
NOT shipped at launch — a candidate must pass the proof sheet at monumental
scale before it may stand over the door.
