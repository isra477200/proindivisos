# Traspaso a Claude Cowork — zonaproindiviso.com (23/10/2026)

Documento único para continuar el trabajo desde Cowork con el MCP de Elementor ya conectado. Todo lo que hay aquí está verificado en la web real. Credenciales: NO están en el repo (Isra las tiene; usuario `admin` con contraseña de aplicación para el MCP y la REST).

## 1. Qué es y cómo se posiciona

- Web de captación de **Zona Proindiviso**: **compramos** proindivisos (cuotas indivisas de pisos, casas, locales, garajes, terrenos) y partes de herencias con fondos propios en toda España. **Nunca** "intermediario", "varias ofertas" ni "te ponemos en contacto".
- Promesa fija en todo el copy: oferta por escrito en 48 h, firma en notaría en 2-4 semanas, pago al contado en notaría, gastos de notaría y gestión a nuestro cargo, sin exclusividad, 40-70 % del valor proporcional de la cuota.
- El nombre del titular (Israel Domingo Gaitán) solo aparece en aviso legal, privacidad y cookies.

## 2. Stack y piezas (IDs reales)

| Pieza | ID / dato |
|---|---|
| WordPress + Hello Elementor + Elementor Pro (editor V4 atómico) + Yoast SEO + Code Snippets + Complianz | Hostinger (LiteSpeed + CDN hcdn) |
| MCP de Elementor | `https://zonaproindiviso.com/wp-json/elementor/mcp/` (Basic auth, Streamable HTTP, header `Mcp-Session-Id`) |
| Cabecera (site part header) | post **20** |
| Popup "Te llamamos nosotros" | post **22** |
| Pie (site part footer) v4 | post **684** (4 columnas + fila de 19 comunidades). Versiones anteriores 21/105/544 borradas |
| Componente formulario corto (hero) | component **83** |
| Componente formulario completo (CTA final) | component **85** |
| Home | página **23** (`/`, slug `inicio`) |
| Páginas de intención | 25 empresas-que-compran-proindivisos · 27 cuanto-pagan · 29 sin-avisar · 31 parte-casa-heredada · 33 opiniones · 35 parte-de-un-piso · 37 con-hipoteca · 39 divorcio · 41 entre-hermanos · 43 extincion-de-condominio (hub) · 45 /entre-hermanos · 47 /hipoteca · 49 /impuestos-y-notario · 51 que-es-un-proindiviso · 53 division-de-cosa-comun · 57 contacto · 59/61/63 legales · **1359** gracias (noindex; la 14 se retiró) |
| Hub geo | página **55** `/vender-proindiviso/` |
| Páginas geo | 225 bajo `/vender-proindiviso/{ccaa}/{provincia}/{ciudad}/` (IDs en `tools/geo/ids.json`; contenido en `tools/geo/geo_A..F.json`) |
| Páginas de cola larga (7) | empresas-que-compran-herencias · vender-derechos-hereditarios · un-heredero-no-quiere-vender · vender-la-mitad-de-una-casa · vender-nuda-propiedad · vender-terreno-proindiviso · vender-proindiviso-con-inquilino-u-okupa (IDs en `tools/blog/ids.json`) |
| Blog | índice: página **680** `/blog/` (construido con Elementor, NO es la página de entradas de WP). 71 entradas en `/blog/{slug}/` (65 + 6 del 23/10), categorías 17 herencias · 18 extincion-de-condominio · 19 copropiedad · 20 division-de-cosa-comun · 21 impuestos-y-tramites (archivos redirigidos 301 a /blog/). Contenido en `tools/blog/blog_1..7.json` |
| Menús | 14 principal (incluye Blog) · 15 legal · 16 pie guías (el pie usa párrafos con enlace, no nav-menu) |
| Medios | 81 hero fachada (webp) · 92 marca 256 · 93 icono 512 · 1392-1497 imágenes de página (MiniMax, mapa en `tools/wordpress/images.json`) |
| Leads | Elementor Forms (V4): acciones collect-submissions + email a `isra4772@gmail.com` + webhook `https://n8n-wmlc.srv1480016.hstgr.cloud/webhook/zp-lead` → workflow n8n `f0SsWTuuAA76405B` → WhatsApp a Isra. Envíos en Elementor › Submissions |
| Yoast | Organización "Zona Proindiviso" (logo 93), imagen OG por defecto (81), migas activas (`[wpseo_breadcrumb]` en el hero de cada página), sitemap en https, autor/fecha/categorías fuera de índice, metas por página vía REST (`_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`) |
| Snippets activos (Code Snippets) | **5** teléfono/WhatsApp/SEO por REST (ajustes `zp_telefono`, `zp_whatsapp`, `zp_email_leads`, `zp_wa_mensaje`; shortcodes `[zp_telefono]`, `[zp_telefono_enlace]`, `[zp_whatsapp_enlace]`; tags dinámicos; metas Yoast en REST) · **10** CSS global (menú, formularios, acordeón, `overflow-x`, oculta botones sin href) · **14** https en sitemap · **18** miga "Blog" · **21** sin caché LiteSpeed de HTML + purga · **22** archivos → /blog/ · **38** schema Service · **45** fecha de actualización + TOC. Los "ZP una vez" ya se ejecutaron (quedan inactivos; se pueden borrar) |
| Tokens de diseño (variables globales) | brand-primary #0d4f78 · brand-primary-dark #093a5a · brand-accent #e87524 (dark #d06316) · surface-soft #eff5f8 · surface-soft-2 #deeef4 · ink #1f2a33 · ink-muted #4f5b66 · line #d8e0e6 · success #58a728 · fuente Manrope |

## 3. Cómo se construye cada página (patrón)

Todas las páginas de intención, geo y blog siguen el mismo esqueleto, generado por `tools/wordpress/pagebuilder.py` (`build(spec)`):
hero azul (migas, overline, H1, sub, botones WhatsApp/Llamar, 3 checks, tarjeta con componente 83) → 5-8 secciones (text, cards, steps, list, table, callout) → FAQ (acordeón con `faq_schema: true`) → "También te puede interesar" (enlaces) → CTA final con componente 85. Las legales usan `build_simple`.

El contenido vive en JSON por pieza (ver `tools/blog/EJEMPLO-spec.json` y `tools/blog/BRIEF-BLOG.md`; geo en `tools/geo/BRIEF.md`). Para crear una página nueva con el mismo diseño desde Cowork: copiar un spec, cambiar textos y ejecutar `blogbuilder.py` o `geobuilder.py` (crean el documento con `elementor-create-page`, componen con `build-composition`, publican con `publish-document` y fijan metas y título corto por REST).

## 4. Reglas aprendidas del MCP de Elementor (importante)

1. **Recomponer un documento ya publicado no actualiza lo publicado.** `build-composition` + `publish-document` sobre una página publicada deja el HTML con clases de estilo nuevas y el CSS local con las antiguas (se ve rota). Procedimiento seguro: pasar la página a **borrador** por REST, componer, publicar, y después **regrabar** el documento con la API de Elementor (`$doc->save()`), como hace `tools/wordpress/resave_recent.php` vía snippet de un solo uso. Comprobar con `tools/wordpress/cssqa.py` (ratio de clases del HTML presentes en `uploads/elementor/css/local-{id}-frontend-desktop.css`; hoy 319 URL, 0 problemas).
2. Site parts (cabecera, pie): no recomponer la publicada; crear una nueva con `manage-site-parts create` (borrador), componer, publicar y borrar la vieja.
3. `publish-document` restaura título y metas del borrador: fijar título y metas de Yoast **después** de publicar.
4. Estilos: no admite selectores anidados en `style`; `flex` abreviado no es fiable (usar flex-grow/shrink/basis); `@media(--tablet)` / `@media(--mobile)` y `&:hover` sí.
5. Formularios V4: `email.to` debe ser lista estática; mensajes de éxito/error necesitan un `e-paragraph` hijo.
6. Páginas creadas por REST no se marcan como Elementor: crear siempre con `elementor-create-page` (acepta `post_type` page o post) y luego fijar slug/padre/categoría por REST.
7. El WAF de Hostinger devuelve 403 a cuerpos PUT con `<style`: el CSS del snippet 10 concatena la etiqueta.
8. LiteSpeed/CDN sirvieron en `/` una copia antigua de la instalación por defecto: el snippet 21 fuerza `X-LiteSpeed-Cache-Control: no-cache` y `Cache-Control: no-cache` en HTML. Si vuelve a verse una página vieja, purgar el CDN en hPanel.
9. Argumentos grandes al MCP: `emcp.sh` admite `@fichero.json` (el índice del blog supera el límite de argv).

## 5. Lo que FALTA (orden recomendado)

### De Isra (bloquea cosas)
1. **Teléfono y WhatsApp** en Ajustes › Zona Proindiviso (WP). Hasta entonces los botones Llamar/WhatsApp están ocultos (CSS `a.e-button-base:not([href])`), aparecen solos al rellenarlos.
2. **NIF y correo de contacto** para aviso legal, privacidad y cookies (hay "[pendiente de completar]" en las tres páginas 59/61/63).
3. **Search Console**: dar de alta la propiedad y enviar `https://zonaproindiviso.com/sitemap_index.xml`. Es lo más urgente para indexar 319 URL.
4. GTM/GA4 (IDs) y configuración del banner de Complianz; conversión de formulario en Google Ads.
5. Purgar una vez el CDN en hPanel. Revocar las contraseñas de aplicación sobrantes y dejar solo la que use Cowork.

### Para Cowork (con el MCP de Elementor)
Hechas el 23/10/2026 desde Cowork (detalle en la sección 8): 1 (revisión visual), 2 (/gracias/ → 1359), 3 (imágenes), 4 (TOC y fecha), 5 (enlazado), 7 (6 entradas nuevas con demanda en el TSV; las 4 sin demanda se descartaron), 9 (Lighthouse medido). Quedan:
6. **Pueblos**: NO crear en bloque. A las 3-4 semanas, abrir Search Console y crear solo los municipios con impresiones reales, con el mismo generador (`geobuilder.py`, tipo "ciudad", padre = provincia).
8. **Revisar cifras**: €/m² y tipos de ITP/AJD por comunidad están marcados como orientativos 2026; validar con Isra antes de campañas. Las 6 entradas nuevas añaden horquillas orientativas propias (ver sección 8).
10. **Leads**: el correo de aviso llega a isra4772@gmail.com y el WhatsApp al alias "isra"; cuando Isra decida destino definitivo, cambiar `email.to` en los componentes 83 y 85 y el alias en el workflow n8n.
11. **Blog, temas descartados por falta de búsqueda en el TSV** (0-2 impresiones): pacto sucesorio en Cataluña/Galicia/País Vasco; hermano fallecido (derecho de representación); cuota en subasta judicial: cómo pujar; arras y contrato privado. Retomar solo si Search Console muestra impresiones.

## 6. QA disponible (en `tools/wordpress/`)
- `seoqa.py`: todas las URL del sitemap: coherencia HTML/CSS, og:image propia, banda de imagen, alt vacíos, TOC y fecha en entradas, FAQPage, un solo H1, noindex. Es el QA completo de la sesión de Cowork.
- `cssqa.py`: coherencia HTML/CSS de todas las URL del sitemap.
- `geo_qa.sh` y `blog_qa.sh`: código 200, FAQPage, acordeón y extensión mínima.
- `cssmatch.sh <url> <id>`, `overflow.js` (elementos que desbordan en móvil), `shotm.js` (capturas por viewport).

## 7. Datos y fuentes
- `docs/datos/terminos-busqueda-6-cuentas-2024-2026.tsv` (1.906 términos con impresiones, clics, conversiones y coste; dos cuentas, 4630614423 y 7078242970, no respondieron por el gateway).
- `docs/datos/keyword-planner-*.csv`, `docs/investigacion-*.md`, `docs/ARQUITECTURA-URLS.md`, `docs/ENCARGO-WEB-PROINDIVISOS-v2.md`, `docs/PLAN-WORDPRESS.md` (bitácora de construcción e incidencias).

## 8. Hecho desde Cowork (23/10/2026)

| Pieza | Qué se hizo |
|---|---|
| Imágenes | 115 imágenes únicas generadas con **MiniMax image-01** vía n8n `/webhook/panel-img` (prohibido OpenRouter en esa sesión), 1280×720 → WebP q82, sin texto ni caras, revisadas una a una (~30 regeneradas). Alt y título descriptivos en la biblioteca. Una por entrada (72+6), una por página de intención (17) y hub/blog (2), una por comunidad (19) que heredan sus provincias y ciudades. `featured_media` en las 321 páginas → og:image/twitter propia. Banda "Figura" (e-image) entre hero y primera sección en todas las páginas del patrón. Mapa en `tools/wordpress/images.json`. Alt del logo (92/93) rellenado (antes `alt=""` en todas las páginas). |
| /gracias/ | Nueva página **1359** con el patrón (check, qué pasa ahora en 4 pasos, 4 guías, WhatsApp/teléfono). La 14 no era de Elementor (marcarla por meta no genera CSS) y se envió a la papelera. noindex. |
| TOC + fecha | Snippet **45** (`snippet_toc.php`): `[zp_actualizado]` bajo las migas (entradas y 7 guías) e índice `<nav class="zp-toc">` server-side con `id` en los H2 (último H2, el CTA, excluido). Lo ven Google, los bots de IA y lectores sin JS. |
| Enlazado | Bloque "Guías para vender tu parte en X" (3 entradas, rotación por hash) en las 19 CCAA y 43 provincias. En 40 entradas, "También te puede interesar" enlaza a la geo de la ciudad/provincia/CCAA mencionada (`geo_related`). |
| Blog | 6 entradas nuevas con demanda real en el TSV (`tools/blog/blog_7.json`, IDs 1972/1984/1995/2010/2019/2027): comprar-la-parte-de-mi-hermano · escision-cesacion-liquidacion-de-condominio-que-significan · cuanto-vale-la-nuda-propiedad-calculo · indivisos-inmobiliarios-que-son-y-quien-los-compra · inmobiliarias-que-compran-pisos-al-contado-o-empresa-de-proindivisos · vender-una-casa-con-problemas-quien-la-compra. Índice /blog/ (680) regenerado con ellas. **Pendiente de validar por Isra**: horquillas orientativas que introducen (ITP 6-10 % / AJD 0,5-1,5 %, financiación 70-80 % de tasación, comisión inmobiliaria 3-5 % + IVA, compra directa 70-85 %, porcentajes por tipo de inmueble en indivisos-inmobiliarios, tabla usufructo 89-edad). |
| Recomposición | Las 319 páginas del patrón se recompusieron (borrador → composición → publicación → metas) y se regrabaron por lotes (`resave_ids.py` / `resave_follow.py`). QA final con `seoqa.py`. |
| Lecciones nuevas del MCP | (a) Una página creada por REST no se convierte en documento de Elementor poniendo `_elementor_edit_mode=builder`: no se genera CSS local; hay que crearla con `elementor-create-page`. (b) Los snippets "single-use" de Code Snippets se ejecutan en la **siguiente petición** (sirve una REST autenticada), en `init`; pero en ese punto no hay usuario (REST_REQUEST se define después) y `Document::save()` devuelve false: el snippet debe hacer `wp_set_current_user(1)`. (c) Yoast reconstruye el indexable en `wp_insert_post`, antes de que la REST fije `featured_media`: hace falta un segundo guardado para que og:image cambie (lo da `meta()`). |

## 9. Semáforo de Yoast (23/10/2026, noche)

Problema: ninguna página tenía puntuación de Yoast (SEO ni legibilidad): las puntuaciones solo las calcula el JavaScript del editor al guardar, y todo se creó por API. Además, al medir con el motor real de Yoast fallaban comprobaciones de verdad.

Método: `tools/wordpress/yoastqa.py` ejecuta la librería oficial `yoastseo` (npm, investigador español) sobre el HTML del documento principal de Elementor, igual que hace la integración Yoast↔Elementor en el editor, y con `--save` escribe `_yoast_wpseo_linkdex` y `_yoast_wpseo_content_score` por REST (snippet **95** los expone; Yoast reconstruye el indexable al cambiar postmeta). Necesita `node` y `npm i yoastseo` en `YOAST_DIR`.

Qué se cambió para pasar (constructores, no a mano):
- Keyphrase en la introducción: el último tramo de las migas es `_yoast_wpseo_bctitle` = keyphrase (`meta()`), y el overline del hero también es la keyphrase. Yoast toma como "introducción" el primer `<p>`, que son las migas.
- Keyphrase en subtítulos: H2 del FAQ y del CTA llevan la keyphrase si el spec no la lleva; en geo, H2 de contexto y trámites. Las preguntas del FAQ van en `<h3>` (también reparte secciones >300 palabras). Los títulos de tarjetas van en `<p>` con estilo de h3 salvo tarjetas de navegación o secciones largas (>280 palabras), para no inflar el recuento de subtítulos (Yoast exige 30-75 % con keyphrase).
- Título SEO ≤ 60 caracteres y empezando por la keyphrase: sin sufijo de marca en entradas y geo; 42 entradas con keyphrase/título/descripción corregidos en `blog_*.json`; páginas de intención en `intencion_kw.py`.
- Meta description con todas las palabras de la keyphrase y 120-156 caracteres (plantilla geo nueva).
- Enlace saliente: "Código Civil (BOE)" en "También te puede interesar" (y en el CTA de la home).
- Alt de imágenes empieza por la keyphrase (adjuntos de entradas e intención; en geo, "Vender proindiviso en {CCAA}: …" vale para provincias y ciudades).
- Legibilidad: los "✓" de los checks van en un párrafo aparte (eran 3 frases seguidas con la misma palabra); en geo, conectores en plantilla y en los extractos de tarjetas (`conecta`), `rompe_repeticion` en textos por lugar, etiquetas de relacionados sin repetir "Vender". `pagebuilder._break_runs()` reordena los enlaces de "También te puede interesar" (BOE incluido) para que nunca haya 3 seguidos que empiecen por la misma palabra; el 2.º enlace geo de las entradas se etiqueta "Compramos proindivisos en …".
- Residuos esperables: "keyphrase en el slug" naranja en geo (el slug es la ciudad, por diseño); "keyphrase en subtítulos" rojo/naranja en páginas con muchas tarjetas de navegación; semáforo general verde en SEO y legibilidad.
