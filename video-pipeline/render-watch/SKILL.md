# render-watch — stall-aware background render with self-alert

Runs a long HyperFrames render (or any long command) in the background, then
watches it. It writes a heartbeat every 15s and a terminal STATUS line so I never
sit blind. Detects three end-states:

- **DONE**   — process exited 0, output file grew, log says "Render complete"
- **STALL**  — process alive but log file hasn't changed in >120s (frozen)
- **DEAD**   — process gone but no completion marker (silent crash)

## Why
Long renders exceed the 300s bash tool limit. Launching with `setsid ... &` and
polling manually means if I forget to poll, momentum dies. This skill makes the
render report its OWN state to a single status file I can cheaply cat.

## Usage
    bash .agents/skills/render-watch/run.sh start  "<dir>" "<cmd>" "<logfile>"
    bash .agents/skills/render-watch/run.sh status "<logfile>"

`start` launches and returns immediately. `status` prints one of:
RUNNING (elapsed, last-log-age) | DONE | STALL | DEAD — cheap to call in a loop.

## Stall rule
If the log mtime is older than STALL_SECS (default 120) while the PID is alive,
status returns STALL so I can kill + relaunch instead of waiting forever.
