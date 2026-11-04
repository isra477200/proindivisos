# Imágenes (MiniMax image-01 vía webhook n8n `panel-img`)

- `manifest.py` → `manifest.json` (1ª tanda, 115: entradas, intención, CCAA). `manifest2.py` → `manifest2.json` (2ª tanda, 145: 43 provincias + 5 ciudades grandes con imagen propia y "Figura 2" en intención, guías y entradas).
- `gen.py` genera (3 hilos, reintentos; WebP q82 1280×720) en `out/`; la clave del webhook va en la variable de entorno `PANEL_IMG_KEY`. `MANIFEST=manifest2.json python3 gen.py [claves…]`.
- `upload.py` sube a la biblioteca de medios con alt/título (`MANIFEST=…`), y guarda `media_map*.json`.
- `../apply_images2.py media_map2.json manifest2.json` vuelca a `../images.json` (cabecera; las ciudades heredan la de su provincia) e `../images2.json` (Figura 2) e imprime los IDs geo a recomponer; después `../set_featured.py <ids>`.
- Revisión: hojas de contacto de 20 (texto, caras); las que salen con texto se regeneran con otra escena (calendarios, mapas, papeles y bancos tienden a sacar letras).
