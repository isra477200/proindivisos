#!/bin/bash
curl -sS "https://zonaproindiviso.com/post-sitemap.xml?q=$RANDOM" | grep -o '<loc>[^<]*' | sed 's/<loc>//' > blog_urls.txt
for s in empresas-que-compran-herencias vender-derechos-hereditarios un-heredero-no-quiere-vender vender-la-mitad-de-una-casa vender-nuda-propiedad vender-terreno-proindiviso vender-proindiviso-con-inquilino-u-okupa blog; do echo "https://zonaproindiviso.com/$s/" >> blog_urls.txt; done
echo "urls: $(wc -l < blog_urls.txt)"; bad=0
while read u; do
  body=$(curl -sS -w '\n%{http_code}' "$u"); code=$(echo "$body" | tail -1)
  faq=$(echo "$body" | grep -c FAQPage); det=$(echo "$body" | grep -c '<details'); art=$(echo "$body" | grep -c '"@type":"Article"')
  w=$(echo "$body" | sed 's/<script[^>]*>[^<]*<\/script>//g; s/<[^>]*>/ /g' | wc -w)
  if [ "$code" != "200" ] || [ "$faq" = "0" ] || [ "$det" = "0" ] || [ "$w" -lt 1200 ]; then echo "PROBLEMA $u http=$code faq=$faq details=$det words=$w article=$art"; bad=$((bad+1)); fi
done < blog_urls.txt
echo "problemas: $bad"
