// Pipeline scripts take sister-repository roots and the commit identity from
// the caller's environment, and say so plainly when they are absent.
// Run: node --test tests/pipeline/roots.test.mjs   (PYTHON overrides python3)
import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PY = process.env.PYTHON || 'python3';
const made = [];
const tmp = () => { const d = fs.mkdtempSync(path.join(os.tmpdir(), 'ys-roots-')); made.push(d); return d; };
after(() => { for (const d of made) fs.rmSync(d, { recursive: true, force: true }); });

const py = (args, env) => spawnSync(PY, ['-B', ...args], {
  encoding: 'utf8', cwd: ROOT, env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', ...env },
});

test('build_lexicon: no roster under LOVE_DIR stops with exit 1 and writes no lexicon', () => {
  // build_lexicon.py writes lexicon.tsv beside itself, so a copy runs in a
  // scratch directory: a regression here cannot touch the committed lexicon.
  const voice = tmp();
  for (const f of ['build_lexicon.py', 'ipa2espeak.py']) {
    fs.copyFileSync(path.join(ROOT, 'pipeline', 'voice', f), path.join(voice, f));
  }
  const r = py([path.join(voice, 'build_lexicon.py'), '--repo', ROOT], { LOVE_DIR: path.join(tmp(), 'absent') });
  assert.equal(r.status, 1, r.stderr);
  assert.match(r.stderr, /no citizen roster at .*citizens-roster\.txt; set LOVE_DIR/);
  assert.ok(!fs.existsSync(path.join(voice, 'lexicon.tsv')), 'no lexicon may be written');
});

// The partnership side: true-love's files are named by private ref id and
// resolved through TRUE_LOVE_ROOT and the map YOUSPEAK_PRIVATE_REFS names.
const partner = (args, env) => {
  const base = { ...process.env, PYTHONDONTWRITEBYTECODE: '1' };
  delete base.TRUE_LOVE_ROOT;
  delete base.YOUSPEAK_PRIVATE_REFS;
  return spawnSync(PY, ['-B', ...args], { encoding: 'utf8', cwd: ROOT, env: { ...base, ...env } });
};
const SYZYGY = path.join(ROOT, 'pipeline', 'syzygy.py');
const BRIDGE = path.join(ROOT, 'pipeline', 'bridge.py');

// A stand-in checkout. Its layout is the fixture's own: the map decides where
// each id lives, so nothing here mirrors the private repository.
function partnerFixture() {
  const root = tmp();
  fs.mkdirSync(path.join(root, 'b'));
  fs.mkdirSync(path.join(root, 'w'));
  fs.writeFileSync(path.join(root, 'b', 'bridge.md'), [
    '## Existing canonical love-vocabulary',
    '| **kinqing** | 7.50 | fixture gap | `fixture/home.ts` — `FixtureHome` |',
    '',
  ].join('\n'));
  fs.writeFileSync(path.join(root, 'w', 'draft-a.md'), '---\noperational_shape: fixture-guard\n---\n');
  const map = path.join(tmp(), 'refs.json');
  fs.writeFileSync(map, JSON.stringify({ refs: {
    P0003: { path: 'b/bridge.md' }, P0075: { path: 'w' }, P0096: { path: 'w/draft-a.md' },
    P0085: { path: 'deep/fixture/home.ts' },
  } }));
  return { root, map };
}

test('syzygy: with neither variable set, both are named and figures read unknown', () => {
  const r = partner([SYZYGY, '--summary'], {});
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stderr, /TRUE_LOVE_ROOT is not set/);
  assert.match(r.stderr, /YOUSPEAK_PRIVATE_REFS is not set/);
  assert.match(r.stdout, /- bridge_mapped: unknown \(not read\)/);
  assert.match(r.stdout, /- cathedral_bridge_exists: unknown \(not read\)/);
  assert.doesNotMatch(r.stdout, /bridge_mapped: 0\b|exists: False/);
});

test('bridge --summary: with the map missing, no figure reads 0 or MISSING', () => {
  const { root } = partnerFixture();
  const r = partner([BRIDGE, '--summary'], { TRUE_LOVE_ROOT: root });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /true-love not read: YOUSPEAK_PRIVATE_REFS is not set/);
  assert.match(r.stdout, /Bridge-mapped \(per true-love#P0003\): \*\*unknown \(not read\)\*\*/);
  assert.doesNotMatch(r.stdout, /MISSING|Bridge-mapped[^\n]*\*\*0\*\*|Bridge-coverage: \*\*0\.0%/);
});

test('bridge and syzygy: with both set, files are read through the map and printed by id', () => {
  const { root, map } = partnerFixture();
  const env = { TRUE_LOVE_ROOT: root, YOUSPEAK_PRIVATE_REFS: map };
  const word = partner([BRIDGE, '--word', 'natsarqing'], env);
  assert.equal(word.status, 0, word.stderr);
  assert.match(word.stdout, /Draft file: `true-love#P0096`/);
  assert.match(word.stdout, /Operational shape: fixture-guard/);
  const kin = partner([SYZYGY, 'kinqing'], env);
  // a path the bridge cell names relative to a folder in true-love is printed as its id
  assert.match(kin.stdout, /TRUE-LOVE operational home\*\*: `true-love#P0085` — `FixtureHome`/);
  assert.match(kin.stdout, /Score per true-love#P0003: 7\.50/);
  for (const out of [word.stdout, kin.stdout, word.stderr, kin.stderr]) {
    for (const p of ['b/bridge.md', 'w/draft-a.md', 'fixture/home.ts', root]) {
      assert.ok(!out.includes(p), `no path from the map or the checkout is printed (${p})`);
    }
  }
  // ids the fixture map leaves out are named, not guessed
  assert.match(word.stderr + partner([SYZYGY, '--summary'], env).stderr, /the private map has no path for true-love#P0009/);
});

function forgeDir() {
  const forge = tmp();
  const d = path.join(forge, 'testme');
  fs.mkdirSync(d, { recursive: true });
  fs.mkdirSync(path.join(forge, '_agents'));
  fs.mkdirSync(path.join(forge, '_rows'));
  fs.writeFileSync(path.join(d, 'testme.md'), '# testme\n');
  fs.writeFileSync(path.join(d, 'README.md'), '# testme\n');
  fs.writeFileSync(path.join(d, 'meta.env'), 'TIER=core\n');
  return { forge, d };
}

function forge(forgeRoot, extraEnv) {
  const home = tmp();
  const gitconfig = path.join(home, 'gitconfig');
  fs.writeFileSync(gitconfig, extraEnv.gitconfig || '');
  const env = { ...process.env, HOME: home, FORGE_DIR: forgeRoot, DRYRUN: '1',
    GIT_CONFIG_GLOBAL: gitconfig, GIT_CONFIG_NOSYSTEM: '1', GIT_CEILING_DIRECTORIES: os.tmpdir() };
  for (const k of ['GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL', 'EMAIL']) delete env[k];
  Object.assign(env, extraEnv.env || {});
  return spawnSync('bash', [path.join(ROOT, 'pipeline', 'forge_citizen.sh'), 'testme'], { encoding: 'utf8', cwd: home, env });
}

const author = d => spawnSync('git', ['-C', d, 'log', '-1', '--format=%an <%ae>'], { encoding: 'utf8' }).stdout.trim();
const committer = d => spawnSync('git', ['-C', d, 'log', '-1', '--format=%cn <%ce>'], { encoding: 'utf8' }).stdout.trim();

test('forge_citizen: no git identity fails before anything is written', () => {
  const { forge: root, d } = forgeDir();
  const r = forge(root, {});
  assert.equal(r.status, 1);
  assert.match(r.stdout, /"ok":false,"err":"no git identity/);
  assert.ok(!fs.existsSync(path.join(d, 'CLAUDE.md')), 'no file may be generated');
});

test("forge_citizen: the caller's git config signs the birth commit", () => {
  const { forge: root, d } = forgeDir();
  const r = forge(root, { gitconfig: '[user]\n\tname = Config Caller\n\temail = caller@example.invalid\n' });
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /"ok":true/);
  assert.equal(author(d), 'Config Caller <caller@example.invalid>');
  assert.equal(committer(d), 'Config Caller <caller@example.invalid>');
});

test('forge_citizen: a lone GIT_COMMITTER_* variable does not mix a second identity into the commit', () => {
  const config = '[user]\n\tname = Config Caller\n\temail = caller@example.invalid\n';
  const cases = [
    [{ GIT_COMMITTER_NAME: 'Other Name' }, config, 'Config Caller <caller@example.invalid>'],
    [{ GIT_COMMITTER_EMAIL: 'other@example.invalid' }, config, 'Config Caller <caller@example.invalid>'],
    [{ GIT_AUTHOR_NAME: 'Env Caller', GIT_AUTHOR_EMAIL: 'env@example.invalid', GIT_COMMITTER_EMAIL: 'other@example.invalid' },
      '', 'Env Caller <env@example.invalid>'],
  ];
  for (const [env, gitconfig, who] of cases) {
    const { forge: root, d } = forgeDir();
    const r = forge(root, { gitconfig, env });
    assert.equal(r.status, 0, r.stdout + r.stderr);
    assert.equal(author(d), who, JSON.stringify(env));
    assert.equal(committer(d), who, JSON.stringify(env));
  }
});

test('forge_citizen: one GIT_AUTHOR_* variable without the other is refused before anything is written', () => {
  const { forge: root, d } = forgeDir();
  const r = forge(root, { gitconfig: '[user]\n\tname = Config Caller\n\temail = caller@example.invalid\n',
    env: { GIT_AUTHOR_NAME: 'Env Caller' } });
  assert.equal(r.status, 1);
  assert.match(r.stdout, /"ok":false,"err":"GIT_AUTHOR_NAME and GIT_AUTHOR_EMAIL must be set together/);
  assert.ok(!fs.existsSync(path.join(d, 'CLAUDE.md')), 'no file may be generated');
});

test('forge_citizen: GIT_AUTHOR_NAME / GIT_AUTHOR_EMAIL sign it when set', () => {
  const { forge: root, d } = forgeDir();
  const r = forge(root, { env: { GIT_AUTHOR_NAME: 'Env Caller', GIT_AUTHOR_EMAIL: 'env@example.invalid' } });
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.equal(author(d), 'Env Caller <env@example.invalid>');
  assert.equal(committer(d), 'Env Caller <env@example.invalid>');
});
