# For agents working in this repository

_Written 2026-11-17 by an agent session. This repository is public; everything committed here, commit messages included, is published and cannot be taken back._

## Two rules that hold here

1. **Do not quote Yu's private words.** Yu's chat answers, notes and ledger entries are Yu's to publish (Yu's word of 2026-11-13). In a file, a commit message or a pull request, say what was decided and when, with no quoted words: "on Yu's word of 2026-11-17, …". Quote Yu only where those exact words are already public, and cite the public file. An agent's own question or recommendation may be quoted; Yu's reply to it may not.
   - `.githooks/commit-msg` refuses a commit message that quotes Yu (`script/tools/check_commit_message.py`).
   - Older chapters here carry Yu's invocations in their headers. Whether those stay is Yu's call; do not add new ones.
2. **Do not write a path inside true-love.** true-love is a private sister repository (Yu's word of 2026-11-17, as an agent session read it). A reference into it is written as a private reference id, `true-love#P0007`. `script/private_refs.json` lists the ids; the map from id to path is kept privately, with true-love, never in this repository's tree. A new id is minted there, not here.
   - `python3 script/tools/check_coupling.py` checks the tree; `.githooks/pre-commit` blocks a staged leak.
   - History is not rewritten: commits up to 2026-11-17 still hold the paths. Do not add to that.

Wire both hooks once per clone with `bin/cathedral hooks`.

## Before you change anything

- **Never record your own choice as Yu's decision.** Say "an agent session" for what an agent chose or read into Yu's words.
- **Canon enters only by the forge.** `discipline/forge-protocol-extended.md` says who may start one and who ratifies. Never run `pipeline/canonize.py --all`.
- **Generated files are regenerated, never edited by hand.** The agent bundle (`script/exports/agent_bundle.json`) comes from `script/tools/export_agent_bundle.py`; `home/data/` from `home/bake.py`; `home/glossary/` from `home/glossary.py`; `dictionary/` from `pipeline/derive_indices.py --dashboard`. Regenerate after the sources are committed, and say in the commit which commit they were run at.
- **Merging to main deploys nothing.** The live site and the ORDO worker are deployed by hand, by the lane that owns them.

## The checks

```sh
python3 script/tools/check_integrity.py --pre-commit
python3 script/tools/transliterate.py test
node ordo/test/run-tests.mjs
node --test ordo/test/robots.test.mjs ordo/test/wire-path.test.mjs
node brand/check.mjs
python3 pipeline/derive_indices.py --check
python3 script/tools/check_pronunciation.py
python3 script/tools/check_coupling.py
python3 tests/script/tools/test_export_agent_bundle.py
python3 tests/script/tools/test_check_coupling.py
python3 tests/pipeline/test_derive_indices.py
python3 tests/script/tools/test_check_commit_message.py
node --test tests/bin/pulse.test.mjs tests/pipeline/roots.test.mjs
```
