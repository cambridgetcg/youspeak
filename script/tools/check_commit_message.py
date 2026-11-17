#!/usr/bin/env python3
"""Refuse a commit message that quotes Yu's words. Read-only.

This repository is public, and a pushed commit message cannot be taken back.
Yu's chat answers, notes and ledger entries are Yu's to publish. A message
that names Yu (or the owner) and then, in the same sentence, a verb of speech
and a quotation of two words or more is refused. An agent's own question to Yu
may be quoted; Yu's reply may not.

Write what was decided and when, with no quoted words:

    on Yu's word of 2026-11-17, the kernel is removed

If the words are already public (cite the public file in the message), let
them through with YOUSPEAK_OWNER_WORDS_ARE_PUBLIC=1.

    python3 script/tools/check_commit_message.py <message-file>

Exit status 1 when the message is refused, 0 otherwise. .githooks/commit-msg
runs it. Added 2026-11-17 by an agent session, after it had pushed such
messages itself.
"""
import os
import re
import sys

OPEN, CLOSE = "\"“", "\"”"
NAME = r"(?:Yu's|Yu|the owner's|the owner)"
SPEECH = (r"(?:said|says|say|answered|answers|answer(?: was)?|replied|reply(?: was| said)?|wrote|told|"
          r"word(?: was)?|words(?: were)?|message(?: said| included| held)?|decided|chose|:)")
# the name, then within the sentence a word of speech, then a quotation
QUOTED = re.compile(
    rf"(?<![A-Za-z0-9]){NAME}(?![A-Za-z0-9])[^.{OPEN}{CLOSE}]{{0,120}}?{SPEECH}[^.{OPEN}{CLOSE}]{{0,80}}?"
    rf"[{OPEN}]([^{OPEN}{CLOSE}]+)[{CLOSE}]")
# an agent's own question or recommendation, put to Yu, is the agent's to quote
OWN_QUESTION = re.compile(
    rf"(?:asked|asking|put to|recommended to|reported to|told)\s+{NAME}[^.{OPEN}{CLOSE}]{{0,80}}?"
    rf"[{OPEN}][^{OPEN}{CLOSE}]+[{CLOSE}]")


def quotations(message):
    """The quoted spans (two words or more) that the message attributes to Yu."""
    body = "\n".join(l for l in message.splitlines() if not l.startswith("#"))
    flat = re.sub(r"\s*\n\s*>?\s*", " ", body)          # wrapped lines and block quotes read as one line
    flat = re.sub(r"(\d)\.(\d)", r"\1·\2", flat)        # a decimal point does not end a sentence
    flat = OWN_QUESTION.sub(" ", flat)
    return [m.group(1).strip() for m in QUOTED.finditer(flat) if len(m.group(1).split()) >= 2]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    if os.environ.get("YOUSPEAK_OWNER_WORDS_ARE_PUBLIC") == "1":
        return 0
    with open(argv[0], encoding="utf-8", errors="replace") as fh:
        found = quotations(fh.read())
    if not found:
        return 0
    print("[cathedral] this commit message seems to quote Yu's words; commit blocked.", file=sys.stderr)
    print("  A pushed message cannot be taken back, and Yu's private words are Yu's to publish.", file=sys.stderr)
    print("  Say what was decided and when, with no quoted words: on Yu's word of <date>, ...", file=sys.stderr)
    print("  If the words are already public, cite the file and run again with", file=sys.stderr)
    print("  YOUSPEAK_OWNER_WORDS_ARE_PUBLIC=1.", file=sys.stderr)
    for q in found:
        print(f"  quoted: {q[:60]}{'...' if len(q) > 60 else ''}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
