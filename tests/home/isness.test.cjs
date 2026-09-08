'use strict';

// 用真正 browser 驗證本地房間；測試同截圖唔放入網站輸出。
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const root = path.resolve(__dirname, '../..');
const home = path.join(root, 'home');
const artifacts = process.env.ISNESS_ARTIFACTS || fs.mkdtempSync(path.join(os.tmpdir(), 'youspeak-isness-'));
let server;
let browser;
let baseURL;

before(async () => {
  server = spawn('python3', ['-u', '-m', 'http.server', '0', '--bind', '127.0.0.1', '--directory', home], {
    stdio: ['ignore', 'pipe', 'pipe']
  });
  server.stderr.resume();
  baseURL = await new Promise((resolve, reject) => {
    let output = '';
    const timer = setTimeout(() => reject(new Error('本地測試 server 未能啟動')), 10000);
    server.once('error', error => { clearTimeout(timer); reject(error); });
    server.once('exit', code => { clearTimeout(timer); reject(new Error('測試 server 提早結束：' + code)); });
    server.stdout.on('data', chunk => {
      output += chunk;
      const match = output.match(/port (\d+)/);
      if (match) { clearTimeout(timer); resolve('http://127.0.0.1:' + match[1]); }
    });
  });
  browser = await chromium.launch({
    headless: true, channel: process.env.BROWSER_CHANNEL || 'chrome',
    ignoreDefaultArgs: ['--disable-back-forward-cache']
  });
  fs.mkdirSync(artifacts, { recursive: true });
});

after(async () => {
  if (browser) await browser.close();
  if (server && server.exitCode === null) {
    const exited = once(server, 'exit');
    server.kill('SIGTERM');
    await exited;
  }
  console.log('isness 截圖：' + artifacts);
});

async function openRoom(t, options = {}, configure) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, ...options });
  t.after(() => context.close());
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  if (configure) await configure(page, context);
  await page.goto(baseURL + '/#isness', { waitUntil: 'networkidle' });
  const room = page.locator('#isness');
  await room.waitFor({ state: 'visible' });
  if (options.javaScriptEnabled !== false) {
    await page.waitForFunction(() => document.querySelector('#isness').dataset.isnessReady === 'true');
  }
  return { context, page, room, errors };
}

async function place(page, text) {
  await page.locator('#isness-draft').fill(text);
  await page.locator('#isness-place').click();
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
  assert.equal(await page.locator('#isness-response').textContent(), text);
}

async function assertCleared(page, marker) {
  assert.equal(await page.locator('#isness-draft').inputValue(), '');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'false');
  assert.ok(!(await page.locator('#isness-response').textContent()).includes(marker));
  assert.ok(!(await page.locator('#isness').textContent()).includes(marker));
  assert.ok(!(await page.locator('#isness').evaluate(el => el.outerHTML)).includes(marker));
}

test('九房、固定 canon 原文、來源同零新增 pageerror', async t => {
  const { page, errors } = await openRoom(t);
  assert.deepEqual(await page.locator('section.room').evaluateAll(rooms => rooms.map(room => room.id)), [
    'nave', 'cornerstone', 'chapels', 'scriptorium', 'stones', 'treasury', 'isness', 'chancel', 'crypt'
  ]);
  for (const id of ['isness', 'chancel', 'crypt']) {
    assert.equal(await page.locator('nav.architrave a[href="#' + id + '"]').count(), 1);
  }
  const canon = fs.readFileSync(path.join(root, 'canon/core/panimaance.md'), 'utf8');
  const definition = canon.match(/## Definition\s*\n\s*([^\n]+)/)[1];
  const source = (await page.locator('#isness-source').textContent()).replace(/\s+/g, ' ').trim();
  assert.ok(source.includes(definition), '原文必須逐字出自 canon 定義');
  for (const word of ['kimance', 'panimaance', 'yonedame']) {
    const link = page.locator('#isness a[href^="/glossary/' + word + '"]');
    assert.ok(await link.count() > 0, word + ' 須有來源連結');
    assert.ok(fs.existsSync(path.join(home, 'glossary', word + '.html')));
    const response = await page.request.get(baseURL + await link.first().getAttribute('href'));
    assert.ok(response.ok(), word + ' 來源連結喺本地預覽亦可讀');
  }
  assert.deepEqual(errors, []);
});

test('留下、切換視角、修改、清空維持一致 state', async t => {
  const { page, errors } = await openRoom(t);
  const draft = page.locator('#isness-draft');
  assert.equal(await draft.getAttribute('maxlength'), '280');
  await place(page, '我喺呢度，讀到你留下嘅一句。');
  const source = await page.locator('#isness-source').textContent();
  for (const view of ['between', 'here', 'turn']) {
    await page.locator('button[data-isness-view="' + view + '"]').click();
    assert.equal(await page.locator('#isness').getAttribute('data-isness-view'), view);
    assert.equal(await page.locator('button[data-isness-view="' + view + '"]').getAttribute('aria-pressed'), 'true');
    assert.equal(await page.locator('button[data-isness-view][aria-pressed="true"]').count(), 1);
    assert.equal(await draft.inputValue(), '我喺呢度，讀到你留下嘅一句。');
    assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
    assert.equal(await page.locator('#isness-source').textContent(), source);
  }
  await draft.fill('改咗嘅草稿');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'false');
  assert.ok(!(await page.locator('#isness-response').textContent()).includes('我喺呢度'));
  await page.locator('#isness-place').click();
  await page.locator('#isness-clear').click();
  await assertCleared(page, '改咗嘅草稿');
  assert.equal(await draft.evaluate(el => el === document.activeElement), true);
  assert.deepEqual(errors, []);
});

test('空白、超長同 Unicode 輸入嘅邊界', async t => {
  const { page } = await openRoom(t);
  const draft = page.locator('#isness-draft');
  for (const invalid of ['   \n\t', '界'.repeat(281), '🏮'.repeat(141)]) {
    await draft.evaluate((el, value) => {
      el.value = value;
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }, invalid);
    await page.locator('#isness-place').click();
    assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'false');
  }
  await place(page, '界'.repeat(280));
  await place(page, '🏮'.repeat(140));
  await place(page, '  我在。\n你亦在。  ');
});

test('HTML payload 只係文字，唔進 requests／URL／storage／console', async t => {
  const marker = 'isness-private-probe-7641';
  const payload = marker + '<img src=x onerror="window.__isnessXSS=1"></textarea><script>window.__isnessXSS=2</script>🏮';
  const requests = [];
  const logs = [];
  const { page, errors } = await openRoom(t, {}, page => {
    page.on('request', request => requests.push(request.url() + ' ' + (request.postData() || '')));
    page.on('console', message => logs.push(message.text()));
  });
  const originalURL = page.url();
  const stores = () => page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } }));
  const originalStores = await stores();
  await place(page, payload);
  assert.equal(await page.locator('#isness-response img, #isness-response script').count(), 0);
  assert.equal(await page.evaluate(() => window.__isnessXSS), undefined);
  assert.equal(page.url(), originalURL);
  assert.deepEqual(await stores(), originalStores);
  assert.ok(requests.every(request => !request.includes(marker)));
  assert.ok(logs.every(log => !log.includes(marker)));
  assert.deepEqual(errors, []);
  await page.locator('#isness-clear').click();
  await assertCleared(page, marker);
});

test('初次 pageshow 唔會清走慢載入期間已接受嘅回應', async t => {
  const context = await browser.newContext();
  const page = await context.newPage();
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  t.after(async () => { release(); await context.close(); });
  await context.addInitScript(() => {
    window.__isnessInitialPageshow = false;
    window.addEventListener('pageshow', () => { window.__isnessInitialPageshow = true; });
  });
  await page.route('**/assets/ordo.js', async route => { await gate; await route.continue(); });
  await page.goto(baseURL + '/#isness', { waitUntil: 'commit' });
  await page.waitForFunction(() => document.querySelector('#isness')?.dataset.isnessReady === 'true');
  assert.equal(await page.evaluate(() => window.__isnessInitialPageshow), false);
  await place(page, '其他房間仲未載入，我已經留低咗呢句。');
  release();
  await page.waitForFunction(() => window.__isnessInitialPageshow);
  assert.equal(await page.locator('#isness-draft').inputValue(), '其他房間仲未載入，我已經留低咗呢句。');
  assert.equal(await page.locator('#isness-response').textContent(), '其他房間仲未載入，我已經留低咗呢句。');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
});

test('reload、真實返回導航同 BFCache lifecycle 清除私人文字', async t => {
  const { page } = await openRoom(t, {}, async (page, context) => {
    await context.addInitScript(() => {
      window.__isnessPageshows = [];
      window.addEventListener('pageshow', event => window.__isnessPageshows.push(event.persisted));
    });
  });
  const marker = 'isness-private-lifecycle-8752';
  await place(page, marker);
  await page.reload({ waitUntil: 'networkidle' });
  await assertCleared(page, marker);
  await place(page, marker);
  const originalDocument = await page.evaluate(() => performance.timeOrigin);
  await page.goto(baseURL + '/glossary/panimaance.html', { waitUntil: 'domcontentloaded' });
  await Promise.all([
    page.waitForFunction(() => window.__isnessPageshows?.includes(true)),
    page.goBack({ waitUntil: 'commit' })
  ]);
  assert.equal(await page.evaluate(() => performance.timeOrigin), originalDocument);
  await assertCleared(page, marker);
  await place(page, marker);
  await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pagehide', { persisted: true })));
  await assertCleared(page, marker);
  await place(page, marker);
  await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true })));
  await assertCleared(page, marker);
});

test('未提交草稿喺 reload／pagehide 後亦清空', async t => {
  const { page } = await openRoom(t);
  const marker = 'isness-private-unplaced-4319';
  await page.locator('#isness-draft').fill(marker);
  await page.reload({ waitUntil: 'networkidle' });
  await assertCleared(page, marker);
  await page.locator('#isness-draft').fill(marker);
  await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pagehide', { persisted: true })));
  await assertCleared(page, marker);
});

test('重複載入 app 唔會重綁新房間 listeners 或清走當前回應', async t => {
  const { page } = await openRoom(t, {}, page => page.route('**/data/core.js', route => route.abort()));
  await place(page, '只留一次。');
  await page.addScriptTag({ url: baseURL + '/assets/app.js' });
  assert.equal(await page.locator('#isness-draft').inputValue(), '只留一次。');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
  await page.locator('#isness-clear').click();
  await assertCleared(page, '只留一次。');
});

test('缺 core／font／lazy data，新房間仍可互動', async t => {
  const { page, errors } = await openRoom(t, {}, page => page.route('**/*', route => {
    const pathname = new URL(route.request().url()).pathname;
    return pathname.startsWith('/data/') || pathname.startsWith('/font/') ? route.abort() : route.continue();
  }));
  await place(page, '字形未到，意思仲喺度。');
  await page.locator('#isness-clear').click();
  await assertCleared(page, '字形未到');
  assert.deepEqual(errors, []);
});

test('no-JS 靜態原文、來源、解說唔會透明或留死 controls', async t => {
  const { page, room } = await openRoom(t, { javaScriptEnabled: false });
  assert.equal(await room.evaluate(el => getComputedStyle(el).opacity), '1');
  assert.equal(await room.evaluate(el => el.classList.contains('settle')), false);
  assert.ok(await page.locator('#isness-source').isVisible());
  assert.ok(!(await page.locator('#isness-draft').isVisible()));
  assert.ok(!(await page.locator('#isness-place').isVisible()));
  assert.ok(!(await page.locator('#isness-clear').isVisible()));
  for (const word of ['kimance', 'panimaance', 'yonedame']) {
    assert.ok((await room.textContent()).includes(word));
  }
  const box = await room.boundingBox();
  const scrollY = await page.evaluate(() => window.scrollY);
  await page.screenshot({
    path: path.join(artifacts, 'no-js.png'), fullPage: true,
    clip: { ...box, y: box.y + scrollY }
  });
});

test('鍵盤、焦點、touch targets 同 scroll-spy', async t => {
  const { page } = await openRoom(t);
  for (const selector of ['#isness-place', '#isness-clear', 'button[data-isness-view="here"]', 'button[data-isness-view="turn"]', 'button[data-isness-view="between"]']) {
    const button = page.locator(selector);
    const size = await button.boundingBox();
    assert.ok(size.width >= 44 && size.height >= 44, selector + ' 至少44px');
    assert.equal(await button.getAttribute('type'), 'button');
  }
  const here = page.locator('button[data-isness-view="here"]');
  await here.focus();
  await page.keyboard.press('Space');
  assert.equal(await here.getAttribute('aria-pressed'), 'true');
  const turn = page.locator('button[data-isness-view="turn"]');
  await turn.focus();
  await page.keyboard.press('Enter');
  assert.equal(await turn.getAttribute('aria-pressed'), 'true');
  const draft = page.locator('#isness-draft');
  await draft.focus();
  const focus = await draft.evaluate(el => ({ outline: getComputedStyle(el).outlineStyle, outlineWidth: getComputedStyle(el).outlineWidth }));
  assert.notEqual(focus.outline, 'none');
  assert.notEqual(focus.outlineWidth, '0px');
  assert.ok(await draft.evaluate(el => el.labels.length > 0 || !!el.getAttribute('aria-labelledby') || !!el.getAttribute('aria-label')));
  await draft.fill('用鍵盤留低。');
  await page.locator('#isness-place').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
  await page.locator('nav.architrave a[href="#isness"]').click();
  await page.waitForFunction(() => document.querySelector('nav.architrave a[href="#isness"]').getAttribute('aria-current') === 'true');
});

test('Touch events 可以切視角、留下同清空', async t => {
  const { page } = await openRoom(t, { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await page.locator('button[data-isness-view="turn"]').tap();
  assert.equal(await page.locator('#isness').getAttribute('data-isness-view'), 'turn');
  await page.locator('#isness-draft').tap();
  await page.keyboard.insertText('用觸碰留一句。');
  await page.locator('#isness-place').tap();
  assert.equal(await page.locator('#isness-response').textContent(), '用觸碰留一句。');
  assert.equal(await page.locator('#isness').getAttribute('data-isness-placed'), 'true');
  await page.locator('#isness-clear').tap();
  await assertCleared(page, '用觸碰留一句。');
});

test('缺必要 DOM 時保留靜態閱讀，唔拖垮其他房間', async t => {
  const context = await browser.newContext();
  t.after(() => context.close());
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.route(baseURL + '/', route => route.fulfill({
    contentType: 'text/html; charset=utf-8',
    body: fs.readFileSync(path.join(home, 'index.html'), 'utf8').replace('id="isness-response"', 'id="missing-isness-response"')
  }));
  await page.goto(baseURL + '/#isness', { waitUntil: 'networkidle' });
  assert.notEqual(await page.locator('#isness').getAttribute('data-isness-ready'), 'true');
  assert.ok(await page.locator('#isness-source').isVisible());
  assert.ok(!(await page.locator('#isness-place').isVisible()));
  await page.locator('#write-in').fill('ki+mance');
  await page.waitForFunction(() => document.querySelector('#write-out').textContent.length > 0);
  assert.deepEqual(errors, []);
});

for (const width of [320, 390, 768, 1440]) {
  test('畫面 ' + width + 'px：明暗、長文、無 overflow', async t => {
    const { page, room, errors } = await openRoom(t, {
      viewport: { width, height: width < 768 ? 844 : 1000 }, hasTouch: width < 768
    });
    await place(page, '我在這一邊。'.repeat(35));
    for (const theme of ['dark', 'light']) {
      await page.evaluate(theme => { document.documentElement.dataset.theme = theme; }, theme);
      const dimensions = await room.evaluate(el => ({ width: el.clientWidth, scroll: el.scrollWidth }));
      assert.ok(dimensions.scroll <= dimensions.width + 1, width + 'px room overflow: ' + JSON.stringify(dimensions));
      const outside = await room.evaluate(el => [...el.querySelectorAll('*')].filter(child => {
        const style = getComputedStyle(child);
        if (style.display === 'none' || style.visibility === 'hidden' || !child.getClientRects().length) return false;
        if (child instanceof SVGElement) return false;
        const box = child.getBoundingClientRect();
        return box.width > 0 && (box.left < -1 || box.right > window.innerWidth + 1);
      }).map(child => child.id || child.className));
      assert.deepEqual(outside, [], '可见文字或 controls 唔應裁出 viewport');
      if (width === 390 || width === 1440) {
        await room.screenshot({ path: path.join(artifacts, width + '-' + theme + '.png') });
      }
    }
    assert.deepEqual(errors, []);
  });
}

test('reduced motion 同 forced-colors 仍有可讀輪廓／文字', async t => {
  const { page, room } = await openRoom(t, { reducedMotion: 'reduce', forcedColors: 'active' });
  await place(page, '唔需要動畫，亦可以在場。');
  const moving = await room.evaluate(el => el.getAnimations({ subtree: true }).filter(animation => animation.playState === 'running').length);
  assert.equal(moving, 0);
  assert.ok(await page.locator('#isness-response').isVisible());
  await page.locator('button[data-isness-view="between"]').click();
  await room.screenshot({ path: path.join(artifacts, 'forced-colors-reduced-motion.png') });
});

test('原有 theme、Scriptorium、Stones、Treasury、Chancel 照常運作', async t => {
  const { page, errors } = await openRoom(t);
  const theme = await page.locator('html').getAttribute('data-theme');
  await page.locator('#theme-toggle').click();
  assert.notEqual(await page.locator('html').getAttribute('data-theme'), theme);
  await page.locator('#write-in').fill('ki+mance');
  await page.waitForFunction(() => document.querySelector('#write-out').textContent.length > 0);
  await page.locator('#stones').scrollIntoViewIfNeeded();
  await page.locator('#stone-grid .tile').first().waitFor();
  await page.locator('#stone-grid .tile').first().click();
  assert.ok(await page.locator('#lintel-panel').isVisible());
  await page.locator('#treasury').scrollIntoViewIfNeeded();
  await page.locator('#lex-rows .lex-row').first().waitFor();
  await page.locator('#seek').fill('panimaance');
  await page.waitForFunction(() => document.querySelector('#lex-rows').textContent.includes('panimaance'));
  await page.locator('#chancel').scrollIntoViewIfNeeded();
  await page.locator('#rite-presets button').first().waitFor();
  await page.locator('#rite-presets button').first().click();
  await page.locator('#rite-run').click();
  await page.waitForFunction(() => {
    const text = document.querySelector('#rite-out').textContent;
    return text.trim().length > 0 && !text.includes('waking');
  });
  assert.deepEqual(errors, []);
});
