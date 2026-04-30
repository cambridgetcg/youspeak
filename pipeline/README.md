# pipeline · assessment + canonization tools

The Python CLI that turns a forge-attempt into a canonical entry (or a refined experiment, or an archived attempt).

## Tools

| Tool | What it does |
|---|---|
| **[assess.py](assess.py)** | Score a forge-experiment on the 5 axes (gap_validity 0.25, phonetic_weight 0.20, semantic_coverage 0.25, cross_linguistic_uniqueness 0.15, memorability 0.15). Verdicts: canon (≥7.5), refine, archive. |
| **[canonize.py](canonize.py)** | Stub a `canon/<word>.md` from a canon-verdict experiment. `--all` walks experiments and stubs all pending. |
| **[discover.py](discover.py)** | Gap-finder. Surveys archaeology and produces a gap-analysis template for a concept. |
| **[forge.py](forge.py)** | Candidate-generator. Combines morphemes, reports phonetic metrics. `--from <experiment.md>` reuses donors. |
| **[diplosemize.py](diplosemize.py)** | Surface diplosemic-potential candidates from a canonical word (anastrophance, enkalyptance, synaphemia, allomance, parallaxance). |

## Common invocations

```
python3 pipeline/assess.py <file.md>                  # grade one
python3 pipeline/assess.py --init <path>              # stub experiment
python3 pipeline/assess.py --batch <dir>              # grade all
python3 pipeline/assess.py status <agent>             # agent fluency report

python3 pipeline/canonize.py <experiment.md>          # promote one
python3 pipeline/canonize.py --all                    # promote every canon-verdict

python3 pipeline/discover.py <concept>                # gap-analysis from archaeology
python3 pipeline/discover.py --list                   # list opened archaeologies
python3 pipeline/discover.py --seed <tongue>          # open a new archaeology dir

python3 pipeline/forge.py <morpheme1> <morpheme2> …   # combine, score
python3 pipeline/forge.py --from <experiment.md>      # reuse donors

python3 pipeline/diplosemize.py <word>                # surface dual-meaning candidates
```

## Primers

- **`primers/`** — Operational language guides for working in YOUSPEAK at each cathedral stage. → [`primers/current.md`](primers/current.md) is the active primer.

## See also

- [../METHOD.md](../METHOD.md) — the Six Patterns
- [../labs/logos/](../labs/logos/) — the forge proper
