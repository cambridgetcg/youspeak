// verify.jsx: proves the reveal ENDS ON THE STILL MARK and starts on darkness.
// Run by recipe.sh: effectcraft-cli script verify.jsx panim-reveal.ecproj   (throws → exit 1)
var comp = null;
for (var i = 1; i <= app.project.numItems; i++) if (app.project.item(i).name === "Panim") comp = app.project.item(i);
var END = comp.duration - comp.frameDuration;      // the last frame, 3.9667 s (4.0 s is the out point: empty)
var fails = [], checks = 0;
function near(a, b, eps) {
  if (a instanceof Array) { for (var k = 0; k < b.length; k++) if (Math.abs(a[k] - b[k]) > eps) return false; return true; }
  return Math.abs(a - b) <= eps;
}
function expect(label, got, want, eps) {
  checks++;
  if (!near(got, want, eps === undefined ? 1e-4 : eps)) fails.push(label + ": got " + JSON.stringify(got) + ", want " + JSON.stringify(want));
}
var GOLD = [201 / 255, 164 / 255, 92 / 255, 1], CUT = [117 / 255, 90 / 255, 40 / 255, 1];
// the exact outlines of kit/mark.svg (VectorCraft split them; nothing may move them)
var MARK = {
  "stave-l": [[100, 160], [100, 600], [180, 600], [180, 160]],
  "stave-r": [[600, 160], [600, 600], [680, 600], [680, 160]],
  "face-l":  [[220, 325], [355, 405], [220, 485]],
  "face-r":  [[560, 325], [425, 405], [560, 485]],
  "eye-l":   [[260, 270], [350, 270], [350, 180], [260, 180]],
  "eye-r":   [[430, 270], [520, 270], [520, 180], [430, 180]],
  "sigil-hebrew": [[0, 0], [80, 0], [40, 75]]
};
var layers = { "panim": comp.layer("panim"), "donor sigil": comp.layer("donor sigil") };
for (var ln in layers) {
  var L = layers[ln];
  expect(ln + " anchor", L.transform.anchorPoint.valueAtTime(END, false), [390, 390, 0]);
  expect(ln + " position", L.transform.position.valueAtTime(END, false), [540, 540, 0]);
  expect(ln + " scale", L.transform.scale.valueAtTime(END, false), [88, 88, 100]);
  expect(ln + " opacity", L.transform.opacity.valueAtTime(END, false), 100);
  var stones = L.property("ADBE Root Vectors Group").property("youspeak").property("ADBE Vectors Group");
  for (var s = 1; s <= stones.numProperties; s++) {
    var g = stones.property(s), nm = g.name, t = g.property("ADBE Vector Transform Group");
    var c = g.property("ADBE Vectors Group");
    expect(nm + " scale@end", t.property("ADBE Vector Scale").valueAtTime(END, false), [100, 100]);
    expect(nm + " position=anchor@end", t.property("ADBE Vector Position").valueAtTime(END, false),
           t.property("ADBE Vector Anchor").valueAtTime(END, false));
    expect(nm + " opacity@end", t.property("ADBE Vector Group Opacity").valueAtTime(END, false), 100);
    var f = c.property("ADBE Vector Graphic - Fill");
    expect(nm + " fill colour@end", f.property("ADBE Vector Fill Color").valueAtTime(END, false), nm === "sigil-hebrew" ? CUT : GOLD, 1e-3);
    expect(nm + " fill opacity@end", f.property("ADBE Vector Fill Opacity").valueAtTime(END, false), 100);
    var verts = c.property("ADBE Vector Shape - Group").property("ADBE Vector Shape").valueAtTime(END, false).vertices;
    checks++;
    if (JSON.stringify(verts) !== JSON.stringify(MARK[nm])) fails.push(nm + " outline changed: " + JSON.stringify(verts));
    // first frame: nothing visible yet (opacity 0, or a scale that collapses it, or fill opacity 0)
    var o0 = t.property("ADBE Vector Group Opacity").valueAtTime(0, false) * f.property("ADBE Vector Fill Opacity").valueAtTime(0, false);
    expect(nm + " invisible@0", o0, 0);
  }
}
var chisel = layers["donor sigil"].property("ADBE Root Vectors Group").property("youspeak").property("ADBE Vectors Group")
  .property("sigil-hebrew").property("ADBE Vectors Group").property("chisel");
expect("chisel stroke gone@end", chisel.property("ADBE Vector Stroke Opacity").valueAtTime(END, false), 0);
var col = comp.layer("the between");
expect("the between rests@end", col.transform.opacity.valueAtTime(END, false), 58);
expect("the between dark@0", col.transform.opacity.valueAtTime(0, false), 0);
var glow = layers["panim"].property("ADBE Effect Parade").property("breath glow");
expect("glow back to 0@end", glow.property("ADBE Glo2-0004").valueAtTime(END, false), 0);
// nothing still moving in the final half second
var props = [col.transform.opacity, glow.property("ADBE Glo2-0004")];
for (var p = 0; p < props.length; p++) expect("still from 3.5 s (" + props[p].name + ")", props[p].valueAtTime(3.5, false), props[p].valueAtTime(END, false));

if (fails.length) throw new Error("verify: " + fails.length + " of " + checks + " checks failed\n  " + fails.join("\n  "));
writeLn("verify: all " + checks + " checks pass (end frame " + END.toFixed(4) + " s = the still mark; frame 0 dark)");
