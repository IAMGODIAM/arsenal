#!/bin/bash
# HyperFrames environment bootstrap — idempotent. Solves Node22 + Chromium + headless-shell + CLI + ffmpeg.
set +e
cd /app
echo "════ HyperFrames Env Bootstrap ════"

NODEMAJ=$(node -v 2>/dev/null | sed 's/v\([0-9]*\).*/\1/')
if [ -z "$NODEMAJ" ] || [ "$NODEMAJ" -lt 22 ]; then
  echo "→ installing Node 22…"
  npm install -g n >/dev/null 2>&1
  N_PREFIX=/usr/local n 22 >/dev/null 2>&1
  hash -r
fi
echo "✓ Node $(node -v)"

if ! command -v chromium >/dev/null 2>&1; then
  echo "→ installing chromium + unzip + ffmpeg…"
  apt-get update -qq >/dev/null 2>&1
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq chromium unzip ffmpeg fonts-liberation >/dev/null 2>&1
fi
command -v unzip >/dev/null 2>&1 || DEBIAN_FRONTEND=noninteractive apt-get install -y -qq unzip >/dev/null 2>&1
command -v ffmpeg >/dev/null 2>&1 || DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg fonts-liberation >/dev/null 2>&1
echo "✓ $(chromium --version 2>/dev/null || echo chromium present)"
echo "✓ $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"

SHELL_BIN=$(find /app/chrome-headless-shell -name chrome-headless-shell -type f 2>/dev/null | head -1)
if [ -z "$SHELL_BIN" ]; then
  echo "→ installing chrome-headless-shell…"
  rm -rf /app/chrome-headless-shell
  npx --yes @puppeteer/browsers install chrome-headless-shell@stable >/dev/null 2>&1
  SHELL_BIN=$(find /app/chrome-headless-shell -name chrome-headless-shell -type f 2>/dev/null | head -1)
fi
echo "✓ headless-shell: ${SHELL_BIN:-(fallback chromium)}"

npm ls -g hyperframes >/dev/null 2>&1 || npm install -g hyperframes >/dev/null 2>&1
echo "✓ hyperframes installed"

touch .agents/.env
grep -q HYPERFRAMES_BROWSER_PATH .agents/.env 2>/dev/null || [ -n "$SHELL_BIN" ] && echo "HYPERFRAMES_BROWSER_PATH=$SHELL_BIN" >> .agents/.env
grep -q "CHROME_PATH=" .agents/.env 2>/dev/null || echo "CHROME_PATH=/usr/bin/chromium" >> .agents/.env
# faster-whisper for word-level caption timing (montage karaoke captions)
python3 -c "import faster_whisper" 2>/dev/null || { echo "→ installing faster-whisper…"; pip install -q faster-whisper 2>/dev/null; }
echo "✓ faster-whisper $(python3 -c 'import faster_whisper;print(faster_whisper.__version__)' 2>/dev/null || echo missing)"
echo "════ Bootstrap complete ════"
