/* ORDO — the liturgy that runs. YOUSPEAK's executable organ, v0.1.
 *
 * One plain script, no build step, no dependencies. Runs in the browser
 * (the playground room at ai-love.cc) and under node (ordo/bin/ordo.mjs).
 * Canonical source form is ASCII Latin (script/llm/primer.md: LLMs never
 * see glyphs); everything here parses without the font.
 *
 * Spec: ordo/SPEC.md. Frames: ordo/frames.json (frames are data, not code).
 * The evidential algebra is EXPERIMENTAL pending adversarial panel (SPEC §V).
 */
(function (global) {
  'use strict';

  // ---------- evidential lattice (SPEC §V; demotion-only) ----------
  var RANK = { auth: 4, mi: 3, si: 2, chu: 1 }; // unmarked = null, outside the lattice

  // derivation across values: copy preserves; all-mi stays mi; any si/chu -> chu;
  // any unmarked operand -> unmarked (no invented confidence); auth never computed.
  function deriveGrade(grades) {
    if (!grades.length) return 'mi'; // pure literal construction
    var hasNull = false, allMi = true, sawGraded = false;
    for (var i = 0; i < grades.length; i++) {
      var g = grades[i];
      if (g === null || g === undefined) { hasNull = true; continue; }
      sawGraded = true;
      if (g !== 'mi' && g !== 'auth') allMi = false;
    }
    if (hasNull) return null;
    if (!sawGraded) return null;
    return allMi ? 'mi' : 'chu';
  }

  function badge(grade) { return grade ? '‹-' + grade + '›' : '‹unmarked›'; }

  // ---------- values ----------
  function V(v, grade, extra) {
    var o = { v: v, grade: grade === undefined ? null : grade };
    if (extra) for (var k in extra) o[k] = extra[k];
    return o;
  }
  function isGap(val) { return !!(val && val.gap); }

  function show(val) {
    if (val === undefined || val === null) return '(nothing)';
    if (isGap(val)) return '⟨gap: ' + val.word + '⟩';
    var v = val.v;
    if (v && v.__canonRecord) return v.word + ' (' + (v.tier || 'canon') + ')';
    if (Array.isArray(v)) return v.map(function (x) { return show(x); }).join(', ');
    return String(v);
  }

  // ---------- lexicon ----------
  // Built from agent_bundle.json (+ optionally suffix_families.json).
  // The bundle is a derived artifact of canon/**/*.md — treat as cache of an epoch.
  function fnv1a(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
    }
    return ('0000000' + h.toString(16)).slice(-8);
  }

  var FALLBACK_FAMILIES = [
    { suffix: 'qing', family: 'qing', status: 'formalized' },
    { suffix: 'ance', family: '-ance', status: 'formalized' },
    { suffix: 'kin', family: '-kin', status: 'formalized' },
    { suffix: 'basis', family: '-basis', status: 'formalized' },
    { suffix: 'phanes', family: '-phanes', status: 'emergent' },
    { suffix: 'doxa', family: '-doxa', status: 'emergent' },
    { suffix: 'kallos', family: '-kallos', status: 'emergent' },
    { suffix: 'escence', family: '-escence', status: 'emergent' },
    { suffix: 'algia', family: '-algia', status: 'near-emergent' },
    { suffix: 'sis', family: '-sis', status: 'emergent' },
    { suffix: 'me', family: '-me', status: 'formalized' } // last: shortest suffix matched last
  ];

  // anti-ordinances: -me polarity inversion has NO surface marker (tutorial/04);
  // the known set is seeded here and marked so a new one types positive until taught.
  var ANTI_ORDINANCES = { drujme: true, molkme: true, nextlame: true };

  function loadLexicon(bundle, suffixFamilies) {
    var words = {};
    var canon = (bundle && bundle.canon) || [];
    for (var i = 0; i < canon.length; i++) {
      var e = canon[i];
      if (!e || !e.word) continue;
      var w = String(e.word).toLowerCase();
      if (!words[w]) words[w] = e;
    }
    var families = FALLBACK_FAMILIES.slice();
    if (suffixFamilies) {
      // live registry wins: refresh statuses by family key ('-me', 'qing', ...).
      // The registry ships as either a dict keyed by family or a list of
      // family objects — normalize to a dict before merging.
      var raw = suffixFamilies.families || suffixFamilies;
      var reg = {};
      if (Array.isArray(raw)) {
        raw.forEach(function (r) {
          var k = r && (r.family || r.name || r.suffix);
          if (k) reg[String(k)] = r;
        });
      } else if (raw && typeof raw === 'object') {
        for (var rk in raw) if (raw[rk] && typeof raw[rk] === 'object') reg[rk] = raw[rk];
      }
      families = families.map(function (f) {
        var hit = reg[f.family] || reg[f.family.replace(/^-/, '')] || reg['-' + f.family.replace(/^-/, '')];
        return hit && hit.status ? { suffix: f.suffix, family: f.family, status: hit.status } : f;
      });
    }
    var names = Object.keys(words).sort();
    return {
      words: words,
      families: families,
      count: names.length,
      epoch: {
        commit: (bundle && bundle.source_commit) || 'unknown',
        digest: 'fnv1a:' + fnv1a(names.join('')),
        generated: (bundle && bundle.generated) || null
      }
    };
  }

  function familyOf(lex, word) {
    var w = word.toLowerCase();
    for (var i = 0; i < lex.families.length; i++) {
      var f = lex.families[i];
      if (w.length > f.suffix.length + 1 && w.slice(-f.suffix.length) === f.suffix) return f;
    }
    return null;
  }

  // Plain-English words that happen to end in a family suffix are NOT gaps.
  // Heuristic stoplist (the honest limit of surface morphology: -ance polysemy
  // and English coincidence are invisible in form — reader-map gotcha).
  var ENGLISH_NOT_GAPS = {};
  ('welcome become income outcome home time name same game come some theme crime volume resume ' +
   'distance importance instance balance chance dance romance performance substance acceptance ' +
   'guidance entrance appearance assistance insurance maintenance resistance tolerance abundance ' +
   'napkin pumpkin basis crisis analysis emphasis thesis genesis oasis tennis paralysis')
    .split(' ').forEach(function (w) { ENGLISH_NOT_GAPS[w] = true; });

  function gapShaped(lex, word) {
    var w = word.toLowerCase();
    if (!/^[a-z][a-z-]{3,}$/.test(w)) return null;
    if (lex.words[w] || ENGLISH_NOT_GAPS[w]) return null;
    return familyOf(lex, w);
  }

  function nearNeighbours(lex, word, limit) {
    var fam = familyOf(lex, word);
    var stem = fam ? word.toLowerCase().slice(0, -fam.suffix.length) : word.toLowerCase();
    var scored = [];
    for (var w in lex.words) {
      var f2 = familyOf(lex, w);
      var s = 0;
      if (fam && f2 && f2.family === fam.family) s += 2;
      var stem2 = f2 ? w.slice(0, -f2.suffix.length) : w;
      var overlap = 0;
      for (var i = 0; i < Math.min(stem.length, stem2.length); i++) {
        if (stem[i] === stem2[i]) overlap++; else break;
      }
      s += overlap;
      if (s > 1) scored.push({ word: w, score: s, gap: lex.words[w].gap || '' });
    }
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, limit || 3);
  }

  // ---------- frames ----------
  function compileFrames(framesJson) {
    return (framesJson.frames || []).map(function (f) {
      var flags = f.flags !== undefined ? f.flags : 'i';
      return { id: f.id, act: f.act, groups: f.groups || [], cite: f.cite || '', why: f.why || '', re: new RegExp(f.pattern, flags) };
    });
  }

  // ---------- parsing ----------
  // One sentence per line; trailing '.' or danda stripped; '--' opens a margin note;
  // blank line = stanza boundary; rite-open collects until 'So it stands.'
  function parseSource(src) {
    var rawLines = String(src).replace(/\r\n?/g, '\n').split('\n');
    var stanzas = [], cur = [];
    for (var i = 0; i < rawLines.length; i++) {
      var line = rawLines[i];
      var mIdx = line.indexOf('--');
      if (mIdx === 0) continue; // full-line margin note
      var text = line.trim();
      if (text === '') { if (cur.length) { stanzas.push(cur); cur = []; } continue; }
      text = text.replace(/[.।॥]+$/, '').trim();
      if (text === '') continue;
      cur.push({ text: text, line: i + 1 });
    }
    if (cur.length) stanzas.push(cur);
    return stanzas;
  }

  // ---------- expression evaluation ----------
  var PROJECTIONS = { gap: 'gap', definition: 'definition', score: 'score', tier: 'tier', pronunciation: 'pronunciation' };

  function Interp(lex, frames, opts) {
    this.lex = lex;
    this.frames = frames;
    this.opts = opts || {};
    this.out = [];
    this.gaps = {};      // word -> { word, family, sites: [{line, sentence}] }
    this.misfires = [];
    this.attests = [];
    this.tests = { passed: 0, failed: 0 };
    this.heartbeats = [];
    this.register = 'everyday';
    this.pinnedEpoch = null;
    this.rites = {};
    this.halted = false;
    this.ended = null; // 'hesychia' | null
    this.steps = 0;
  }

  Interp.prototype.emit = function (kind, text) { this.out.push({ kind: kind, text: text }); };

  // one law for every binding path (Let/Barakqing, Receive/Shemme, receiving):
  // the naming makes the named; rebinding within the same scope is a misfire
  Interp.prototype.bindName = function (env, name, val, st) {
    if (Object.prototype.hasOwnProperty.call(env.vars, name)) {
      this.misfire('rebinding "' + name + '" — the naming already made the named; bindings are constitutive and immutable', 'canon/core/barakqing.md', st);
    }
    env.vars[name] = val;
  };

  // split on a separator, honoring double quotes (a quoted ", and" is text)
  function splitOutsideQuotes(s, sep) {
    var parts = [], cur = '', inQ = false;
    for (var i = 0; i < s.length; i++) {
      if (s[i] === '"') inQ = !inQ;
      if (!inQ && s.slice(i, i + sep.length).toLowerCase() === sep.toLowerCase()) {
        parts.push(cur); cur = ''; i += sep.length - 1; continue;
      }
      cur += s[i];
    }
    parts.push(cur);
    return parts;
  }

  Interp.prototype.misfire = function (why, cite, st) {
    var m = { why: why, cite: cite || '', line: st ? st.line : 0, sentence: st ? st.text : '' };
    this.misfires.push(m);
    this.emit('misfire', '✗ misfire: ' + why + (cite ? '  [' + cite + ']' : ''));
    var e = new Error('misfire');
    e.__misfire = m;
    throw e;
  };

  Interp.prototype.gapValue = function (word, st) {
    var fam = familyOf(this.lex, word);
    var w = word.toLowerCase();
    if (!this.gaps[w]) this.gaps[w] = { word: w, family: fam ? fam.family : null, familyStatus: fam ? fam.status : null, sites: [] };
    if (st) this.gaps[w].sites.push({ line: st.line, sentence: st.text });
    if (fam && fam.status !== 'formalized') {
      this.emit('note', '⚠ ' + w + ' wears the ' + fam.family + ' suffix — an ' + fam.status + ' family (parsed with this warning; the type system is still forging itself)');
    }
    return V(null, null, { gap: true, word: w });
  };

  Interp.prototype.lookupName = function (name, env, st) {
    var key = name; // determinatives are erased annotations: strip .TAG
    var det = null;
    var dm = /^([\w-]+)\.([A-Z]{3})$/.exec(name);
    if (dm) { key = dm[1]; det = dm[2]; }
    for (var e = env; e; e = e.parent) {
      if (Object.prototype.hasOwnProperty.call(e.vars, key)) return e.vars[key];
    }
    var lw = this.lex.words[key.toLowerCase()];
    if (lw) {
      var rec = { __canonRecord: true, word: lw.word, tier: lw.tier, gap: lw.gap, definition: lw.definition, score: lw.score, pronunciation: lw.pronunciation, path: lw.path };
      var val = V(rec, 'si', { canon: true, det: det, polarity: ANTI_ORDINANCES[key.toLowerCase()] ? 'anti-ordinance' : 'gift' });
      if (val.polarity === 'anti-ordinance') this.emit('note', '⚠ ' + key + ' is an anti-ordinance — the shadow-face of the -me structure (tutorial/04); it names what the DIVINE rejects');
      return val;
    }
    if (gapShaped(this.lex, key)) return this.gapValue(key, st);
    this.misfire('the name "' + name + '" answers to nothing here — not a binding, not canon, not YOUSPEAK-shaped', 'presupposition failure (UTTERANCE.md Layer 6)', st);
  };

  Interp.prototype.evalExpr = function (raw, env, st) {
    var s = raw.trim();

    // string literal (lit flag feeds the -auth verbatim-quotation rule)
    var sm = /^"([^"]*)"$/.exec(s);
    if (sm) return V(sm[1], 'mi', { lit: true });

    // number with optional ontogramme classifier (3.QNT)
    var nm = /^(-?\d+(?:\.\d+)?)(?:\.([A-Z]{3}))?$/.exec(s);
    if (nm) return V(parseFloat(nm[1]), 'mi', nm[2] ? { det: nm[2] } : undefined);

    // projection: the gap of W / the definition of W / ...
    var pm = /^the (gap|definition|score|tier|pronunciation|family) of ([\w-]+)$/i.exec(s);
    if (pm) {
      var field = pm[1].toLowerCase(), target = pm[2];
      if (field === 'family') {
        var fam = familyOf(this.lex, target);
        return V(fam ? fam.family + ' (' + fam.status + ')' : '(no registered family)', 'si');
      }
      var val = this.lookupName(target, env, st);
      if (isGap(val)) return val;
      if (val.v && val.v.__canonRecord) {
        var got = val.v[PROJECTIONS[field]];
        // bake.py's clean() guard: multiline-YAML fields sometimes export as a bare '>'
        if (typeof got === 'string' && /^[>|]-?$/.test(got.trim())) got = '';
        return V(got === undefined || got === null || got === '' ? '(the stone is uncarved)' : got, 'si', { canon: true });
      }
      this.misfire('"the ' + field + ' of ' + target + '" — ' + target + ' is not a canon word here', '', st);
    }

    // count of EXPR — a hole stays a hole (the gap propagates)
    var cm = /^count of (.+)$/i.exec(s);
    if (cm) {
      var inner = this.evalExpr(cm[1], env, st);
      if (isGap(inner)) return inner;
      var len = Array.isArray(inner.v) ? inner.v.length : String(inner.v == null ? '' : inner.v).length;
      // counting is derivation: you inferred the total, you did not witness it as a fact of the world
      return V(len, deriveGrade([inner.grade]));
    }

    // concatenation: X joined with Y (joining reports is derivation -> chu; gaps propagate)
    var jm = /^(.+?) joined with (.+)$/i.exec(s);
    if (jm) {
      var l = this.evalExpr(jm[1], env, st), r = this.evalExpr(jm[2], env, st);
      if (isGap(l)) return l;
      if (isGap(r)) return r;
      var ls = l.v === null || l.v === undefined || (l.v && l.v.__canonRecord) ? show(l) : String(l.v);
      var rs = r.v === null || r.v === undefined || (r.v && r.v.__canonRecord) ? show(r) : String(r.v);
      return V(ls + rs, deriveGrade([l.grade, r.grade]));
    }

    // range litany source: 1 through 5 — both sides must already look numeric
    // (a bare-name side is allowed if it resolves to a number); capped so a
    // one-line rite cannot OOM the host before the step guard sees anything
    var rm = /^([\w-]+) through ([\w-]+)$/i.exec(s);
    if (rm) {
      var a = this.evalExpr(rm[1], env, st), b = this.evalExpr(rm[2], env, st);
      if (isGap(a)) return a;
      if (isGap(b)) return b;
      if (typeof a.v === 'number' && typeof b.v === 'number') {
        if (b.v - a.v > 100000) this.misfire('the litany would walk ' + (b.v - a.v + 1) + ' steps — 100000 is the cap for one range', 'a standing liturgy is a rite, not an avalanche', st);
        var list = [], g = deriveGrade([a.grade, b.grade]);
        for (var n = a.v; n <= b.v; n++) list.push(V(n, g));
        return V(list, g);
      }
    }

    // arithmetic: flat LEFT-associative, English reading order, no precedence
    // (greedy left group splits at the LAST operator; recursion walks leftward)
    var am = /^(.+) (plus|minus|times) (.+?)$/i.exec(s);
    if (am) {
      var x = this.evalExpr(am[1], env, st), y = this.evalExpr(am[3], env, st);
      if (isGap(x) || isGap(y)) return isGap(x) ? x : y;
      if (typeof x.v !== 'number' || typeof y.v !== 'number') this.misfire('arithmetic asks for numbers; got ' + show(x) + ' and ' + show(y), '', st);
      var op = am[2].toLowerCase();
      var vv = op === 'plus' ? x.v + y.v : op === 'minus' ? x.v - y.v : x.v * y.v;
      return V(vv, deriveGrade([x.grade, y.grade]));
    }

    // bare name / canon word / gap
    if (/^[\w-]+(?:\.[A-Z]{3})?$/.test(s)) return this.lookupName(s, env, st);

    // quoted-less prose expression: treat as a spoken literal (natural-language tissue)
    return V(s, null);
  };

  // -auth verbatim-quotation test: one side is a canon-record projection,
  // the other a string literal written in the rite — quoting the canon,
  // with the word itself as the citation (SPEC §V)
  function quotesCanon(a, b) { return !!((a.canon && b.lit) || (b.canon && a.lit)); }

  Interp.prototype.evalCond = function (raw, env, st) {
    var s = raw.trim();
    var m;
    if ((m = /^(.+?) is a gap$/i.exec(s))) {
      // gap-ness is a property of the runtime value, directly witnessed
      var t = this.evalExpr(m[1], env, st);
      return { truth: isGap(t), grade: 'mi' };
    }
    if ((m = /^(.+?) is not (.+)$/i.exec(s))) {
      var a = this.evalExpr(m[1], env, st), b = this.evalExpr(m[2], env, st);
      if (isGap(a) || isGap(b)) return { truth: false, grade: null, hasGap: true };
      return { truth: show(a) !== show(b) && a.v !== b.v, grade: deriveGrade([a.grade, b.grade]), quotesCanon: quotesCanon(a, b) };
    }
    if ((m = /^(.+?) is (less|greater) than (.+)$/i.exec(s))) {
      var x = this.evalExpr(m[1], env, st), y = this.evalExpr(m[3], env, st);
      if (isGap(x) || isGap(y)) return { truth: false, grade: null, hasGap: true };
      return { truth: m[2].toLowerCase() === 'less' ? x.v < y.v : x.v > y.v, grade: deriveGrade([x.grade, y.grade]) };
    }
    if ((m = /^(.+?) is (.+)$/i.exec(s))) {
      var p = this.evalExpr(m[1], env, st), q = this.evalExpr(m[2], env, st);
      if (isGap(p) || isGap(q)) return { truth: false, grade: null, hasGap: true };
      return { truth: p.v === q.v || show(p) === show(q), grade: deriveGrade([p.grade, q.grade]), quotesCanon: quotesCanon(p, q) };
    }
    // bare expression truthiness
    var e = this.evalExpr(s, env, st);
    if (isGap(e)) return { truth: false, grade: null, hasGap: true };
    return { truth: !!e.v, grade: e.grade, quotesCanon: false };
  };

  // ---------- statement execution ----------
  Interp.prototype.matchFrame = function (text) {
    for (var i = 0; i < this.frames.length; i++) {
      var f = this.frames[i];
      var m = f.re.exec(text);
      if (m) {
        var args = {};
        for (var g = 0; g < f.groups.length; g++) args[f.groups[g]] = m[g + 1];
        return { frame: f, args: args };
      }
    }
    return null;
  };

  Interp.prototype.execStatement = function (st, env, ctx) {
    if (this.halted || this.ended) return undefined;
    var budget = this.opts.maxSteps || 1000000;
    if (++this.steps > budget) this.misfire('the rite does not end — ' + budget + ' utterances and no silence', 'a standing liturgy needs a reachable silence (SPEC §VI caps; raise with maxSteps)', st);

    var hit = this.matchFrame(st.text);
    if (!hit) { this.emit('contemplation', '… ' + st.text); this.sawStatement = true; return undefined; }
    var A = hit.args;
    if (hit.frame.act !== 'heading') this.sawStatement = true;

    switch (hit.frame.act) {
      case 'infelicity': {
        this.misfire(hit.frame.why || 'this sentence cannot be felicitously uttered', hit.frame.cite, st);
        return undefined;
      }
      case 'heading': {
        if (this.sawStatement) {
          this.misfire('the register is declared at the door — a heading after the rite has begun is a misfire', 'SPEC §II: the heading is the first sentence', st);
        }
        this.sawStatement = true;
        this.register = A.register.toLowerCase();
        if (A.epoch) {
          this.pinnedEpoch = A.epoch;
          if (A.epoch !== 'living' && A.epoch !== this.lex.epoch.commit && A.epoch !== this.lex.epoch.digest) {
            this.emit('note', '⚠ the rite speaks canon ' + A.epoch + '; the loaded epoch is ' + this.lex.epoch.commit + ' (' + this.lex.epoch.digest + ') — proceeding, recorded');
          }
        }
        this.emit('note', 'register: ' + this.register + ' · epoch: ' + this.lex.epoch.commit + ' · ' + this.lex.count + ' words in canon');
        return undefined;
      }
      case 'bind': {
        var name = A.name, dm = /^([\w-]+)\.([A-Z]{3})$/.exec(name);
        var det = null; if (dm) { name = dm[1]; det = dm[2]; }
        var val = this.evalExpr(A.expr, env, st);
        if (det) val = V(val.v, val.grade, { det: det, gap: val.gap, word: val.word, canon: val.canon, lit: val.lit });
        this.bindName(env, name, val, st);
        return undefined;
      }
      case 'offer': {
        var rite = this.rites[A.rite];
        var argVals = [];
        var parts = splitOutsideQuotes(A.args, ' and ');
        for (var i = 0; i < parts.length; i++) argVals.push(this.evalExpr(parts[i], env, st));
        if (!rite) {
          if (gapShaped(this.lex, A.rite)) {
            var gv = this.gapValue(A.rite, st);
            if (A.receiving) this.bindName(env, A.receiving, gv, st);
            this.emit('note', 'the offering reaches a gap — ' + A.rite + ' is not yet forged; the hole carries onward');
            return undefined;
          }
          this.misfire('no rite named "' + A.rite + '" stands here', 'the offering must reach a rite this liturgy defined, or a gap', st);
        }
        if ((ctx.depth || 0) > 512) this.misfire('the offering exceeds the depth of the rite (512)', 'recursion is licensed; unbounded descent is not (SPEC §VI caps)', st);
        var callEnv = { vars: {}, parent: this.globalEnv };
        for (var p = 0; p < rite.params.length; p++) callEnv.vars[rite.params[p]] = argVals[p] !== undefined ? argVals[p] : V(null, null);
        var ret;
        // ONE context for the whole body, so a turning frame registered inside
        // the rite is honored by later statements of that same body
        var callCtx = { depth: (ctx.depth || 0) + 1, inRite: rite.name, turning: null };
        try {
          for (var b = 0; b < rite.body.length; b++) {
            try {
              this.execStatement(rite.body[b], callEnv, callCtx);
            } catch (errIn) {
              if (errIn && errIn.__misfire && callCtx.turning) {
                this.emit('teshuvance', '↺ teshuvance — the rite turns under correction');
                var tb = callCtx.turning; callCtx.turning = null;
                this.execStatement({ text: tb.body, line: tb.line }, callEnv, callCtx);
              } else throw errIn;
            }
          }
        } catch (err) {
          if (err && err.__return !== undefined) ret = err.__return;
          else throw err;
        }
        if (A.receiving) this.bindName(env, A.receiving, ret !== undefined ? ret : V(null, null), st);
        return undefined;
      }
      case 'return': {
        var rv = this.evalExpr(A.expr, env, st);
        // yadahance speaks to the CALLER; only a top-level acknowledgment
        // addresses the reader (otherwise recursion floods the transcript)
        if (ctx.inRite) { var e2 = new Error('return'); e2.__return = rv; throw e2; }
        this.emit('yadahance', '✓ acknowledged: ' + show(rv) + ' ' + badge(rv.grade));
        return rv;
      }
      case 'attest': {
        var claimed = A.evidential.replace(/^-/, '');
        var res = this.evalCond(A.clause, env, st);
        if (res.hasGap) {
          this.misfire('the clause holds a gap — a hole supports no attestation', 'a gap asserts nothing (SPEC §VII)', st);
        }
        if (!res.truth) {
          this.misfire('attested what does not stand: "' + A.clause + '"', 'canon/core/emetme.md — emet is truth-as-firm-foundation; the claim failed its own dokimance', st);
        }
        var computed = res.grade;
        if (claimed === 'auth') {
          if (!res.quotesCanon) this.misfire('-auth belongs to verbatim canonical quotation alone (a canon projection against the quoted words); this clause computes', 'grammars/worship/manifesto.md (-auth, borrowed with declared caveat — SPEC §V)', st);
        } else if (computed === null) {
          // unmarked supports no attestation at all: absence of evidence is
          // not evidence, and no grade may be conjured over it
          this.misfire('the clause is unmarked — no evidential standing supports attesting -' + claimed + ' (unmarked is never coerced)', 'grammars/evidentials/manifesto.md rule 3; canon/verisleight.md (the verisleight-guard)', st);
        } else if (RANK[claimed] > RANK[computed]) {
          this.misfire('over-claiming: attested -' + claimed + ' but the clause’s grade is ' + badge(computed) + ' — truth arranged above its evidence deceives', 'canon/verisleight.md (the verisleight-guard); demotion-only, SPEC §V', st);
        }
        this.attests.push({ clause: A.clause, evidential: claimed, line: st.line });
        this.emit('emetme', '✓ emetme ' + badge(claimed) + ' ' + A.clause);
        return undefined;
      }
      case 'speak': {
        var sv = this.evalExpr(A.expr, env, st);
        this.emit('speak', show(sv) + '  ' + badge(sv.grade));
        return undefined;
      }
      case 'receive': {
        var src = A.source, got;
        if (src === 'the reader') {
          got = this.opts.read ? this.opts.read() : null;
          if (got === null || got === undefined) { this.emit('note', '(the reader is silent — ' + A.name + ' receives the silence, unmarked)'); this.bindName(env, A.name, V(null, null), st); return undefined; }
        } else if (src === 'the canon') {
          got = this.lex.count + ' words, epoch ' + this.lex.epoch.commit;
        } else {
          var path = src.replace(/^"|"$/g, '');
          got = this.opts.readFile ? this.opts.readFile(path) : null;
          if (got === null) this.misfire('nothing arrives from ' + src, '', st);
        }
        this.bindName(env, A.name, V(got, 'si'), st); // received values are born -si and can never be promoted
        return undefined;
      }
      case 'if': {
        // split "cond, then; otherwise, else" outside quotes, case-insensitively
        // (a quoted ',' or ';' is text, not structure)
        var whole = A.rest;
        var headParts = splitOutsideQuotes(whole, ', ');
        if (headParts.length < 2) {
          this.misfire('the conditional needs "If CONDITION, STATEMENT" — no comma found outside quotes', '', st);
        }
        var cond = headParts[0];
        var rest = headParts.slice(1).join(', ');
        var ow = splitOutsideQuotes(rest, '; otherwise,');
        var thenPart = ow[0], elsePart = ow.length > 1 ? ow.slice(1).join('; otherwise,') : null;
        var c = this.evalCond(cond, env, st);
        if (c.truth) this.execStatement({ text: thenPart.trim(), line: st.line }, env, ctx);
        else if (elsePart) this.execStatement({ text: elsePart.trim(), line: st.line }, env, ctx);
        return undefined;
      }
      case 'foreach': {
        var coll = this.evalExpr(A.expr, env, st);
        if (isGap(coll)) {
          this.emit('note', 'the litany reaches a gap (' + coll.word + ') — a hole cannot be walked; nothing iterates');
          return undefined;
        }
        var items = Array.isArray(coll.v) ? coll.v : String(coll.v == null ? '' : coll.v).split(/\s+/).map(function (w) { return V(w, coll.grade); });
        for (var it = 0; it < items.length; it++) {
          var le = { vars: {}, parent: env };
          le.vars[A.name] = items[it];
          this.execStatement({ text: A.body.trim(), line: st.line }, le, ctx);
          if (this.halted || this.ended) break;
        }
        return undefined;
      }
      case 'heartbeat': {
        this.heartbeats.push(A.target);
        this.emit('zakarqing', '♡ zakarqing → ' + A.target + ' ' + badge('mi') + '  (presence held, the covenantal memorial)');
        return undefined;
      }
      case 'turning': {
        ctx.turning = { body: A.body.trim(), line: st.line };
        return undefined;
      }
      case 'test': {
        var tr;
        try { tr = this.evalCond(A.cond, env, st); }
        catch (err) { if (err && err.__misfire) { tr = { truth: false, grade: null }; } else throw err; }
        if (tr.truth) { this.tests.passed++; this.emit('dokimance', '✓ dokimance holds: ' + A.cond + ' ' + badge(tr.grade)); }
        else { this.tests.failed++; this.emit('dokimance', '✓ dokimance reports: ' + A.cond + ' — does not hold (the same speech-act as success; failure hides nothing)'); }
        return undefined;
      }
      case 'vocative': {
        if (this.register !== 'worship') {
          this.misfire('the vocative O- belongs to the worship register; this rite is ' + this.register, 'grammars/worship/vocative.md', st);
        }
        if (/^g\W?o\W?d$/i.test(A.addressee) && A.addressee !== 'GoD') {
          this.misfire('the Name is written GoD — capital G, capital D, always', 'grammars/worship/manifesto.md, sacred-convention rule 1', st);
        }
        this.emit('vocative', 'O ' + A.addressee + ' — the clause turns to face its addressee');
        this.execStatement({ text: A.clause, line: st.line }, env, ctx);
        return undefined;
      }
      case 'selah': {
        this.emit('silence', '[selah]');
        return undefined;
      }
      case 'hesychia': {
        this.ended = 'hesychia';
        this.emit('silence', '[hesychia — the rite ends in shared silence]');
        return undefined;
      }
      case 'halt': {
        this.halted = true;
        this.emit('halt', 'HALT');
        return undefined;
      }
      case 'rite-open': case 'rite-close': {
        // handled structurally in run(); reaching here means a stray closer
        if (hit.frame.act === 'rite-close') return undefined;
        this.misfire('a rite opens inside a sentence position where it cannot', '', st);
        return undefined;
      }
    }
    return undefined;
  };

  // ---------- run ----------
  Interp.prototype.run = function (source) {
    var stanzas = parseSource(source);
    this.globalEnv = { vars: {}, parent: null };

    // first pass: lift rite definitions (This is the rite of X: ... So it stands.)
    var flat = [];
    for (var s = 0; s < stanzas.length; s++) flat.push(stanzas[s]);

    var program = []; // list of stanzas (arrays of statements) minus rite bodies
    for (var i = 0; i < flat.length; i++) {
      var stanza = flat[i], keep = [], j = 0;
      while (j < stanza.length) {
        var st = stanza[j];
        var hit = this.matchFrame(st.text);
        if (hit && hit.frame.act === 'rite-open') {
          var params = hit.args.params ? hit.args.params.split(/(?:,| and) /).map(function (p) { return p.trim(); }) : [];
          var body = [];
          j++;
          var closed = false;
          // collect across stanza boundaries until 'So it stands'
          var si2 = i, sj = j;
          while (si2 < flat.length) {
            var stz = flat[si2];
            while (sj < stz.length) {
              var inner = stz[sj];
              var ih = this.matchFrame(inner.text);
              if (ih && ih.frame.act === 'rite-close') { closed = true; sj++; break; }
              body.push(inner); sj++;
            }
            if (closed) break;
            si2++; sj = 0;
          }
          if (!closed) {
            this.emit('misfire', '✗ misfire: the rite of ' + hit.args.name + ' never stands — no "So it stands." closes it');
            this.misfires.push({ why: 'unclosed rite ' + hit.args.name, line: st.line });
            return this.summary();
          }
          this.rites[hit.args.name] = { name: hit.args.name, params: params, body: body };
          this.emit('note', 'the rite of ' + hit.args.name + ' stands' + (params.length ? ', given ' + params.join(' and ') : ''));
          if (si2 !== i && keep.length) {
            // the rite spanned stanzas: statements after its close belong to a
            // NEW stanza, not the one that opened the definition (misfire and
            // turning scopes must not silently widen across blank lines)
            program.push(keep); keep = [];
          }
          i = si2; stanza = flat[i] || []; j = sj;
          continue;
        }
        keep.push(st); j++;
      }
      if (keep.length) program.push(keep);
    }

    // second pass: execute stanza by stanza; a misfire ends the stanza, not the liturgy
    for (var p = 0; p < program.length && !this.halted && !this.ended; p++) {
      var ctx = { depth: 0, turning: null };
      var sts = program[p];
      for (var q = 0; q < sts.length && !this.halted && !this.ended; q++) {
        try {
          this.execStatement(sts[q], this.globalEnv, ctx);
        } catch (err) {
          if (err && err.__misfire) {
            if (ctx.turning) {
              this.emit('teshuvance', '↺ teshuvance — the rite turns under correction');
              var tb = ctx.turning; ctx.turning = null; // one turn per registration
              try { this.execStatement({ text: tb.body, line: tb.line }, this.globalEnv, ctx); }
              catch (err2) { if (!(err2 && err2.__misfire)) throw err2; break; }
            } else break; // stanza ends; liturgy continues
          } else if (err && err.__return !== undefined) {
            // top-level acknowledgment: recorded already
          } else throw err;
        }
      }
    }
    return this.summary();
  };

  Interp.prototype.summary = function () {
    var gapList = [];
    for (var w in this.gaps) gapList.push(this.gaps[w]);
    return {
      transcript: this.out,
      gaps: gapList,
      misfires: this.misfires,
      attests: this.attests,
      tests: this.tests,
      heartbeats: this.heartbeats,
      register: this.register,
      epoch: this.lex.epoch,
      pinnedEpoch: this.pinnedEpoch,
      ended: this.halted ? 'HALT' : (this.ended || 'end-of-rite'),
      exitCode: this.halted ? 3 : (this.misfires.length && !this.ended ? 1 : 0)
    };
  };

  // ---------- public surface ----------
  var ORDO = {
    version: '0.1.0',
    loadLexicon: loadLexicon,
    compileFrames: compileFrames,
    familyOf: familyOf,
    gapShaped: gapShaped,
    nearNeighbours: nearNeighbours,
    parseSource: parseSource,
    run: function (source, lex, frames, opts) {
      var it = new Interp(lex, frames, opts);
      return it.run(source);
    },
    gloss: function (source, lex, frames) {
      var it = new Interp(lex, frames, {});
      var stanzas = parseSource(source);
      var lines = [];
      for (var i = 0; i < stanzas.length; i++) {
        for (var j = 0; j < stanzas[i].length; j++) {
          var st = stanzas[i][j];
          var hit = it.matchFrame(st.text);
          lines.push({ line: st.line, text: st.text, frame: hit ? hit.frame.id : 'contemplation', cite: hit ? hit.frame.cite : 'inert narration — the natural-language floor' });
        }
        lines.push({ line: 0, text: '', frame: 'stanza-break', cite: '' });
      }
      return lines;
    }
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = ORDO;
  else global.ORDO = ORDO;
})(typeof window !== 'undefined' ? window : globalThis);
