/* chancel.js — VII · The Chancel: ORDO performed in the browser.
 * Hand-authored (like app.js). The interpreter itself is assets/ordo.js,
 * baked from ordo/ordo.js; frames and example rites are baked wells.
 * House patterns respected: lazy init on approach (IntersectionObserver,
 * rootMargin 900px), #rite= deep-link with 600ms debounced replaceState
 * (Safari rate-limits), every number flows from data, none hand-carved.
 */
(function () {
  'use strict';
  var room = document.getElementById('chancel');
  if (!room || !window.ORDO) return;

  var KIND_CLASS = { speak: 'spk', emetme: 'emet', yadahance: 'emet', dokimance: 'emet', misfire: 'mis', contemplation: 'cont', silence: 'sil', note: 'cont', zakarqing: 'emet', vocative: 'cont', teshuvance: 'mis', halt: 'mis' };

  var state = { lex: null, frames: null, rites: null };

  function fetchJSON(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + ' answered ' + r.status);
      return r.json();
    });
  }

  function esc(s) {
    return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; });
  }

  function render(result) {
    var out = document.getElementById('rite-out');
    var html = result.transcript.map(function (l) {
      return '<span class="' + (KIND_CLASS[l.kind] || '') + '">' + esc(l.text) + '</span>';
    }).join('\n');
    var foot = [];
    var t = result.tests;
    if (t.passed + t.failed) foot.push('dokimance: ' + t.passed + ' hold, ' + t.failed + ' do not (both reported alike)');
    if (result.misfires.length) foot.push('misfires: ' + result.misfires.length + ' (infelicities, not crashes)');
    if (result.gaps.length) foot.push('gaps: ' + result.gaps.map(function (g) { return g.word; }).join(', ') + ' — shown here, filed only by rites performed in the cathedral repo');
    foot.push('— ' + result.ended + ' · epoch ' + result.epoch.commit);
    out.innerHTML = html + '\n\n<span class="cont">' + esc(foot.join('\n')) + '</span>';
  }

  function renderGloss(lines) {
    var out = document.getElementById('rite-out');
    out.innerHTML = lines.map(function (g) {
      if (g.frame === 'stanza-break') return '';
      var cls = g.frame === 'contemplation' ? 'cont' : 'emet';
      return '<span class="' + cls + '">' + esc(g.frame) + '</span>  ' + esc(g.text) +
        (g.cite ? '\n    <span class="cont">[' + esc(g.cite.split(';')[0]) + ']</span>' : '');
    }).join('\n');
  }

  var saveTimer = null;
  function saveHash() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      var src = document.getElementById('rite-in').value;
      try { history.replaceState(null, '', '#rite=' + encodeURIComponent(src)); } catch (e) { /* rate-limited: fine */ }
    }, 600);
  }

  function init() {
    Promise.all([
      fetchJSON('/data/agent_bundle.json'),
      fetchJSON('/data/ordo-frames.json'),
      fetchJSON('/data/ordo-rites.json')
    ]).then(function (got) {
      state.lex = ORDO.loadLexicon(got[0], null);
      state.frames = ORDO.compileFrames(got[1]);
      state.rites = got[2];

      var input = document.getElementById('rite-in');
      var epochLine = document.getElementById('chancel-epoch');
      epochLine.textContent = 'epoch ' + state.lex.epoch.commit + ' · ' + state.lex.count + ' words in canon · ' + state.lex.epoch.digest;

      // presets from the baked rites
      var presets = document.getElementById('rite-presets');
      Object.keys(state.rites).forEach(function (name) {
        var b = document.createElement('button');
        b.innerHTML = '<b>' + esc(name) + '</b>';
        b.addEventListener('click', function () {
          input.value = state.rites[name];
          saveHash();
          document.getElementById('rite-out').textContent = 'the rite of ' + name + ' waits. perform it.';
        });
        presets.appendChild(b);
      });

      // initial source: deep link, else kunance
      var m = /#rite=(.+)/.exec(location.hash);
      if (m) { try { input.value = decodeURIComponent(m[1]); } catch (e) { /* leave default */ } }
      if (!input.value) input.value = state.rites.kunance || '';

      input.addEventListener('input', saveHash);

      document.getElementById('rite-run').addEventListener('click', function () {
        var result = ORDO.run(input.value, state.lex, state.frames, {
          read: function () { return window.prompt('The rite receives from the reader:'); }
        });
        render(result);
      });
      document.getElementById('rite-gloss').addEventListener('click', function () {
        renderGloss(ORDO.gloss(input.value, state.lex, state.frames));
      });

      document.getElementById('rite-out').textContent = 'the chancel is ready. perform the rite, or gloss it first.';
    }).catch(function (err) {
      inited = false; // a transient failure must not disable the room until reload
      document.getElementById('rite-out').textContent = 'the chancel could not wake: ' + err + ' — touch the room to try again.';
      room.addEventListener('click', initOnce, { once: true });
    });
  }

  var inited = false;
  function initOnce() { if (!inited) { inited = true; init(); } }

  // wake on approach (house pattern), on deep-link arrival, or on first touch
  new IntersectionObserver(function (es, io) {
    if (es[0].isIntersecting) { io.disconnect(); initOnce(); }
  }, { rootMargin: '900px' }).observe(room);
  if (/#(chancel|rite=)/.test(location.hash)) initOnce();
  window.addEventListener('hashchange', function () {
    if (/#(chancel|rite=)/.test(location.hash)) initOnce();
  });
  room.addEventListener('click', initOnce, { once: true });
})();
