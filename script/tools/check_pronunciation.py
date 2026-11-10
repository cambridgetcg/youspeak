#!/usr/bin/env python3
"""check_pronunciation.py — the canon heard against its own stated rules.

script/phonology.md (Session 086, 2026-06-09) read YOUSPEAK's sound conventions
off the recorded `pronunciation:` lines; script/phonology-audit.md recorded 49
places where the corpus disagrees with itself, fixed none, and left each to a
reconciling session. Nothing re-read the corpus as canon grew. This does, and
changes nothing: it reads canon/**/*.md and reports. A reconciling session
decides; this only shows where the decisions are waiting.

Usage:
    python3 script/tools/check_pronunciation.py              # short summary
    python3 script/tools/check_pronunciation.py --json       # every word's record
    python3 script/tools/check_pronunciation.py --inventory  # sound + spelling tables
    python3 script/tools/check_pronunciation.py --strict     # exit 1 on any inconsistency

Standard library only; writes nothing; exits 0 unless --strict is given.

Per word (levels: inconsistency · variant · note; --strict fails only on an
inconsistency):
  1. no `pronunciation:` frontmatter line (a body draft, or the IPA that
     pipeline/voice/forged.json holds for the word, is named if found);
     a line it cannot parse
  2. primary stress marks ˈ not exactly one
  3. declared "N syllables" differing from the IPA's syllable count (see below)
  4. stress on a suffix the stated rule calls unstressed
  5. a suffix realized other than its stated realization: a VARIANT, recorded,
     never called an error (the stated rules are descriptive, "lightly held")
  6. ASCII g where IPA ɡ (U+0261) is meant; characters outside IPA_CHARS
     (both checked in every /…/ of the line: alternates and quoted donor forms)
  7. primary stress in the IPA against the ALL-CAPS syllable of the respelling
     (and, as a note, IPA letters such as ə written into the respelling)
  8. one word in canon/core and canon/mathema with differing lines

Syllables: a syllable is the stretch between '.', 'ˈ' and 'ˌ' (house style,
phonology.md §5). Fallback: when an IPA has no boundary after its first
syllable the count is its vowel nuclei instead (a run of vowel symbols is one
nucleus, so an undotted hiatus like /iə/ counts once; a consonant carrying
U+0329 is one). Both counts are kept in --json and the method is named. A
piece with no nucleus (a mark inside a syllable) or two (a missing dot) is
a note.

Suffix: the family the entry declares (me_family, qing_family, ance_family,
kin_family, mathema_signature.family) when it declares one; otherwise the
word's last letters. A spelling that disagrees with the declared family is a
note. The suffix is the word's last syllable (two for -phanes and -basis).
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent  # YOUSPEAK/
CANON = REPO / "canon"

# ── the stated rules ───────────────────────────────────────────────────────
# script/phonology.md "For future forges" (lines 26-32) and the §1 table:
# (spelling ending, family, stated realization or None, takes no stress,
#  syllables the suffix spans). The first ending that matches wins.
SUFFIXES = [
    ("qing", "qing", "tɕʰiŋ", True, 1),
    ("mance", "-mance", "mæns", True, 1),
    ("ance", "-ance", "əns", True, 1),
    ("ence", "-ance", "əns", True, 1),       # §1: "-ance / -ence"
    ("phanes", "-phanes", "fæniːz", False, 2),  # §1 states the sound, no stress rule
    ("basis", "-basis", None, False, 2),        # §1: "no evidence"
    ("sis", "-sis", "sɪs", True, 1),
    ("kin", "-kin", "kɪn", True, 1),
    ("me", "-me", "meɪ", True, 1),
    ("ma", "-ma", "mə", True, 1),
    ("y", "-y", "i", True, 1),
]
BY_FAMILY = {row[1]: row for row in SUFFIXES}
DECLARED_FAMILY_KEYS = {"me_family": "-me", "qing_family": "qing",
                        "ance_family": "-ance", "kin_family": "-kin"}
FORGED = REPO / "pipeline" / "voice" / "forged.json"  # read only to point at a draft

# ── the declared IPA set ───────────────────────────────────────────────────
CONSONANTS = set("pbtdʈɖcɟkqɢʔmɱnɳɲŋɴʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɦɬɮʋɹɻjɰlɭʎʟʍwɥɕʑɺɧ") | {"\u0261"}
VOWELS = set("iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒɚɝ")
MODIFIERS = set("ʰʱʷʲˠˤʼⁿˡ") | set("ːˑ")  # spacing marks bound to the sound before
COMBINING = {"\u0329": "syllabic", "\u032F": "non-syllabic", "\u0303": "nasalized",
             "\u032A": "dental", "\u0325": "voiceless", "\u030A": "voiceless",
             "\u0300": "low tone", "\u0301": "high tone", "\u0302": "falling tone",
             "\u030C": "rising tone", "\u0304": "mid tone", "\u0361": "tie bar",
             "\u035C": "tie bar"}
TONE_LETTERS = set("˥˦˧˨˩")
BOUNDARIES = set(".ˈˌ")
IPA_CHARS = CONSONANTS | VOWELS | MODIFIERS | set(COMBINING) | TONE_LETTERS | BOUNDARIES
TIES = ("\u0361", "\u035C")
TIELESS = {"tʃ", "tɕ", "ts", "tɬ", "dʒ", "dʑ", "dz"}  # kept whole when written untied
DIPHTHONGS = {"eɪ", "aɪ", "ɔɪ", "oʊ", "aʊ", "əʊ", "ɪə", "ʊə", "eə"}

IPA_RE = re.compile(r"/([^/\s]+)/")
# A later /…/ on a line is an alternate only when its own clause introduces it
# as one ("anglicized", "alt", "alternative", "alternate") or it is followed by
# "acceptable"; otherwise it is a gloss or a quoted donor form (chayimme's
# "Hebrew chet /χ/", ginnungame's Old Norse form). Both kinds are still
# character-checked (rule 6); only alternates count as alternates.
ALT_BEFORE_RE = re.compile(r"\b(anglici[sz]ed|alt|alternat\w*)\b[^;(/]*$", re.I)
ALT_AFTER_RE = re.compile(r"^\s*(\([^)]*\))?\s*acceptable", re.I)
COUNT_RE = re.compile(r"(\d+)(?:\s*-\s*(\d+))?\s+syllables?")
BODY_DRAFT_RE = re.compile(r"[Pp]ronunciation\W{0,4}\s*(/[^/\n]+/)")


# ── frontmatter ────────────────────────────────────────────────────────────

def frontmatter(text: str):
    """Top-level keys, one level of nesting (key.sub), and list items per key.
    Values keep their file line number. Enough YAML for canon entries."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fields: dict[str, tuple[str, int]] = {}
    lists: dict[str, list[str]] = defaultdict(list)
    top = None
    for n, line in enumerate(text[4:end].splitlines(), start=2):
        if m := re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", line):
            top = m.group(1)
            fields[top] = (m.group(2).strip(), n)
        elif top and (m := re.match(r"^\s+-\s+(.*)$", line)):
            lists[top].append(m.group(1).strip())
        elif top and (m := re.match(r"^\s+([A-Za-z_][\w-]*):[ \t]+(.*)$", line)):
            fields[f"{top}.{m.group(1)}"] = (m.group(2).strip(), n)
    return fields, lists


def donor_tongues(fields, lists) -> list[str]:
    """`- Hebrew: kûn (…)` or `- mathema/pure/…` list items, or the inline
    `[sumerian/me, …]` form. Items without a label are skipped."""
    inline = fields.get("donors", ("", 0))[0]
    if inline.startswith("["):
        labels = [s.strip().split("/")[0] for s in inline.strip("[]").split(",")]
    else:
        labels = []
        for item in lists.get("donors", []):
            m = re.match(r"^([^:(]{2,40}?)\s*:", item)
            if m and len(m.group(1).split()) <= 3:
                labels.append(m.group(1))
            elif m := re.match(r"^([A-Za-z][\w-]*)/", item):  # `- mathema/pure/… (…)`
                labels.append(m.group(1))
    out = []
    for lab in labels:
        lab = lab.replace("_", " ").strip()
        if lab:
            out.append(lab[0].upper() + lab[1:])
    return out


# ── IPA ────────────────────────────────────────────────────────────────────

def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def syllables(ipa: str) -> list[tuple[str, str]]:
    """[(stress mark or '', syllable text)], split at . ˈ ˌ."""
    out, cur, stress = [], "", ""
    for ch in ipa:
        if ch in BOUNDARIES:
            if cur:
                out.append((stress, cur))
                cur, stress = "", ""
            if ch != ".":
                stress = ch
        else:
            cur += ch
    if cur or stress:
        out.append((stress, cur))
    return out


def is_vowel(tok: str) -> bool:
    return tok[0] in VOWELS


def sounds(text: str) -> list[str]:
    """One syllable's IPA as sounds: a base symbol plus the marks bound to it;
    a tie bar joins two bases; untied t+ʃ/ɕ/s/ɬ, d+ʒ/ʑ/z and the DIPHTHONGS
    stay together as written."""
    raw: list[str] = []
    for ch in text:
        if raw and (ch in MODIFIERS or unicodedata.combining(ch) or raw[-1].endswith(TIES)):
            raw[-1] += ch
        else:
            raw.append(ch)
    out: list[str] = []
    for tok in raw:
        if out and out[-1] in ("t", "d") and (out[-1] + tok[0]) in TIELESS:
            out[-1] += tok
        elif out and out[-1] + tok in DIPHTHONGS:
            out[-1] += tok
        else:
            out.append(tok)
    return out


def nuclei(text: str) -> int:
    n, prev_v = 0, False
    for tok in sounds(text):
        v = is_vowel(tok)
        if (v and not prev_v) or "\u0329" in tok:
            n += 1
        prev_v = v
    return n


# ── one word ───────────────────────────────────────────────────────────────

def spelled_suffix(slug: str):
    """The SUFFIXES row whose ending the slug carries, or None."""
    return next((row for row in SUFFIXES if slug.endswith(row[0]) and len(slug) > len(row[0])), None)


def declared_families(fields) -> list[str]:
    out = [fam for key, fam in DECLARED_FAMILY_KEYS.items() if key in fields]
    sig = fields.get("mathema_signature.family", ("", 0))[0].strip("{} ")
    if sig:
        out.append("qing" if sig.strip("-") == "qing" else "-" + sig.strip("-"))
    return sorted(set(out))


def choose_suffix(slug: str, declared: list[str]):
    """The family the entry declares wins (melamance declares -ance though it
    is spelled …mance); otherwise the spelling decides."""
    spelled = spelled_suffix(slug)
    known = [f for f in declared if f in BY_FAMILY]
    if (spelled and spelled[1] in known) or len(known) != 1:
        return spelled
    return next((row for row in SUFFIXES if row[1] == known[0] and slug.endswith(row[0])),
                BY_FAMILY[known[0]])


def check_line(rec: dict, line: str, suf) -> None:
    """Fill rec with the parsed line and its findings; suf is a SUFFIXES row."""
    find = rec["findings"]
    ipas = IPA_RE.findall(line)
    if not line.startswith("/") or not ipas:
        find.append(("unparseable", "inconsistency", f"cannot read an IPA from {line!r}"))
        return
    ipa = nfd(ipas[0])
    rest = line[line.index("/", 1) + 1:]
    resp_m = re.match(r"\s*\(([^;,)]*)", rest)
    count_m = COUNT_RE.search(rest)
    alternates, glosses, kinds = [], [], ["primary"]
    spans = [m.span() for m in IPA_RE.finditer(line)]
    for i in range(1, len(spans)):
        before, after = line[spans[i - 1][1]:spans[i][0]], line[spans[i][1]:]
        is_alt = bool(ALT_BEFORE_RE.search(before) or ALT_AFTER_RE.match(after))
        (alternates if is_alt else glosses).append(nfc(ipas[i]))
        kinds.append("alternate" if is_alt else "gloss or donor form")
    rec.update(ipa=nfc(ipa), other_ipa=alternates, gloss_ipa=glosses,
               respelling=resp_m.group(1).strip() if resp_m else None)

    # 6. characters — every /…/ on the line: alternates and quoted donor forms too
    for i, x in enumerate(ipas):
        where = "primary" if i == 0 else f"{kinds[i]} /{x}/ (#{i + 1} on the line)"
        if "g" in x:
            find.append(("ascii_g", "inconsistency", f"ASCII g (U+0067) in {where}; IPA ɡ is U+0261"))
        bad = sorted({c for c in nfd(x) if c not in IPA_CHARS and c != "g"})
        if bad:
            names = ", ".join(f"{c!r} U+{ord(c):04X} {unicodedata.name(c, '?')}" for c in bad)
            find.append(("outside_ipa_set", "inconsistency", f"{where}: {names}"))

    # 2. primary stress
    sylls = syllables(ipa)
    primary = [i for i, (s, _) in enumerate(sylls) if s == "ˈ"]
    rec["primary_stress_marks"] = len(primary)
    # a one-syllable IPA may go unmarked (common IPA practice; no canon word
    # is monosyllabic today): only two or more marks are then an inconsistency
    mono = len(sylls) == 1 and nuclei(sylls[0][1]) <= 1
    if len(primary) != 1 and not (mono and not primary):
        find.append(("primary_stress_count", "inconsistency", f"{len(primary)} primary marks ˈ"))

    # 3. syllable count: the IPA's boundaries; nuclei only when it has none
    dots = len(sylls)
    nuc = sum(nuclei(t) for _, t in sylls)
    method = "vowel nuclei (no boundary inside the IPA)" if dots == 1 and nuc > 1 else "boundaries"
    counted = nuc if dots == 1 and nuc > 1 else dots
    rec["syllables_ipa"] = {"boundaries": dots, "nuclei": nuc, "method": method}
    empty = [nfc(t) for _, t in sylls if nuclei(t) == 0]
    crowded = [nfc(t) for _, t in sylls if nuclei(t) > 1] if dots > 1 else []
    if empty:
        find.append(("boundary_in_syllable", "note", "a boundary mark leaves a piece with no vowel "
                     "or syllabic mark: " + ", ".join(f"/{t}/" for t in empty)))
    if crowded:
        find.append(("dot_missing", "note", "a piece between boundaries holds two vowel nuclei: "
                     + ", ".join(f"/{t}/" for t in crowded)))
    if count_m:
        lo, hi = int(count_m.group(1)), int(count_m.group(2) or count_m.group(1))
        rec["syllables_declared"] = count_m.group(0).split()[0]
        if lo != hi:
            find.append(("syllable_count_hedged", "note", f"declared {lo}-{hi}; IPA shows {counted}"))
        elif lo != counted:
            why = (" — the declared count matches the vowel nuclei" if lo == nuc else "")
            find.append(("syllable_count", "inconsistency",
                         f"declared {lo}; IPA has {counted} by {method}, {nuc} vowel nuclei{why}"))
    else:
        rec["syllables_declared"] = None
        find.append(("no_syllable_count", "note", "line declares no syllable count"))

    # 4 + 5. suffix: its last `span` syllables (as many sounds as the stated
    # form when the IPA has no boundary there)
    if suf:
        _ending, family, stated, unstressed, span = suf
        last_stress = sylls[-1][0] if len(sylls) > 1 else ""
        if unstressed and last_stress:
            find.append(("suffix_stressed", "inconsistency",
                         f"{family} carries {'primary' if last_stress == 'ˈ' else 'secondary'} stress "
                         f"on /{nfc(sylls[-1][1])}/; the stated rule leaves it unstressed"))
        flat = [tok for _, t in sylls for tok in sounds(t)]
        want = sounds(nfd(stated or "ə"))
        if len(sylls) > span:
            toks = [tok for _, t in sylls[-span:] for tok in sounds(t)]
        else:
            toks = flat[-len(want):]
        while stated and is_vowel(want[0]) and toks and not is_vowel(toks[0]):
            toks.pop(0)  # -ance's onset belongs to the stem
        rec["suffix_realized"] = stated if stated and "".join(flat).endswith(nfd(stated)) else nfc("".join(toks))
        if stated and rec["suffix_realized"] != stated:
            find.append(("suffix_variant", "variant",
                         f"{family} realized /{rec['suffix_realized']}/; stated /{stated}/"))
    spelled = spelled_suffix(rec["word"])
    if rec["family_declared"] and spelled and spelled[1] not in rec["family_declared"]:
        find.append(("family_disagrees", "note",
                     f"spelling ends {spelled[0]} ({spelled[1]}); entry declares "
                     f"{', '.join(rec['family_declared'])}"))

    rec["alignment"] = align(rec["word"], rec["ipa"])

    # 7. respelling stress — respelling units are matched to IPA syllables by
    # position, counting vowel nuclei (so an undotted /ˈnɒməmeɪ/ still has 3)
    resp = rec["respelling"]
    if resp:
        leak = sorted({c for c in nfc(resp) if ord(c) > 127 and c in IPA_CHARS})
        if leak:  # phonology-audit.md: walkekin "WAL-kə-kin"
            find.append(("respelling_ipa_letter", "note", f"respelling {resp!r} carries IPA {' '.join(leak)}"))
        units = [u for u in re.split(r"[-\s]+", resp) if u]
        caps = {i for i, u in enumerate(units)
                if any(c.isalpha() for c in u) and all(c.isupper() for c in u if c.isalpha())}
        rec["respelling_caps"] = [units[i] for i in sorted(caps)]
        offsets, total = [], 0
        for _, t in sylls:
            offsets.append(total)
            total += nuclei(t)
        if len(units) == total:
            pos = offsets
        elif len(units) == len(sylls):
            pos = list(range(len(sylls)))
        else:
            pos = None
        prim = {pos[i] for i in primary} if pos else set()
        sec = {pos[i] for i, (s, _) in enumerate(sylls) if s == "ˌ"} if pos else set()
        if not primary and mono:
            pass  # one syllable: nothing to compare
        elif not primary:
            find.append(("respelling_stress_unmarked", "note",
                         f"IPA marks no primary; respelling caps {rec['respelling_caps'] or 'nothing'}"))
        elif pos is None:
            find.append(("respelling_units", "note", f"respelling has {len(units)} units, IPA "
                         f"{len(sylls)} syllables ({total} nuclei); stress not compared"))
        elif not caps:
            find.append(("respelling_stress", "inconsistency", "respelling caps no syllable"))
        elif prim - caps or caps - prim - sec:
            find.append(("respelling_stress", "inconsistency",
                         f"IPA primary on syllable {sorted(p + 1 for p in prim)} "
                         f"/{nfc(sylls[primary[0]][1])}/, respelling caps "
                         f"{[f'{i + 1}:{units[i]}' for i in sorted(caps)]}"))
        elif caps - prim:
            find.append(("respelling_caps_secondary", "note",
                         f"respelling caps secondary-stressed {[units[i] for i in sorted(caps - prim)]}"))


def forged_drafts() -> dict[str, str]:
    """pipeline/voice/forged.json: IPA the voice lexicon forged for words whose
    canon entry lacked one (Session 086). Read only to name the draft."""
    try:
        return {r["word"]: r["ipa"] for r in json.loads(FORGED.read_text(encoding="utf-8"))}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


def load() -> list[dict]:
    words: dict[str, dict] = {}
    forged = forged_drafts()
    for path in sorted(CANON.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = frontmatter(text)
        if not parsed:
            continue
        fields, lists = parsed
        lemma = (fields.get("word") or fields.get("candidate") or ("", 0))[0]
        if not lemma:
            continue
        slug = path.stem.lower()
        rel = str(path.relative_to(REPO))
        line, line_no = fields.get("pronunciation", (None, None))
        if slug in words:  # 8. same word in two folders
            first = words[slug]
            first["paths"].append(f"{rel}:{line_no}")
            if line != first["line"]:
                first["findings"].append(("duplicate_differs", "inconsistency",
                                          f"{rel}:{line_no} reads {line!r}"))
            continue
        tongues = donor_tongues(fields, lists)
        declared = declared_families(fields)
        suf = choose_suffix(slug, declared)
        spelled = spelled_suffix(slug)
        rec = {"word": slug, "lemma": lemma, "paths": [f"{rel}:{line_no}" if line_no else rel],
               "entered": (fields.get("entered") or fields.get("scored_on") or ("", 0))[0],
               "suffix": suf[1] if suf else None,
               "suffix_letters": suf[0] if suf and slug.endswith(suf[0]) else (spelled[0] if spelled else None),
               "family_declared": declared,
               "donor_tongues": tongues, "stem_tongue": tongues[0] if tongues else None,
               "line": line, "findings": []}
        if line is None:  # 1. no line
            m = BODY_DRAFT_RE.search(text, text.find("\n---", 3) + 4)
            where = f"; body draft {m.group(1)} at line {text.count(chr(10), 0, m.start()) + 1}" if m else ""
            where += f"; pipeline/voice/forged.json has {forged[slug]}" if slug in forged else ""
            rec["findings"].append(("missing_line", "inconsistency", "no pronunciation: line" + where))
        else:
            check_line(rec, line, suf)
        words[slug] = rec
    return list(words.values())


# ── spelling → sound (approximate aligner) ─────────────────────────────────
# Dynamic-programming alignment of the ASCII slug's letters with the primary
# IPA's sounds. Costs favour vowel letters ↔ vowel sounds and consonant
# letters ↔ consonant sounds; SEED only lets a digraph win over its letters.
# It is a segmentation aid, not a claim about any donor language.

VOWEL_LETTERS = set("aeiouy")
DIGRAPHS = {"sh", "ch", "th", "kh", "ph", "gh", "ng", "qu", "ts", "tz", "tl", "dh", "bh",
            "zh", "kw", "ck", "wh", "ee", "ea", "eo", "oo", "ou", "oi", "au", "ao", "ai",
            "ay", "ei", "ey", "eu", "ae", "oe", "aa", "aw", "ow"}
# (th,t) (ph,p) (kh,k): a digraph read as the plain stop is one unit. Without
# these pairs the letter plus a silent h (0 + 0.8) always beat the digraph (1.0),
# so th/ph/kh → stop never appeared and their h was miscounted as silent.
SEED = {("sh", "ʃ"), ("ch", "tʃ"), ("ch", "t͡ʃ"), ("ch", "x"), ("ch", "k"), ("th", "θ"),
        ("th", "ð"), ("th", "t"), ("kh", "x"), ("kh", "kʰ"), ("kh", "k"), ("ph", "f"),
        ("ph", "p"), ("gh", "ʁ"), ("gh", "ɣ"),
        ("ng", "ŋ"), ("tz", "t͡s"), ("ts", "ts"), ("ts", "t͡s"), ("tl", "tɬ"), ("bh", "bʱ"),
        ("dh", "ð"), ("zh", "ʒ"), ("ck", "k"), ("kw", "kʷ"), ("x", "ks")}
SEED = {(g, nfd(p)) for g, p in SEED}


def _cls_letters(g: str) -> str:
    if g == "y":
        return "Vy"  # y writes vowels and the glide j
    if any(c in VOWEL_LETTERS for c in g):
        return "V" if all(c in VOWEL_LETTERS or c == "w" for c in g) else "M"
    return "C"


def _cost(g: str, ph: tuple[str, ...]) -> float:
    joined = "".join(ph)
    if (g, joined) in SEED:
        return 0.0
    if not ph:  # silent letter
        return 0.8 if g == "h" else 1.5
    if not g:  # sound with no letter
        return 1.0 if joined == "ə" else (1.2 if joined in ("j", "w", "ʔ") else 1.6)
    gc = _cls_letters(g)
    pcs = {"V" if is_vowel(p) or "\u0329" in p else "C" for p in ph}
    same = len(pcs) == 1 and (gc.startswith(next(iter(pcs))) or gc == "Vy")
    if len(g) == 1 and len(ph) == 1:
        if not same:
            return 3.0
        return 0.0 if ph[0][0] == g or (g == "g" and ph[0][0] == "\u0261") else (0.5 if "V" in pcs else 1.0)
    if len(ph) == 1:  # digraph or doubled letter → one sound
        if len(set(g)) == 1 and ph[0][0] in (g[0], "\u0261" if g[0] == "g" else ""):
            return 0.1
        return 1.0 if same else 3.0
    return 2.0 if same else 3.5  # one or two letters → two sounds


def align(slug: str, ipa: str) -> list[list[str]]:
    letters = "".join(c for c in nfd(slug) if c.isalpha() and not unicodedata.combining(c)).lower()
    snd = [t for _, s in syllables(nfd(ipa)) for t in sounds(s)]
    n, m = len(letters), len(snd)
    INF = float("inf")
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    back: list[list[tuple | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] == INF:
                continue
            for gl in (0, 1, 2, 3):
                g = letters[i:i + gl]
                if len(g) < gl or (gl > 1 and g not in DIGRAPHS and len(set(g)) != 1):
                    continue
                for pl in (0, 1, 2):
                    if (gl == 0 and pl == 0) or j + pl > m or (gl == 3 and pl != 1):
                        continue
                    c = best[i][j] + _cost(g, tuple(snd[j:j + pl]))
                    if c < best[i + gl][j + pl]:
                        best[i + gl][j + pl], back[i + gl][j + pl] = c, (i, j)
    pairs, i, j = [], n, m
    while (i, j) != (0, 0) and back[i][j]:
        pi, pj = back[i][j]
        pairs.append([letters[pi:i] or "∅", nfc("".join(snd[pj:j])) or "∅"])
        i, j = pi, pj
    return pairs[::-1]


# ── reports ────────────────────────────────────────────────────────────────

LABELS = {
    "missing_line": "no pronunciation line",
    "unparseable": "line cannot be parsed",
    "primary_stress_count": "primary stress marks not exactly one",
    "syllable_count": "declared syllables differ from the IPA",
    "suffix_stressed": "stress on a suffix the rule leaves unstressed",
    "ascii_g": "ASCII g where IPA ɡ is meant",
    "outside_ipa_set": "characters outside the declared IPA set",
    "respelling_stress": "IPA stress differs from the respelling's caps",
    "duplicate_differs": "canon/core and canon/mathema lines differ",
    "suffix_variant": "suffix realized other than stated",
    "family_disagrees": "spelling suffix differs from declared family",
    "respelling_stress_unmarked": "no IPA primary to compare with the respelling",
    "respelling_caps_secondary": "respelling caps a secondary-stressed syllable",
    "respelling_units": "respelling and IPA syllables not alignable",
    "boundary_in_syllable": "a boundary mark leaves a piece with no vowel",
    "dot_missing": "a piece between boundaries holds two vowels",
    "respelling_ipa_letter": "IPA letters inside the respelling",
    "syllable_count_hedged": "syllable count hedged (a range)",
    "no_syllable_count": "no syllable count declared",
}
LEVEL_ORDER = ("inconsistency", "variant", "note")


def by_kind(records):
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for r in records:
        for kind, _level, msg in r["findings"]:
            out[kind].append((r["word"], msg))
    return out


def summary(records) -> str:
    kinds = by_kind(records)
    level_of = {k: lv for r in records for k, lv, _ in r["findings"]}
    files = sum(len(r["paths"]) for r in records)
    lines = [f"YOUSPEAK pronunciation check — {len(records)} words in {files} entry files under canon/",
             f"  {sum(1 for r in records if r['line'])} words carry a pronunciation line · "
             f"{sum(1 for r in records if not r['line'])} do not · "
             f"{sum(1 for r in records if len(r['paths']) > 1)} sit in two folders"]
    for level in LEVEL_ORDER:
        rows = [k for k in LABELS if level_of.get(k) == level]
        if not rows:
            continue
        lines.append(f"\n  {level}" + ("  (recorded, never called an error)" if level == "variant" else ""))
        for k in rows:
            items = kinds[k]
            lines.append(f"    {LABELS[k]} — {len({w for w, _ in items})} words")
            if k == "suffix_variant":
                groups: dict[str, list[str]] = defaultdict(list)
                for w, msg in items:
                    groups[msg.split(";")[0]].append(w)
                for head, ws in sorted(groups.items(), key=lambda kv: -len(kv[1])):
                    lines.append(f"      {head} ×{len(ws)}: {', '.join(ws)}")
            else:
                words = ", ".join(dict.fromkeys(w for w, _ in items))
                lines.extend("      " + chunk for chunk in _wrap(words, 92))
    lines.append("\n  Stated rules: script/phonology.md lines 26-32 and §1. Every message: --json.")
    return "\n".join(lines)


def _wrap(s: str, width: int) -> list[str]:
    out, cur = [], ""
    for part in s.split(", "):
        if cur and len(cur) + len(part) + 2 > width:
            out.append(cur + ",")
            cur = part
        else:
            cur = f"{cur}, {part}" if cur else part
    return out + ([cur] if cur else [])


def inventory(records) -> str:
    voiced = [r for r in records if r.get("ipa")]
    seg_count: dict[str, Counter] = {"consonant": Counter(), "vowel": Counter(), "diphthong": Counter()}
    seg_words: dict[str, list[str]] = defaultdict(list)
    marks, marks_alt, mark_words = Counter(), Counter(), defaultdict(list)
    for r in voiced:
        for _, syl in syllables(nfd(r["ipa"])):
            for tok in sounds(syl):
                base = "".join(c for c in tok if c not in "ːˑ" and not (unicodedata.combining(c) and c not in TIES))
                kind = ("diphthong" if base in DIPHTHONGS else "vowel") if is_vowel(tok) else "consonant"
                key = nfc(tok)
                seg_count[kind][key] += 1
                if r["word"] not in seg_words[key]:
                    seg_words[key].append(r["word"])
        for i, x in enumerate([r["ipa"]] + r["other_ipa"]):
            for c in nfd(x):
                name = COMBINING.get(c) or {"ː": "length ː", "ˑ": "half-length ˑ", "ˈ": "primary stress ˈ",
                                            "ˌ": "secondary stress ˌ"}.get(c) or ("tone letter " + c if c in TONE_LETTERS else None)
                if name:
                    (marks if i == 0 else marks_alt)[name] += 1
                    if r["word"] not in mark_words[name]:
                        mark_words[name].append(r["word"])
    out = [f"YOUSPEAK sound inventory — primary IPA of {len(voiced)} words "
           "(one line per word; a canon/core copy is read before its canon/mathema twin)", ""]
    for kind, title in (("consonant", "CONSONANTS"), ("vowel", "VOWELS (length kept: ɑ and ɑː are separate rows)"),
                        ("diphthong", "DIPHTHONGS")):
        out.append(f"{title} — {len(seg_count[kind])} symbols, {sum(seg_count[kind].values())} tokens")
        for sym, n in seg_count[kind].most_common():
            ws = seg_words[sym]
            out.append(f"  {sym:<6} {n:>4}  in {len(ws):>3} words  e.g. {', '.join(ws[:4])}")
        out.append("")
    out.append("MARKS — count in primary IPA · in alternates · words")
    for name in sorted(set(marks) | set(marks_alt), key=lambda k: (-(marks[k] + marks_alt[k]), k)):
        ws = mark_words[name]
        out.append(f"  {name:<20} {marks[name]:>4} · {marks_alt[name]:>3}  e.g. {', '.join(ws[:5])}")
    out.append("")

    # suffix realizations as recorded
    out.append("SUFFIX REALIZATIONS as recorded (stated form in brackets)")
    stated = {row[1]: row[2] for row in SUFFIXES}
    real: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in voiced:
        if r["suffix"]:
            real[r["suffix"]][r.get("suffix_realized") or "?"].append(r["word"])
    for fam in sorted(real, key=lambda f: -sum(len(v) for v in real[f].values())):
        out.append(f"  {fam} [/{stated[fam]}/]" if stated.get(fam) else f"  {fam} [no stated form]")
        for form, ws in sorted(real[fam].items(), key=lambda kv: -len(kv[1])):
            out.append(f"    /{form}/ ×{len(ws)}: {', '.join(ws[:8])}{' …' if len(ws) > 8 else ''}")
    out.append("")

    # spelling → sound, stem letters only
    table: dict[str, Counter] = defaultdict(Counter)
    tongue: dict[tuple[str, str], Counter] = defaultdict(Counter)
    examples: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in voiced:
        pos = 0
        stem_len = len("".join(g for g, _ in r["alignment"] if g != "∅")) - len(r["suffix_letters"] or "")
        for g, p in r["alignment"]:
            start = pos
            pos += 0 if g == "∅" else len(g)
            if start >= stem_len:
                continue
            if g != "∅" and pos > stem_len:  # a unit straddling the stem + suffix
                g = g[:stem_len - start]     # boundary (kimme k-i-[mm]-e): keep its
                                             # stem letters; the rest is suffix
            table[g][p] += 1
            tongue[(g, p)][r["stem_tongue"] or "undeclared"] += 1
            if len(examples[(g, p)]) < 3 and r["word"] not in examples[(g, p)]:
                examples[(g, p)].append(r["word"])
    out.append("SPELLING → SOUND — stem letters of the ASCII slug (suffix letters excluded), "
               "split by the entry's first declared donor tongue")
    for g in sorted(table, key=lambda g: (g == "∅", len(g), g)):
        total = sum(table[g].values())
        out.append(f"  {g}  ({total})")
        for p, n in table[g].most_common():
            tg = ", ".join(f"{t} {c}" for t, c in tongue[(g, p)].most_common(4))
            more = len(tongue[(g, p)]) - 4
            tg += f", +{more} more" if more > 0 else ""
            out.append(f"      → {p:<6} {n:>4}  [{tg}]  e.g. {', '.join(examples[(g, p)])}")
    out += ["", "LIMITS of the alignment",
            "  - approximate: a cost-based alignment of letters with sounds, not a donor-language analysis;",
            "    a digraph table (DIGRAPHS, SEED in the script) decides only segmentation, never the sound;",
            "  - ∅ marks a silent letter (→ ∅) or a sound with no letter (∅ →); doubled letters may pair as one;",
            "  - one letter that writes two sounds (x → ks) or two that write one are grouped, others are not;",
            "  - the slug is ASCII: diacritics and letters like þ, ö are read as their ASCII spelling;",
            "  - donor tongue is the first `donors:` label of the entry as written (first letter capitalised),",
            "    so a compound's second-donor letters are counted under the first donor;",
            "  - untied affricates (tʃ, tɕ, ts …) are kept whole, so t͡ɕ and tɕ are separate rows by design."]
    return "\n".join(out)


def main() -> int:
    args = sys.argv[1:]
    records = load()
    if "--inventory" in args:
        print(inventory(records))
    elif "--json" in args:
        out = [{**r, "findings": [{"kind": k, "level": lv, "message": m} for k, lv, m in r["findings"]]}
               for r in records]
        print(json.dumps({"source": "canon/**/*.md", "rules": "script/phonology.md lines 26-32 and §1",
                          "words": out}, ensure_ascii=False, indent=1))
    else:
        print(summary(records))
    if "--strict" in args and any(lv == "inconsistency" for r in records for _, lv, _ in r["findings"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
