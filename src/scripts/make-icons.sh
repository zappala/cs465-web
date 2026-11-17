#!/usr/bin/env bash
# Generate the site icons in public/ from public/icon.svg (the only source).
#
#   public/icon.svg              browser tabs (modern browsers), hand-edited source
#   public/favicon.ico           32x32, older browsers and tools that fetch /favicon.ico
#   public/apple-touch-icon.png  180x180, iPhone/iPad home screen
#   public/icon-192.png          192x192, Android (listed in manifest.webmanifest)
#   public/icon-512.png          512x512, Android (listed in manifest.webmanifest)
#
# Needs Google Chrome (to render the SVG) and macOS `sips` (to resize and make
# the .ico). Run from anywhere: src/scripts/make-icons.sh
set -euo pipefail

cd "$(dirname "$0")/../../public"
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cp icon.svg "$work/"
cat > "$work/render.html" <<'HTML'
<html><body style="margin:0"><img src="icon.svg" style="width:512px;height:512px;display:block"></body></html>
HTML

# Render once at 512x512, then scale down.
"$chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=512,512 \
    --screenshot="$work/icon-512.png" "file://$work/render.html" >/dev/null 2>&1

cp "$work/icon-512.png" icon-512.png
sips -z 192 192 "$work/icon-512.png" --out icon-192.png >/dev/null
sips -z 180 180 "$work/icon-512.png" --out apple-touch-icon.png >/dev/null
sips -z 32 32 "$work/icon-512.png" --out "$work/icon-32.png" >/dev/null
sips -s format ico "$work/icon-32.png" --out favicon.ico >/dev/null

file icon-512.png icon-192.png apple-touch-icon.png favicon.ico
