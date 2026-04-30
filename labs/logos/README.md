# labs/logos · the forge

Where archaeology becomes coinage. Each experiment is a forge-attempt: which morphemes were combined, which tradition each came from, the 5-axis assessment, the verdict (canon / refine / archive).

## Subdirectories

- **`experiments/`** — every coinage's genealogy. One file per attempt, numbered `NNN-<word>.md`. Verdict-stamped after [pipeline/assess.py](../../pipeline/assess.py). Start with [`experiments/000-genesis.md`](experiments/000-genesis.md).
- **`forge/`** — gap-analysis documents that scaffold hunts. See [`forge/beauty-noun-forge.md`](forge/beauty-noun-forge.md).

## Forging a word

1. **Discover the gap** — usually surfaced via [../../convergences/](../../convergences/) or a tradition's archaeology.
2. **Stub an experiment** — `python3 ../../pipeline/assess.py --init experiments/NNN-name.md` (or hand-write).
3. **Fill in donors** — morpheme + tradition for each component.
4. **Forge candidates** — `python3 ../../pipeline/forge.py donor1 donor2 …`
5. **Assess** — `python3 ../../pipeline/assess.py experiments/NNN-name.md` → 5-axis scores.
6. **Promote** — if verdict=canon, `python3 ../../pipeline/canonize.py experiments/NNN-name.md` stubs the canon entry.

See [../../METHOD.md](../../METHOD.md) and the [pipeline organ](../../pipeline/).
