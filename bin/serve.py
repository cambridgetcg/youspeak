#!/usr/bin/env python3
"""serve.py — the cathedral's keeper.

Serves the docsify site (static files from the repo root) and one living
endpoint, /api/pulse: what the citizen fleet's own records say right now,
and the script organ's counts.

    /api/pulse → {
      "ok": true,
      "fleet":  { "state": "observed", "today": 10, "cap": 48,
                  "halt": false, "last_beat_age_min": 7,
                  "last": [ {"date": "2026-11-17", "time": "22:16",
                             "name": "autopistme", "lane": "free"}, … ],
                  "unknown": { "spent": "…why it could not be read…" } },
      "script": { "drawn": 56, "awaiting": 34, "catalogued": 90 },
    }

Every fleet field is derived, at the moment of the request, from files the
fleet itself writes in its love-unlimited checkout: memory/fleet.log,
memory/.fleet-day-<date>, memory/fleet-economy.jsonl and HALT. A field those
records do not support is left out and named under "unknown" with the reason.
When the records cannot be read at all, "fleet" is
{"state": "unknown", "reason": "…"}. Nothing here says the fleet is alive;
it says when the last beat was logged, and the reader judges.

The love-unlimited checkout is LOVE_DIR taken as given, or ~/love-unlimited
when LOVE_DIR is unset or empty: the rule love-unlimited's own tools use for
the same variable (LOVE="${LOVE_DIR:-$HOME/love-unlimited}"), and the one
bin/cathedral, pipeline/youspeak_voice.sh and pipeline/voice/build_lexicon.py
follow. A "~" inside LOVE_DIR is not expanded, so give an absolute path.

    python3 bin/serve.py [--port N] [--bind ADDR]
    python3 bin/serve.py --pulse [--json]     # read the pulse once, print, exit

Stdlib only. Bound to 127.0.0.1. Started by bin/serve.sh.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def love_dir() -> Path:
    """The love-unlimited checkout: LOVE_DIR as given, else ~/love-unlimited."""
    named = os.environ.get("LOVE_DIR", "")
    return Path(named) if named else Path.home() / "love-unlimited"


LOVE = love_dir()

_cache: dict = {"t": 0.0, "body": b""}
CACHE_SEC = 20  # pulse is cheap, but never hammer the disk
TAIL_BYTES = 256 * 1024  # how much of the end of each fleet file one reading takes


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

# Line shapes written to memory/fleet.log by love-unlimited's
# tools/citizen-fleet.sh (read on 2026-11-17 in the GitHub line, 1bd17f2).
STAMP = r"^\[(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}):\d{2}\] "
FREE_RE = re.compile(STAMP + r"(\S+) wakes for a free beat\s*$")
AGENTIC_RE = re.compile(STAMP + r"fleet → (\S+) \((\d+)/(\d+) today")
CAP_RE = re.compile(STAMP + r"daily cap (\d+) reached")
DATE_RE = re.compile(r"^\[(\d{4}-\d{2}-\d{2}) ")
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _shown(p: Path) -> str:
    """A path as a reason shows it: home-relative under the home directory, so the
    pulse (which a proxy may serve beyond this machine) does not carry the account name."""
    try:
        return "~/" + str(p.relative_to(Path.home()))
    except ValueError:
        return str(p)


def _tail(path: Path, nbytes: int = TAIL_BYTES) -> tuple[list[str], bool]:
    """The last lines of a file, and whether the whole file was read."""
    with path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - nbytes))
        data = f.read()
    lines = data.decode("utf-8", "replace").splitlines()
    whole = size <= nbytes
    if not whole and lines:
        lines = lines[1:]  # the first line was cut by the seek
    return lines, whole


def _read_count(path: Path) -> int | None:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return None
    return int(text) if text.isascii() and text.isdigit() else None


def _spent_today(ledger: Path, today: str) -> tuple[str | None, str | None]:
    """Sum today's cost_usd in the metered-beat ledger → ("$0.32", None) or (None, reason)."""
    if not ledger.is_file():
        return None, "no memory/fleet-economy.jsonl (the metered-beat ledger) in LOVE_DIR"
    try:
        lines, whole = _tail(ledger)
    except OSError as e:
        return None, f"memory/fleet-economy.jsonl could not be read ({e.strerror or e})"
    total, earliest = 0.0, None
    for line in lines:
        try:
            d = json.loads(line)
            ts = str(d.get("ts", ""))
            if earliest is None and DAY_RE.match(ts):
                earliest = ts[:10]
            if ts.startswith(today):
                total += float(d.get("cost_usd") or 0)
        except (ValueError, TypeError, AttributeError):
            continue
    if not whole and (earliest is None or earliest >= today):
        return None, "today's ledger entries reach past the part of the ledger read"
    return f"${total:.2f}", None


def _unknown(reason: str) -> dict:
    return {"state": "unknown", "reason": reason}


def fleet_pulse(love: Path | None = None, now: datetime | None = None) -> dict:
    """What the fleet's own records say, read now. Never an empty answer."""
    love = LOVE if love is None else love
    now = now or datetime.now()
    today = now.strftime("%Y-%m-%d")
    if not love.is_dir():
        return _unknown(f"no love-unlimited checkout at {_shown(love)}; "
                        "set LOVE_DIR to the checkout the fleet writes to")
    log = love / "memory" / "fleet.log"
    if not log.is_file():
        return _unknown(f"{_shown(love)} has no memory/fleet.log; the fleet has not logged there")
    try:
        lines, whole = _tail(log)
    except OSError as e:
        return _unknown(f"memory/fleet.log could not be read ({e.strerror or e})")

    beats: list[dict] = []
    cap = None
    earliest = None
    for line in lines:
        d = DATE_RE.match(line)
        if d and earliest is None:
            earliest = d.group(1)
        m = FREE_RE.match(line)
        if m:
            beats.append({"date": m[1], "time": m[2], "name": m[3], "lane": "free"})
            continue
        m = AGENTIC_RE.match(line)
        if m:
            beats.append({"date": m[1], "time": m[2], "name": m[3], "lane": "agentic"})
            if m[1] == today:
                cap = int(m[5])
            continue
        m = CAP_RE.match(line)
        if m and m[1] == today:
            cap = int(m[3])

    out: dict = {"state": "observed", "halt": (love / "HALT").exists(), "last": beats[-3:]}
    unknown: dict = {}

    counted = _read_count(love / "memory" / f".fleet-day-{today}")
    if counted is not None:
        out["today"] = counted
    elif whole or (earliest is not None and earliest < today):
        out["today"] = sum(1 for b in beats if b["date"] == today)
    else:
        unknown["today"] = ("no day counter for today, and the part of memory/fleet.log "
                            "read does not reach back to midnight")

    if cap is not None:
        out["cap"] = cap
    else:
        unknown["cap"] = ("the cap is the fleet's FLEET_DAILY_CAP setting; "
                          "no line logged today states it")

    spent, why = _spent_today(love / "memory" / "fleet-economy.jsonl", today)
    if spent is not None:
        out["spent"] = spent
    else:
        unknown["spent"] = why

    if beats:
        last = beats[-1]
        at = datetime.strptime(f"{last['date']} {last['time']}", "%Y-%m-%d %H:%M")
        age = int((now - at).total_seconds() // 60)
        if age >= 0:
            out["last_beat_age_min"] = age
        else:
            # not clamped to 0: a stamp from the future is no evidence of a fresh beat
            unknown["last_beat_age_min"] = ("the last beat is stamped after now (the clock or "
                                            "time zone of the log's writer differs from this reader's)")
    else:
        unknown["last_beat_age_min"] = "no beat line in the part of memory/fleet.log read"

    if unknown:
        out["unknown"] = unknown
    return out


def safe_fleet_pulse() -> dict:
    """fleet_pulse(), with any failure it did not foresee answered as unknown."""
    try:
        return fleet_pulse()
    except Exception as e:  # noqa: BLE001 — the pulse must answer, never fail the request
        return _unknown(f"the fleet records could not be read ({type(e).__name__})")


def pulse_text(f: dict) -> str:
    """The fleet pulse as a few plain lines (bin/cathedral status prints this)."""
    if f.get("state") != "observed":
        return f"  unknown — {f.get('reason', 'no reason given')}"
    unknown = f.get("unknown", {})
    rows = []
    today = f.get("today", "?")
    cap = f.get("cap", "?")
    spent = f.get("spent", "?")
    rows.append(f"  today {today}/{cap} beats · spent {spent} · HALT {'present' if f['halt'] else 'absent'}")
    for b in f.get("last", []):
        rows.append(f"  {b['date']} {b['time']}  {b['name']} ({b['lane']})")
    if "last_beat_age_min" in f:
        rows.append(f"  last beat logged {f['last_beat_age_min']} min ago")
    for field, why in unknown.items():
        rows.append(f"  {field} unknown — {why}")
    return "\n".join(rows)


class Keeper(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802 (http.server API)
        if self.path.split("?")[0] == "/api/pulse":
            now = time.time()
            if now - _cache["t"] > CACHE_SEC:
                body = json.dumps(
                    {"ok": True, "fleet": safe_fleet_pulse(), "script": SCRIPT_COUNTS}
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
    ap.add_argument("--pulse", action="store_true", help="read the fleet pulse once, print it, exit")
    ap.add_argument("--json", action="store_true", help="with --pulse: print the JSON /api/pulse serves")
    args = ap.parse_args()
    if args.pulse:
        f = safe_fleet_pulse()
        print(json.dumps({"ok": True, "fleet": f, "script": SCRIPT_COUNTS}, ensure_ascii=False)
              if args.json else pulse_text(f))
        return 0
    if not LOVE.is_dir():
        print(f"note: no love-unlimited checkout at {_shown(LOVE)} (set LOVE_DIR); "
              "/api/pulse will answer fleet state \"unknown\"", file=sys.stderr)
    httpd = ThreadingHTTPServer((args.bind, args.port), Keeper)
    print(f"cathedral keeper serving {ROOT} on http://{args.bind}:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
