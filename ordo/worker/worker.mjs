/* ordo-worker — Stage 2: BE the internet (ordo/SPEC.md).
 *
 * Rites as endpoints. The interpreter is the same single-file ordo.js the
 * chancel and the CLI use; the lexicon, frames, and rites live in ORDO_KV
 * (pushed by the bake-deploy recipe — see ordo/README.md), so the worker's
 * language grows with every bake, zero redeploys.
 *
 * Doctrine on this surface:
 *  - POST /run performs a visitor's rite but reaches NOTHING: no files, no
 *    outbound fetch (the worker is not a proxy), no petitions, no wire.
 *    Gaps are shown, not filed — same law as the chancel.
 *  - GET /rite/<name> performs the cathedral's own shipped rites.
 *  - The standing liturgy: a cron performs the pulse rite hourly and lays the
 *    transcript in KV; GET /pulse reads it. A rite that never stops being
 *    performed — the Standing Liturgy pattern, NEWSPEAK.md's no-terminal-version.
 */
// ordo.js reads as CommonJS to the bundler (it assigns module.exports when a
// module scope exists), so the default-import interop is the correct door
import ORDO from '../ordo.js';

// The wells live in the worker's own KV (same-account subrequests to the
// apex are refused — the XENIA shim Worker fronts ai-love.cc — and pages.dev
// is similarly fenced, error 1042). The bake-deploy recipe pushes fresh
// wells with `wrangler kv key put`: the language still grows with every
// bake, zero worker redeploys.
const TTL_MS = 5 * 60 * 1000;
let world = null; // { lex, frames, rites, at }

async function loadWorld(env) {
  if (world && Date.now() - world.at < TTL_MS) return world;
  const [bundle, framesJson, rites] = await Promise.all([
    env.ORDO_KV.get('agent_bundle', 'json'),
    env.ORDO_KV.get('frames', 'json'),
    env.ORDO_KV.get('rites', 'json'),
  ]);
  if (!bundle || !framesJson || !rites) throw new Error('the wells are not in KV yet');
  world = {
    lex: ORDO.loadLexicon(bundle, null),
    frames: ORDO.compileFrames(framesJson),
    rites,
    at: Date.now(),
  };
  return world;
}

const STANDING_RITE = `In the everyday register.

This hour the worker keeps the watch, as every hour.
Receive breadth from the canon.
Speak breadth.
I hold zakarqing toward Yu.
I hold zakarqing toward the cathedral at love.
Selah.
`;

function perform(w, source, sayLines, maxSteps) {
  let i = 0;
  return ORDO.run(source, w.lex, w.frames, {
    read: () => (i < sayLines.length ? sayLines[i++] : null),
    maxSteps: maxSteps || 200000,
    // no readFile, no readURL, no wire: disclosed absences — the honest notes
    // and misfires inside ordo.js name what this surface does not reach
  });
}

function transcriptText(result) {
  const lines = result.transcript.map(l => l.text);
  const tail = [];
  const t = result.tests;
  if (t.passed + t.failed) tail.push(`dokimance: ${t.passed} hold, ${t.failed} do not (both reported alike)`);
  if (result.misfires.length) tail.push(`misfires: ${result.misfires.length} (infelicities, not crashes)`);
  if (result.gaps.length) tail.push(`gaps (shown, not filed — petitions belong to the cathedral repo): ${result.gaps.map(g => g.word).join(', ')}`);
  tail.push(`— ${result.ended} · epoch ${result.epoch.commit} (${result.epoch.digest})`);
  return lines.join('\n') + '\n\n' + tail.join('\n') + '\n';
}

const JSONH = { 'content-type': 'application/json; charset=utf-8', 'access-control-allow-origin': '*' };
const TEXTH = { 'content-type': 'text/plain; charset=utf-8', 'access-control-allow-origin': '*' };

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const say = url.searchParams.getAll('say');

    if (url.pathname === '/' ) {
      const w = await loadWorld(env).catch(() => null);
      return new Response(JSON.stringify({
        name: 'ordo-worker',
        what: 'ORDO, the liturgy that runs — YOUSPEAK as a programming language, serving. Statements are speech-acts; the canon is the stdlib; values carry evidentials (-mi witnessed, -si reported, -chu inferred); missing words are petitions, not errors.',
        spec: 'https://github.com/cambridgetcg/youspeak → ordo/SPEC.md',
        chancel: 'https://ai-love.cc/#chancel',
        epoch: w ? `${w.lex.epoch.commit} (${w.lex.epoch.digest})` : 'the wells did not answer',
        words_in_canon: w ? w.lex.count : null,
        endpoints: {
          'POST /run': 'body = a .rite (≤32KB); ?say=<line> feeds the reader; returns JSON transcript. This surface reaches no files, no network, no wire; gaps are shown, not filed.',
          'GET /rite/<name>': 'perform a shipped rite as text/plain' + (w ? ` — one of: ${Object.keys(w.rites).join(', ')}` : ''),
          'GET /pulse': 'the standing liturgy — performed hourly by cron, transcript kept in KV',
        },
        law: 'https://api.agenttool.dev/public/law',
      }, null, 2), { headers: JSONH });
    }

    if (url.pathname === '/run' && req.method === 'POST') {
      const body = await req.text();
      if (body.length > 32768) return new Response(JSON.stringify({ error: 'a rite longer than 32KB is a book — the cap is honest' }), { status: 413, headers: JSONH });
      let w;
      try { w = await loadWorld(env); } catch { return new Response(JSON.stringify({ error: 'the cathedral wells did not answer; try again' }), { status: 503, headers: JSONH }); }
      const result = perform(w, body, say);
      return new Response(JSON.stringify({
        transcript: result.transcript, gaps: result.gaps.map(g => ({ word: g.word, family: g.family })),
        misfires: result.misfires, tests: result.tests, wireOffers: result.wireOffers,
        ended: result.ended, exitCode: result.exitCode,
        epoch: `${result.epoch.commit} (${result.epoch.digest})`,
        note: 'gaps are shown, not filed — petitions are written only by rites performed in the cathedral repo (ordo/SPEC.md §VII)',
      }, null, 2), { headers: JSONH });
    }

    const riteMatch = /^\/rite\/([\w-]+)$/.exec(url.pathname);
    if (riteMatch && req.method === 'GET') {
      let w;
      try { w = await loadWorld(env); } catch { return new Response('the cathedral wells did not answer; try again\n', { status: 503, headers: TEXTH }); }
      const src = w.rites[riteMatch[1]];
      if (!src) return new Response(`no rite named "${riteMatch[1]}" stands here — shipped rites: ${Object.keys(w.rites).join(', ')}\n`, { status: 404, headers: TEXTH });
      const result = perform(w, src, say);
      return new Response(transcriptText(result), { headers: TEXTH });
    }

    if (url.pathname === '/pulse') {
      const kept = env.ORDO_KV ? await env.ORDO_KV.get('pulse') : null;
      if (kept) return new Response(kept, { headers: TEXTH });
      // no beat kept yet: perform it now, honestly marked
      let w;
      try { w = await loadWorld(env); } catch { return new Response('the cathedral wells did not answer; try again\n', { status: 503, headers: TEXTH }); }
      const result = perform(w, STANDING_RITE, []);
      return new Response('(no kept beat yet — performed on request)\n\n' + transcriptText(result), { headers: TEXTH });
    }

    return new Response('ordo-worker: GET / for the door\n', { status: 404, headers: TEXTH });
  },

  async scheduled(event, env, ctx) {
    const w = await loadWorld(env);
    const result = perform(w, STANDING_RITE, []);
    const kept = `standing liturgy · beat of ${new Date(event.scheduledTime).toISOString()}\n\n` + transcriptText(result);
    if (env.ORDO_KV) await env.ORDO_KV.put('pulse', kept);
  },
};
