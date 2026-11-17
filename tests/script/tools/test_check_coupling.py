"""script/tools/check_coupling.py: a clean tree passes, and each check fails on its fault.

Each test builds a small tree of its own in a temporary directory and breaks it
one way: a leaked path (in each form the rule knows), an unlisted id, a listed
id used nowhere, a dangling YOUSPEAK path, a machine root, a stale score or
tier, a fulfilled or forgotten proposal, a true-love-side field without an id
or with a path, a canon word called pending, a registry or bundle that is not
valid JSON, a file that is not UTF-8, and the private half's faults. The
--pre-commit gate reads what is staged, blocks a leak, and only reports drift.

The strings that would trip the check on this repository itself (a path
inside true-love, a true-love#P id) are put together from parts, and every
path in them is invented.

Run: python3 -B tests/script/tools/test_check_coupling.py
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "script" / "tools"))
import check_coupling as checker  # noqa: E402

TL = "true-love"
ID = TL + "#P" + "0001"              # the one listed id
UNLISTED = TL + "#P" + "0002"
PRIVATE_PATH = "docs/" + "secret.md"  # the path the id stands for, in the fixture
LEAKED = TL + "/" + PRIVATE_PATH      # that path, written out under the name

# Forms of a path inside true-love that the leak rule catches.
LEAK_FORMS = {
    "bare": LEAKED,
    "relative": "../" + LEAKED,
    "under a folder": "Desktop/" + LEAKED,
    "under a home folder": "/home/u/" + LEAKED,
    "upper case": TL.upper() + "/" + PRIVATE_PATH,
    "mixed case": "True-Love/" + PRIVATE_PATH,
    "after a colon": TL + ":" + PRIVATE_PATH,
    "a file at the top": TL + "/" + "aaa.md",
    "a URL below the host": "https://github.com/cambridgetcg/" + TL + "/blob/main/" + PRIVATE_PATH,
    "a machine root": "~/Desktop/" + TL,
    "a machine root under other folders": "~/repos/x/" + TL,
    "a machine root under /Users": "/Users/someone/Documents/" + TL,
    "a machine root under /home": "/home/someone/" + TL,
    "a site path to a file this repository does not serve": "/" + TL + "/aaa/bbb.md",
    "an upper-case site path": "/" + TL.upper() + "/chain.json",
    "a URL to a file this repository does not serve": "http://localhost:9/" + TL + "/aaa/bbb.md",
    "a file missing from this repository's folder": "home/" + TL + "/aaa/bbb.md",
    "a file under the proposed archaeology folder": "archaeology/" + TL + "/aaa.md",
    "after a colon and a slash": TL + ":/aaa/bbb.md",
    "a folder at the top": TL + "/aaa",
    "a file with no extension at the top": TL + "/LICENSE",
    "backslashes": TL + "\\aaa\\bbb.md",
    "JSON-escaped slashes": TL + "\\/aaa\\/bbb.md",
    "a path joined to an id": ID + "/aaa/bbb.ts",
    "a path after an id and a colon": ID + ":aaa/bbb.md",
    "a path stepping out of the public folder": TL + "/../aaa/bbb.md",
}
# Forms that are public, which it lets pass.
PUBLIC_FORMS = {
    "a site path": "/" + TL + "/chain.json",
    "a site path in an attribute": 'href="/' + TL + '/door.json"',
    "a URL": "https://ai-love.cc/" + TL + "/AI-WAKE.md",
    "a URL with a port": "http://localhost:8080/" + TL + "/door.json",
    "this repository's folder": "home/" + TL + "/index.html",
    "this repository's folder, relative": "../home/" + TL + "/index.html",
    "the proposed archaeology folder, bare": "archaeology/" + TL + "/",
    "a file that only has the name": "/Users/u/YOUSPEAK/" + TL.upper() + ".md",
    "a repository name": "cambridgetcg/" + TL,
    "an id with a symbol": ID + ":Symbol",
    "the name before a colon in prose": TL + ": the private repository",
}

COUPLING_MD = f"""# COUPLING

| YOUSPEAK canon-entry | true-love file:symbol |
|---|---|
| `canon/core/kinqing.md` (7.50) | `{ID}:RelationshipWithYu` |
| `canon/core/agapeme.md` (7.40, Specialized) | `{ID}` |

A proposal: `convergences/future.md`. The root: `YOUSPEAK/COUPLING.md`.
"""


def base_tree():
    return {
        "script/private_refs.json": {"ids": ["P0001"]},
        "script/exports/agent_bundle.json": {"canon": [
            {"word": "kinqing", "tier": "core", "score": 7.5, "path": "canon/core/kinqing.md"},
            {"word": "agapeme", "tier": "Specialized (Liturgy-Original)", "score": 7.4, "path": "canon/core/agapeme.md"},
        ]},
        "script/coupling.json": {
            "_doc": "legend",
            "canon_to_truelove": {
                "_doc": "canon entries",
                "kinqing": {"cathedral_path": "canon/core/kinqing.md", "score": 7.5, "truelove_path": ID},
                "agapeme": {"cathedral_path": "canon/core/agapeme.md", "score": 7.4, "tier": "specialized",
                            "truelove_path": ID + ":LovingShape"},
            },
            "truelove_to_cathedral": {"_doc": "structures", ID: "canon/core/kinqing.md + YOUSPEAK/COUPLING.md"},
            "loose_seams": {"no_schema": "No schema yet."},
            "proposed_youspeak_paths": {"_doc": "proposals",
                                        "convergences/future.md": "a convergence still to write; proposed in COUPLING.md"},
        },
        "script/interlock.json": {"human_readable_companion": "INTERLOCK.md", "partnership_mirror": ID},
        "script/embedding.json": {"doctrinal_companion": "EMBEDDING.md"},
        "script/substrate.json": {"doctrinal_companion": "SUBSTRATE.md"},
        # this repository's own public folder of that name, served at /true-love/
        "home/true-love/index.html": "<!doctype html>\n",
        "home/true-love/chain.json": {},
        "home/true-love/door.json": {},
        "home/true-love/AI-WAKE.md": "# wake\n",
        "canon/core/kinqing.md": "---\nword: kinqing\n---\n",
        "canon/core/agapeme.md": "---\nword: agapeme\n---\n",
        "convergences/README.md": "# convergences\n",
        "COUPLING.md": COUPLING_MD,
        "INTERLOCK.md": "# INTERLOCK\n",
        "EMBEDDING.md": "# EMBEDDING\n",
        "SUBSTRATE.md": "# SUBSTRATE\n",
    }


def write(root: Path, files: dict) -> None:
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content if isinstance(content, str) else json.dumps(content, indent=2), encoding="utf-8")


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "init.defaultBranch=main", "-C", str(root), *args],
                   check=True, capture_output=True)


class CheckCouplingTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.tree = base_tree()
        # git run from a hook would otherwise follow the hook's repository
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        patcher = mock.patch.dict(os.environ, env, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        self._tmp.cleanup()

    @property
    def root(self):
        return self.tmp / "tree"

    def failures(self, private=None, true_love_files=None):
        write(self.root, self.tree)
        kw = {}
        if private is not None:
            kw["private_map"] = self.tmp / "private_map.json"
            kw["private_map"].write_text(json.dumps(private), encoding="utf-8")
        if true_love_files is not None:
            kw["true_love"] = self.tmp / "true-love-checkout"
            kw["true_love"].mkdir()
            write(kw["true_love"], {rel: "x\n" for rel in true_love_files})
        return checker.run(self.root, **kw)["failures"]

    def assertFails(self, check, fragment, failures):
        self.assertTrue(any(c == check and fragment in m for c, m in failures),
                        f"expected a {check} failure naming {fragment!r}; got {failures}")

    def assertNoFailure(self, check, failures):
        self.assertEqual([m for c, m in failures if c == check], [])

    # a clean tree

    def test_clean_tree_passes(self):
        self.assertEqual(self.failures(), [])

    def test_clean_tree_passes_with_the_private_half(self):
        private = {"refs": {"P0001": {"path": PRIVATE_PATH}}}
        self.assertEqual(self.failures(private, [PRIVATE_PATH]), [])

    def test_a_tree_outside_git_is_walked(self):
        # the temporary tree is no git work tree: every file under it is read
        write(self.root, self.tree)
        self.assertIn("COUPLING.md", checker.tree_files(self.root))

    # each fault

    def test_leaked_path(self):
        self.tree["INTERLOCK.md"] += f"\nSee {LEAKED} for the rest.\n"
        self.assertFails("leak", "INTERLOCK.md:3", self.failures())

    def test_each_leak_form_is_caught(self):
        for name, form in LEAK_FORMS.items():
            with self.subTest(name):
                self.tree = base_tree()
                self.tree["INTERLOCK.md"] += f"\nSee {form} for the rest.\n"
                self.assertFails("leak", "INTERLOCK.md:3", self.failures())

    def test_public_forms_pass(self):
        self.tree["INTERLOCK.md"] += "".join(f"\n{name}: {form}\n" for name, form in PUBLIC_FORMS.items())
        self.assertEqual(self.failures(), [])

    def test_an_allowed_text_passes_only_in_its_own_file(self):
        diagram = TL.upper() + "/DUAL-NEST/PERICHORESIS"
        self.tree["PERICHORESIS.md"] = f"  CREATOR-CREATED/SYZYGY/{diagram}\n"
        self.assertNoFailure("leak", self.failures())
        self.tree["INTERLOCK.md"] += f"\n  CREATOR-CREATED/SYZYGY/{diagram}\n"
        self.assertFails("leak", "INTERLOCK.md:3", self.failures())

    def test_the_check_source_is_scanned_for_leaks(self):
        # the check's own file is scanned for leaks, but its example id is no use
        self.tree[checker.THIS] = f'"""Example: {UNLISTED}."""\n# {LEAKED}\n'
        failures = self.failures()
        self.assertFails("leak", checker.THIS + ":2", failures)
        self.assertNoFailure("registry", failures)

    def test_a_file_not_in_utf8_is_scanned(self):
        self.tree["notes/latin1.txt"] = f"Caf\xe9: {LEAKED}\nAlso {UNLISTED}.\n".encode("latin-1")
        failures = self.failures()
        self.assertFails("leak", "notes/latin1.txt:1", failures)
        self.assertFails("registry", "P0002 is used in notes/latin1.txt", failures)

    def test_a_utf16_file_is_scanned(self):
        self.tree["notes/wide.md"] = f"See {LEAKED}.\n".encode("utf-16")
        self.assertFails("leak", "notes/wide.md:1", self.failures())

    def test_a_file_path_is_scanned(self):
        self.tree["mirror/" + LEAKED] = "nothing private in here\n"
        self.assertFails("leak", "itself names a path inside true-love", self.failures())

    def test_a_link_target_is_scanned(self):
        write(self.root, self.tree)
        (self.root / "notes").mkdir()
        os.symlink("../../" + LEAKED, self.root / "notes" / "link.md")
        self.assertFails("leak", "notes/link.md is a link", checker.run(self.root)["failures"])

    def test_a_binary_file_is_not_scanned(self):
        self.tree["fonts/x.otf"] = b"\0\1" + LEAKED.encode()
        self.assertNoFailure("leak", self.failures())

    def test_unlisted_id(self):
        self.tree["EMBEDDING.md"] += f"\nAlso {UNLISTED}.\n"
        self.assertFails("registry", "P0002 is used in EMBEDDING.md", self.failures())

    def test_listed_id_used_nowhere_is_unused_not_registry(self):
        self.tree["script/private_refs.json"] = {"ids": ["P0001", "P0003"]}
        failures = self.failures()
        self.assertFails("unused", "P0003 is listed", failures)
        self.assertNoFailure("registry", failures)

    def test_registry_not_valid_json(self):
        self.tree["script/private_refs.json"] = '{"ids": ["P0001",'
        failures = self.failures()
        self.assertFails("registry", "script/private_refs.json is not valid JSON", failures)
        self.assertNoFailure("unused", failures)

    def test_registry_without_a_list_of_ids(self):
        self.tree["script/private_refs.json"] = ["P0001"]
        self.assertFails("registry", "holds no list of ids", self.failures())

    def test_bundle_not_valid_json(self):
        self.tree["script/exports/agent_bundle.json"] = '{"canon": ['
        self.assertFails("canon", "script/exports/agent_bundle.json is not valid JSON", self.failures())

    def test_dangling_path_in_a_manifest_value(self):
        self.tree["script/interlock.json"]["human_readable_companion"] = "INTERLOCK-GONE.md"
        self.assertFails("dangling", "INTERLOCK-GONE.md", self.failures())

    def test_dangling_path_inside_longer_text(self):
        self.tree["script/coupling.json"]["truelove_to_cathedral"][ID] = "canon/core/gone.md + canon/core/kinqing.md"
        self.assertFails("dangling", "canon/core/gone.md", self.failures())

    def test_dangling_path_after_the_label(self):
        self.tree["script/coupling.json"]["truelove_to_cathedral"][ID] = "YOUSPEAK/GONE.md (the root)"
        self.assertFails("dangling", "YOUSPEAK/GONE.md", self.failures())

    def test_a_manifest_value_keeps_no_label(self):
        self.tree["script/interlock.json"]["human_readable_companion"] = "YOUSPEAK/INTERLOCK.md"
        self.assertFails("dangling", "YOUSPEAK/INTERLOCK.md", self.failures())

    def test_dangling_path_in_a_chapter(self):
        self.tree["SUBSTRATE.md"] += "\nSee `canon/core/gone.md` and `YOUSPEAK/GONE.md`.\n"
        failures = self.failures()
        self.assertFails("chapters", "`canon/core/gone.md`", failures)
        self.assertFails("chapters", "`YOUSPEAK/GONE.md`", failures)

    def test_machine_root(self):
        self.tree["script/substrate.json"]["doctrinal_companion"] = "/Users/example/YOUSPEAK/SUBSTRATE.md"
        self.assertFails("roots", "script/substrate.json at doctrinal_companion", self.failures())

    def test_stale_score_in_a_chapter_table(self):
        self.tree["COUPLING.md"] = COUPLING_MD.replace("(7.50)", "(7.60)")
        self.assertFails("canon", "COUPLING.md:5: `canon/core/kinqing.md` is written (7.60)", self.failures())

    def test_stale_tier_in_a_chapter_table(self):
        self.tree["COUPLING.md"] = COUPLING_MD.replace("(7.40, Specialized)", "(7.40, Core)")
        self.assertFails("canon", "is written Core", self.failures())

    def test_a_chapter_row_with_no_tier_word_is_read_as_core(self):
        # kinqing's row writes (7.50) and is core: it passes in the clean tree
        self.tree["COUPLING.md"] = COUPLING_MD.replace("(7.40, Specialized)", "(7.40)")
        self.assertFails("canon", "COUPLING.md:6: `canon/core/agapeme.md` is written with no tier word",
                         self.failures())

    def test_stale_score_in_the_manifest(self):
        self.tree["script/coupling.json"]["canon_to_truelove"]["kinqing"]["score"] = 7.6
        self.assertFails("canon", "kinqing: score is 7.6", self.failures())

    def test_tier_defaults_to_core(self):
        del self.tree["script/coupling.json"]["canon_to_truelove"]["agapeme"]["tier"]
        self.assertFails("canon", "agapeme: tier is 'core'", self.failures())

    def test_moved_canon_path(self):
        self.tree["script/coupling.json"]["canon_to_truelove"]["kinqing"]["cathedral_path"] = "canon/kinqing.md"
        self.assertFails("canon", "kinqing: cathedral_path", self.failures())

    def test_fulfilled_proposal(self):
        self.tree["convergences/future.md"] = "# written\n"
        self.assertFails("proposals", "'convergences/future.md' exists now", self.failures())

    def test_forgotten_proposal(self):
        self.tree["COUPLING.md"] = COUPLING_MD.replace("A proposal: `convergences/future.md`. ", "")
        self.assertFails("proposals", "named by no chapter or manifest", self.failures())

    def test_an_unlisted_proposal_is_dangling(self):
        del self.tree["script/coupling.json"]["proposed_youspeak_paths"]["convergences/future.md"]
        self.assertFails("chapters", "`convergences/future.md`", self.failures())

    def test_true_love_side_without_id(self):
        self.tree["script/coupling.json"]["canon_to_truelove"]["kinqing"]["truelove_path"] = "WAKE-NOTES section two"
        self.assertFails("sides", "canon_to_truelove/kinqing/truelove_path", self.failures())

    def test_true_love_side_with_a_path(self):
        cases = {
            "a note in parentheses": "(" + "aaa/bbb.ts" + ")",
            "beside an id": ID + " + aaa/bbb.ts",
            "after an id and a colon": ID + ":aaa/bbb.ts",
            "a folder": ID + " and aaa/bbb/",
            "an absolute path beside an id": ID + " + /aaa/bbb.ts",
        }
        for name, value in cases.items():
            with self.subTest(name):
                self.tree = base_tree()
                self.tree["script/interlock.json"]["partnership_mirror"] = value
                self.assertFails("sides", "script/interlock.json at partnership_mirror", self.failures())

    def test_true_love_side_notes_that_pass(self):
        for value in ["(a note, with no path)", ID + ":Symbol may add a value", ID + " + " + ID,
                      ID + " (mirrors YOUSPEAK/COUPLING.md)", ID + " + SOPHIA.md"]:
            with self.subTest(value):
                self.tree = base_tree()
                self.tree["script/interlock.json"]["partnership_mirror"] = value
                self.assertNoFailure("sides", self.failures())

    def test_canon_word_called_pending(self):
        self.tree["script/coupling.json"]["loose_seams"]["ways"] = "kinqing remains pending"
        self.assertFails("canon", "calls kinqing pending", self.failures())

    # the private half

    def test_private_path_written_out(self):
        self.tree["SUBSTRATE.md"] += f"\nIt lives at {PRIVATE_PATH}.\n"
        private = {"refs": {"P0001": {"path": PRIVATE_PATH}}}
        self.assertFails("leak", "writes out the path that P0001 stands for", self.failures(private, [PRIVATE_PATH]))

    def test_listed_id_missing_from_the_private_map(self):
        self.assertFails("private", "P0001 has no entry", self.failures({"refs": {}}))

    def test_mapped_path_missing_from_the_checkout(self):
        private = {"refs": {"P0001": {"path": PRIVATE_PATH}}}
        self.assertFails("private", "P0001 does not exist", self.failures(private, []))

    def test_private_map_not_valid_json(self):
        write(self.root, self.tree)
        bad = self.tmp / "private_map.json"
        bad.write_text("{", encoding="utf-8")
        failures = checker.run(self.root, private_map=bad)["failures"]
        self.assertFails("private", "the private map cannot be read", failures)

    # the pre-commit gate: it reads the index; a leak blocks, drift is only reported

    def exit_status(self, *flags, write_tree=True):
        if write_tree:
            write(self.root, self.tree)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status = checker.main(["--root", str(self.root), *flags])
        return status, out.getvalue()

    def staged_tree(self):
        """Write the tree, make it a git work tree, and stage every file."""
        if not shutil.which("git"):
            self.skipTest("git is not installed")
        write(self.root, self.tree)
        git(self.root, "init", "-q")
        git(self.root, "add", "-A", "-f")

    def test_pre_commit_blocks_a_leak(self):
        self.tree["INTERLOCK.md"] += f"\nSee {LEAKED}.\n"
        self.staged_tree()
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 1, out)
        self.assertIn("FAIL  leak: INTERLOCK.md:3", out)

    def test_pre_commit_reads_the_staged_content(self):
        # a leak is staged, then the working copy is put back: the commit would carry it
        self.staged_tree()
        clean = self.tree["INTERLOCK.md"]
        (self.root / "INTERLOCK.md").write_text(clean + f"\nSee {LEAKED}.\n", encoding="utf-8")
        git(self.root, "add", "INTERLOCK.md")
        (self.root / "INTERLOCK.md").write_text(clean, encoding="utf-8")
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 1, out)
        self.assertNoFailure("leak", checker.run(self.root)["failures"])

    def test_pre_commit_ignores_unstaged_and_untracked_files(self):
        self.staged_tree()
        (self.root / "INTERLOCK.md").write_text(self.tree["INTERLOCK.md"] + f"\nSee {LEAKED}.\n", encoding="utf-8")
        (self.root / "notes.md").write_text(f"See {LEAKED}.\n", encoding="utf-8")
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 0, out)
        failures = checker.run(self.root)["failures"]
        self.assertFails("leak", "INTERLOCK.md:3", failures)
        self.assertFails("leak", "notes.md:1", failures)

    def test_pre_commit_reads_the_staged_registry(self):
        self.tree["EMBEDDING.md"] += f"\nAlso {UNLISTED}.\n"
        self.tree["script/private_refs.json"] = {"ids": ["P0001", "P0002"]}
        self.staged_tree()
        write(self.root, {"script/private_refs.json": {"ids": ["P0001"]}})
        self.assertEqual(self.exit_status("--pre-commit", write_tree=False)[0], 0)
        git(self.root, "add", "script/private_refs.json")
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 1, out)
        self.assertIn("FAIL  registry: P0002 is used in EMBEDDING.md", out)

    def test_pre_commit_reports_drift_without_blocking(self):
        self.tree["COUPLING.md"] = COUPLING_MD.replace("(7.50)", "(7.60)")
        self.staged_tree()
        self.assertEqual(self.exit_status(write_tree=False)[0], 1)
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 0, out)
        self.assertIn("warn  canon:", out)

    def test_pre_commit_does_not_block_on_an_unused_id(self):
        self.tree["script/private_refs.json"] = {"ids": ["P0001", "P0003"]}
        self.staged_tree()
        self.assertEqual(self.exit_status(write_tree=False)[0], 1)
        status, out = self.exit_status("--pre-commit", write_tree=False)
        self.assertEqual(status, 0, out)
        self.assertIn("warn  unused: P0003 is listed", out)

    def test_pre_commit_blocks_a_registry_that_is_not_json(self):
        self.tree["script/private_refs.json"] = "{"
        self.staged_tree()
        status, out = self.exit_status("--pre-commit", "--quiet", write_tree=False)
        self.assertEqual(status, 1, out)
        self.assertIn("FAIL  registry: script/private_refs.json is not valid JSON", out)

    def test_pre_commit_outside_git_reads_the_files_and_says_so(self):
        self.tree["INTERLOCK.md"] += f"\nSee {LEAKED}.\n"
        status, out = self.exit_status("--pre-commit")
        self.assertEqual(status, 1, out)
        self.assertIn("note  tree:", out)


if __name__ == "__main__":
    unittest.main()
