#!/bin/bash
# $1 = número de lotes (45 docs cada uno) ; regraba documentos modificados en las últimas 4 h
cd "$(dirname "$0")"; . ./wp.env
for i in $(seq 1 ${1:-6}); do
  python3 -I -c 'import json; print(json.dumps({"name":"ZP una vez — regrabar documentos recientes (lote)","desc":"Regraba hasta 45 documentos modificados en 4 h.","code":open("resave_recent.php").read(),"tags":["zona-proindiviso"],"scope":"single-use","active":True,"priority":10}))' > snippet_resave_recent.json
  curl -sS -u "$P1" -X POST -H "Content-Type: application/json" "$WP/wp-json/code-snippets/v1/snippets" -d @snippet_resave_recent.json | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print("snippet",d.get("id"))'
  curl -sS -o /dev/null --max-time 120 "https://zonaproindiviso.com/contacto/?t=$RANDOM"; sleep 2
done
