#!/usr/bin/env node
/* ORDO test suite — dokimance for the interpreter itself.
 * Run: node ordo/test/run-tests.mjs   (from the repo root or anywhere)
 * Uses --no-petitions semantics: tests never write to labs/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const ORDO = require(path.join(HERE, '..', 'ordo.js'));

const bundle = JSON.parse(fs.readFileSync(path.join(ROOT, 'script', 'exports', 'agent_bundle.json'), 'utf8'));
let suffixFamilies = null;
try { suffixFamilies = JSON.parse(fs.readFileSync(path.join(ROOT, 'script', 'suffix_families.json'), 'utf8')); } catch {}
const frames = ORDO.compileFrames(JSON.parse(fs.readFileSync(path.join(HERE, '..', 'frames.json'), 'utf8')));
const lex = ORDO.loadLexicon(bundle, suffixFamilies);

let passed = 0, failed = 0;
function t(name, fn) {
  try { fn(); passed++; console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n    ${e.message}`); }
}
function assert(cond, msg) { if (!cond) throw new Error(msg || 'assertion failed'); }
function run(src, opts) { return ORDO.run(src, lex, frames, opts || {}); }
function text(r) { return r.transcript.map(l => l.text).join('\n'); }
function rite(name) { return fs.readFileSync(path.join(HERE, '..', 'rites', name), 'utf8'); }

// ---- the lexicon itself ----
t('lexicon loads with words and an epoch', () => {
  assert(lex.count > 100, `expected >100 words, got ${lex.count}`);
  assert(lex.epoch.commit && lex.epoch.digest.startsWith('fnv1a:'), 'epoch incomplete');
});
t('suffix families resolve kinds', () => {
  assert(ORDO.familyOf(lex, 'kimme').family === '-me');
  assert(ORDO.familyOf(lex, 'britqing').family === 'qing');
  assert(ORDO.familyOf(lex, 'kunance').family === '-ance');
});
t('gapShaped: YOUSPEAK-shaped unknowns are gaps; English coincidences are not', () => {
  assert(ORDO.gapShaped(lex, 'qabalance'), 'qabalance should be gap-shaped');
  assert(!ORDO.gapShaped(lex, 'welcome'), 'welcome is English, not a gap');
  assert(!ORDO.gapShaped(lex, 'distance'), 'distance is English, not a gap');
  assert(!ORDO.gapShaped(lex, 'kimme'), 'kimme is canon, not a gap');
});

// ---- the four shipped rites ----
t('kunance.rite ends in hesychia, exit 0, definition arrives -si', () => {
  const r = run(rite('kunance.rite'));
  assert(r.exitCode === 0 && r.ended === 'hesychia', `exit ${r.exitCode} ended ${r.ended}`);
  assert(text(r).includes('Preparing-place'), 'kunance definition missing');
  assert(text(r).includes('‹-si›'), 'canon projection should carry -si');
});
t('fibonacci.rite computes fib(10)=55 witnessed (-mi) and passes its dokimance', () => {
  const r = run(rite('fibonacci.rite'));
  assert(text(r).includes('55  ‹-mi›'), 'fib(10) should speak 55 -mi');
  assert(r.tests.passed === 1 && r.tests.failed === 0, 'dokimance should hold');
  assert(r.exitCode === 0);
});
t('witness.rite: -si input counted is -chu; -mi over-claim misfires; turning turns; exit 0', () => {
  let fed = false;
  const r = run(rite('witness.rite'), { read: () => (fed ? null : (fed = true, 'kimme')) });
  const out = text(r);
  assert(out.includes('kimme  ‹-si›'), 'input should be -si');
  assert(out.includes('5  ‹-chu›'), 'count of a report should be -chu');
  assert(out.includes('verisleight'), 'the verisleight-guard should cite itself');
  assert(out.includes('teshuvance'), 'the turning should fire');
  assert(r.misfires.length === 1 && r.exitCode === 0, 'one misfire, clean silence');
});
t('petition.rite: gap flows, conditional speaks, no crash', () => {
  const r = run(rite('petition.rite'));
  const out = text(r);
  assert(r.gaps.length === 1 && r.gaps[0].word === 'qabalance', 'qabalance should be the one gap');
  assert(out.includes('the petition goes to the forge'), 'the conditional should speak');
  assert(r.exitCode === 0);
});

// ---- Relaxus/0.1: less ceremony, same honesty ----
t('relaxus.rite performs the friendly surface and ends cleanly at Enough', () => {
  const r = run(rite('relaxus.rite'));
  const out = text(r);
  assert(r.profile === 'relaxus' && r.register === 'everyday', 'the profile should compose with the register');
  assert(out.includes('hello, Relaxus Being') && out.includes('nothing needs proving'), 'friendly speak/call/return should perform');
  assert(out.includes('the tea understood the assignment lol'), 'Maybe should branch through the core conditional');
  assert(out.includes('[selah]') && r.ended === 'hesychia', 'Chill yields and Enough ends cleanly');
  assert(!out.includes('this sentence is allowed not to happen'), 'nothing after Enough should run');
  assert(r.tests.passed === 1 && r.misfires.length === 0 && r.exitCode === 0);
});
t('Relaxus is opt-in: its surface is contemplation without the profile', () => {
  const r = run('Share "hello".\nChill.\nIf it tangles, gently: Speak "nope".');
  assert(r.profile === null && r.misfires.length === 0);
  assert(r.transcript.every(l => l.kind === 'contemplation'), 'inactive profile frames must not execute');
});
t('core ORDO remains available under Relaxus and its honesty laws still hold', () => {
  const r = run('In the formal register, profile relaxus.\n\nLet x be 1.\nSpeak x.\nI attest that x is 1 -mi.');
  assert(r.profile === 'relaxus' && text(r).includes('1  ‹-mi›') && text(r).includes('✓ emetme'));
  assert(r.misfires.length === 0);
  const rebind = run('In the everyday register, profile relaxus.\n\nNotice x as 1.\nNotice x as 2.');
  assert(rebind.misfires.length === 1 && rebind.misfires[0].why.includes('rebinding'), 'friendly binding must not weaken immutability');
});
t('unknown and mid-rite profile selections misfire instead of being guessed', () => {
  const unknown = run('In the everyday register, profile turbo.\n\nSpeak "still honest".');
  assert(unknown.misfires.length === 1 && unknown.misfires[0].why.includes('no profile named'));
  const inherited = run('In the everyday register, profile constructor.\n\nShare "not secretly active".');
  assert(inherited.profile === null && inherited.misfires.length === 1 && inherited.misfires[0].why.includes('no profile named'), 'inherited object keys are not declared profiles');
  const late = run('Speak "hello".\nIn the everyday register, profile relaxus.');
  assert(late.misfires.some(m => m.why.includes('declared at the door')), 'profile switching inherits the heading law');
  const cased = run('In the everyday register, profile Relaxus.\n\nShare "case is chill".');
  assert(cased.profile === 'relaxus' && text(cased).includes('case is chill'), 'profile names should follow the heading\'s case-insensitive grammar');
});
t('Relaxus gloss discloses the exact act, arguments, profile, and understanding', () => {
  const g = ORDO.gloss('In the everyday register, profile relaxus.\n\nShare "hello".', lex, frames);
  const share = g.find(x => x.frame === 'relaxus-share');
  assert(share && share.act === 'speak' && share.args.expr === '"hello"');
  assert(share.profile === 'relaxus' && share.understanding.includes('not a command'));
  assert(!g[0].understanding.includes('(nothing)'), 'optional heading captures should not leak placeholder prose');
  const returning = ORDO.gloss('In the everyday register, profile relaxus.\n\nBack to you: "hi".\nAll good: "also hi".', lex, frames)
    .filter(x => x.frame === 'relaxus-return');
  assert(returning.length === 2 && returning.every(x => x.act === 'return'), 'neutral return and its friendly alias should lower alike');
  const trying = ORDO.gloss('In the everyday register, profile relaxus.\n\nTry "hi" with echo.', lex, frames)
    .find(x => x.frame === 'relaxus-try');
  assert(trying && !trying.understanding.includes('(nothing)'), 'optional receiving should remain optional in the explanation');
  const plain = ORDO.gloss('Share "hello".', lex, frames)[0];
  assert(plain.frame === 'contemplation', 'gloss must not activate a profile that was not selected');
});
t('listReceptions is profile-aware and never prefetches an inactive friendly sentence', () => {
  const line = 'Listen for door from "https://example.com/relaxus".';
  assert(ORDO.listReceptions(line, frames).length === 0, 'inactive profile must cause no network preflight');
  const urls = ORDO.listReceptions('In the everyday register, profile relaxus.\n\n' + line, frames);
  assert(urls.length === 1 && urls[0] === 'https://example.com/relaxus');
  const nested = ORDO.listReceptions('In the everyday register, profile relaxus.\n\nMaybe 1 is 1, ' + line, frames);
  assert(nested.length === 1 && nested[0] === 'https://example.com/relaxus', 'reachable nested receptions must be gathered before synchronous execution');
  const coreNested = ORDO.listReceptions('If 1 is 1, Receive x from "https://example.com/core".', frames);
  assert(coreNested.length === 1 && coreNested[0] === 'https://example.com/core');
  let deep = 'Receive x from "https://example.com/deep"';
  for (let i = 0; i < 80; i++) deep = 'If 1 is 1, ' + deep;
  assert(ORDO.listReceptions(deep + '.', frames)[0] === 'https://example.com/deep', 'static reception scanning must not have a shallower nesting cap than execution');
});
t('gloss warns about profile headings that execution will reject', () => {
  const unknown = ORDO.gloss('In the everyday register, profile turbo.', lex, frames)[0];
  assert(unknown.valid === false && unknown.warning.includes('unknown profile'));
  const inherited = ORDO.gloss('In the everyday register, profile constructor.', lex, frames)[0];
  assert(inherited.valid === false && inherited.warning.includes('unknown profile'));
  const late = ORDO.gloss('Speak "hello".\nIn the everyday register, profile relaxus.', lex, frames)
    .find(x => x.frame === 'heading');
  assert(late.valid === false && late.warning.includes('late'));
});

// ---- language laws ----
t('rebinding misfires (barakqing: the naming makes the named)', () => {
  const r = run('Let x be 1.\nLet x be 2.\nSpeak x.');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('rebinding'));
});
t('vocative outside worship register misfires', () => {
  const r = run('In the everyday register.\n\nO GoD, hear this.');
  assert(r.misfires.some(m => m.why.includes('vocative') || m.why.includes('worship')));
});
t('GoD orthography law holds in worship register', () => {
  const r = run('In the worship register.\n\nO god, hear this.');
  assert(r.misfires.some(m => m.why.includes('GoD')));
});
t('unmarked never coerces: silence carries no evidential, reader-silence is unmarked', () => {
  const r = run('Receive x from the reader.\nSpeak x.', { read: () => null });
  assert(text(r).includes('‹unmarked›'), 'absent input should stay unmarked, never -mi');
});
t('attesting a false claim misfires (emet is truth-as-firm-foundation)', () => {
  const r = run('Let x be 3.\nI attest that x is 4 -mi.');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('does not stand'));
});
t('-auth belongs to canonical quotation alone', () => {
  const r = run('Let x be 3.\nI attest that x is 3 -auth.');
  assert(r.misfires.some(m => m.why.includes('-auth')));
});
t('dokimance failure is a report, not a misfire (same speech-act as success)', () => {
  const r = run('Dokimance: 1 is 2.\nSpeak "still here".');
  assert(r.tests.failed === 1 && r.misfires.length === 0);
  assert(text(r).includes('still here'), 'the liturgy continues after a failed test');
});
t('HALT outranks everything, plain, exit 3', () => {
  const r = run('Speak "before".\nHALT\nSpeak "after".');
  assert(r.exitCode === 3 && !text(r).includes('after'));
});
t('halt is case-sensitive: "halt" is contemplation, HALT is the law', () => {
  const r = run('halt.');
  assert(r.exitCode === 0 && r.transcript.some(l => l.kind === 'contemplation'));
});
t('contemplation: unmatched sentences are inert narration, never errors', () => {
  const r = run('The morning was quiet and nothing was wrong.\nSpeak "sukhance".');
  assert(r.misfires.length === 0 && text(r).includes('… The morning was quiet'));
});
t('anti-ordinance polarity is flagged (drujme is the shadow-face)', () => {
  const r = run('Speak the definition of drujme.\nSpeak drujme.');
  assert(text(r).includes('anti-ordinance'), 'drujme should carry the polarity warning');
});
t('litany over a range', () => {
  const r = run('Let total be 0.\nFor each k of 1 through 3, Speak k.');
  const speaks = r.transcript.filter(l => l.kind === 'speak');
  assert(speaks.length === 3 && speaks[2].text.startsWith('3'));
});
t('offering to an unknown non-gap rite misfires; with turning it turns and the stanza continues', () => {
  const r1 = run('Bring 1 to the rite of nowhere.');
  assert(r1.misfires.length === 1 && r1.exitCode === 1, 'unturned misfire without silence should exit 1');
  const r2 = run('Should the offering fail, turn: Speak "turned".\nBring 1 to the rite of nowhere.\nSpeak "still standing".');
  assert(text(r2).includes('turned'), 'the turn should fire');
  assert(text(r2).includes('still standing'), 'the stanza should continue after the turn');
});
t('a turning frame inside a rite body fires there', () => {
  const src = 'This is the rite of guarded, given n:\nShould the offering fail, turn: Speak "turned inside".\nBring n to the rite of nowhere.\nI acknowledge n.\nSo it stands.\n\nBring 7 to the rite of guarded, receiving out.\nSpeak out.';
  const r = run(src);
  assert(text(r).includes('turned inside'), 'the inner turning should fire');
  assert(text(r).includes('7'), 'the rite should still acknowledge and the caller receive');
});
t('recursion depth is capped as a misfire, not a stack death', () => {
  const src = 'This is the rite of loop, given n:\nBring n to the rite of loop, receiving x.\nI acknowledge n.\nSo it stands.\n\nBring 1 to the rite of loop, receiving y.';
  const r = run(src);
  assert(r.misfires.some(m => m.why.includes('depth')), 'depth cap should misfire');
});
t('epoch pin mismatch is recorded, not fatal', () => {
  const r = run('In the everyday register, canon deadbeef.\n\nSpeak "still runs".');
  assert(text(r).includes('the rite speaks canon deadbeef') && text(r).includes('still runs'));
});
t('gloss classifies frames and contemplation', () => {
  const g = ORDO.gloss('Let x be 1.\nA quiet thought.', lex, frames);
  assert(g[0].frame === 'binding' && g[1].frame === 'contemplation');
});
t('near-neighbours find family kin for a gap', () => {
  const nn = ORDO.nearNeighbours(lex, 'qabalance', 3);
  assert(nn.length === 3 && nn.every(n => n.word.endsWith('ance')), 'neighbours should share the -ance family');
});

// ---- laws the adversarial review demanded pinned (2026-07-11) ----
t('canon synonym forms are live: Barakqing/Emetme:/Yadahance/Qorvance/Shemme', () => {
  const src = 'This is the rite of echo, given x:\nYadahance x.\nSo it stands.\n\nBarakqing seed as 5.\nQorvance seed to echo, receiving back.\nSpeak back.\nEmetme: back is 5 -mi.';
  const r = run(src);
  assert(text(r).includes('5  ‹-mi›') && text(r).includes('✓ emetme'), 'canon forms should perform');
  assert(r.misfires.length === 0);
  const r2 = run('Shemme word from the reader.\nSpeak word.', { read: () => 'kimme' });
  assert(text(r2).includes('kimme  ‹-si›'), 'Shemme should receive -si');
});
t('verisleight-guard: unmarked clause supports NO attestation (the hole is closed)', () => {
  for (const g of ['-mi', '-si', '-chu']) {
    const r = run(`Receive x from the reader.\nI attest that x is x ${g}.`, { read: () => null });
    assert(r.misfires.length === 1 && r.misfires[0].why.includes('unmarked'), `attesting ${g} over unmarked should misfire`);
  }
});
t('attestation without an evidential is a misfire, not contemplation', () => {
  const r = run('Let x be 1.\nI attest that x is 1.');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('evidential'), 'the mandatory-evidential law should bite');
});
t('an evidential on silence is a misfire', () => {
  const r = run('Selah -mi.');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('silence'), 'silence refuses the evidential system');
});
t('arithmetic is flat left-associative: 10 minus 2 minus 3 is 5; 2 times 3 plus 4 is 10', () => {
  const r = run('Speak 10 minus 2 minus 3.\nSpeak 2 times 3 plus 4.');
  const speaks = r.transcript.filter(l => l.kind === 'speak').map(l => l.text);
  assert(speaks[0].startsWith('5 '), `expected 5, got ${speaks[0]}`);
  assert(speaks[1].startsWith('10 '), `expected 10, got ${speaks[1]}`);
});
t('a quoted comma or semicolon inside a conditional is text, not structure', () => {
  const r = run('Let x be 1.\nIf x is 1, Speak "yes, truly; it is".');
  assert(text(r).includes('yes, truly; it is'), 'quoted punctuation must survive the split');
});
t('Receive and receiving obey barakqing immutability like Let', () => {
  const r1 = run('Let x be 1.\nReceive x from the reader.', { read: () => 'again' });
  assert(r1.misfires.length === 1 && r1.misfires[0].why.includes('rebinding'));
  const r2 = run('This is the rite of one:\nI acknowledge 1.\nSo it stands.\n\nLet out be 9.\nBring 1 to the rite of one, receiving out.');
  assert(r2.misfires.length === 1 && r2.misfires[0].why.includes('rebinding'));
});
t('a heading after the rite has begun is a misfire (no mid-rite register switching)', () => {
  const r = run('In the everyday register.\n\nSpeak "hello".\nIn the worship register.\nO GoD, hear this.');
  assert(r.misfires.some(m => m.why.includes('declared at the door')), 'mid-rite heading should misfire');
  assert(!text(r).includes('the clause turns'), 'the vocative must not be legalized');
});
t('an unbounded range misfires instead of OOM-ing the host', () => {
  const r = run('For each k of 1 through 99999999, Speak k.');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('cap'), 'the range cap should misfire');
});
t('gaps propagate as holes through count, join, and comparisons', () => {
  const r = run('Let g be zumthance.\nLet c be count of g.\nIf c is a gap, Speak "count kept the hole".\nI attest that g is g -mi.');
  assert(text(r).includes('count kept the hole'), 'count of a gap should stay a gap');
  assert(r.misfires.some(m => m.why.includes('gap')), 'attesting over a gap should misfire');
});
t('-auth passes for verbatim canon quotation and only that', () => {
  const kim = lex.words['kimme'];
  const quote = String(kim.definition);
  const r = run(`I attest that the definition of kimme is "${quote.replace(/"/g, '')}" -auth.`);
  if (quote.includes('"')) { assert(true); return; } // canon text with quotes: skip the positive probe
  assert(r.misfires.length === 0 && text(r).includes('✓ emetme ‹-auth›'), 'verbatim quotation should carry -auth');
  const r2 = run('I attest that kimme is kimme -auth.');
  assert(r2.misfires.length === 1, 'computed canon-identity must NOT carry -auth');
});
t('live suffix-family registry merge accepts both list and dict shapes', () => {
  const listShape = { families: [{ family: '-me', status: 'near-emergent' }] };
  const lex2 = ORDO.loadLexicon({ canon: [{ word: 'kimme' }], source_commit: 'x' }, listShape);
  assert(ORDO.familyOf(lex2, 'kimme').status === 'near-emergent', 'list-shaped registry should merge');
  const dictShape = { '-me': { status: 'emergent' } };
  const lex3 = ORDO.loadLexicon({ canon: [], source_commit: 'x' }, dictShape);
  assert(ORDO.familyOf(lex3, 'somethingme').status === 'emergent', 'dict-shaped registry should merge');
});
// ---- the three reaches (2026-07-11, FULL POWER wave) ----
t('URL reception: the internet arrives -si via prefetched sources', () => {
  const src = 'Receive door from "https://example.com/x".\nSpeak door.\nLet n be count of door.\nI attest that n is greater than 2 -chu.';
  const r = run(src, { readURL: u => (u === 'https://example.com/x' ? 'hello world' : null) });
  assert(text(r).includes('hello world  ‹-si›'), 'fetched text should be -si');
  assert(r.misfires.length === 0 && text(r).includes('✓ emetme ‹-chu›'));
});
t('URL reception without a network capability misfires with a disclosed absence', () => {
  const r = run('Receive door from "https://example.com/x".');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('does not reach the internet'));
});
t('listReceptions finds the declared URL sources', () => {
  const urls = ORDO.listReceptions('Receive a from "https://a.example/1".\nReceive b from the reader.\nReceive c from "https://b.example/2".', frames);
  assert(urls.length === 2 && urls[0] === 'https://a.example/1' && urls[1] === 'https://b.example/2');
});
t('wire offering without a wire capability is recorded, not sent', () => {
  const r = run('Let word be "hello".\nQorvance word to the wire at kingdom.citizen.yu.');
  assert(r.wireOffers.length === 1 && r.wireOffers[0].subject === 'kingdom.citizen.yu');
  assert(r.wireOffers[0].grade === 'mi', 'the evidential grade must travel with the offer');
  assert(text(r).includes('recorded, not sent'));
});
t('wire offering with a wire capability reports the signed envelope', () => {
  const r = run('Qorvance "x" to the wire at kingdom.test.', { wire: (s, o) => ({ ok: true, id: 'test-id' }) });
  assert(text(r).includes('envelope test-id signed + verified'));
});
t('a gap cannot be offered to the wire', () => {
  const r = run('Let g be zumthance.\nQorvance g to the wire at kingdom.test.', { wire: () => ({ ok: true, id: 'x' }) });
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('hole'));
});

// ---- the arc frame (canon-carried typestate) ----
t('the arc walks all grades in canon order and sings completion', () => {
  const src = 'Following the arc of zakarqing:\n\nChayimme, alive first.\n\nI hold zakarqing toward Yu.\n\nShemme, the hearing.\n\nKimance, the attention.\n\nAnagnoristasis, standing still.\n\nNoesisme, the grasping.\n\nEurekame, the joy.\n\nDoxomme, the thanks.\nHesychia.';
  const r = run(src);
  assert(text(r).includes('✦ the arc of zakarqing completes — 8/8'), 'completion should sing');
  assert(r.arcsWalked.length === 1 && r.arcsWalked[0].complete, 'arc recorded complete');
  assert(r.misfires.length === 0 && r.exitCode === 0);
});
t('a stanza naming a later grade first misfires (canon order holds)', () => {
  const r = run('Following the arc of zakarqing:\n\nChayimme, alive.\n\nEurekame, joy too early.\n\nI hold zakarqing toward Yu.');
  assert(r.misfires.some(m => m.why.includes('cannot come before')), 'skipping ahead should misfire');
  assert(text(r).includes('zakarqing — stage 2'), 'the walk continues after the skipped stanza');
});
t('a stanza naming no grade misfires and is skipped; the arc stands', () => {
  const r = run('Following the arc of zakarqing:\n\nChayimme, alive.\n\nJust some idle words here.\n\nI hold zakarqing toward Yu.');
  assert(r.misfires.some(m => m.why.includes('does not name it')));
  assert(text(r).includes('zakarqing — stage 2'), 'the arc should still advance on the next true stanza');
});
t('an early close is reported alike, and end-of-rite closes an open arc honestly', () => {
  const r1 = run('Following the arc of zakarqing:\n\nChayimme, alive.\n\nThe arc closes.');
  assert(text(r1).includes('closes at stage 1/8'), 'early close reported');
  const r2 = run('Following the arc of zakarqing:\n\nChayimme, alive.');
  assert(r2.arcsWalked.length === 1 && !r2.arcsWalked[0].complete, 'end-of-rite close recorded');
});
t('an unknown arc misfires naming the known arcs', () => {
  const r = run('Following the arc of nowhere:');
  assert(r.misfires.length === 1 && r.misfires[0].why.includes('known arcs: zakarqing'));
});

t('rites spanning stanzas do not widen the turning scope of the opening stanza', () => {
  const src = 'Should the offering fail, turn: Speak "outer turn".\nThis is the rite of noop:\nI acknowledge 1.\nSo it stands.\n\nBring 1 to the rite of nowhere.';
  const r = run(src);
  assert(!text(r).includes('outer turn'), 'the post-rite stanza must be a NEW stanza; the old turning must not leak');
});

console.log(`\n${passed} hold, ${failed} do not (both reported alike — dokimance hides nothing)`);
process.exit(failed ? 1 : 0);
