#!/bin/bash
# render-watch — stall-aware background render with self-alert.
# Subcommands: start <dir> <cmd> <logfile> | status <logfile>
# Tracks the real child PID (in <logfile>.pid) so detection is command-agnostic.
set +e
STALL_SECS="${STALL_SECS:-120}"
SUB="$1"; shift

if [ "$SUB" = "start" ]; then
  DIR="$1"; CMD="$2"; LOG="$3"; PIDF="${LOG}.pid"
  SHELL_BIN=$(find /app/chrome-headless-shell -name chrome-headless-shell -type f 2>/dev/null | head -1)
  : > "$LOG"; rm -f "$PIDF"
  setsid bash -c "cd '$DIR'; export PATH=/usr/bin:/usr/local/bin:\$PATH; \
    export HYPERFRAMES_BROWSER_PATH='$SHELL_BIN'; export CHROME_PATH=/usr/bin/chromium; \
    echo \$\$ > '$PIDF'; \
    $CMD >> '$LOG' 2>&1; echo \"__EXIT_\$?\" >> '$LOG'" </dev/null >/dev/null 2>&1 &
  sleep 1
  echo "STARTED log=$LOG pid=$(cat "$PIDF" 2>/dev/null) (stall ${STALL_SECS}s)"
  exit 0
fi

if [ "$SUB" = "status" ]; then
  LOG="$1"; PIDF="${LOG}.pid"
  [ -f "$LOG" ] || { echo "NO_LOG"; exit 0; }
  EXIT_LINE=$(grep -o "__EXIT_[0-9]*" "$LOG" | tail -1)
  COMPLETE=$(grep -c "Render complete" "$LOG")
  # terminal: explicit exit marker present
  if [ -n "$EXIT_LINE" ]; then
    CODE=$(echo "$EXIT_LINE" | grep -o '[0-9]*' | tail -1)
    if [ "$CODE" = "0" ]; then echo "DONE (exit 0)"; else echo "DEAD (exit $CODE)"; fi
    exit 0
  fi
  # alive? check the tracked PID
  PID=$(cat "$PIDF" 2>/dev/null)
  ALIVE=no; [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null && ALIVE=yes
  NOW=$(date +%s); LOGMTIME=$(stat -c %Y "$LOG" 2>/dev/null || echo "$NOW"); LOGAGE=$((NOW - LOGMTIME))
  if [ "$ALIVE" = "no" ]; then echo "DEAD (pid $PID gone, no exit marker — silent crash)"; exit 0; fi
  if [ "$LOGAGE" -gt "$STALL_SECS" ]; then echo "STALL (pid $PID alive but log idle ${LOGAGE}s > ${STALL_SECS}s — kill+relaunch)"; exit 0; fi
  PCT=$(grep -oE "[0-9]+%" "$LOG" | tail -1)
  echo "RUNNING (pid $PID, log fresh ${LOGAGE}s, progress ${PCT:-init})"
  exit 0
fi

echo "usage: run.sh start <dir> <cmd> <logfile> | status <logfile>"
