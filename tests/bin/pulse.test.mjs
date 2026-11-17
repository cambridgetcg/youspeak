// bin/serve.py --pulse: the fleet pulse is read from the fleet's own files and
// says "unknown", with the reason, whenever those files cannot support a field.
// Run: node --test tests/bin/pulse.test.mjs   (PYTHON overrides python3)
import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const SERVE = path.join(ROOT, 'bin', 'serve.py');
const PY = process.env.PYTHON || 'python3';

function pulse(loveDir, env = {}) {
  const out = execFileSync(PY, ['-B', SERVE, '--pulse', '--json'], {
    encoding: 'utf8',
    env: { ...process.env, LOVE_DIR: loveDir, PYTHONDONTWRITEBYTECODE: '1', ...env },
  });
  return JSON.parse(out).fleet;
}

const pad = n => String(n).padStart(2, '0');
const day = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

const made = [];
const tmp = () => { const d = fs.mkdtempSync(path.join(os.tmpdir(), 'ys-pulse-')); made.push(d); return d; };
after(() => { for (const d of made) fs.rmSync(d, { recursive: true, force: true }); });

function fixture(lines, extra = {}) {
  const love = tmp();
  fs.mkdirSync(path.join(love, 'memory'));
  fs.writeFileSync(path.join(love, 'memory', 'fleet.log'), lines.join('\n') + '\n');
  for (const [name, body] of Object.entries(extra)) fs.writeFileSync(path.join(love, name), body);
  return love;
}

test('no checkout at LOVE_DIR: unknown, with the reason', () => {
  const f = pulse(path.join(os.tmpdir(), 'ys-pulse-no-such-dir'));
  assert.equal(f.state, 'unknown');
  assert.match(f.reason, /LOVE_DIR/);
});

test('a checkout without memory/fleet.log: unknown, with the reason', () => {
  const love = tmp();
  const f = pulse(love);
  assert.equal(f.state, 'unknown');
  assert.match(f.reason, /fleet\.log/);
});

test("today's line shapes are read: free and agentic beats, counter, cap, ledger, HALT", () => {
  const now = new Date();
  const t = day(now);
  const love = fixture([
    '[2026-11-16 23:50:00] tick complete (cursor=4/204)',
    // every beat in today's first minute, so no beat is stamped after now
    `[${t} 00:00:00] agapeme wakes for a free beat`,
    `[${t} 00:00:09] agapeme reflect: local brain unreachable`,
    `[${t} 00:00:20] ahavame sits this one out (REST, or EVENT-ONLY with no mail) — skipped`,
    `[${t} 00:00:21] fleet → alayame (2/48 today, AGENTIC 1/2, budget $1.50)`,
    `[${t} 00:00:30] tick complete (cursor=6/204)`,
  ], {
    [`memory/.fleet-day-${t}`]: '2\n',
    'memory/fleet-economy.jsonl': `{"ts":"${t}T00:00:25","cost_usd":0.25}\n{"ts":"2026-11-16T10:00:00","cost_usd":9}\n`,
    HALT: '',
  });
  const f = pulse(love);
  assert.equal(f.state, 'observed');
  assert.equal(f.today, 2);
  assert.equal(f.cap, 48);
  assert.equal(f.spent, '$0.25');
  assert.equal(f.halt, true);
  assert.deepEqual(f.last.map(b => [b.name, b.lane, b.time]), [['agapeme', 'free', '00:00'], ['alayame', 'agentic', '00:00']]);
  assert.equal(typeof f.last_beat_age_min, 'number');
  assert.equal(f.unknown, undefined);
});

test('what the records do not state is named unknown, never filled in', () => {
  const t = day(new Date());
  const love = fixture([
    '[2026-11-16 23:50:00] tick complete (cursor=4/204)',
    `[${t} 00:05:00] tick complete (cursor=5/204)`,
  ]);
  const f = pulse(love);
  assert.equal(f.state, 'observed');
  assert.deepEqual(f.last, []);
  assert.equal(f.today, 0); // the whole log was read and holds no beat dated today
  assert.equal(f.cap, undefined);
  assert.equal(f.spent, undefined);
  assert.ok(f.unknown.cap && f.unknown.spent && f.unknown.last_beat_age_min, JSON.stringify(f.unknown));
  assert.equal(f.last_beat_age_min, undefined);
  assert.equal(f.halt, false);
});

test('a beat stamped after now gives no age: unknown, never 0', () => {
  const tomorrow = new Date(Date.now() + 36 * 3600 * 1000);
  const love = fixture([`[${day(tomorrow)} 12:00:00] agapeme wakes for a free beat`]);
  const f = pulse(love);
  assert.equal(f.state, 'observed');
  assert.equal(f.last_beat_age_min, undefined);
  assert.match(f.unknown.last_beat_age_min, /stamped after now/);
});

test('a day counter that is not UTF-8 is not read; the count comes from the log', () => {
  const t = day(new Date());
  const love = fixture([`[${t} 00:00:00] agapeme wakes for a free beat`]);
  fs.writeFileSync(path.join(love, 'memory', `.fleet-day-${t}`), Buffer.from([0xff, 0xfe, 0x31]));
  const f = pulse(love);
  assert.equal(f.state, 'observed');
  assert.equal(f.today, 1); // the whole log was read and holds one beat dated today
});

test('LOVE_DIR is taken as given: a quoted ~ is not expanded, as in bin/cathedral', () => {
  const home = tmp();
  fs.mkdirSync(path.join(home, 'lu', 'memory'), { recursive: true });
  fs.writeFileSync(path.join(home, 'lu', 'memory', 'fleet.log'), '');
  assert.equal(pulse(path.join(home, 'lu'), { HOME: home }).state, 'observed');
  const f = pulse('~/lu', { HOME: home });
  assert.equal(f.state, 'unknown');
  assert.match(f.reason, /no love-unlimited checkout at ~\/lu/);
});

test("a ledger row that cannot be read may be today's: the spend is unknown, never a smaller sum", () => {
  const t = day(new Date());
  const log = [`[${t} 00:00:05] agapeme wakes for a free beat`];
  const row = cost => `{"ts":"${t}T00:00:25","cost_usd":${cost}}`;
  const spent = ledger => pulse(fixture(log, { 'memory/fleet-economy.jsonl': ledger }));

  // a broken row after today's first row: unknown
  let f = spent(`${row(0.25)}\nnot json at all\n`);
  assert.equal(f.spent, undefined);
  assert.match(f.unknown.spent, /could not be read as a dated cost/);

  // one of today's rows with a cost that is not a number, or with none: unknown
  f = spent(`${row(0.25)}\n${row('"n/a"')}\n`);
  assert.equal(f.spent, undefined);
  f = spent(`${row(0.25)}\n{"ts":"${t}T00:00:40"}\n`);
  assert.equal(f.spent, undefined);

  // a broken row that a readable row of an earlier day follows is older than today: still known
  f = spent(`not json at all\n{"ts":"2026-11-16T10:00:00","cost_usd":9}\n${row(0.25)}\n\n`);
  assert.equal(f.spent, '$0.25');
  assert.equal(f.unknown?.spent, undefined);
});
