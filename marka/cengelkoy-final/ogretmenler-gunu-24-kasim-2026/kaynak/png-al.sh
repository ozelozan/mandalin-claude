#!/bin/bash
# Kullanim: bash kaynak/png-al.sh <cikti-klasoru>   (hikaye-*.html -> 1080x1920 PNG)
C="${CHROMIUM:-$HOME/tools/chromium/browsers/chromium-1148/chrome-mac/Chromium.app/Contents/MacOS/Chromium}"
KOK="$(cd "$(dirname "$0")/.." && pwd)"; OUT="${1:-$KOK/png}"; mkdir -p "$OUT"
for f in "$KOK"/hikaye-*.html; do
  n=$(basename "$f" .html)
  "$C" --headless=old --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1080,1920 --virtual-time-budget=5000 --screenshot="$OUT/$n.png" "file://$f#png" >/dev/null 2>&1
  echo "$OUT/$n.png"
done
