"""Re-run the confusability audit (../../audit/confusability.py, unmodified) on the three
designers' sets plus the final set. Its outputs are redirected into final/audit/; the
auditor's own folder is not written to. Run: /opt/homebrew/bin/python3 -B work/run_audit.py"""
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path
FINAL = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("confusability", FINAL.parent / "audit" / "confusability.py")
conf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conf)
OUT = FINAL / "audit"
conf.SETS = ["A-address-kin", "B-standing-ground", "C-bond-first", "final"]
conf.HERE = OUT
conf.OUT_JSON = OUT / "results.json"
conf.OUT_PNG = OUT / "neighbours.png"
conf.BUILD_DIR = OUT / "build"
conf.SCRATCH_OTF = OUT / "build" / "anchor-candidates-audit.otf"
_draw = conf.draw_png
def draw_png(*a, out=None, **k):
    return _draw(*a, out=(out if out is not None and str(out).startswith(str(OUT)) else
                          (OUT / Path(out).name if out is not None else OUT / "neighbours.png")), **k)
conf.draw_png = draw_png
conf.main()
