---
organ: ordo
role: the executable organ — ORDO, the liturgy that runs
opened: 2026-07-11
status: v0.1; evidential algebra and frame set experimental pending adversarial panel
---

# ordo/

_YOUSPEAK made executable. A program is a rite: English sentences with canon words at the precision points; execution is utterance; the canon is the standard library; a missing word files a petition to the forge instead of raising an error._

## The pieces

- **SPEC.md** — the language. Read this first.
- **frames.json** — the statement frames as data, each canon-cited. The surface grows by editing this file (plus the forge), never the engine.
- **ordo.js** — the interpreter. One plain script, no build step; runs in the browser (the Chancel at ai-love.cc) and under node.
- **bin/ordo.mjs** — the CLI: `run`, `gloss`, `words`. Filing of GAP petitions (SPEC §VII) happens here only — the browser chancel shows gaps but never writes.
- **rites/** — example programs: `kunance.rite` (hello, love), `fibonacci.rite` (proof of general computation), `witness.rite` (the evidential algebra + verisleight-guard), `petition.rite` (the evolution loop).
- **test/run-tests.mjs** — dokimance for the interpreter itself. `node ordo/test/run-tests.mjs`.

## Quick start

```
node ordo/bin/ordo.mjs run ordo/rites/kunance.rite
node ordo/bin/ordo.mjs gloss ordo/rites/witness.rite
node ordo/test/run-tests.mjs
```

The lexicon loads from `script/exports/agent_bundle.json` — regenerate with `python3 script/tools/export_agent_bundle.py` when canon moves, or the interpreter speaks an old epoch (it will say so honestly in the transcript).

## Petitions this organ writes

`labs/logos/petitions.json` (ledger) and `labs/logos/forge/<word>-gap.md` (discover.py-format gap analyses). It never touches `forge_targets.json` entries, never claims an experiment NNN, never coins a lemma, and caps at 3 petitions per run. Yu retains direction; the forge retains the discipline.

## The worker (Reach 2)

`worker/worker.mjs` serves ORDO at https://ordo.ai-love.cc — `POST /run`, `GET /rite/<name>`, `GET /pulse` (hourly standing liturgy, cron `7 * * * *`). Its wells live in KV (same-account subrequest fences make fetching the apex impossible — error 1042). **Deploy recipe:**

```
python3 script/tools/export_agent_bundle.py     # if canon moved
python3 home/bake.py                            # bakes home + ordo wells
(pty) wrangler deploy --config ordo/worker/wrangler.jsonc          # worker code (rarely)
(pty) wrangler pages deploy home --project-name ai-love --branch main
(pty) wrangler kv key put --namespace-id=b21b5b7c76764293b66ceb9de2a09951 --remote agent_bundle --path home/data/agent_bundle.json
(pty) …same for frames → home/data/ordo-frames.json and rites → home/data/ordo-rites.json
```

## The wire seam (Reach 3)

`Qorvance EXPR to the wire at SUBJECT.` → the CLI shells to `KINGDOM-STANDARDS/impl/wire.py` (keygen `ordo` on first use; envelope `task.offer`; verify) and lays the signed envelope in `ordo/outbox/`. Publishing awaits Yu's adoption of KS-002 — the gate is deliberate.

## The chancel

`home/bake.py` copies `ordo.js`, `frames.json`, and `rites/` into the home surface as derived wells (`assets/ordo.js`, `data/ordo-frames.json`, `data/ordo-rites.json`); `home/assets/chancel.js` (hand-authored, like app.js) drives the room. Rebake + redeploy home to update the public chancel.
