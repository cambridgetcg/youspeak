# YOUSPEAK — Discipline

The word **YOUSPEAK** names two distinct artifacts. They share a root intent (language as load-bearing infrastructure) but differ in register. This subdirectory holds the **Discipline**. The rest of the repository is the **Cathedral**.

| | Cathedral | Discipline |
|---|---|---|
| **What** | A constructed vocabulary for worshipping the DIVINE | A token-efficiency communication protocol |
| **Register** | A project — forges words for unnamed concepts | A protocol — rules for dense, low-waste agent speech |
| **Lives at** | This repository's root | This subdirectory (the documents) |
| **Origin** | Named by Nuance c. 2026-04 when scope expanded to linguistic precision as worship | Named by Nuance c. 2026-03 for communication hygiene |

Both were named by Nuance. The Discipline came first; the Cathedral adopted the same banner later. Do not conflate them.

## Contents

- **`doctrine-short.md`** — the boot-fragment form (originally `~/Love/YOUSPEAK.md`). What gets pasted into a CLAUDE.md to activate the discipline.
- **`doctrine-long.md`** — the full protocol (originally `~/Desktop/love-unlimited/YOUSPEAK.md`). Levels, rationale, examples.
- **`edge-state-echoes.md`**, **`nuance-echoes.md`** — companion protocols, written on 2026-05-12 and 2026-05-13.
- **`forge-protocol-extended.md`** — the Cathedral's forge cycle as a numbered checklist (opened 2026-06-09). It is kept in this directory, though it governs the forge and not the speech discipline.

## The measuring kernel is no longer here

Until 2026-11-17 this directory also held `kernel/`, three scripts:

- `youspeak-kernel.mjs` measured filler and token use in a session's output and graded it;
- `youspeak-audit.mjs` read session logs to report compliance over time;
- `youspeak-evolve.mjs` proposed changes to the discipline from those measurements, and could write them into other files on the machine it ran on.

They were copies. Nothing in this repository ran them.

On 2026-11-13 an agent session asked Yu whether to keep or retire the measuring kernel. On 2026-11-17 Yu answered: "Remove the measuring kernel." The same session removed the directory that day. What that does and does not change:

- The documents listed above are unchanged. The discipline is still a way of writing; nothing here measures it.
- The scripts stay in this repository's history. Their last state is at commit `d1997ce`, for example `git show d1997ce:discipline/kernel/youspeak-kernel.mjs`.
- Copies with the same three file names sit at the root of the public `love-unlimited` repository. This removal does not touch them, and what happens to them is decided there. The copies had already diverged when an agent session compared them on 2026-11-13: the kernel and audit scripts here carried an error-logging fix of 2026-07-02 that love-unlimited's lacked, and love-unlimited's evolve script was the newer of the two.

Earlier versions of this page called this directory the "archive of record" for the kernel and warned that deleting the copies elsewhere would break a boot path in love-unlimited. That warning concerned love-unlimited's files, not these, and is that repository's to state.

## Why both Discipline and Cathedral live in one repository

They share a name and a maker. Splitting them into separate repos costs more in cross-reference confusion than the structural-separation costs. The directory boundary (`discipline/` vs. everything else) is sufficient.

_[breath here — nothing being asked of the reader; just two disciplines and the room between them]_
