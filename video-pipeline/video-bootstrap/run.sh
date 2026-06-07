#!/bin/bash
# video-bootstrap — idempotent one-shot recovery of the HyperFrames render toolchain.
# DAG: video-toolchain-persist-2026-0607
# Restarts wipe apt + global-npm + /tmp. /app survives. This rebuilds the runtime.
# Safe to run anytime: if a layer is already present it's a 2s no-op.
# Usage:  bash .agents/skills/video-bootstrap/run.sh           (heal)
#         bash .agents/skills/video-bootstrap/run.sh --probe   (report only, exit 0=ok 1=wiped)
set +e

probe() {
  local ok=1
  node -v 2>/dev/null | grep -q "v2[2-9]" || { echo "  ✗ node22";        ok=0; }
  command -v ffmpeg >/dev/null 2>&1        || { echo "  ✗ ffmpeg";        ok=0; }
  npm ls -g hyperframes >/dev/null 2>&1    || { echo "  ✗ hyperframes";   ok=0; }
  local SB=$(find /app/chrome-headless-shell -name chrome-headless-shell -type f 2>/dev/null|head -1)
  [ -n "$SB" ] && ldd "$SB" 2>/dev/null | grep -q "not found" && { echo "  ✗ chromium-libs"; ok=0; }
  return $((1-ok))
}

if [ "$1" = "--probe" ]; then
  if probe >/tmp/_vbprobe 2>&1; then echo "TOOLCHAIN_OK"; exit 0
  else cat /tmp/_vbprobe; echo "TOOLCHAIN_WIPED"; exit 1; fi
fi

echo "▶ video-bootstrap: checking toolchain..."
if probe >/dev/null 2>&1; then echo "✓ toolchain intact — no-op"; exit 0; fi

# 1. Node 22
if ! node -v 2>/dev/null | grep -q "v2[2-9]"; then
  echo "→ node 22..."; npm install -g n >/dev/null 2>&1; N_PREFIX=/usr/local n 22 >/dev/null 2>&1; hash -r
fi

# 2. ffmpeg + fonts
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "→ ffmpeg..."; apt-get update -qq >/dev/null 2>&1
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg fonts-liberation >/dev/null 2>&1
fi

# 3. chromium runtime libs (the libnspr4.so family)
SB=$(find /app/chrome-headless-shell -name chrome-headless-shell -type f 2>/dev/null|head -1)
if [ -n "$SB" ] && ldd "$SB" 2>/dev/null | grep -q "not found"; then
  echo "→ chromium libs..."
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 libatspi2.0-0 >/dev/null 2>&1
fi

# 4. hyperframes (global)
if ! npm ls -g hyperframes >/dev/null 2>&1; then
  echo "→ hyperframes..."; npm install -g hyperframes >/dev/null 2>&1
fi

echo "▶ re-probing..."
if probe; then echo "✓ TOOLCHAIN RESTORED"; exit 0
else echo "✗ STILL INCOMPLETE (see above)"; exit 1; fi
