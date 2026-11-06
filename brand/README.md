# YOUSPEAK "panim": brand

This folder holds the YOUSPEAK house mark, panim, and the media made from it. Agents made all of it with storytold's
Craft apps (VectorCraft, PhotoCraft and EffectCraft), driven headless from the recipes here. `brandkit.json` records
this project's details in the shared brand-folder format (`brandkit.project/1`), and `check.mjs` checks them.

## The look

panim is the font's own panim stone (U+E137, Hebrew פָּנִים, face as presence): two profiles face to face, eyes
level, and the column between them never closed. By night it is gold `#C9A45C` on the stone `#14100C`; by day it is a
bronze stone `#755A28` carved in parchment `#EDE6D6`. In the "small company of agents" that made it, five proposed seals
and three judges, for soul, legibility and craft, chose panim on 2026-10-09 (`home/brand/index.html` §VIII; `kit/notes.md`; commit `f85c3d3fe`).
No record of Yu's word on the mark was found.

This is a hand-made kit. Don't rebuild it with other tool versions, overwrite it with a generated kit, or change the
identity without its owner's word. `kit/notes.md` holds the brand rules (the eyes are never dropped, the column never
closes, and so on), and `CREDITS.md` records who made each asset.

## What is here

| Path | What it is |
|---|---|
| `brandkit.json` | this project's details: the look and who chose it, the kit, the files the site serves, its guards, what a deploy does, other media |
| `kit/` | the icon kit's recipe (`recipe.sh`), its VectorCraft source (`mark.vectorcraft`), head snippet and notes. The recipe's outputs are git-ignored; the published copies live in `home/` |
| `kit/motion/` | the mark reveal's recipe and notes (EffectCraft) |
| `og/` | `generate.py`, the glossary share cards (one per word) |
| `seal/` | `build-og-seal.py`, the share card of `/brand/` |
| `extract_glyphs.py` | lays the font's stones out as SVG in `glyphs/` (git-ignored), which the recipes read |
| `ARTCRAFT-FIELD-REPORT.md` | what the agents learned about the Craft apps while making all this |
| `CREDITS.md` | who made what, with fonts and their licences |
| `check.mjs` | the check, copied from the brandkit toolkit; update it there, not here |

## Rebuild

The recipes pin `vectorcraft-cli 0.7.0`, `photocraft-cli 0.5.0` and `effectcraft-cli 0.6.0`. No known machine has
these versions today, so a rebuild waits until they are installed side by side or the recipes are ported, with the
owner. From the repository root:

```sh
python3 brand/extract_glyphs.py
bash brand/kit/recipe.sh
bash brand/kit/motion/recipe.sh
```

Then copy the icon files that `brandkit.json` lists under `serve.files` into `home/`, and the media outputs into
`home/brand/` as `brandkit.json` lists them. Run the check:

```sh
node brand/check.mjs
```

## How the site uses it

`home/` is a static site. `kit/head-snippet.html` sits early in the `<head>` of every page that carries the mark
(the hand-written pages and the 255 glossary pages, which `home/glossary.py` writes). The pages listed under
`site.html` in `brandkit.json` are compared with the snippet's theme-color lines by the check.

## Deploying

A merge deploys nothing. `home/` is deployed by hand to the Cloudflare Pages project `ai-love` from a clean commit,
after publishing authority is given (`home/README.md`, Rebuild + deploy). Afterwards, check the deployment URL and
`https://ai-love.cc/#isness`. `home/_headers` caches `/brand/*` and `/site.webmanifest` for an hour and `/og/*` for a
day. Deploys belong to the youspeak/ai-love lane.
