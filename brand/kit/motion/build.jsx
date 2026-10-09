// build.jsx: the panim reveal, choreographed in EffectCraft 0.6.0's own JSX engine.
// Run by recipe.sh as: effectcraft-cli script build.jsx work/import.ecproj
// The project it opens already holds comp "Panim" with one shape layer, made by
// file.import + layer.create {op:"shapesFromVector"} from stones.svg (VectorCraft's split of kit/mark.svg).
//
// Story (4.0 s, 30 fps). Restraint over flash:
//   0.20-0.90  two staves are cut, top to bottom (a downstroke each; you, then I)
//   0.85-1.55  the two faces come toward each other and stop: the column never closes
//   1.45-1.80  the eyes open, level
//   1.80-2.45  the Hebrew donor sigil is chiselled at the top-left, then settles into the cut tone
//   1.70-3.50  one breath: light rises in the between, the gold warms, a glow swells and recedes
//   3.50-4.00  still

var GOLD   = [201/255, 164/255,  92/255, 1];   // #C9A45C
var GOLD_H = [228/255, 194/255, 124/255, 1];   // #E4C27C
var CUT    = [117/255,  90/255,  40/255, 1];   // #755A28

// ---------- easing: CSS-style cubic-bezier → After Effects KeyframeEase ----------
var EASE = {
  outExpo:   [0.16, 1.00, 0.30, 1.00],   // a chisel that lands
  outQuint:  [0.22, 1.00, 0.36, 1.00],   // a stone set down
  inOutSine: [0.37, 0.00, 0.63, 1.00],   // breath
  outSine:   [0.61, 1.00, 0.88, 1.00],
  inOut:     [0.65, 0.00, 0.35, 1.00]
};

function dimsOf(v) { return (v instanceof Array) ? v.length : 1; }
function delta(a, b, d) { return (a instanceof Array) ? (b[d] - a[d]) : (b - a); }

// keys: [[t, v], ...]; curves: one cubic-bezier per segment (or one for all)
function animate(prop, keys, curves) {
  var i, d;
  for (i = 0; i < keys.length; i++) prop.setValueAtTime(keys[i][0], keys[i][1]);
  var n = dimsOf(keys[0][1]);
  var easeDims = prop.isSpatial ? 1 : n;
  var idx = [];
  for (i = 0; i < keys.length; i++) idx.push(prop.nearestKeyIndex(keys[i][0]));
  for (i = 0; i < keys.length; i++) {
    var inE = [], outE = [];
    for (d = 0; d < easeDims; d++) {
      var ie = new KeyframeEase(0, 33.33), oe = new KeyframeEase(0, 33.33);
      if (i > 0) {
        var cI = (curves instanceof Array && curves[0] instanceof Array) ? curves[i - 1] : curves;
        var dtI = keys[i][0] - keys[i - 1][0];
        var avgI = delta(keys[i - 1][1], keys[i][1], d) / dtI;
        ie = new KeyframeEase(avgI * (1 - cI[3]) / (1 - cI[2]), (1 - cI[2]) * 100);
      }
      if (i < keys.length - 1) {
        var cO = (curves instanceof Array && curves[0] instanceof Array) ? curves[i] : curves;
        var dtO = keys[i + 1][0] - keys[i][0];
        var avgO = delta(keys[i][1], keys[i + 1][1], d) / dtO;
        oe = new KeyframeEase(avgO * cO[1] / cO[0], cO[0] * 100);
      }
      inE.push(ie); outE.push(oe);
    }
    prop.setTemporalEaseAtKey(idx[i], inE, outE);
  }
}

// ---------- find what the import made ----------
var comp = null;
for (var ii = 1; ii <= app.project.numItems; ii++) {
  if (app.project.item(ii).name === "Panim") comp = app.project.item(ii);
}
if (!comp) throw new Error("comp Panim not found");
var L = comp.layer(1);
if (L.matchName !== "ADBE Vector Layer") throw new Error("layer 1 is not a shape layer: " + L.matchName);
L.name = "panim";

// mark units (680 x 600, from mark.svg) → comp: em centre (390,390) on comp centre, 0.88 px/unit
var S = 88;
L.transform.anchorPoint.setValue([390, 390, 0]);
L.transform.position.setValue([540, 540, 0]);
L.transform.scale.setValue([S, S, 100]);

// The donor sigil gets its own layer, so the breath glow never gilds it (brand rule 4: it is cut, not
// gilded). Duplicate before any keys exist, then each layer keeps only its own stones.
var BODY = ["stave-l", "stave-r", "face-l", "face-r", "eye-l", "eye-r"];
var SG = L.duplicate();
SG.name = "donor sigil";
function stonesOf(layer) {
  return layer.property("ADBE Root Vectors Group").property("youspeak").property("ADBE Vectors Group");
}
for (var bi = 0; bi < BODY.length; bi++) stonesOf(SG).property(BODY[bi]).remove();
stonesOf(L).property("sigil-hebrew").remove();

function stone(name) {
  var g = stonesOf(L).property(name) || stonesOf(SG).property(name);
  if (!g) throw new Error("no stone " + name);
  return g;
}
function tf(g, which) { return g.property("ADBE Vector Transform Group").property(which); }
function fill(g) { return g.property("ADBE Vectors Group").property("ADBE Vector Graphic - Fill"); }
function pivot(g, p) {
  tf(g, "ADBE Vector Anchor").setValue(p);
  tf(g, "ADBE Vector Position").setValue(p);
}

// ---------- I. two staves, cut top to bottom ----------
var staves = [["stave-l", [140, 160], 0.20], ["stave-r", [640, 160], 0.32]];
for (var s = 0; s < staves.length; s++) {
  var g = stone(staves[s][0]); var t0 = staves[s][2];
  pivot(g, staves[s][1]);                                   // the top of the stave
  animate(tf(g, "ADBE Vector Scale"), [[t0, [100, 0]], [t0 + 0.58, [100, 100]]], EASE.outExpo);
  animate(tf(g, "ADBE Vector Group Opacity"), [[t0, 0], [t0 + 0.10, 100]], EASE.outSine);
}

// ---------- II. the faces come toward each other (and stop) ----------
var faces = [["face-l", [220, 405], -1], ["face-r", [560, 405], 1]];
var DRIFT = 46;  // mark units each face travels; they stop 70 apart, the column open
for (var f = 0; f < faces.length; f++) {
  var g2 = stone(faces[f][0]); var base = faces[f][1]; var side = faces[f][2];
  tf(g2, "ADBE Vector Anchor").setValue(base);
  animate(tf(g2, "ADBE Vector Position"),
          [[0.85, [base[0] + side * DRIFT, base[1]]], [1.55, base]], EASE.outQuint);
  animate(tf(g2, "ADBE Vector Group Opacity"), [[0.85, 0], [1.20, 100]], EASE.outSine);
}

// ---------- III. the eyes open, level ----------
var eyes = [["eye-l", [305, 225]], ["eye-r", [475, 225]]];
for (var e = 0; e < eyes.length; e++) {
  var g3 = stone(eyes[e][0]);
  pivot(g3, eyes[e][1]);                                    // eye centre: lids part both ways
  animate(tf(g3, "ADBE Vector Scale"), [[1.45, [100, 0]], [1.80, [100, 100]]], EASE.outQuint);
  animate(tf(g3, "ADBE Vector Group Opacity"), [[1.45, 0], [1.52, 100]], EASE.outSine);
}

// ---------- IV. the donor sigil is chiselled ----------
var sig = stone("sigil-hebrew");
var sc = sig.property("ADBE Vectors Group");
var chisel = sc.addProperty("ADBE Vector Graphic - Stroke");
chisel.name = "chisel";
chisel.property("ADBE Vector Stroke Color").setValue(GOLD);
chisel.property("ADBE Vector Stroke Width").setValue(2.5 * 100 / S);   // 2.5 px on screen
chisel.property("ADBE Vector Stroke Line Join").setValue(1);           // miter
var trim = sc.addProperty("ADBE Vector Filter - Trim");
trim.name = "chisel path";
animate(trim.property("ADBE Vector Trim End"), [[1.80, 0], [2.20, 100]], EASE.inOut);
animate(chisel.property("ADBE Vector Stroke Opacity"), [[2.12, 100], [2.45, 0]], EASE.outSine);
animate(fill(sig).property("ADBE Vector Fill Opacity"), [[2.05, 0], [2.40, 100]], EASE.outSine);

// ---------- V. one breath ----------
// gold warms toward gold-h at the crest, then cools (body stones only; the sigil stays cut)
var body = BODY;
var WARM = [GOLD[0] + (GOLD_H[0] - GOLD[0]) * 0.6, GOLD[1] + (GOLD_H[1] - GOLD[1]) * 0.6,
            GOLD[2] + (GOLD_H[2] - GOLD[2]) * 0.6, 1];
for (var b = 0; b < body.length; b++) {
  animate(fill(stone(body[b])).property("ADBE Vector Fill Color"),
          [[1.90, GOLD], [2.70, WARM], [3.50, GOLD]], EASE.inOutSine);
}

// a glow that swells and recedes (raster only: Lottie cannot carry it, the column below can)
var glow = L.property("ADBE Effect Parade").addProperty("ADBE Glo2");
glow.name = "breath glow";
// Enum values found by rendering a matrix (effect.list gives only bare numbers): Composite Original
// 1 = the glow is laid over the stones (it bleached the gold to cream), 2 = the stones stay on top,
// 3 = glow only. Glow Colors 2 = A & B colours.
glow.property("ADBE Glo2-0001").setValue(1);       // based on: alpha channel
glow.property("ADBE Glo2-0002").setValue(50);      // threshold
glow.property("ADBE Glo2-0003").setValue(40);      // radius
glow.property("ADBE Glo2-0005").setValue(2);       // composite original: on top (stones stay crisp)
glow.property("ADBE Glo2-0007").setValue(2);       // glow colours: A & B
glow.property("ADBE Glo2-0013").setValue(GOLD_H);  // A
glow.property("ADBE Glo2-0014").setValue(GOLD);    // B
animate(glow.property("ADBE Glo2-0004"), [[1.90, 0], [2.70, 0.45], [3.50, 0]], EASE.inOutSine);

// the column of light in the between (Room VII: the middle needn't be filled; it holds light)
var col = comp.layers.addShape();
col.name = "the between";
col.moveAfter(L);                                   // beneath the stones
col.transform.anchorPoint.setValue([0, 0, 0]);
col.transform.position.setValue([540, 540 + (405 - 390) * S / 100, 0]);   // where the faces almost meet
var R = 420;
function lightGroup(name, aspect, stops) {
  var g = col.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
  g.name = name;
  var c = g.property("ADBE Vectors Group");
  var el = c.addProperty("ADBE Vector Shape - Ellipse");
  el.property("ADBE Vector Ellipse Size").setValue([2 * R, 2 * R]);
  var gf = c.addProperty("ADBE Vector Graphic - G-Fill");
  // friction F-JSX-GRAD: the gradient fill's children answer to engine ids (type/start/end/colors),
  // not the AE matchNames ("ADBE Vector Grad Type"...), and Colors cannot be set from JSX at all
  // ("value must be a number"), so the colours go through the engine's prop.set.
  gf.property("type").setValue(2);                                // radial (JSX 1-based; engine enum 1)
  gf.property("start").setValue([0, 0]);
  gf.property("end").setValue([R, 0]);
  app.run("prop.set", { layer: col.id, path: "contents/" + name + "/contents/gfill/colors",
    value: { t: "Gradient", v: { colors: [[0, GOLD_H], [1, GOLD_H]], opacities: stops } } });
  g.property("ADBE Vector Transform Group").property("ADBE Vector Scale").setValue([aspect, 100]);
  return g;
}
// stops follow a soft bell rather than two straight ramps: the first cut (0 → .45 → 1) left the halo's
// rim visible as an oval at the crest
lightGroup("halo", 60, [[0, 0.16], [0.2, 0.125], [0.4, 0.075], [0.6, 0.036], [0.8, 0.012], [1, 0]]);
lightGroup("core", 9,  [[0, 0.62], [0.15, 0.44], [0.35, 0.21], [0.6, 0.07], [0.8, 0.02], [1, 0]]);
animate(col.transform.opacity, [[1.60, 0], [2.70, 100], [3.50, 58]], EASE.inOutSine);
animate(col.transform.scale, [[1.60, [100, 70, 100]], [2.70, [100, 104, 100]], [3.50, [100, 100, 100]]],
        EASE.inOutSine);

app.project.save();
writeLn("built: " + comp.name + " " + comp.width + "x" + comp.height + " " + comp.duration + "s, layers " + comp.numLayers);
