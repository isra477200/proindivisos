# Herramientas de construcción (zonaproindiviso.com)

Scripts usados para construir la web con el MCP oficial de Elementor (editor V4) y la REST de WordPress. **No contienen credenciales**: leen un fichero `wp.env` local (fuera del repo) con `WP=https://...`, `P1=usuario:app-password`.

- `emcp.sh` — llamador del MCP de Elementor: `./emcp.sh <tool> '<json>'`.
- `design.py` — tokens, helpers (`Comp`, `btn_style`, `section`, `inner`, `overline`) y tags dinámicos (teléfono, WhatsApp, popup 22).
- `pagebuilder.py` — `build(spec)` / `run(spec)` para páginas de intención (hero con formulario corto, secciones text/cards/steps/list/callout/table, FAQ con schema, relacionados, CTA con formulario completo) y `build_simple` para legales. `meta()` fija título corto y metas de Yoast por REST (siempre **después** de publicar: publish-document restaura título y metas del borrador).
- `lote1..5` — contenido de cada página (IDs en `pages_ids.json` del cuaderno de trabajo).
- `geobuilder.py` — genera las páginas geo a partir de `tools/geo/geo_*.json` (texto local único por lugar escrito según `tools/geo/BRIEF.md`): crea la página hija bajo `/vender-proindiviso/`, compone, publica y fija metas.
- `gen_home.py`, `gen_hf_body.py` — home (23), cabecera (20) y pie (105).
- `snippet_zp.php` — snippet (Code Snippets, global) con teléfono/WhatsApp como ajustes, shortcodes, tags dinámicos de Elementor, teléfono en el schema Organization de Yoast y metas de Yoast expuestas a REST.

Añadido desde Cowork (23/10/2026):
- `images.json` — mapa `post_id -> media_id` de la imagen de cada página (generado en la sesión de imágenes; las geo heredan la de su comunidad). `pagebuilder.build()` lo lee y, si hay imagen, inserta la banda "Figura" (e-image, aspecto 2.4:1 en escritorio, 16:9 en móvil) entre el hero y la primera sección. En entradas y en las 7 guías (`DATED_PAGES`) añade bajo las migas el párrafo `[zp_actualizado]`.
- `set_featured.py` — fija `featured_media` según `images.json` (og:image/twitter:image de Yoast; Yoast reconstruye el indexable en el siguiente guardado, que `meta()` ya provoca).
- `snippet_toc.php` — snippet 45 (global): shortcode `[zp_actualizado]` e índice de contenidos server-side (`<nav class="zp-toc">` con anclas `id` en los H2; entradas y 7 guías; el último H2, el del CTA, se excluye).
- `gracias.py` — página /gracias/ (ahora **1359**; la 14 no era de Elementor y marcarla por meta no basta: sin `elementor-create-page` no se genera CSS local).
- `resave_ids.py` — regraba documentos por ID vía snippet de un solo uso. Dos lecciones: el snippet se ejecuta en la **siguiente petición** tras activarse (vale una petición REST autenticada), y `Document::save()` exige usuario con permiso de edición, así que el snippet hace `wp_set_current_user(1)` (en `init` aún no hay usuario aunque la petición lleve Basic auth). Sin eso, "regraba" sin regrabar nada.
- `resave_follow.py` — sigue los logs de los builders y regraba por lotes lo ya publicado, para acortar la ventana sin estilos.
- `build_new.py` — crea y publica las entradas de `blog/blog_7.json` asignando su imagen.
- `blogbuilder.py` — `geo_related()` añade a "También te puede interesar" hasta 2 enlaces a la página geo de la ciudad/provincia/CCAA que el texto menciona. `geobuilder.py` — bloque "Guías" (3 entradas rotadas por hash) en CCAA y provincias.
- `yoastqa.py` — puntuación real de Yoast (SEO + legibilidad) de todas las URL con la librería `yoastseo`; `--save` guarda las puntuaciones en Yoast. `intencion_kw.py` — keyphrase, título SEO y descripción de las páginas de intención (lo leen `pagebuilder.page_kw()` y `metas_intencion.py`). `snippet_yoast_scores.php` — snippet 95.
- Los builders esperan `blog/` y `geo/` junto a ellos: en este repo son enlaces simbólicos a `../blog` y `../geo`.

Lecciones del MCP de Elementor V4: `style` no admite selectores anidados; `flex` abreviado no es fiable; email.to del formulario debe ser estático; build-composition sobre un documento ya publicado (página o site part) no actualiza la versión publicada: `run()` pasa la página a borrador antes de componer; para site parts, crear una nueva en borrador, publicar y borrar la vieja; el WAF de Hostinger devuelve 403 a cuerpos PUT con `<style`.
