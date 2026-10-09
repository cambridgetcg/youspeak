// gif.jsx: a 512 px, 20 fps cut of comp "Panim" that holds the still mark at the end.
// Run by recipe.sh after build.jsx, on the same project:  effectcraft-cli script gif.jsx panim-reveal.ecproj
// Why 20 fps: GIF delays are in 1/100 s, so 30 fps becomes 30 ms frames and plays 11% fast.
// Why loop off: the GIF plays once and ends on the still mark. The 0.5 s hold is for viewers that loop
// it anyway. It is short because the v0.6.0 GIF writer stores every frame whole (no frame differencing,
// no merging of identical frames), so each held frame costs about 21 KB.
var src = null, old = null;
for (var i = 1; i <= app.project.numItems; i++) {
  var it = app.project.item(i);
  if (it.name === "Panim") src = it;
  if (it.name === "Panim GIF") old = it;
}
if (!src) throw new Error("comp Panim not found");
if (old) old.remove();

var HOLD = 0.5, SIZE = 512, FPS = 20;
var gif = app.project.items.addComp("Panim GIF", SIZE, SIZE, 1, src.duration + HOLD, FPS);
gif.bgColor = [20 / 255, 16 / 255, 12 / 255];                     // #14100C
var N = gif.layers.add(src);
N.name = "panim reveal";
N.transform.position.setValue([SIZE / 2, SIZE / 2, 0]);
N.transform.scale.setValue([100 * SIZE / src.width, 100 * SIZE / src.height, 100]);
N.collapseTransformation = true;     // the shapes are cut at 512 px, not shrunk from a 1080 raster
// hold the last frame: time-remap 0 → last frame, then stretch the layer over the hold
N.timeRemapEnabled = true;
// key on this comp's 20 fps grid: setValueAtTime snaps the key's TIME to the frame grid but keeps the
// value, so a key at the source's last frame (3.9667 s) lands at 3.95 s with value 3.9667
var last = Math.floor((src.duration - src.frameDuration) * FPS) / FPS;     // 3.95
var tr = N.property("ADBE Time Remapping");
while (tr.numKeys > 0) tr.removeKey(1);
tr.setValueAtTime(0, 0);
tr.setValueAtTime(last, last);
tr.setInterpolationTypeAtKey(1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
tr.setInterpolationTypeAtKey(2, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.HOLD);
N.outPoint = gif.duration;

// one render-queue item, written next to the project (replacing any earlier one for this comp)
var dir = app.project.file.parent.fsName;
var q = app.run("renderQueue.list", {});
for (var k = q.items.length - 1; k >= 0; k--) {
  if (q.items[k].compName === "Panim GIF") app.run("renderQueue.remove", { item: q.items[k].id });
}
var item = app.run("renderQueue.add", { comp: "Panim GIF", format: "gif", loop: false,
                                        output: dir + "/mark-reveal-512.gif" });
app.project.save();
writeLn("gif comp: " + gif.width + "x" + gif.height + " @" + gif.frameRate + " " + gif.duration + "s; remap t(3.0)=" +
        tr.valueAtTime(3.0, false) + " t(4.2)=" + tr.valueAtTime(4.2, false) + "; queue item " + item.id +
        " frames " + item.frames + " loop " + item.output.gif_loop + " → " + item.outputPath);
