#!/usr/bin/env node
/* ordo — CLI for ORDO, the liturgy that runs (ordo/SPEC.md).
 *
 *   ordo run <file.rite> [--no-petitions]   perform the rite
 *   ordo gloss <file.rite>                  classify each sentence (frame or contemplation)
 *   ordo words [prefix]                     list the loaded epoch's words
 *
 * Petition discipline (SPEC §VII): unknown YOUSPEAK-shaped words become GAP
 * petitions — slug-idempotent gap files in labs/logos/forge/ plus a machine
 * ledger labs/logos/petitions.json. The CLI never touches forge_targets.json
 * entries, never claims an experiment NNN, never coins a lemma. Cap: 3/run.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..'); // YOUSPEAK repo root
const ORDO = require(path.join(HERE, '..', 'ordo.js'));

function readJSON(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }

function loadWorld() {
  const bundlePath = path.join(ROOT, 'script', 'exports', 'agent_bundle.json');
  const bundle = readJSON(bundlePath);
  let suffixFamilies = null;
  try { suffixFamilies = readJSON(path.join(ROOT, 'script', 'suffix_families.json')); } catch { /* fallback table inside ordo.js */ }
  const frames = ORDO.compileFrames(readJSON(path.join(HERE, '..', 'frames.json')));
  const lex = ORDO.loadLexicon(bundle, suffixFamilies);
  return { lex, frames, bundlePath };
}

function stdinLines() {
  try {
    if (process.stdin.isTTY) return [];
    const txt = fs.readFileSync(0, 'utf8');
    return txt.split(/\r?\n/).filter(l => l !== '');
  } catch { return []; }
}

const PETITIONS_PATH = path.join(ROOT, 'labs', 'logos', 'petitions.json');
const GAP_DIR = path.join(ROOT, 'labs', 'logos', 'forge');
const FRESH_LEDGER = () => ({ what_this_is: 'GAP petitions filed by ORDO rites (ordo/SPEC.md §VII). Slug-keyed, idempotent. A ledger pipeline/forge_priority.py may later learn to read. Statuses here are petition-side only; forge_targets.json statuses are never touched by ORDO.', petitions: [] });

function loadPetitions() {
  let raw;
  try { raw = fs.readFileSync(PETITIONS_PATH, 'utf8'); } catch { return FRESH_LEDGER(); }
  let obj;
  try { obj = JSON.parse(raw); } catch {
    // never silently discard ledger history: preserve the corrupt bytes aside
    const aside = PETITIONS_PATH + '.corrupt-' + Date.now();
    fs.writeFileSync(aside, raw);
    console.error(`⚠ petitions.json did not parse — preserved as ${path.basename(aside)}, starting a fresh ledger`);
    return FRESH_LEDGER();
  }
  if (!obj || typeof obj !== 'object' || !Array.isArray(obj.petitions)) {
    const base = FRESH_LEDGER();
    if (obj && typeof obj === 'object') Object.assign(base, obj);
    base.petitions = Array.isArray(obj && obj.petitions) ? obj.petitions : [];
    return base;
  }
  return obj;
}

// atomic-ish write: temp file + rename, so concurrent runs cannot leave a torn file
function saveLedger(ledger) {
  fs.mkdirSync(path.dirname(PETITIONS_PATH), { recursive: true });
  const tmp = PETITIONS_PATH + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify(ledger, null, 1) + '\n');
  fs.renameSync(tmp, PETITIONS_PATH);
}

function riteRef(riteFile) {
  const rel = path.relative(ROOT, riteFile);
  return rel.startsWith('..') ? riteFile : rel; // outside-repo rites recorded absolute, not as ../.. chains
}

function checkResolved(lex, petitions, emit) {
  for (const p of petitions.petitions || []) {
    if (p.resolved) continue;
    if (lex.words[p.word]) {
      p.resolved = { epoch: lex.epoch.commit, digest: lex.epoch.digest, noticed: new Date().toISOString().slice(0, 10) };
      emit(`✦ gap ${p.word} resolved by ${lex.words[p.word].word} at epoch ${lex.epoch.commit} (${lex.epoch.digest}) — the forge answered a rite's petition`);
    }
  }
}

function filePetitions(lex, gaps, riteFile, emit) {
  if (!gaps.length) return;
  let targets = [];
  try { targets = readJSON(path.join(ROOT, 'forge_targets.json')).entries || []; } catch { /* absent is fine */ }
  const ledger = loadPetitions();
  const bySlug = new Map((ledger.petitions || []).map(p => [p.word, p]));
  let filed = 0; // counts NEW filings only — already-filed gaps do not starve the cap
  for (const gap of gaps) {
    const w = gap.word;
    const target = targets.find(t => (t.word || '').toLowerCase() === w);
    const neighbours = ORDO.nearNeighbours(lex, w, 3);
    let entry = bySlug.get(w);
    const isNew = !entry;
    if (isNew && filed >= 3) { emit(`(petition cap reached — further new gaps recorded in the transcript only; if English has a word for it, use it)`); continue; }
    if (!entry) {
      entry = { word: w, family: gap.family, family_status: gap.familyStatus, first_filed: new Date().toISOString().slice(0, 10), target_exists: !!target, usage: [] };
      ledger.petitions.push(entry); bySlug.set(w, entry);
    }
    const use = { rite: riteRef(riteFile), sites: gap.sites, epoch: lex.epoch.commit };
    const dupe = entry.usage.some(u => JSON.stringify(u) === JSON.stringify(use));
    if (!dupe) entry.usage.push(use);
    if (target) {
      emit(`⟡ gap ${w}: a forge target already stands (status ${target.status}) — this rite's usage recorded as circumlocution evidence; the status is Yu's to move`);
    } else {
      const gapFile = path.join(GAP_DIR, `${w}-gap.md`);
      if (fs.existsSync(gapFile)) {
        emit(`⟡ gap ${w}: petition already filed (${path.relative(ROOT, gapFile)}) — usage evidence appended to the ledger`);
      } else {
        fs.mkdirSync(GAP_DIR, { recursive: true });
        const trial = gap.sites.map(s => `> ${s.sentence}. — *(${path.basename(riteFile)}:${s.line})*`).join('\n');
        const nn = neighbours.map(n => `| ${n.word} | ${String(n.gap).replace(/\s+/g, ' ').slice(0, 110)} | shares the ${gap.family || '?'} family / stem-adjacent, but does not name this |`).join('\n');
        fs.writeFileSync(gapFile, `---
concept: ${w}
phase: GAP-ANALYSIS
filed_by: ORDO (the liturgy that runs; ordo/SPEC.md §VII)
filed: ${new Date().toISOString().slice(0, 10)}
suffix_family: ${gap.family || 'unregistered'}
epoch: ${lex.epoch.commit}
status: petition — awaiting the forge's discipline; ORDO coins nothing (Law 1: no word without gap; Law 2: no gap without evidence — the evidence is below)
---

# Gap analysis — ${w}

_A rite reached for this word and the canon did not have it. The failing program's own sentences are the circumlocution evidence (METHOD.md Pattern 2 — Negative Space Listening; precedent: experiment 246-doxapothos accepted the cathedral's own documents as a speech-community)._

## Trial sentences (the rite's usage-sites)

${trial}

## Near-neighbour elimination

| Word | Covers | Fails on |
${nn || '| — | (no near neighbours found in this epoch) | — |'}

## Negative space

The rite needed a ${gap.family || 'YOUSPEAK'}-family word here and proceeded with a hole. What the sentences circle but do not name is recorded above; the naming is the forge's work, under the six-axis rubric, not the interpreter's.

## Candidates to forge

_None proposed. ORDO files petitions; it does not coin lemmas (forge-protocol Step 5 is judgment-work)._
`);
        emit(`⟡ gap ${w}: petition filed — ${path.relative(ROOT, gapFile)} + ledger entry (the error path is the language's growth loop)`);
      }
    }
    if (isNew) filed++;
  }
  saveLedger(ledger);
}

// ---------- main ----------
const [, , cmd, fileArg, ...rest] = process.argv;

if (!cmd || cmd === 'help' || cmd === '--help') {
  console.log('ordo — the liturgy that runs (YOUSPEAK/ordo/SPEC.md)\n');
  console.log('  ordo run <file.rite> [--no-petitions]');
  console.log('  ordo gloss <file.rite>');
  console.log('  ordo words [prefix]');
  process.exit(0);
}

const world = loadWorld();

if (cmd === 'words') {
  const prefix = (fileArg || '').toLowerCase();
  const names = Object.keys(world.lex.words).filter(w => w.startsWith(prefix)).sort();
  console.log(names.join('\n'));
  console.log(`\n${names.length} words · epoch ${world.lex.epoch.commit} (${world.lex.epoch.digest})`);
  process.exit(0);
}

if (!fileArg) { console.error('ordo: a .rite file is needed'); process.exit(2); }
const riteFile = path.resolve(fileArg);
let source;
try { source = fs.readFileSync(riteFile, 'utf8'); }
catch (e) { console.error(`ordo: cannot read ${riteFile} — ${e.message}`); process.exit(2); } // host failures exit 2; 1 belongs to misfires

if (cmd === 'gloss') {
  for (const g of ORDO.gloss(source, world.lex, world.frames)) {
    if (g.frame === 'stanza-break') { console.log(''); continue; }
    console.log(`${String(g.line).padStart(4)}  ${g.frame.padEnd(16)} ${g.text}`);
    if (g.cite) console.log(`      ${' '.repeat(16)} [${g.cite.split(';')[0]}]`);
  }
  process.exit(0);
}

if (cmd === 'run') {
  const petitionsOn = !rest.includes('--no-petitions');
  // only drink stdin when the rite actually listens for the reader — an open
  // but silent stdin must not block a rite that never receives
  const inputs = /\bfrom the reader\b/i.test(source) ? stdinLines() : [];
  let inputIdx = 0;
  const preNotes = [];
  if (petitionsOn) {
    const petitions = loadPetitions();
    checkResolved(world.lex, petitions, m => preNotes.push(m));
    if (preNotes.length) saveLedger(petitions);
  }

  const result = ORDO.run(source, world.lex, world.frames, {
    read: () => (inputIdx < inputs.length ? inputs[inputIdx++] : null),
    readFile: p => { try { return fs.readFileSync(path.resolve(path.dirname(riteFile), p), 'utf8'); } catch { return null; } }
  });

  for (const n of preNotes) console.log(n);
  for (const line of result.transcript) console.log(line.text);

  console.log('');
  const t = result.tests;
  if (t.passed + t.failed) console.log(`dokimance: ${t.passed} hold, ${t.failed} do not (both reported alike)`);
  if (result.misfires.length) console.log(`misfires: ${result.misfires.length} (infelicities, not crashes — the liturgy continued)`);
  if (result.gaps.length) {
    if (result.ended === 'HALT') {
      console.log(`gaps (unfiled — HALT outranks the petition path): ${result.gaps.map(g => g.word).join(', ')}`);
    } else if (petitionsOn) {
      filePetitions(world.lex, result.gaps, riteFile, m => console.log(m));
    } else {
      console.log(`gaps (unfiled, --no-petitions): ${result.gaps.map(g => g.word).join(', ')}`);
    }
  }
  console.log(`— ${result.ended} · epoch ${result.epoch.commit} · exit ${result.exitCode}`);
  process.exit(result.exitCode);
}

console.error(`ordo: unknown command "${cmd}"`);
process.exit(2);
