#!/bin/bash
# $1 url  $2 docid : cuántas clases de estilo del HTML del documento existen en su CSS local
u="$1"; id="$2"
curl -sS "$u?c=$RANDOM" > /tmp/pg_$id.html
curl -sS "https://zonaproindiviso.com/wp-content/uploads/elementor/css/local-$id-frontend-desktop.css?x=$RANDOM" > /tmp/l_$id.css
python3 -I - "$id" <<'PY'
import re,sys
id=sys.argv[1]; h=open(f'/tmp/pg_{id}.html').read(); c=open(f'/tmp/l_{id}.css').read()
i=h.find(f'data-elementor-id="{id}"'); seg=h[i:]
j=seg.find('data-elementor-id="',30); seg=seg[:j] if j>0 else seg
cls=set(re.findall(r'\be-([0-9a-f]{5,8}-[0-9a-f]{4})\b',seg))
hit=sum(1 for x in cls if f'e-{x}' in c)
print(f'doc {id}: clases html={len(cls)} en css={hit} css_bytes={len(c)}')
PY
