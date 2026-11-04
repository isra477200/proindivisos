#!/bin/bash
# para cada URL del sitemap: ratio de clases de estilo del documento principal presentes en su CSS local
curl -sS "https://zonaproindiviso.com/page-sitemap.xml?q=$RANDOM" | grep -o '<loc>[^<]*' | sed 's/<loc>//' > all_urls.txt
curl -sS "https://zonaproindiviso.com/post-sitemap.xml?q=$RANDOM" | grep -o '<loc>[^<]*' | sed 's/<loc>//' >> all_urls.txt
echo "urls: $(wc -l < all_urls.txt)"; bad=0
while read u; do
  html=$(curl -sS "$u"); id=$(echo "$html" | grep -o 'data-elementor-id="[0-9]*"' | grep -v '"20"\|"22"\|"684"' | head -1 | grep -o '[0-9]*')
  [ -z "$id" ] && { echo "SIN ELEMENTOR $u"; bad=$((bad+1)); continue; }
  css=$(curl -sS "https://zonaproindiviso.com/wp-content/uploads/elementor/css/local-$id-frontend-desktop.css?x=$RANDOM")
  r=$(python3 -I - "$id" "$u" <<PY
import re,sys
h='''$(echo "$html" | sed "s/'''//g")'''
c='''$(echo "$css" | sed "s/'''//g")'''
id=sys.argv[1]
i=h.find('data-elementor-id="'+id+'"'); seg=h[i:]; j=seg.find('data-elementor-id="',30); seg=seg[:j] if j>0 else seg
cls=set(re.findall(r'\be-([0-9a-f]{5,8}-[0-9a-f]{4})\b',seg)); hit=sum(1 for x in cls if 'e-'+x in c)
print(f'{len(cls)} {hit}')
PY
)
  n=${r% *}; k=${r#* }
  if [ "$n" -gt 0 ] && [ $((k*100/n)) -lt 60 ]; then echo "MISMATCH $u doc=$id $k/$n"; bad=$((bad+1)); fi
done < all_urls.txt
echo "problemas css: $bad"
