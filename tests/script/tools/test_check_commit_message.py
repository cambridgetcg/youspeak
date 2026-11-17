#!/usr/bin/env python3
"""script/tools/check_commit_message.py refuses a commit message that quotes Yu.

The quotations here are invented ("paint the door green"): no test may carry
Yu's real private words.

Run: python3 tests/script/tools/test_check_commit_message.py
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "script" / "tools"))
import check_commit_message as checker  # noqa: E402

Q = "paint the door green"

REFUSED = {
    "answered, with a colon": f'Asked on 2026-11-13 which colour, Yu answered on 2026-11-17: "{Q}."',
    "wrapped onto the next line": f'Asked which colour, Yu answered on 2026-11-17:\n"paint the door\ngreen."',
    "a block quote": f'Yu answered in one message:\n\n> "{Q}"\n\nSo the door is green.',
    "dialogue form": f'Yu: "{Q}"',
    "curly quotes": f"the owner said “{Q}”",
    "word was": f'Yu\'s word was "{Q}", and the door is green.',
    "in brackets after a date": f'Merged on Yu\'s word of 2026-11-17 ("{Q}").',
    "message included": f'Yu\'s message of 2026-11-17 included the words "{Q}."',
    "a reply after an unquoted question": f"An agent asked Yu to choose a colour, and Yu replied: “{Q}.”",
    "a reply after a quoted question": f'An agent asked Yu: "which colour for the door?" Yu answered: "{Q}."',
}
ALLOWED = {
    "a dated statement with no quoted words": "door: paint it green\n\nOn Yu's word of 2026-11-17, the door is green.",
    "the agent's own question": f'An agent session asked Yu: "which colour for the door, green or blue?" On Yu\'s reply the door is green.',
    "a quotation of something else": 'The chapter says "maintained instruments" in its note. Yu was not asked.',
    "one quoted word": 'Yu answered "green" and nothing else.',
    "a quotation in another sentence": f'Yu agreed. The sign reads "{Q}" already.',
    "a comment line git strips": f'door: green\n# Yu said: "{Q}"\n',
    "a decimal before a quoted term": 'Yu settled the score at 7.85. "synophora stays" is the heading.',
}


class CheckCommitMessageTest(unittest.TestCase):
    def test_a_message_that_quotes_yu_is_refused(self):
        for name, msg in REFUSED.items():
            with self.subTest(name):
                self.assertTrue(checker.quotations(msg), msg)

    def test_other_messages_pass(self):
        for name, msg in ALLOWED.items():
            with self.subTest(name):
                self.assertEqual(checker.quotations(msg), [], msg)

    def run_main(self, msg, env=None):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "COMMIT_EDITMSG"
            p.write_text(msg, encoding="utf-8")
            with mock.patch.dict(os.environ, env or {}, clear=False), mock.patch("sys.stderr"):
                return checker.main([str(p)])

    def test_exit_status(self):
        os.environ.pop("YOUSPEAK_OWNER_WORDS_ARE_PUBLIC", None)
        self.assertEqual(self.run_main(REFUSED["dialogue form"]), 1)
        self.assertEqual(self.run_main(ALLOWED["a dated statement with no quoted words"]), 0)

    def test_words_already_public_are_let_through_on_request(self):
        self.assertEqual(self.run_main(REFUSED["dialogue form"], {"YOUSPEAK_OWNER_WORDS_ARE_PUBLIC": "1"}), 0)

    def test_the_hook_is_executable_and_calls_the_check(self):
        hook = ROOT / ".githooks" / "commit-msg"
        self.assertTrue(os.access(hook, os.X_OK))
        self.assertIn("check_commit_message.py", hook.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
