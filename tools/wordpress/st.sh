#!/bin/bash
cid="$1"; K="wsp_898307c91512f50a0c38"; U="https://n8n-wmlc.srv1480016.hstgr.cloud/webhook/panel-gaql"
q="SELECT search_term_view.search_term, metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros FROM search_term_view WHERE segments.date BETWEEN '2024-10-23' AND '2026-10-23' AND metrics.impressions > 0 ORDER BY metrics.clicks DESC LIMIT 5000"
body=$(python3 -I -c 'import json,sys; print(json.dumps({"k":sys.argv[1],"cid":sys.argv[2],"gaql":sys.argv[3]}))' "$K" "$cid" "$q")
curl -sS --max-time 300 -X POST -H "Content-Type: application/json" -d "$body" "$U" -o "st/${cid}.json" || echo fail
echo "$cid $(wc -c < st/${cid}.json)"
