#!/bin/bash
# uso: ./emcp.sh <tool> '<json args>'  -> imprime el texto del resultado
. "$(dirname "$0")/wp.env"
SID_FILE="$(dirname "$0")/emcp_sid"
if [ ! -s "$SID_FILE" ]; then
  curl -sS --max-time 60 -u "$P1" -X POST -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" "$WP/wp-json/elementor/mcp/" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"claude","version":"1"}}}' -D - -o /dev/null | grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r' > "$SID_FILE"
fi
SID=$(cat "$SID_FILE")
ARGS="${2:-}"; [ -z "$ARGS" ] && ARGS="{}"
BODY=$(python3 -I -c 'import json,sys; print(json.dumps({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":sys.argv[1],"arguments":json.loads(sys.argv[2])}}))' "$1" "$ARGS")
curl -sS --max-time 180 -u "$P1" -X POST -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: $SID" "$WP/wp-json/elementor/mcp/" -d "$BODY" | python3 -I -c '
import json,sys
raw=sys.stdin.read()
if raw.startswith("event:") or raw.startswith("data:"): raw=[l[5:] for l in raw.splitlines() if l.startswith("data:")][-1]
d=json.loads(raw)
if "error" in d: print("ERROR:", json.dumps(d["error"], ensure_ascii=False)); sys.exit(1)
r=d.get("result",{})
for c in r.get("content",[]):
    if c.get("type")=="text": print(c["text"])
    else: print(json.dumps(c, ensure_ascii=False)[:2000])
if r.get("isError"): print("isError: true")
'
