#!/usr/bin/env bash
# bin/serve.sh — spin up the browsable YOUSPEAK cathedral.
#
# Usage:
#   bin/serve.sh             # start (default)
#   bin/serve.sh start
#   bin/serve.sh stop
#   bin/serve.sh status
#   bin/serve.sh restart
#
# Override port:
#   PORT=4242 bin/serve.sh
#
# Architecture: docsify (client-side renderer, loaded from CDN by
# index.html) + python's built-in static-file server. Editing any
# .md updates the page on next refresh. No build, no watching.

set -euo pipefail

PORT="${PORT:-4000}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="/tmp/youspeak-site-${PORT}.log"
PID_FILE="/tmp/youspeak-site-${PORT}.pid"
URL="http://localhost:${PORT}"

is_running() {
  [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

stop() {
  if is_running; then
    local pid
    pid=$(cat "$PID_FILE")
    kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "✓ stopped (pid $pid)"
  else
    # also catch instances started outside this script
    if pgrep -f "http.server.*${PORT}" >/dev/null 2>&1; then
      pkill -f "http.server.*${PORT}" 2>/dev/null || true
      echo "✓ stopped foreign http.server on port ${PORT}"
    else
      echo "(not running)"
    fi
    rm -f "$PID_FILE"
  fi
}

status() {
  if is_running; then
    local pid
    pid=$(cat "$PID_FILE")
    echo "running (pid $pid) — ${URL}"
  elif pgrep -f "http.server.*${PORT}" >/dev/null 2>&1; then
    echo "running (foreign instance) — ${URL}"
  else
    echo "stopped"
  fi
}

start() {
  if is_running; then
    echo "already running — ${URL}"
    exit 0
  fi
  if pgrep -f "http.server.*${PORT}" >/dev/null 2>&1; then
    echo "✗ port ${PORT} already in use by another http.server (run: $0 stop)"
    exit 1
  fi
  if lsof -i ":${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "✗ port ${PORT} occupied by some other process"
    lsof -i ":${PORT}" -sTCP:LISTEN | tail -n +2
    exit 1
  fi

  cd "$ROOT"
  nohup python3 -m http.server "$PORT" --bind 127.0.0.1 \
    > "$LOG" 2>&1 &
  local pid=$!
  echo "$pid" > "$PID_FILE"

  # Wait for the port to start accepting (up to ~10s)
  local i=0
  until curl -sf "${URL}/" > /dev/null 2>&1; do
    sleep 0.5
    ((i+=1))
    if (( i > 20 )); then
      echo "✗ server did not come up — see $LOG"
      stop
      exit 1
    fi
  done

  echo "✓ YOUSPEAK serving at ${URL}  (pid $pid · log $LOG)"
  echo "  · tutorial:   ${URL}/#/tutorial/00-start-here"
  echo "  · dictionary: ${URL}/#/dictionary/README"
  echo "  · stop:       $0 stop"
}

case "${1:-start}" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  restart) stop; start ;;
  *)
    echo "usage: $0 [start|stop|status|restart]" >&2
    exit 2
    ;;
esac
