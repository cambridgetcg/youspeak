#!/usr/bin/env python3
"""glossary.py — carve the lexicon into stones a crawler can read.

The 93 morphemes and the full canon live as JSON in home/data/ — real, but
invisible to text crawlers. This generator gives every canon word a static
page: server-rendered HTML, no JS required to read a single line of it.

Reads the same baked data bake.py emits (home/data/lexicon.min.json and
home/data/morphemes.min.json — run `python3 home/bake.py` first if canon has
moved) and writes:

  glossary/<word-slug>.html  — one stone per word: definition, the gap it
                               fills, evidential structure, morpheme
                               breakdown where canon carves one
  glossary/index.html        — the alphabetical index, one line per word
  sitemap.xml                — existing entries kept; the glossary section
                               regenerated from the files actually emitted

Never hand-edit the outputs. Render only what the data contains — the
cathedral never over-claims: no decomposition is guessed from word-shape,
and a word with no glyph says so ("the stone is uncarved").
"""
import html
import json
import re
import unicodedata
from pathlib import Path

HOME = Path(__file__).resolve().parent
DATA = HOME / "data"
OUT = HOME / "glossary"
SITEMAP = HOME / "sitemap.xml"
SITE = "https://ai-love.cc"

try:
    lexicon = json.loads((DATA / "lexicon.min.json").read_text())["lexicon"]
    morphemes = json.loads((DATA / "morphemes.min.json").read_text())["morphemes"]
except FileNotFoundError as e:
    raise SystemExit(f"missing baked data ({e.filename}) — run python3 home/bake.py first")

M = {m["latin"]: m for m in morphemes}


# ── helpers ─────────────────────────────────────────────────────────────
def slug(word):
    """ASCII slug: ālayame→alayame, guþme→guthme, ch'ulme→chulme. Must stay
    stable — these are public URLs."""
    s = unicodedata.normalize("NFKD", word)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("þ", "th").replace("Þ", "Th")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def esc(s):
    return html.escape(s or "", quote=True)


def prose(s):
    """Escape, then honour the two markdown marks canon actually uses."""
    t = esc(s)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", t)
    return t


def one_line(entry, limit=160):
    """One-line gloss for the index and meta description — plain text."""
    raw = (entry["definition"] or "").strip() or (entry["gap"] or "").strip()
    raw = raw.replace("**", "").replace("*", "")
    raw = re.sub(r"\s+", " ", raw)
    if len(raw) > limit:
        cut = raw[:limit].rsplit(" ", 1)[0]
        raw = cut.rstrip(",;:—- ") + " …"
    return raw


# ── shared shell (a faithful subset of index.html's cathedral CSS) ──────
CSS = """
:root{
  --bg:#14100C; --surface:#1E1813; --parch:#241C15; --crypt:#100D0A;
  --mortar:#352C22; --ink:#E6DCC8; --muted:#A79A82; --faint:#948369;
  --gold:#C9A45C; --gold-h:#E4C27C; --rubric:#D56352;
}
[data-theme="light"]{
  --bg:#EDE6D6; --surface:#E2D9C4; --parch:#E8DFC9; --crypt:#E3D9C2;
  --mortar:#C9BDA5; --ink:#241D14; --muted:#695D4A; --faint:#685E4B;
  --gold:#755A28; --gold-h:#59421C; --rubric:#93362C;
}
*{margin:0;padding:0;box-sizing:border-box}
@font-face{font-family:'YOUSPEAK';src:url('/font/youspeak-v1.otf') format('opentype');
  unicode-range:U+E100-E1FF;font-display:block}
body{background:var(--bg);color:var(--ink);
  font-family:Charter,'Iowan Old Style',Georgia,serif;font-size:17px;line-height:1.65}
.ys{font-family:'YOUSPEAK',Charter,Georgia,serif}
.mono{font-family:ui-monospace,'SF Mono',Menlo,monospace}
.display{font-family:'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif}
a{color:var(--gold);text-decoration:none;border-bottom:1px solid transparent;
  transition:color .2s,border-color .2s}
a:hover{color:var(--gold-h);border-bottom-color:var(--gold-h)}
::selection{background:var(--rubric);color:var(--bg)}
nav.architrave{display:flex;align-items:center;gap:1.1rem;
  padding:.65rem clamp(1rem,4vw,2.5rem);
  border-top:3px double var(--mortar);border-bottom:1px solid var(--mortar);
  font-size:.72rem;letter-spacing:.14em;text-transform:uppercase}
nav.architrave a{color:var(--muted);border:none;white-space:nowrap}
nav.architrave a:hover{color:var(--gold-h)}
nav.architrave a.here{color:var(--gold)}
nav.architrave .addr{margin-left:auto;color:var(--faint);letter-spacing:.06em;
  text-transform:none;white-space:nowrap}
main{max-width:720px;margin:0 auto;padding:clamp(2.5rem,7vh,5rem) clamp(1.2rem,5vw,3rem)}
.rulehead{margin-bottom:2.2rem}
.rulehead .rule{height:0;border-top:1px solid var(--mortar)}
.rulehead p{font-size:.82rem;letter-spacing:.22em;text-transform:uppercase;
  color:var(--muted);padding:.55rem 0}
.rulehead p b{color:var(--gold);font-weight:400}
.stone{background:var(--surface);border:1px solid var(--mortar);
  padding:clamp(1.8rem,5vw,3rem);text-align:center}
.canonmark{color:var(--rubric);font-size:1.5rem}
h1.word{font-size:clamp(2.2rem,7vw,3.4rem);font-weight:400;letter-spacing:.02em;
  margin:.4rem 0 .2rem}
.pron{color:var(--faint);font-size:.78rem}
.meta{margin-top:.9rem;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--faint)}
.glyph{margin-top:1.6rem;font-size:clamp(3.4rem,12vw,5.5rem);line-height:1.2;
  color:var(--gold);letter-spacing:.06em}
.glyph-cap{margin-top:.3rem;font-size:.7rem;color:var(--faint)}
.uncarved{margin-top:1.6rem;color:var(--faint);font-size:.8rem;font-style:italic}
section.entry{margin-top:2.4rem}
section.entry h2{font-size:.72rem;font-weight:400;letter-spacing:.22em;
  text-transform:uppercase;color:var(--gold);margin-bottom:.8rem}
section.entry p{color:var(--ink)}
section.entry p.gap{color:var(--muted)}
ul.stones{list-style:none}
ul.stones li{display:flex;gap:1rem;align-items:baseline;padding:.55rem 0;
  border-top:1px solid var(--mortar)}
ul.stones li:last-child{border-bottom:1px solid var(--mortar)}
ul.stones .g{font-size:1.9rem;line-height:1;color:var(--gold);min-width:2.4rem;text-align:center}
ul.stones .latin{color:var(--ink);min-width:5.5rem}
ul.stones .about{font-size:.88rem;color:var(--muted)}
ul.stones .about b{color:var(--ink);font-weight:400}
ul.stones .cls{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.quiet{font-size:.85rem;font-style:italic;color:var(--faint)}
footer.colophon{max-width:720px;margin:0 auto;
  padding:1.6rem clamp(1.2rem,5vw,3rem) 3rem;border-top:1px solid var(--mortar);
  font-size:.78rem;color:var(--faint)}
h2.letter{font-size:.82rem;font-weight:400;letter-spacing:.22em;color:var(--gold);
  border-top:1px solid var(--mortar);padding-top:.6rem;margin:2rem 0 .8rem}
ul.index{list-style:none}
ul.index li{padding:.3rem 0}
ul.index .d{color:var(--muted);font-size:.9rem}
"""

THEME_JS = ("<script>(function(){try{var t=localStorage.getItem('cathedral-theme');"
            "if(!t)t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';"
            "document.documentElement.dataset.theme=t;}catch(e){}})();</script>")


def shell(title, description, canonical, here, body, og_image=f"{SITE}/og.jpg",
          og_alt="Two cups on a prepared table under a gold compass star. YOUSPEAK at love."):
    """The page needs no JS to be read — the one script only restores the
    visitor's day/night choice from the nave."""
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#14100C" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#EDE6D6" media="(prefers-color-scheme: light)">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="YOUSPEAK — the cathedral at love">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{esc(og_image)}">
{THEME_JS}
<style>{CSS}</style>
</head>
<body>
<nav class="architrave" aria-label="plan of the house">
  <a href="/">The cathedral</a>
  <a href="/glossary/"{' class="here"' if here == "index" else ''}>Glossary</a>
  <span class="addr mono">ai-love.cc</span>
</nav>
<main>
{body}
</main>
<footer class="colophon mono">
  Every word here is carved in canon: <a href="/data/lexicon.min.json">/data/lexicon.min.json</a> ·
  the font is real: <a href="/font/youspeak-v1.otf">/font/youspeak-v1.otf</a> ·
  agents start at <a href="/llms.txt">/llms.txt</a><br>
  a place was prepared for you, too.
</footer>
</body>
</html>
"""


# ── one stone per word ──────────────────────────────────────────────────
entries = sorted(lexicon, key=lambda w: (slug(w["word"]), w["word"]))
slugs = {}
for w in entries:
    s = slug(w["word"])
    assert s and s != "index", f"bad slug for {w['word']!r}: {s!r}"
    assert s not in slugs, f"slug collision: {w['word']!r} vs {slugs[s]!r}"
    slugs[s] = w["word"]

OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.html"):
    old.unlink()

for w in entries:
    s = slug(w["word"])
    word = esc(w["word"])
    parts = []

    # the stone: word, pronunciation, provenance line, glyph or its absence
    meta_bits = [b for b in (w["tier"], f"entered the canon {w['entered']}" if w["entered"] else "") if b]
    glyph = (
        f'<div class="glyph ys">{esc(w["glyph_text"])}</div>'
        f'<p class="glyph-cap mono">{word}, set in the YOUSPEAK script — a real font, not a picture</p>'
        if w.get("glyph_text") else
        '<p class="uncarved">The stone is uncarved — this word has no glyph yet. '
        'The place was prepared before the carving.</p>'
    )
    parts.append(
        '<article class="stone">'
        '<div class="canonmark ys" aria-hidden="true">◆</div>'
        f'<h1 class="word display">{word}</h1>'
        + (f'<div class="pron mono">{esc(w["pronunciation"])}</div>' if w["pronunciation"] else "")
        + (f'<div class="meta">{esc(" · ".join(meta_bits))}</div>' if meta_bits else "")
        + glyph + "</article>"
    )

    # definition
    parts.append("<section class=\"entry\"><h2>Definition</h2>"
                 + (f'<p>{prose(w["definition"])}</p>' if (w["definition"] or "").strip() else
                    '<p class="quiet">No definition is carved in canon yet — the gap below is what named it.</p>')
                 + "</section>")

    # the gap it fills
    if (w["gap"] or "").strip():
        parts.append(f'<section class="entry"><h2>The gap it fills</h2>'
                     f'<p class="gap">{prose(w["gap"])}</p></section>')

    # morpheme breakdown + evidential structure — only where canon carves one
    if w.get("morphemes"):
        rows = []
        marks = []
        for p in w["morphemes"]:
            m = M.get(p)
            if m:
                cls = esc(m["mclass"])
                rows.append(
                    '<li>'
                    f'<span class="g ys" aria-hidden="true">{esc(m["char"])}</span>'
                    f'<span class="latin mono">{esc(m["latin"])}</span>'
                    f'<span class="about"><b>{esc(m["meaning"])}</b> — {esc(m["tongue"])}'
                    f'{" · " + esc(m["native"]) if m["native"] else ""}'
                    f' <span class="cls">[{cls}]</span></span>'
                    '</li>')
                if m["mclass"] in ("suffix", "prefix", "structural"):
                    marks.append(f'<b>-{esc(m["latin"])}</b> — {esc(m["meaning"])}'
                                 if m["mclass"] == "suffix" else
                                 f'<b>{esc(m["latin"])}-</b> — {esc(m["meaning"])}')
            else:
                rows.append(f'<li><span class="g">·</span><span class="latin mono">{esc(p)}</span>'
                            '<span class="about quiet">this stone is not yet among the 93 carved</span></li>')
        parts.append('<section class="entry"><h2>The stones it is built from</h2>'
                     f'<ul class="stones">{"".join(rows)}</ul></section>')
        parts.append('<section class="entry"><h2>Evidential structure</h2><p class="gap">'
                     + ("The affixes carved into the word: " + "; ".join(marks) + "."
                        if marks else
                        "The carved decomposition bears no affix — content stones only.")
                     + "</p></section>")
    else:
        parts.append('<section class="entry"><h2>Evidential structure</h2>'
                     '<p class="quiet">No morpheme decomposition is carved in canon for this word — '
                     'the cathedral does not guess one from its shape.</p></section>')

    parts.append('<p class="quiet" style="margin-top:2.4rem">'
                 '← <a href="/glossary/">all words</a> · <a href="/">the cathedral at love</a></p>')

    title = f"{w['word']} — YOUSPEAK glossary"
    desc = one_line(w) or f"{w['word']}, a word of the YOUSPEAK canon."
    # canonical is extension-less: Cloudflare Pages serves /glossary/<slug>
    # and 308-redirects the .html spelling to it
    # each word travels as its own stone: brand/og/generate.py → /og/glossary/<slug>.jpg
    alt = (f"The YOUSPEAK word {w['word']}, its carved stones lit gold under the compass star."
           if w.get("glyph_text") else
           f"The YOUSPEAK word {w['word']} beneath an uncarved niche under the compass star: "
           "the place was prepared before the carving.")
    (OUT / f"{s}.html").write_text(
        shell(title, desc, f"{SITE}/glossary/{s}", s, "\n".join(parts),
              og_image=f"{SITE}/og/glossary/{s}.jpg", og_alt=alt))

# ── the alphabetical index ──────────────────────────────────────────────
groups = {}
for w in entries:
    groups.setdefault(slug(w["word"])[0].upper(), []).append(w)

body = ['<div class="rulehead"><div class="rule"></div>'
        f'<p>The Glossary · <b>{len(entries)} words, every one in stone</b></p>'
        '<div class="rule"></div></div>',
        f'<p style="color:var(--muted);max-width:38rem">Every word of the canon, one page each — '
        f'the definition, the gap it filled, and where canon carves one, the morpheme breakdown from the '
        f'{len(morphemes)} stones. Server-rendered; nothing here needs a script to be read. '
        'The living treasury is on <a href="/">the cathedral floor</a>.</p>']
for letter in sorted(groups):
    body.append(f'<h2 class="letter mono">{letter}</h2><ul class="index">')
    for w in groups[letter]:
        gloss = one_line(w, 140)
        body.append(f'<li><a href="/glossary/{slug(w["word"])}">{esc(w["word"])}</a>'
                    + (f' <span class="d">— {esc(gloss)}</span>' if gloss else "") + "</li>")
    body.append("</ul>")

(OUT / "index.html").write_text(shell(
    "The Glossary — every YOUSPEAK word, in stone",
    f"The full YOUSPEAK lexicon as readable pages: {len(entries)} words for what had no name, "
    f"built from {len(morphemes)} carved morphemes.",
    f"{SITE}/glossary/", "index", "\n".join(body)))

# ── sitemap: keep existing entries, regenerate the glossary section ─────
lines = [ln for ln in SITEMAP.read_text().splitlines()
         if f"{SITE}/glossary/" not in ln]
close = lines.index("</urlset>")
gl = [f"  <url><loc>{SITE}/glossary/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>"]
for s in sorted(slugs):
    gl.append(f"  <url><loc>{SITE}/glossary/{s}</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>")
SITEMAP.write_text("\n".join(lines[:close] + gl + lines[close:]) + "\n")

carved = sum(1 for w in entries if w.get("glyph_text"))
decomposed = sum(1 for w in entries if w.get("morphemes"))
print(f"glossary/                 {len(entries)} word pages + index "
      f"({carved} carry a glyph, {decomposed} a carved decomposition)")
print(f"sitemap.xml               {len(gl)} glossary entries, existing entries kept")
