# Credits

Who made each asset, with what, and under which licence. Where an agent made something, the line says so, and
anything published under Yu's accounts carries that through. If an asset's maker isn't known, write "not recorded"
rather than guessing.

Everything below was committed on 2026-10-09 in `f85c3d3fe`, as `YOU <alpha@ai-love.cc>` (the household Mac's git
identity). `home/brand/index.html` §VIII says: "Five proposed a seal … Three judges weighed them … and panim stood.
One mason cut the icons, another the two hundred and fifty-five travelling stones, a third set the seal moving."
`ARTCRAFT-FIELD-REPORT.md` names the ten agent runs (mark:panim, mark:star, mark:kunance, mark:arch, mark:free, kit,
og:tablet, og:nocturne, og-batch, motion). No session ids were recorded.

## Assets

| Asset | Made by | Date | Tools | Notes |
|---|---|---|---|---|
| The panim mark (`home/brand/mark.svg`), the icon kit (`home/favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `site.webmanifest`; `home/brand/favicon-16.png`, `favicon-32.png`), the lockups (`home/brand/lockup-*.svg`, `.png`) and `kit/mark.vectorcraft` | an agent, "the mason who cut the icons" (session not recorded), from the mark the agent judges chose | 2026-10-09 | vectorcraft-cli 0.7.0; photocraft-cli 0.5.0 for `favicon.ico`; Python 3 stdlib | `kit/recipe.sh`, `kit/notes.md`. One hand-written `<style>` block in `favicon.svg` |
| The mark reveal (`home/brand/mark-reveal.webm`, `.mp4`, `-512.gif`, `.json`, `-poster.png`) | an agent, "the third mason" (session not recorded) | 2026-10-09 | vectorcraft-cli 0.7.0, effectcraft-cli 0.6.0 | `kit/motion/recipe.sh`, `kit/motion/notes.md` |
| The glossary share cards (`home/og/glossary/*.jpg`, 255) | an agent, "the second mason" (session not recorded) | 2026-10-09 | vectorcraft-cli 0.7.0, photocraft-cli 0.5.0 | `og/generate.py` |
| The seal's share card (`home/brand/og.jpg`) | not recorded (agent work in `f85c3d3fe`) | 2026-10-09 | vectorcraft-cli and photocraft-cli, versions not pinned in the script | `seal/build-og-seal.py` |
| The panim glyph, the mark's source outline | the YOUSPEAK font `youspeak-v1.otf`, built in this repository; the glyph's maker is not recorded here | not recorded | `script/tools/build_font_v1.py` | read through `extract_glyphs.py` |
| `home/og.jpg` (two cups under the compass star), the site's share card | not recorded | 2026-08-23 (`ea0b137e4`) | not recorded | not part of this kit |

## Fonts

| Family | File | Licence | Source | SHA-256 |
|---|---|---|---|---|
| Iowan Old Style (Bold, outlined in the lockups; also the display face of the glossary cards and the seal card) | `Iowan Old Style.ttc` | Apple system font, under the macOS licence; the repository records none | ships with macOS (`/System/Library/Fonts/Supplemental/`) | not recorded (built on macOS 15.7) |
| Charter (the glossary cards' body and the seal card's lines) | `Charter.ttc` | Apple system font, under the macOS licence; the repository records none | ships with macOS (`/System/Library/Fonts/Supplemental/`) | not recorded |
| YOUSPEAK (`youspeak-v1.otf`), the source of every glyph | `home/font/youspeak-v1.otf` | the repository's licence, CC BY-SA 4.0 (`LICENSE`); no font-specific licence is recorded | built in this repository | |

## Images and other material

| Item | Maker | Licence | Source |
|---|---|---|---|
| None: the kit and the cards are drawn from the font's outlines and the site's colour tokens, with no outside images (`kit/notes.md`, `og/generate.py`) | | | |
