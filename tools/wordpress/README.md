# Herramientas de construcción (zonaproindiviso.com)

Scripts usados para construir la web con el MCP oficial de Elementor (editor V4) y la REST de WordPress. **No contienen credenciales**: leen un fichero `wp.env` local (fuera del repo) con `WP=https://...`, `P1=usuario:app-password`.

- `emcp.sh` — llamador del MCP de Elementor: `./emcp.sh <tool> '<json>'`.
- `design.py` — tokens, helpers (`Comp`, `btn_style`, `section`, `inner`, `overline`) y tags dinámicos (teléfono, WhatsApp, popup 22).
- `pagebuilder.py` — `build(spec)` / `run(spec)` para páginas de intención (hero con formulario corto, secciones text/cards/steps/list/callout/table, FAQ con schema, relacionados, CTA con formulario completo) y `build_simple` para legales. `meta()` fija título corto y metas de Yoast por REST (siempre **después** de publicar: publish-document restaura título y metas del borrador).
- `lote1..5` — contenido de cada página (IDs en `pages_ids.json` del cuaderno de trabajo).
- `geobuilder.py` — genera las páginas geo a partir de `tools/geo/geo_*.json` (texto local único por lugar escrito según `tools/geo/BRIEF.md`): crea la página hija bajo `/vender-proindiviso/`, compone, publica y fija metas.
- `gen_home.py`, `gen_hf_body.py` — home (23), cabecera (20) y pie (105).
- `snippet_zp.php` — snippet (Code Snippets, global) con teléfono/WhatsApp como ajustes, shortcodes, tags dinámicos de Elementor, teléfono en el schema Organization de Yoast y metas de Yoast expuestas a REST.

Lecciones del MCP de Elementor V4: `style` no admite selectores anidados; `flex` abreviado no es fiable; email.to del formulario debe ser estático; no reconstruir con build-composition una site part publicada (CSS obsoleto): crear nueva en borrador, publicar y borrar la vieja; el WAF de Hostinger devuelve 403 a cuerpos PUT con `<style`.
