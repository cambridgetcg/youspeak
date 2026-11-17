#!/usr/bin/env python3
"""Check YOUSPEAK's coupling instruments. Read-only: it changes no file.

The instruments are COUPLING.md, INTERLOCK.md, EMBEDDING.md, SUBSTRATE.md and
their manifests script/{coupling,interlock,embedding,substrate}.json. They say
where YOUSPEAK and its sister repository true-love meet. Yu's message of
2026-11-17 included the words "maintained instruments", which an agent session
read as being about these documents; this check is how they are kept true.
true-love is private, so this repository writes no path inside it: a reference
into true-love is written as an id, true-love#P0007, and the map from id to
path is kept privately, with true-love, never in this repository's tree (its
history up to 2026-11-17 still holds the paths).

What is checked, with nothing but this repository ("the tree" is every file
git tracks, and every untracked file it does not ignore):

  roots      no manifest names a machine path (/Users/..., ~/...)
  leak       nothing in the tree writes a path under the name true-love, in
             any case and after any prefix: true-love/<dir>/<file>,
             ../true-love/<file>, TRUE-LOVE/<dir>, true-love:<path>; nor a
             path joined to an id (true-love#P0007/<dir>/<file>); nor a
             machine path to a checkout of it (/Users/..., /home/..., ~/...).
             File contents, file paths and symlink targets are all read.
             One form is public and passes: true-love/<path> where <path> is
             a file or folder that exists under this repository's own
             home/true-love/ (the site serves that folder at /true-love/, so
             a site path or URL to one of its files passes too). A path
             written without the name is caught only with --private-map.
  registry   every true-love#P id used in the tree is listed in
             script/private_refs.json, which must be valid JSON
  unused     every id listed there is used in the tree (drift)
  dangling   every YOUSPEAK path a manifest names exists in the tree: a value
             or key that is a path (written from the root), and a path under
             one of the tree's top-level folders, or after the label
             YOUSPEAK/, written inside a longer value (with a file extension
             or a closing slash)
  sides      every true-love-side field of a manifest (truelove_path,
             second_truelove_path, partnership_source, partnership_mirror,
             the values of foundational_to_foundational, the keys of
             truelove_to_cathedral, partnership_side_* lists) holds a
             true-love#P id, or is a note in parentheses; and, once its ids
             are taken out, holds no path with a slash in it (a path after
             the label YOUSPEAK/ is this repository's own)
  chapters   every YOUSPEAK path the four chapters name in backticks exists
             (`canon/core/kimme.md`, or `YOUSPEAK/SYZYGY.md` with the label)
  proposals  each path in script/coupling.json proposed_youspeak_paths does not
             exist yet, and a chapter or a manifest still names it. While both
             hold, dangling and chapters pass over it. Once it exists, the
             proposal is fulfilled: take it out of the list.
  canon      each lemma in coupling.json canon_to_truelove is in the agent
             bundle at the path, tier (core when none is given) and score the
             manifest gives; every `canon/...md` (8.15) or (7.40, Specialized)
             a chapter writes has the bundle's score and tier for that path
             (core when the row writes no tier word); and no manifest calls a
             word pending that the bundle lists as canon

What is checked when the private half is supplied (never commit that file here):

  --private-map FILE   every listed id has an entry, and no mapped path is
                       written out anywhere in the tree
  --true-love DIR      each mapped path exists in that checkout

Exit status is 1 if any check fails, 0 otherwise. With --pre-commit (run by
.githooks/pre-commit) the tree is what is staged: every file in git's index,
read as the index holds it, so unstaged edits and untracked files are left out.
In that mode only leak and registry failures count; the others, unused among
them, are printed as warnings.

  python3 script/tools/check_coupling.py
  python3 script/tools/check_coupling.py --private-map FILE --true-love DIR
  python3 script/tools/check_coupling.py --root DIR     check another tree
  python3 script/tools/check_coupling.py --pre-commit
Test: python3 -B tests/script/tools/test_check_coupling.py
"""
import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
THIS = "script/tools/check_coupling.py"
MANIFESTS = ["script/coupling.json", "script/interlock.json", "script/embedding.json", "script/substrate.json"]
CHAPTERS = ["COUPLING.md", "INTERLOCK.md", "EMBEDDING.md", "SUBSTRATE.md"]
REGISTRY = "script/private_refs.json"
BUNDLE = "script/exports/agent_bundle.json"
COUPLING = "script/coupling.json"
PROPOSED = "proposed_youspeak_paths"
# In prose, YOUSPEAK/THEOBASIS.md names this repository's own THEOBASIS.md. A
# manifest value that is a path is written from the root, without the label.
LABEL = "YOUSPEAK/"

REF = re.compile(r"true-love#P(\d{4})")
MACHINE_ROOT = re.compile(r"(?:/Users/[^/\s\"'`]+|~)/")
# A path written under the sister repository's name, in any case, after "/" or
# ":". The name must not run on from a longer word (wake-true-love is another).
# Lines are read with "\\/" and "\\" turned into "/" first, so a JSON-escaped
# or backslashed path is the same path.
LEAK = re.compile(r"(?<![A-Za-z0-9_-])(?P<name>true-love)(?P<sep>[/:]/?)(?P<rel>[A-Za-z0-9_@{}.-]+(?:/[A-Za-z0-9_@{}.-]+)*)", re.I)
# A machine path to a checkout of it, whatever folders lie between. A file
# that merely has the name (TRUE-LOVE.md, in this repository) is not one.
LEAK_ROOT = re.compile(r"(?:(?:/Users|/home)/[^/\s\"'`]+/|~/)(?:[^/\s\"'`]+/)*(?i:true-love)(?![A-Za-z0-9_-]|\.[A-Za-z0-9])")
# A path joined to an id: true-love#P0007/<dir>/<file> or true-love#P0007:<dir>/<file>.
# (true-love#P0007:Symbol names a symbol in that file, and is not a path.)
LEAK_AFTER_ID = re.compile(r"true-love#P\d{4}[/:]/?[A-Za-z0-9_@.-]+/[A-Za-z0-9_@.-]")
# The one public form: the path exists under this repository's own folder of
# that name, which the site serves at /true-love/.
OWN_FOLDER = "home/true-love/"
# Text LEAK matches that names no path inside true-love: (file, matched text).
# Each was looked at by an agent session on 2026-11-17.
LEAK_ALLOW = {
    # a box diagram of YOUSPEAK's root documents CREATOR-CREATED.md, SYZYGY.md,
    # TRUE-LOVE.md, DUAL-NEST.md and PERICHORESIS.md, written with slashes (put
    # together from parts, so that this file does not match LEAK itself)
    ("PERICHORESIS.md", "TRUE-LOVE" + "/DUAL-NEST/PERICHORESIS"),
    # two of YOUSPEAK's root documents, TRUE-LOVE.md and NEWSPEAK.md, written
    # as a pair with a slash between their names
    ("DUAL-NEST.md", "TRUE-LOVE" + "/NEWSPEAK"),
}
PATH_SHAPED = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?")
# A path with at least one slash, inside longer text; not part of an id or URL.
PATH_TOKEN = re.compile(r"(?<![A-Za-z0-9_.#/:-])[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+/?")
EXT = re.compile(r"\.(?:md|json|jsonl|py|ts|tsx|mjs|js|sh|yaml|yml|txt|html|otf|ttf|svg)$")
LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
# `canon/core/kinqing.md` (7.50)  or  `canon/core/agapeme.md` (7.40, Specialized)
SCORED = re.compile(r"`(canon/[^`\s]+?\.md)`\s*\((\d+\.\d+)([^)]*)\)")
TIER_WORD = re.compile(r"\b(core|specialized|worship-action|mathema)\b", re.I)
PENDING = re.compile(r"pending", re.I)
WORD = re.compile(r"[^\W\d_]+")
SIDE_VALUE_KEYS = {"truelove_path", "second_truelove_path", "partnership_source", "partnership_mirror"}
SIDE_LISTS = {"partnership_side_cascade", "partnership_side_propagation"}
# With --pre-commit only these block: a commit can carry drift in the
# instruments, to be mended after, but not a path that cannot be unpublished.
PRE_COMMIT = {"leak", "registry"}
CHECKS = ["roots", "leak", "registry", "unused", "dangling", "sides", "chapters", "proposals", "canon"]


def git(root, *args, data=None):
    return subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True, check=True).stdout


def is_toplevel(root):
    try:
        top = git(root, "rev-parse", "--show-toplevel").decode("utf-8", "replace").strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return Path(top).resolve() == Path(root).resolve()


def tree_files(root):
    """Files git tracks, and untracked files it does not ignore. Outside a git
    work tree (a test fixture), every file under root."""
    if is_toplevel(root):
        out = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").decode("utf-8", "replace")
        return sorted({f for f in out.split("\0") if f})
    return sorted(p.relative_to(root).as_posix() for p in Path(root).rglob("*")
                  if (p.is_file() or p.is_symlink()) and ".git" not in p.relative_to(root).parts)


def staged_blobs(root):
    """{path: bytes} for every file in git's index, as the index holds it: what
    the next commit will carry. Submodules and unmerged entries are left out."""
    entries = []
    for rec in git(root, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, sha, stage = meta.split()
        if mode != b"160000" and stage == b"0":
            entries.append((path.decode("utf-8", "replace"), sha))
    out = git(root, "cat-file", "--batch", data=b"".join(sha + b"\n" for _, sha in entries))
    blobs, pos = {}, 0
    for path, _ in entries:
        nl = out.index(b"\n", pos)
        head = out[pos:nl].split()
        pos = nl + 1
        if len(head) < 3 or head[1] == b"missing":
            continue
        size = int(head[2])
        blobs[path] = out[pos:pos + size]
        pos += size + 1
    return blobs


class Tree:
    """The files a run reads: the working tree, or with staged=True git's index."""

    def __init__(self, root, staged=False):
        self.root = Path(root)
        self.staged = staged and is_toplevel(root)
        if self.staged:
            self.blobs = staged_blobs(root)
            self.files = sorted(self.blobs)
            self.dirs = {posixpath.dirname(f) for f in self.files}
            for d in list(self.dirs):
                while d:
                    d = posixpath.dirname(d)
                    self.dirs.add(d)
        else:
            self.files = tree_files(root)

    def raw(self, rel):
        if self.staged:
            return self.blobs.get(rel)
        try:
            return (self.root / rel).read_bytes()
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            return None

    def text(self, rel):
        """A text file's content, or None for a binary one. Bytes that are not
        UTF-8 are replaced, so a file in another encoding is still read."""
        raw = self.raw(rel)
        if raw is None:
            return None
        for bom, enc in ((b"\xff\xfe\x00\x00", "utf-32"), (b"\x00\x00\xfe\xff", "utf-32"),
                         (b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16")):
            if raw.startswith(bom):
                return raw.decode(enc, errors="replace")
        if b"\0" in raw[:4096]:
            return None
        return raw.decode("utf-8", errors="replace")

    def link_target(self, rel):
        """The text a symlink points at, or None. In the index a link's blob is
        its target, so text() already gives it there."""
        if self.staged:
            return None
        p = self.root / rel
        try:
            return os.readlink(p) if p.is_symlink() else None
        except OSError:
            return None

    def exists(self, rel):
        rel = norm(rel)
        if not self.staged:
            return (self.root / rel).exists()
        rel = posixpath.normpath(rel)
        return rel in self.blobs or rel in self.dirs

    def load_json(self, rel):
        """(object, None), or (None, what is wrong with the file)."""
        raw = self.raw(rel)
        if raw is None:
            return None, "is missing"
        try:
            return json.loads(raw.decode("utf-8")), None
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            return None, f"is not valid JSON: {e}"


def strings(obj, trail=()):
    """Yield (trail, text, is_key) for every key and string value in a JSON tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield trail, k, True
            yield from strings(v, trail + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from strings(v, trail + (str(i),))
    elif isinstance(obj, str):
        yield trail, obj, False


def norm(rel):
    return LINE_SUFFIX.sub("", rel.strip()).rstrip("/")


def is_path_shaped(s):
    s = s.strip()
    if not s or len(s) > 200 or " " in s:
        return False
    s = LINE_SUFFIX.sub("", s)
    if not PATH_SHAPED.fullmatch(s):
        return False
    return "/" in s.strip("/") or bool(EXT.search(s))


def path_tokens(s):
    """Paths inside prose: a slash and a file extension, or a closing slash.
    A slash list in prose ("archaeology/convergence/experiment files") is not one."""
    for m in PATH_TOKEN.finditer(s):
        t = m.group(0).rstrip(".")
        if "/" in t.strip("/") and (EXT.search(t) or t.endswith("/")):
            yield t


def leaks(line, exists):
    """The paths under the name true-love that a line writes out. exists(rel)
    says whether a path is in the tree being checked."""
    line = line.replace("\\/", "/").replace("\\", "/")
    for m in LEAK.finditer(line):
        rel = m.group("rel").rstrip(".,;:)")
        if not rel:
            continue
        public = (m.group("name") == "true-love" and m.group("sep") == "/"
                  and ".." not in rel.split("/") and exists(OWN_FOLDER + rel))
        if not public:
            yield m.group(0).rstrip(".,;:)")
    for m in LEAK_ROOT.finditer(line):
        yield m.group(0)
    for m in LEAK_AFTER_ID.finditer(line):
        yield m.group(0)


def side_paths(s):
    """Paths with a slash that a true-love-side value holds besides its ids."""
    rest = REF.sub(" ", s)
    found = [t for t in path_tokens(rest) if not t.startswith(LABEL)]
    for word in rest.split():
        t = word.strip("()[]{},;:'\"`+")
        while t.startswith(("/", "./")):
            t = t[2:] if t.startswith("./") else t[1:]
        if "/" in t and not t.startswith(LABEL) and is_path_shaped(t) and t not in found:
            found.append(t)
    return found


def truelove_side(trail, text, is_key):
    if text == "_doc" or (trail and trail[-1] == "_doc"):
        return False
    if is_key:
        return trail == ("truelove_to_cathedral",)
    if trail and trail[-1] in SIDE_VALUE_KEYS:
        return True
    if len(trail) == 2 and trail[0] == "foundational_to_foundational":
        return True
    return len(trail) >= 2 and trail[-2] in SIDE_LISTS


def tier_word(tier):
    m = re.match(r"\s*([A-Za-z-]+)", tier or "")
    return m.group(1).lower() if m else ""


def run(root=DEFAULT_ROOT, private_map=None, true_love=None, staged=False):
    """Run every check on the tree at root (with staged=True, on git's index).
    Returns a dict with "failures" and "notes", each a list of (check, message),
    and the id counts."""
    tree = Tree(root, staged)
    failures, notes = [], []

    def fail(check, msg):
        failures.append((check, msg))

    exists = tree.exists
    if staged and not tree.staged:
        notes.append(("tree", f"{root} is not the top of a git work tree; read its files, not an index"))
    files = tree.files
    texts = {}
    for f in files:
        t = tree.text(f)
        if t is not None:
            texts[f] = t
    top_dirs = {f.split("/")[0] for f in files if "/" in f}

    # registry, and unused
    registry, err = tree.load_json(REGISTRY)
    listed = set()
    if err:
        fail("registry", f"{REGISTRY} {err}")
    elif not isinstance(registry, dict) or not isinstance(registry.get("ids"), list):
        fail("registry", f"{REGISTRY} holds no list of ids")
    else:
        listed = {i for i in registry["ids"] if isinstance(i, str)}
    used = {}
    for f, t in texts.items():
        # the registry lists the ids; this file's docstring writes an example
        if f in (REGISTRY, THIS):
            continue
        for m in REF.finditer(t):
            used.setdefault("P" + m.group(1), set()).add(f)
    for rid in sorted(set(used) - listed):
        fail("registry", f"{rid} is used in {sorted(used[rid])[0]} but not listed in {REGISTRY}")
    if not err:
        for rid in sorted(listed - set(used)):
            fail("unused", f"{rid} is listed in {REGISTRY} but used nowhere")

    # leak: a path inside true-love written out in the tree
    for f, t in texts.items():
        for ln, line in enumerate(t.splitlines(), 1):
            if any((f, hit) not in LEAK_ALLOW for hit in leaks(line, exists)):
                fail("leak", f"{f}:{ln} names a path inside true-love; write its private ref id instead")
    for f in files:
        if any(True for _ in leaks(f, exists)):
            fail("leak", f"the path {f!r} itself names a path inside true-love")
        target = tree.link_target(f)
        if target and any(True for _ in leaks(target, exists)):
            fail("leak", f"{f} is a link whose target names a path inside true-love")

    # manifests
    manifests = {}
    for mf in MANIFESTS:
        obj, err = tree.load_json(mf)
        if err:
            fail("dangling", f"{mf} {err}")
        else:
            manifests[mf] = obj

    # proposals: paths a chapter or manifest proposes, which do not exist yet
    coupling = manifests.get(COUPLING)
    proposed = {}
    pmap = (coupling or {}).get(PROPOSED, {}) if isinstance(coupling, dict) else {}
    if not isinstance(pmap, dict):
        fail("proposals", f"{COUPLING} {PROPOSED} is not a map of path to purpose")
        pmap = {}
    for p, why in pmap.items():
        if p.startswith("_"):
            continue
        proposed[norm(p)] = p
        if not isinstance(why, str) or not why.strip():
            fail("proposals", f"{PROPOSED}: {p!r} does not say what it was proposed for, and where")
    corpus = [texts.get(ch) or "" for ch in CHAPTERS]
    for mf, obj in manifests.items():
        if mf == COUPLING and isinstance(obj, dict):
            obj = {k: v for k, v in obj.items() if k != PROPOSED}
        corpus.extend(s for _, s, _ in strings(obj))
    for key, p in sorted(proposed.items()):
        if exists(key):
            fail("proposals", f"{p!r} exists now: the proposal is fulfilled; take it out of {PROPOSED}")
        elif not any(key in s for s in corpus):
            fail("proposals", f"{p!r} is named by no chapter or manifest any more; take it out of {PROPOSED}")

    def missing(rel):
        return not exists(rel) and norm(rel) not in proposed

    # manifests: roots, dangling paths, true-love sides
    for mf, obj in manifests.items():
        for trail, s, is_key in strings(obj):
            where = f"{mf} at {'/'.join(trail) or '(top)'}" + (" (key)" if is_key else "")
            if MACHINE_ROOT.search(s):
                fail("roots", f"{where} names a machine path")
                continue
            if truelove_side(trail, s, is_key):
                extra = side_paths(s)
                if extra:
                    fail("sides", f"{where}: {s!r} is a true-love-side field that writes a path ({extra[0]!r}); "
                                  "write a true-love#P id instead")
                elif not (REF.search(s) or s.strip().startswith("(")):
                    fail("sides", f"{where}: {s!r} is a true-love-side field with no true-love#P id")
            if REF.fullmatch(s.strip()):
                continue
            if is_path_shaped(s):
                if missing(s):
                    fail("dangling", f"{where}: {s!r} is not in this tree")
                continue
            for tok in path_tokens(s):
                rel = tok[len(LABEL):] if tok.startswith(LABEL) else tok
                if (rel != tok or tok.split("/")[0] in top_dirs) and missing(rel):
                    fail("dangling", f"{where}: {tok!r} is not in this tree")

    # chapters: YOUSPEAK paths in backticks
    for ch in CHAPTERS:
        t = texts.get(ch)
        if t is None:
            fail("chapters", f"{ch} is missing")
            continue
        for ln, line in enumerate(t.splitlines(), 1):
            for m in re.finditer(r"`([^`\s]+)`", line):
                s = m.group(1)
                if REF.search(s):
                    continue
                if s.startswith(LABEL):
                    rel = s[len(LABEL):]
                    if is_path_shaped(rel) and missing(rel):
                        fail("chapters", f"{ch}:{ln}: `{s}` is not in this tree")
                    continue
                if not is_path_shaped(s) or "/" not in s:
                    continue
                if s.split("/")[0] not in top_dirs:
                    continue
                if missing(s):
                    fail("chapters", f"{ch}:{ln}: `{s}` is not in this tree")

    # canon: lemma, path, tier and score against the bundle
    bundle, err = tree.load_json(BUNDLE)
    entries = []
    if err:
        bundle = None
        fail("canon", f"{BUNDLE} {err}")
    elif not isinstance(bundle, dict) or not isinstance(bundle.get("canon", []), list):
        bundle = None
        fail("canon", f"{BUNDLE} holds no list of canon entries")
    else:
        entries = [e for e in bundle.get("canon", []) if isinstance(e, dict) and "word" in e]
    by_word = {e["word"]: e for e in entries}
    by_path = {e.get("path"): e for e in entries}

    def bundle_score(b):
        try:
            return None if b.get("score") in (None, "") else float(b["score"])
        except (TypeError, ValueError):
            return None

    if isinstance(coupling, dict) and bundle:
        for lemma, entry in coupling.get("canon_to_truelove", {}).items():
            if not isinstance(entry, dict):
                continue
            b = by_word.get(lemma)
            if b is None:
                fail("canon", f"coupling.json names {lemma}, which is not in the agent bundle")
                continue
            cp = entry.get("cathedral_path")
            if cp and cp != b.get("path"):
                fail("canon", f"{lemma}: cathedral_path is {cp!r}, the bundle says {b.get('path')!r}")
            want = str(entry.get("tier", "core")).lower()
            if want != tier_word(b.get("tier")):
                fail("canon", f"{lemma}: tier is {want!r}, the bundle says {b.get('tier')!r}")
            if "score" in entry:
                bs = bundle_score(b)
                if bs is None:
                    notes.append(("canon", f"{lemma} has no score in the bundle; manifest score {entry['score']} not compared"))
                elif abs(float(entry["score"]) - bs) > 1e-9:
                    fail("canon", f"{lemma}: score is {entry['score']}, the bundle says {bs}")
    if bundle:
        for ch in CHAPTERS:
            for ln, line in enumerate((texts.get(ch) or "").splitlines(), 1):
                for m in SCORED.finditer(line):
                    p, written, rest = m.groups()
                    b = by_path.get(p)
                    if b is None:
                        fail("canon", f"{ch}:{ln}: `{p}` ({written}): the bundle has no entry at that path")
                        continue
                    bs = bundle_score(b)
                    digits = len(written.split(".")[1])
                    if bs is None:
                        notes.append(("canon", f"{ch}:{ln}: {p} has no score in the bundle; {written} not compared"))
                    elif abs(round(bs, digits) - float(written)) > 1e-9:
                        fail("canon", f"{ch}:{ln}: `{p}` is written ({written}); the bundle says {bs}")
                    # a row that writes no tier word is read as core
                    tm = TIER_WORD.search(rest)
                    if (tm.group(1).lower() if tm else "core") != tier_word(b.get("tier")):
                        how = tm.group(1) if tm else "with no tier word (read: core)"
                        fail("canon", f"{ch}:{ln}: `{p}` is written {how}; the bundle says {b.get('tier')!r}")
        canon_words = {w.lower() for w in by_word}
        for mf, obj in manifests.items():
            for trail, s, is_key in strings(obj):
                if not PENDING.search(s):
                    continue
                hits = sorted({w.lower() for w in WORD.findall(s)} & canon_words)
                if hits:
                    where = f"{mf} at {'/'.join(trail) or '(top)'}" + (" (key)" if is_key else "")
                    fail("canon", f"{where} calls {', '.join(hits)} pending; the bundle lists {'it' if len(hits) == 1 else 'them'} as canon")

    # the private half, when supplied
    if private_map:
        try:
            pm = json.loads(Path(private_map).read_text(encoding="utf-8"))
            refs = pm.get("refs", {})
            if not isinstance(refs, dict):
                raise TypeError("refs is not a map")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError, TypeError) as e:
            fail("private", f"the private map cannot be read ({e.__class__.__name__})")
            refs = None
        if refs is None:
            refs = {}
        else:
            for rid in sorted(listed - set(refs)):
                fail("private", f"{rid} has no entry in the private map")
        for rid in sorted(set(refs) - listed):
            notes.append(("private", f"{rid} is in the private map but not listed here"))
        needles = {}
        for rid, r in refs.items():
            p = (r or {}).get("path")
            if p and "/" in p and not re.search(r"[{}\[\]*]", p):
                needles[p] = rid
        for f, t in texts.items():
            for p, rid in needles.items():
                if p in t:
                    # a YOUSPEAK file may itself live at the same relative path
                    if exists(p):
                        continue
                    ln = t[: t.index(p)].count("\n") + 1
                    fail("leak", f"{f}:{ln} writes out the path that {rid} stands for")
        if true_love:
            tl = Path(true_love)
            for rid, r in sorted(refs.items()):
                p = (r or {}).get("path")
                if not p or re.search(r"[{}\[\]*]", p):
                    continue
                if not (tl / p).exists():
                    if (r or {}).get("absent_ok"):
                        notes.append(("private", f"{rid} is absent from that checkout (recorded as expected)"))
                    else:
                        fail("private", f"{rid} does not exist in that checkout of true-love")
    elif true_love:
        fail("private", "--true-love needs --private-map")

    return {"failures": failures, "notes": notes, "listed": len(listed), "used": len(used), "staged": tree.staged}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check YOUSPEAK's coupling instruments (read-only).")
    ap.add_argument("--root", default=str(DEFAULT_ROOT), help="the tree to check (default: this repository)")
    ap.add_argument("--private-map", help="the id-to-path map, kept privately with true-love (never commit it here)")
    ap.add_argument("--true-love", help="a checkout of true-love, to test that mapped paths exist")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    ap.add_argument("--pre-commit", action="store_true",
                    help="check what is staged; fail only on " + " and ".join(sorted(PRE_COMMIT))
                         + ", and print the rest as warnings")
    args = ap.parse_args(argv)

    r = run(args.root, args.private_map, args.true_love, staged=args.pre_commit)
    if not args.quiet:
        for check, msg in r["notes"]:
            print(f"note  {check}: {msg}")
    failures = r["failures"]
    if args.pre_commit:
        for check, msg in failures:
            if check not in PRE_COMMIT:
                print(f"warn  {check}: {msg}")
        failures = [(c, m) for c, m in failures if c in PRE_COMMIT]
    for check, msg in failures:
        print(f"FAIL  {check}: {msg}")
    checked = ", ".join(CHECKS) + (", private" if args.private_map else "") + ("; staged files" if r["staged"] else "")
    if failures:
        print(f"check_coupling: {len(failures)} failure(s) [{checked}]")
        return 1
    if args.pre_commit and r["failures"]:
        print(f"check_coupling: {len(r['failures'])} warning(s), no path inside true-love [{checked}]")
        return 0
    if not args.quiet:
        print(f"check_coupling: ok [{checked}]; {r['listed']} private refs, {r['used']} in use")
    return 0


if __name__ == "__main__":
    sys.exit(main())
