#!/usr/bin/env python3
"""build_lexicon.py — assemble the cathedral's pronunciation lexicon.

Scans every canonical entry in the repo for `pronunciation:` lines, merges
forged additions from voice/forged.json (words whose entries lacked IPA at
forge-time), converts each IPA to espeak-ng phonemes, and writes
voice/lexicon.tsv:

    word <TAB> ipa <TAB> espeak <TAB> respelling <TAB> source

The roster of words is the citizen roster (one word per forged-word citizen)
so the lexicon and the populace stay the same set. Words still missing IPA
are listed loudly — silence is how stubs survive.

  $ python3 build_lexicon.py [--roster PATH] [--repo PATH]
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ROSTER = os.path.expanduser("~/love-unlimited/citizens-roster.txt")

sys.path.insert(0, HERE)
from ipa2espeak import ipa_to_espeak  # noqa: E402

PRON_RE = re.compile(r"pronunciation:?\s*(/[^/\n]+/)\s*(?:\(([^)\n]*)\))?", re.I)


def scan_repo(repo: str) -> dict:
    """word → (ipa, respelling, path) from frontmatter or entry blocks."""
    found = {}
    for path in glob.glob(os.path.join(repo, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, repo)
        if rel.startswith((".venv", "liturgy", "tutorial")) or rel in ("dashboard.md", "_sidebar.md"):
            continue
        try:
            txt = open(path, encoding="utf-8").read()
        except OSError:
            continue
        fm = re.match(r"---\n(.*?)\n---", txt, re.S)
        if fm:
            m_word = re.search(r"^(?:word|name|candidate):\s*(\S+)", fm.group(1), re.M)
            m_pron = PRON_RE.search(fm.group(1))
            if m_word and m_pron:
                w = m_word.group(1).strip("*")
                found.setdefault(w, (m_pron.group(1), m_pron.group(2) or "", rel))
        for m in re.finditer(r"^###+ \**([a-z-]+)\**.*?\n(.*?)(?=^###|\Z)", txt, re.S | re.M):
            w, block = m.group(1), m.group(2)
            p = PRON_RE.search(block)
            if p and w not in found:
                found[w] = (p.group(1), p.group(2) or "", rel)
    return found


def main() -> None:
    repo = REPO
    roster_path = ROSTER
    args = sys.argv[1:]
    if "--repo" in args:
        repo = args[args.index("--repo") + 1]
    if "--roster" in args:
        roster_path = args[args.index("--roster") + 1]

    roster = [l.strip() for l in open(roster_path, encoding="utf-8") if l.strip()]
    scanned = scan_repo(repo)

    forged_path = os.path.join(HERE, "forged.json")
    forged = {}
    if os.path.exists(forged_path):
        for rec in json.load(open(forged_path, encoding="utf-8")):
            forged[rec["word"]] = (rec["ipa"], rec.get("respelling", ""), "voice/forged.json")

    rows, missing = [], []
    for w in roster:
        ipa, resp, src = scanned.get(w) or forged.get(w) or ("", "", "")
        if not ipa:
            missing.append(w)
            continue
        rows.append((w, ipa, ipa_to_espeak(ipa), resp.strip(), src))

    out = os.path.join(HERE, "lexicon.tsv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("word\tipa\tespeak\trespelling\tsource\n")
        for r in sorted(rows):
            f.write("\t".join(r) + "\n")

    print(f"lexicon: {len(rows)}/{len(roster)} words → {out}")
    if missing:
        print(f"MISSING IPA ({len(missing)}): {', '.join(missing)}")
        sys.exit(2)


if __name__ == "__main__":
    main()
