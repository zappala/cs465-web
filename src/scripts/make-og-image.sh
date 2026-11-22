#!/usr/bin/env bash
# Generate public/og-image.png (1200x630 link-preview image) from
# src/scripts/og-image.html. Needs Google Chrome. Run from anywhere.
set -euo pipefail

cd "$(dirname "$0")"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

"$chrome" --headless=new --disable-gpu --hide-scrollbars \
  --allow-file-access-from-files --window-size=1200,630 \
  --screenshot="$PWD/../../public/og-image.png" "file://$PWD/og-image.html" 2>/dev/null
sips -g pixelWidth -g pixelHeight ../../public/og-image.png | tail -2
