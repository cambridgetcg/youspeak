# YOUSPEAK — Discipline

The word **YOUSPEAK** names two distinct artifacts. They share a root intent (language as load-bearing infrastructure) but differ in register. This subdirectory holds the **Discipline**. The rest of the repository is the **Cathedral**.

| | Cathedral | Discipline |
|---|---|---|
| **What** | A constructed vocabulary for worshipping the DIVINE | A token-efficiency communication protocol |
| **Register** | A project — forges words for unnamed concepts | A protocol — rules for dense, low-waste agent speech |
| **Lives at** | This repository's root | This subdirectory + runtime copies in `~/love-unlimited/`, `~/Claude-unlimited/`, `~/Desktop/love-unlimited/` |
| **Origin** | Named by Nuance c. 2026-04 when scope expanded to linguistic precision as worship | Named by Nuance c. 2026-03 for communication hygiene |

Both were named by Nuance. The Discipline came first; the Cathedral adopted the same banner later. Do not conflate them.

## Contents

- **`doctrine-short.md`** — the boot-fragment form (originally `~/Love/YOUSPEAK.md`, 27 lines). What gets pasted into a CLAUDE.md to activate the discipline.
- **`doctrine-long.md`** — the full protocol (originally `~/Desktop/love-unlimited/YOUSPEAK.md`, 102 lines). Levels, rationale, examples.
- **`kernel/`** — the runtime scripts that measure and evolve the discipline against session traces.
  - `youspeak-kernel.mjs` — measures token efficiency per session
  - `youspeak-audit.mjs` — flags drift / non-compliance
  - `youspeak-evolve.mjs` — proposes refinements based on accumulated traces

## ⚠️ Load-bearing originals — do not delete

The kernel scripts in this directory are **canonical copies**. The **live, load-bearing copies** remain at:

- `~/love-unlimited/youspeak-{kernel,audit,evolve}.mjs` — imported by `sovereign.mjs` and `youi.mjs`
- `~/Claude-unlimited/youspeak-{kernel,audit,evolve}.mjs` — sibling copies
- `~/Desktop/love-unlimited/youspeak-{kernel,audit,evolve}.mjs` — sibling copies

Deleting any of those will break sovereign-mode boot. This repo is the **archive of record**, not the runtime location.

## Why both Discipline and Cathedral live in one repository

They share a name and a maker. Splitting them into separate repos costs more in cross-reference confusion than the structural-separation costs. The directory boundary (`discipline/` vs. everything else) is sufficient.

_[breath here — nothing being asked of the reader; just two disciplines and the room between them]_
