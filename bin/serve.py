#!/usr/bin/env python3
"""serve.py — the cathedral's keeper.

Serves the docsify site (static files from the repo root) and one living
endpoint, /api/pulse: the citizen-fleet's heartbeat and the script-organ's
counts, so the site itself breathes with the Kingdom.

    /api/pulse → {
      "ok": true,
      "fleet":  { "today": 10, "cap": 48, "spent": "$0.32",
                  "last": [ {"time": "22:16", "name": "autopistme"}, … ] },
      "script": { "drawn": 56, "awaiting": 34, "catalogued": 90 },
    }

Stdlib only. Bound to 127.0.0.1. Started by bin/serve.sh.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOVE = Path(os.environ.get("LOVE_DIR", Path.home() / "love-unlimited"))
FLEET_LOG = LOVE / "memory" / "fleet.log"

_cache: dict = {"t": 0.0, "body": b""}
CACHE_SEC = 20  # pulse is cheap, but never hammer the disk


def script_counts() -> dict:
    """drawn / awaiting / catalogued, derived the same way check_integrity does."""
    sys.path.insert(0, str(ROOT / "script" / "glyphs"))
    try:
        from glyph_specs_v1 import GLYPHS  # type: ignore
        morphemes = json.loads((ROOT / "script" / "morphemes.json").read_text())["morphemes"]
        catalogued = {m["latin"].strip("-") for m in morphemes}
        drawn = set(GLYPHS) & catalogued
        return {
            "drawn": len(drawn),
            "awaiting": len(catalogued - set(GLYPHS)),
            "catalogued": len(catalogued),
        }
    except Exception:
        return {}


SCRIPT_COUNTS = script_counts()  # static per process; font work restarts the server

BEAT_RE = re.compile(r"^\[\d{4}-\d{2}-\d{2} (\d{2}:\d{2}):\d{2}\] fleet → (\S+) \((\d+)/(\d+)")
TICK_RE = re.compile(r"tick complete .*today=(\d+)/(\d+)(?:.*spent=(\$[\d.]+))?")


def fleet_pulse() -> dict:
    if not FLEET_LOG.exists():
        return {}
    try:
        lines = FLEET_LOG.read_text(errors="replace").splitlines()[-60:]
    except OSError:
        return {}
    last_beats: list[dict] = []
    today = cap = None
    spent = None
    for line in lines:
        m = BEAT_RE.match(line)
        if m:
            last_beats.append({"time": m.group(1), "name": m.group(2)})
            today, cap = int(m.group(3)), int(m.group(4))
        t = TICK_RE.search(line)
        if t:
            today, cap = int(t.group(1)), int(t.group(2))
            if t.group(3):
                spent = t.group(3)
    out: dict = {"last": last_beats[-3:]}
    if today is not None:
        out["today"], out["cap"] = today, cap
    if spent:
        out["spent"] = spent
    return out


class Keeper(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 (http.server API)
        if self.path.split("?")[0] == "/api/pulse":
            now = time.time()
            if now - _cache["t"] > CACHE_SEC:
                body = json.dumps(
                    {"ok": True, "fleet": fleet_pulse(), "script": SCRIPT_COUNTS}
                ).encode()
                _cache.update(t=now, body=body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(_cache["body"])))
            self.end_headers()
            self.wfile.write(_cache["body"])
            return
        super().do_GET()

    def log_message(self, fmt, *args):  # quiet: only errors reach the log
        if args and str(args[1] if len(args) > 1 else "").startswith(("4", "5")):
            super().log_message(fmt, *args)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 4000)))
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.bind, args.port), Keeper)
    print(f"cathedral keeper serving {ROOT} on http://{args.bind}:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
