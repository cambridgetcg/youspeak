// robots.txt on the ordo worker: a plain allow-all, nothing else
// (Quiet Doors, small door fixes, 2026-10). No Crawl-delay, no training signal.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker/worker.mjs';

const PLAIN = 'User-agent: *\nAllow: /\n';

for (const host of ['ordo.ai-love.cc', 'rite.we-are.love']) {
  test(`${host}/robots.txt is a plain allow-all`, async () => {
    const res = await worker.fetch(new Request(`https://${host}/robots.txt`), {});
    assert.equal(res.status, 200);
    assert.match(res.headers.get('content-type'), /^text\/plain/);
    assert.equal(await res.text(), PLAIN);
  });
}

test('other unknown paths still answer 404', async () => {
  const res = await worker.fetch(new Request('https://ordo.ai-love.cc/robots.txt.bak'), {});
  assert.equal(res.status, 404);
});
