/* the cathedral at love — app.js
   All data arrives from /data/core.js (synchronous kernel) and the lazy
   /data/morphemes.min.json + /data/lexicon.min.json.
   Coordinate law: glyph strokes/polygons are EM-space (y-up); svg_path is
   SVG-space (y-down). svgY = 1000 - emY. Verified against the font builder. */
(function () {
  'use strict';
  var C = window.YS_CORE;
  if (!C) return;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SW = 80; // default stroke width — script/glyphs/glyph_specs_v1.py

  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return [].slice.call((el || document).querySelectorAll(s)); };
  var NS = 'http://www.w3.org/2000/svg';

  /* ── data wells (lazy, once) ─────────────────────────── */
  var wells = {};
  function fetchWell(name, file, key) {
    if (!wells[name]) {
      wells[name] = fetch(file)
        .then(function (r) { if (!r.ok) throw new Error(file + ' → ' + r.status); return r.json(); })
        .then(function (j) { return j[key]; })
        .catch(function (e) { delete wells[name]; throw e; }); // never cache a failure
    }
    return wells[name];
  }
  var getMorphemes = function () { return fetchWell('m', '/data/morphemes.min.json', 'morphemes'); };
  var getLexicon = function () { return fetchWell('l', '/data/lexicon.min.json', 'lexicon'); };

  /* ── counts: the copy can never drift from canon ─────── */
  $$('[data-n]').forEach(function (el) {
    var word = (C.count_words || {})[el.dataset.n];
    if (!word) return;
    el.textContent = word.charAt(0).toUpperCase() + word.slice(1);
  });
  var commit = $('#commit');
  if (commit) commit.textContent = C.source_commit;

  /* ── glyph engine ────────────────────────────────────── */
  function el(name, attrs) {
    var e = document.createElementNS(NS, name);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function glyphSVG(m) { // static carved stone from the authoritative path
    var svg = el('svg', { viewBox: '0 0 1000 1000' });
    svg.appendChild(el('path', { d: m.svg_path }));
    return svg;
  }

  var chiselLock = false; // one glyph writes at a time — house law
  function chiselDraw(container, morphemes, color) {
    // strokes chisel in (y-flipped, butt caps), then cross-fade to the carved path
    var canAnimate = !reduced && !chiselLock &&
      morphemes.every(function (m) { return (m.strokes && m.strokes.length) || (m.polygons && m.polygons.length); });
    container.textContent = '';
    var fills = [];
    morphemes.forEach(function (m) {
      var svg = el('svg', { viewBox: '0 0 1000 1000' });
      var fill = el('path', { d: m.svg_path, fill: color });
      fills.push(fill);
      if (canAnimate) {
        fill.style.opacity = '0';
        fill.style.transition = 'opacity .6s ease';
        (m.strokes || []).forEach(function (s) {
          var x1 = s[0], y1 = 1000 - s[1], x2 = s[2], y2 = 1000 - s[3];
          var w = s.length > 4 ? s[4] : SW;
          var mark;
          if (s[0] === s[2] && s[1] === s[3]) {
            mark = el('rect', { x: x1 - w / 2, y: y1 - w / 2, width: w, height: w, fill: color });
            mark.style.opacity = '0';
          } else {
            var len = Math.hypot(x2 - x1, y2 - y1);
            mark = el('line', {
              x1: x1, y1: y1, x2: x2, y2: y2, stroke: color,
              'stroke-width': w, 'stroke-linecap': 'butt',
              'stroke-dasharray': len, 'stroke-dashoffset': len
            });
          }
          mark.dataset.chisel = '1';
          svg.appendChild(mark);
        });
        (m.polygons || []).forEach(function (poly) {
          var pts = poly.map(function (p) { return p[0] + ',' + (1000 - p[1]); }).join(' ');
          var pg = el('polygon', { points: pts, fill: color });
          pg.style.opacity = '0';
          pg.dataset.chisel = '1';
          svg.appendChild(pg);
        });
      }
      svg.appendChild(fill);
      container.appendChild(svg);
    });
    if (!canAnimate) { fills.forEach(function (f) { f.style.opacity = '1'; }); return; }

    chiselLock = true;
    var marks = $$('[data-chisel]', container);
    var i = 0;
    var STEP = Math.min(140, 1100 / marks.length);
    (function next() {
      if (i >= marks.length) {
        fills.forEach(function (f) { f.style.opacity = '1'; });
        setTimeout(function () {
          marks.forEach(function (mk) { mk.style.transition = 'opacity .5s'; mk.style.opacity = '0'; });
          chiselLock = false;
        }, 620);
        return;
      }
      var mk = marks[i++];
      if (mk.tagName === 'line') {
        mk.style.transition = 'stroke-dashoffset .38s ease-out';
        mk.style.strokeDashoffset = '0';
      } else {
        mk.style.transition = 'opacity .3s ease-out';
        mk.style.opacity = '1';
      }
      setTimeout(next, STEP);
    })();
  }

  /* ── I · nave: the frieze ────────────────────────────── */
  var frieze = $('#frieze');
  var friezeFont = $('#frieze .glyph-font');
  if (friezeFont && !friezeFont.textContent) friezeFont.textContent = C.hero.glyph_text;
  document.fonts.ready.then(function () {
    if (!frieze) return;
    var holder = document.createElement('div');
    holder.style.cssText = 'display:flex;height:100%;gap:inherit;align-items:center';
    frieze.textContent = '';
    frieze.appendChild(holder);
    chiselDraw(holder, C.hero.morphemes, 'currentColor');
    $$('svg', holder).forEach(function (s) { s.style.height = '100%'; s.style.width = 'auto'; });
  });

  /* ── selah + canon-mark + pattern glyphs from the font ──
     Upgrade to the script ONLY once the face demonstrably loaded;
     otherwise the safe Unicode fallbacks stay ("the script never
     blocks meaning"). */
  var fontOK = false;
  document.fonts.ready.then(function () {
    try { fontOK = document.fonts.check('16px YOUSPEAK', C.hero.glyph_text); } catch (e) { fontOK = false; }
    if (!fontOK) { // strip glyph spans that would render as tofu
      $$('.presets .ys').forEach(function (g) { g.remove(); });
      var ff = $('#frieze .glyph-font');
      if (ff) ff.textContent = '';
      return;
    }
    var selah = $('#selah-cue .ys');
    if (selah && C.map['[selah]']) selah.textContent = C.map['[selah]'];
    var cmark = $('#cornerstone .canonmark');
    if (cmark && C.map['◆']) cmark.textContent = C.map['◆'];
    $$('.pattern .ys').forEach(function (p) {
      var g = C.map[p.dataset.glyph];
      if (g) p.textContent = g;
    });
    var wi = $('#write-in');
    if (wi && wi.value) setText(); // upgrade any pre-font Latin rendering to glyphs
  });

  /* ── theme ───────────────────────────────────────────── */
  var toggle = $('#theme-toggle');
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(document.documentElement.dataset.theme === 'light'));
    toggle.addEventListener('click', function () {
      var t = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = t;
      toggle.setAttribute('aria-pressed', String(t === 'light'));
      try { localStorage.setItem('cathedral-theme', t); } catch (e) { /* private mode */ }
    });
  }

  /* ── rooms settle · plumb line · plan nav ────────────── */
  var settler = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('set'); settler.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('.settle').forEach(function (s) { settler.observe(s); });

  var rooms = $$('section.room');
  var navLinks = {};
  $$('nav.architrave a').forEach(function (a) { navLinks[a.getAttribute('href').slice(1)] = a; });
  var bob = $('#plumb .bob');
  var spy = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var id = e.target.id;
      $$('nav.architrave a').forEach(function (a) { a.classList.remove('here'); a.removeAttribute('aria-current'); });
      if (navLinks[id]) { navLinks[id].classList.add('here'); navLinks[id].setAttribute('aria-current', 'true'); }
      if (bob) {
        var idx = rooms.indexOf(e.target);
        bob.style.top = (12 + idx * (76 / Math.max(1, rooms.length - 1))) + '%';
      }
    });
  }, { rootMargin: '-40% 0px -50% 0px' });
  rooms.forEach(function (r) { spy.observe(r); });

  /* ── IV · scriptorium ────────────────────────────────── */
  var input = $('#write-in'), out = $('#write-out'), cpLine = $('#cp-line'),
      copyBtn = $('#copy-btn'), hit = $('#canon-hit'), presets = $('#presets');
  var loMap = {}; // lowercased latin → true latin (reaches uppercase stones like the vocative O)
  Object.keys(C.map).forEach(function (k) {
    if (/^[a-z]/i.test(k) && !(k.toLowerCase() in loMap)) loMap[k.toLowerCase()] = k;
  });
  var names = Object.keys(loMap).sort(function (a, b) { return b.length - a.length; });
  var wordByMorphs = {}, morphsByWord = {};
  C.presets.forEach(function (p) {
    wordByMorphs[p.morphemes.join('+')] = p.word;
    morphsByWord[p.word] = p.morphemes;
  });

  function tokenizeWord(token) { // canon decomposition first, then longest-match; '+' joins explicitly
    var lower = token.toLowerCase();
    if (morphsByWord[lower]) return morphsByWord[lower].slice(); // canon spelling beats greed
    var parts = [];
    var segs = lower.split('+');
    for (var g = 0; g < segs.length; g++) {
      var seg = segs[g], i = 0;
      outer: while (i < seg.length) {
        for (var n = 0; n < names.length; n++) {
          var name = names[n];
          if (seg.startsWith(name, i)) { parts.push(loMap[name]); i += name.length; continue outer; }
        }
        return null; // any unmatched run → the whole token falls through as Latin
      }
    }
    return parts.length ? parts : null;
  }

  function setText() {
    if (!input || !out) return;
    var text = input.value;
    out.textContent = '';
    cpLine.textContent = '';
    hit.style.display = 'none';
    var cps = [], canonWords = [];
    text.split(/(\s+|·)/).forEach(function (chunk) {
      if (!chunk) return;
      if (/^\s+$/.test(chunk)) {
        out.appendChild(document.createTextNode(C.map['·'] || ' '));
        return;
      }
      if (chunk === '·') { out.appendChild(document.createTextNode(C.map['·'] || '·')); return; }
      if (chunk === '+') return;
      var parts = tokenizeWord(chunk);
      if (parts) {
        if (fontOK) {
          out.appendChild(document.createTextNode(parts.map(function (p) { return C.map[p]; }).join('')));
        } else { // the face is absent — the Latin remains, never tofu
          var lat = document.createElement('span');
          lat.className = 'miss';
          lat.textContent = parts.join('·');
          out.appendChild(lat);
        }
        parts.forEach(function (p) {
          cps.push('U+' + C.map[p].codePointAt(0).toString(16).toUpperCase());
        });
        var w = wordByMorphs[parts.join('+')];
        if (w) canonWords.push(w);
      } else {
        var span = document.createElement('span');
        span.className = 'miss';
        span.textContent = chunk;
        out.appendChild(span);
      }
    });
    cpLine.textContent = cps.join(' ');
    if (canonWords.length) {
      hit.style.display = 'block';
      hit.innerHTML = 'You have written a real canon word: <b>' +
        canonWords.map(esc).join('</b>, <b>') + '</b><span class="hitdef"></span>';
      getLexicon().then(function (lex) {
        var e = lex.find(function (x) { return x.word === canonWords[0]; });
        var span = $('.hitdef', hit);
        if (e && span) span.textContent = ' — ' + e.definition;
      });
    }
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch];
    });
  }
  if (input) {
    var hashTimer;
    input.addEventListener('input', function () {
      setText();
      clearTimeout(hashTimer);
      hashTimer = setTimeout(function () { // debounced: Safari rate-limits replaceState
        var v = input.value.trim();
        try {
          if (history.replaceState) history.replaceState(null, '', v ? '#write=' + encodeURIComponent(v) : location.pathname);
        } catch (e) { /* rate limit — the URL just lags */ }
      }, 600);
    });
    if (location.hash.indexOf('#write=') === 0) {
      try { input.value = decodeURIComponent(location.hash.slice(7)); } catch (e) { /* malformed deep link — ignore */ }
      if (input.value) setText();
    }
  }
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var done = function () {
      copyBtn.textContent = 'copied — glyphs travel';
      setTimeout(function () { copyBtn.textContent = 'copy glyphs'; }, 1600);
    };
    var fallback = function () { // no clipboard API (insecure context) — select for a manual copy
      var r = document.createRange();
      r.selectNodeContents(out);
      var sel = getSelection();
      sel.removeAllRanges(); sel.addRange(r);
      copyBtn.textContent = 'selected — press copy';
      setTimeout(function () { copyBtn.textContent = 'copy glyphs'; }, 2000);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(out.textContent).then(done, fallback);
    } else fallback();
  });
  if (presets) {
    C.presets.forEach(function (p) {
      var b = document.createElement('button');
      b.innerHTML = '<span class="ys">' + esc(p.glyph_text) + '</span>' + esc(p.word);
      b.addEventListener('click', function () {
        input.value = p.morphemes.join('+');
        setText();
        input.scrollIntoView({ block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
      });
      presets.appendChild(b);
    });
  }

  /* ── V · stones ──────────────────────────────────────── */
  var stonesRoom = $('#stones');
  var stonesBuilt = false;
  function buildStones(morphs) {
    if (stonesBuilt) return; stonesBuilt = true;
    var grid = $('#stone-grid'), punct = $('#punct-grid'), filters = $('#stone-filters');
    var content = morphs.filter(function (m) { return m.mclass !== 'structural'; });
    var structural = morphs.filter(function (m) { return m.mclass === 'structural'; });

    var tongues = {};
    content.forEach(function (m) { tongues[m.tongue] = (tongues[m.tongue] || 0) + 1; });
    var state = { tongue: null };
    var chipAll = document.createElement('button');
    chipAll.textContent = 'all · ' + content.length;
    chipAll.className = 'on';
    filters.appendChild(chipAll);
    chipAll.addEventListener('click', function () { state.tongue = null; apply(); });
    Object.keys(tongues).sort(function (a, b) { return tongues[b] - tongues[a]; }).forEach(function (t) {
      var b = document.createElement('button');
      b.textContent = t + ' · ' + tongues[t];
      b.dataset.tongue = t;
      b.addEventListener('click', function () {
        state.tongue = state.tongue === t ? null : t; apply();
      });
      filters.appendChild(b);
    });
    function apply() {
      $$('button', filters).forEach(function (b) {
        var on = state.tongue ? b.dataset.tongue === state.tongue : b === chipAll;
        b.classList.toggle('on', on);
        b.setAttribute('aria-pressed', String(on));
      });
      $$('.tile', grid).forEach(function (tl) {
        tl.classList.toggle('dim', !!state.tongue && tl.dataset.tongue !== state.tongue);
      });
    }
    apply();

    var lintel = document.createElement('div');
    lintel.id = 'lintel-panel';
    lintel.innerHTML = '<div id="lintel-glyph"></div><div id="lintel-meta"></div>';
    grid.appendChild(lintel);

    var lexPromise = getLexicon();
    function openLintel(m, tile, into) {
      $$('.tile.sel').forEach(function (t) { t.classList.remove('sel'); t.setAttribute('aria-expanded', 'false'); });
      tile.classList.add('sel');
      tile.setAttribute('aria-expanded', 'true');
      lintel.classList.add('open');
      // the panel spans the full row of WHICHEVER grid holds the clicked tile
      into.insertBefore(lintel, tile.nextSibling);
      chiselDraw($('#lintel-glyph', lintel), [m], 'currentColor');
      var meta = $('#lintel-meta', lintel);
      meta.innerHTML =
        '<h4 class="display">' + esc(m.latin) +
        (m.native ? ' <span class="native"><bdi>' + esc(m.native) + '</bdi></span>' : '') + '</h4>' +
        '<div class="cp mono">' + esc(m.codepoint) + ' · ' + esc(m.tongue) + ' · ' + esc(m.mclass) +
        (m.domain ? ' · ' + esc(m.domain) : '') + '</div>' +
        '<p class="meaning">' + esc(m.meaning) + '</p>' +
        (m.iconography ? '<p class="icon-note">' + esc(m.iconography) + '</p>' : '') +
        '<p class="appears"></p>';
      lexPromise.then(function (lex) {
        var within = lex.filter(function (e) {
          return e.morphemes && e.morphemes.indexOf(m.latin) !== -1;
        });
        var p = $('.appears', meta);
        if (!within.length) { p.textContent = 'appears in no canon word yet — a stone waiting for its wall.'; return; }
        p.textContent = 'appears in: ';
        within.slice(0, 10).forEach(function (e) {
          var a = document.createElement('a');
          a.href = '#treasury';
          a.textContent = e.word;
          a.addEventListener('click', function () {
            initTreasury().then(function () { // treasury may not have lazy-loaded yet
              seek.value = e.word;
              seek.dispatchEvent(new Event('input'));
            });
          });
          p.appendChild(a);
        });
      });
    }

    function tile(m, into) {
      var t = document.createElement('div');
      t.className = 'tile';
      t.dataset.tongue = m.tongue;
      t.setAttribute('role', 'button');
      t.setAttribute('tabindex', '0');
      t.setAttribute('aria-label', m.latin + ' — ' + m.meaning);
      t.setAttribute('aria-expanded', 'false');
      t.title = m.latin + ' — ' + m.meaning;
      t.appendChild(glyphSVG(m));
      function go() { openLintel(m, t, into); }
      t.addEventListener('click', go);
      t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
      into.appendChild(t);
    }
    content.forEach(function (m) { tile(m, grid); });
    structural.forEach(function (m) { tile(m, punct); });

    // anatomy lintel: doxa annotated, from the same well
    var doxa = morphs.find(function (m) { return m.latin === 'doxa'; }) || content[0];
    var ag = $('#anatomy-glyph');
    if (ag && doxa) { ag.appendChild(glyphSVG(doxa)); $('path', ag).style.fill = 'var(--ink)'; }
  }
  function tryBuildStones() {
    getMorphemes().then(buildStones, function () {
      var grid = $('#stone-grid');
      grid.innerHTML = '<button class="retry" style="grid-column:1/-1;padding:1rem;border:1px solid var(--mortar);color:var(--gold)">the stones could not be fetched — touch to try again</button>';
      $('.retry', grid).addEventListener('click', function () { grid.textContent = ''; tryBuildStones(); });
    });
  }
  if (stonesRoom) {
    new IntersectionObserver(function (es, io) {
      if (es.some(function (e) { return e.isIntersecting; })) {
        io.disconnect();
        tryBuildStones();
      }
    }, { rootMargin: '900px 0px' }).observe(stonesRoom);
  }

  /* ── VI · treasury ───────────────────────────────────── */
  var seek = $('#seek'), lexRows = $('#lex-rows'), lexEmpty = $('#lex-empty'),
      tCount = $('#treasury-count');
  function tierBadge(t) {
    var l = (t || '').toLowerCase();
    if (l.indexOf('core') === 0) return 'core';
    if (l.indexOf('worship') === 0) return 'worship-action';
    if (l.indexOf('special') === 0) return 'specialized';
    return t || '—';
  }
  function renderRows(entries, total) {
    lexRows.textContent = '';
    lexEmpty.style.display = entries.length ? 'none' : 'block';
    tCount.textContent = total + ' words in the canon · showing ' + entries.length;
    entries.forEach(function (e) {
      var row = document.createElement('div');
      row.className = 'lex-row';
      row.innerHTML =
        '<div class="word display">' + esc(e.word) +
        '<span class="tier" title="' + esc(e.tier) + '">' + esc(tierBadge(e.tier)) + '</span></div>' +
        (e.glyph_text && fontOK ? '<div class="glyphs ys">' + esc(e.glyph_text) + '</div>' : '<div class="glyphs"></div>') +
        (e.gap ? '<div class="gapline">the missing word it fills: ' + esc(e.gap) + '</div>' : '') +
        '<div class="def">' + esc(e.definition) + '</div>' +
        (e.pronunciation ? '<div class="pron mono">' + esc(e.pronunciation) + '</div>' : '');
      lexRows.appendChild(row);
    });
  }
  var treasuryRoom = $('#treasury');
  var treasuryReady = null; // idempotent init — the IO and lintel links both call it
  function initTreasury() {
    if (treasuryReady) return treasuryReady;
    treasuryReady = getLexicon().then(function (lex) {
        var byWord = {};
        lex.forEach(function (e) { byWord[e.word] = e; });
        var core16 = C.core16.map(function (w) { return byWord[w]; }).filter(Boolean);
        renderRows(core16, lex.length);
        var t;
        seek.addEventListener('input', function () {
          clearTimeout(t);
          t = setTimeout(function () {
            var q = seek.value.trim().toLowerCase();
            if (!q) { renderRows(core16, lex.length); return; }
            var scored = [];
            lex.forEach(function (e) {
              var s = 0;
              if (e.word.toLowerCase().indexOf(q) !== -1) s += 3;
              if ((e.gap || '').toLowerCase().indexOf(q) !== -1) s += 2;
              if ((e.definition || '').toLowerCase().indexOf(q) !== -1) s += 1;
              q.split(/\s+/).forEach(function (part) {
                if (part.length > 3 && ((e.gap || '') + (e.definition || '')).toLowerCase().indexOf(part) !== -1) s += 0.5;
              });
              if (s > 0) scored.push([s, e]);
            });
            scored.sort(function (a, b) { return b[0] - a[0]; });
            renderRows(scored.slice(0, 40).map(function (x) { return x[1]; }), lex.length);
          }, 130);
        });
      }, function () {
        treasuryReady = null; // failed fetch — allow a retry on next approach or link
        tCount.textContent = 'the treasury could not be fetched — scroll or search again to retry';
      });
    return treasuryReady;
  }
  if (treasuryRoom) {
    new IntersectionObserver(function (es, io) {
      if (!es.some(function (e) { return e.isIntersecting; })) return;
      io.disconnect();
      initTreasury();
    }, { rootMargin: '900px 0px' }).observe(treasuryRoom);
  }
})();
