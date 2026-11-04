#!/bin/bash
# uso: run.sh <url> <salida.json>
CHROME_PATH="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome" npx lighthouse "$1" --only-categories=performance --form-factor=mobile --screenEmulation.mobile --throttling-method=simulate --chrome-flags="--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage" --output=json --output-path="$2" --quiet 2>&1 | tail -2
