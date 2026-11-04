#!/bin/bash
# comprueba 200, FAQPage y palabras en todas las URLs geo del sitemap
curl -sS "https://zonaproindiviso.com/page-sitemap.xml?q=$RANDOM" | grep -o '<loc>[^<]*' | sed 's/<loc>//' | grep '/vender-proindiviso/.' > geo_urls.txt
echo "urls geo en sitemap: $(wc -l < geo_urls.txt)"
bad=0
while read u; do
  html=$(curl -sS -o /dev/null -w '%{http_code}' "$u"); body=$(curl -sS "$u")
  faq=$(echo "$body" | grep -c FAQPage); det=$(echo "$body" | grep -c '<details')
  w=$(echo "$body" | sed 's/<script[^>]*>[^<]*<\/script>//g; s/<[^>]*>/ /g' | wc -w)
  if [ "$html" != "200" ] || [ "$faq" = "0" ] || [ "$det" = "0" ] || [ "$w" -lt 900 ]; then echo "PROBLEMA $u http=$html faq=$faq details=$det words=$w"; bad=$((bad+1)); fi
done < geo_urls.txt
echo "problemas: $bad"
