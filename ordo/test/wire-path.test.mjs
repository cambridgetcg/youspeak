// The CLI finds the KS-002 reference impl (impl/wire.py) by KINGDOM_STANDARDS_DIR,
// then by a short list of candidate checkouts, and misfires with a clear message
// when there is none. These tests never reach a real wire.py: HOME is a fresh
// temp dir, so no key is minted, and nothing reaches ordo/outbox/.
// Run: node --test ordo/test/wire-path.test.mjs
import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const CLI = path.join(ROOT, 'ordo', 'bin', 'ordo.mjs');

const home = fs.mkdtempSync(path.join(os.tmpdir(), 'ordo-wire-'));
after(() => fs.rmSync(home, { recursive: true, force: true }));
const rite = path.join(home, 'offer.rite');
fs.writeFileSync(rite, 'Let word be "hello".\nQorvance word to the wire at kingdom.test.\n');

function offer(extraEnv) {
  const env = { ...process.env, HOME: home, ...extraEnv };
  if (extraEnv.KINGDOM_STANDARDS_DIR === undefined) delete env.KINGDOM_STANDARDS_DIR;
  const r = spawnSync(process.execPath, [CLI, 'run', rite, '--no-petitions'], { encoding: 'utf8', env });
  return r.stdout + r.stderr;
}

test('KINGDOM_STANDARDS_DIR naming a place without impl/wire.py misfires, naming it', () => {
  const out = offer({ KINGDOM_STANDARDS_DIR: path.join(home, 'nowhere') });
  assert.match(out, /KINGDOM_STANDARDS_DIR is set, but .*nowhere.*impl.*wire\.py does not exist/);
  assert.doesNotMatch(out, /signed \+ verified/);
});

test('KINGDOM_STANDARDS_DIR is the wire.py the CLI calls', () => {
  const ks = path.join(home, 'ks');
  fs.mkdirSync(path.join(ks, 'impl'), { recursive: true });
  // a stand-in that refuses at once: proves which file was called, writes nothing
  fs.writeFileSync(path.join(ks, 'impl', 'wire.py'), 'import sys\nsys.stderr.write("stand-in wire.py reached\\n")\nsys.exit(1)\n');
  const out = offer({ KINGDOM_STANDARDS_DIR: ks });
  assert.match(out, /stand-in wire\.py reached/);
  assert.ok(!fs.existsSync(path.join(home, '.kingdom')), 'no key directory may appear');
});

test('unset, the candidates are tried and every one is named when none holds wire.py', (t) => {
  const sibling = path.resolve(ROOT, '..', 'kingdom-standards', 'impl', 'wire.py');
  if (fs.existsSync(sibling)) { t.skip('a sibling kingdom-standards checkout exists beside this repo'); return; }
  const out = offer({ KINGDOM_STANDARDS_DIR: undefined });
  assert.match(out, /no kingdom-standards checkout found/);
  assert.match(out, /Kingdom.standards.kingdom-standards/);
  assert.match(out, /set KINGDOM_STANDARDS_DIR/);
});
