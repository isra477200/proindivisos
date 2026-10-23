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
| Páginas de intención | 25 empresas-que-compran-proindivisos · 27 cuanto-pagan · 29 sin-avisar · 31 parte-casa-heredada · 33 opiniones · 35 parte-de-un-piso · 37 con-hipoteca · 39 divorcio · 41 entre-hermanos · 43 extincion-de-condominio (hub) · 45 /entre-hermanos · 47 /hipoteca · 49 /impuestos-y-notario · 51 que-es-un-proindiviso · 53 division-de-cosa-comun · 57 contacto · 59/61/63 legales · 14 gracias (noindex) |
| Hub geo | página **55** `/vender-proindiviso/` |
| Páginas geo | 225 bajo `/vender-proindiviso/{ccaa}/{provincia}/{ciudad}/` (IDs en `tools/geo/ids.json`; contenido en `tools/geo/geo_A..F.json`) |
| Páginas de cola larga (7) | empresas-que-compran-herencias · vender-derechos-hereditarios · un-heredero-no-quiere-vender · vender-la-mitad-de-una-casa · vender-nuda-propiedad · vender-terreno-proindiviso · vender-proindiviso-con-inquilino-u-okupa (IDs en `tools/blog/ids.json`) |
| Blog | índice: página **680** `/blog/` (construido con Elementor, NO es la página de entradas de WP). 65 entradas en `/blog/{slug}/`, categorías 17 herencias · 18 extincion-de-condominio · 19 copropiedad · 20 division-de-cosa-comun · 21 impuestos-y-tramites (archivos redirigidos 301 a /blog/). Contenido en `tools/blog/blog_1..6.json` |
| Menús | 14 principal (incluye Blog) · 15 legal · 16 pie guías (el pie usa párrafos con enlace, no nav-menu) |
| Medios | 81 hero fachada (webp) · 92 marca 256 · 93 icono 512 |
| Leads | Elementor Forms (V4): acciones collect-submissions + email a `isra4772@gmail.com` + webhook `https://n8n-wmlc.srv1480016.hstgr.cloud/webhook/zp-lead` → workflow n8n `f0SsWTuuAA76405B` → WhatsApp a Isra. Envíos en Elementor › Submissions |
| Yoast | Organización "Zona Proindiviso" (logo 93), imagen OG por defecto (81), migas activas (`[wpseo_breadcrumb]` en el hero de cada página), sitemap en https, autor/fecha/categorías fuera de índice, metas por página vía REST (`_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`) |
| Snippets activos (Code Snippets) | **5** teléfono/WhatsApp/SEO por REST (ajustes `zp_telefono`, `zp_whatsapp`, `zp_email_leads`, `zp_wa_mensaje`; shortcodes `[zp_telefono]`, `[zp_telefono_enlace]`, `[zp_whatsapp_enlace]`; tags dinámicos; metas Yoast en REST) · **10** CSS global (menú, formularios, acordeón, `overflow-x`, oculta botones sin href) · **14** https en sitemap · **18** miga "Blog" · **21** sin caché LiteSpeed de HTML + purga · **22** archivos → /blog/ · **38** schema Service. Los "ZP una vez" ya se ejecutaron y se borraron |
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
1. **Revisar visualmente una muestra** (home, /empresas-que-compran-herencias/, una geo, una entrada) en escritorio y móvil tras cualquier cambio; si algo sale sin estilos, aplicar la regla 4.1.
2. **Página /gracias/ (14)**: está publicada con diseño básico; rehacerla con el patrón (mensaje, qué pasa ahora, WhatsApp).
3. **Imágenes**: hoy solo hay el hero de fachada. Añadir imagen destacada por entrada (MiniMax vía n8n `/webhook/panel-img` o Krea) con alt descriptivo y OG propia; en geo, una imagen por comunidad como máximo (no por ciudad).
4. **Tabla de contenidos** (anclas a los H2) en las entradas largas y "Última actualización" visible.
5. **Enlazado**: añadir en cada página geo de provincia un bloque "Guías" (3 entradas del blog más afines) y en las entradas un enlace a la geo de su ciudad cuando el texto la mencione.
6. **Pueblos**: NO crear en bloque. A las 3-4 semanas, abrir Search Console y crear solo los municipios con impresiones reales, con el mismo generador (`geobuilder.py`, tipo "ciudad", padre = provincia).
7. **Blog, siguientes temas** (todos con búsqueda real en `docs/datos/terminos-busqueda-6-cuentas-2024-2026.tsv`): "vender piso heredado en [ciudad]" solo si hay demanda; "comprar la parte de mi hermano con hipoteca"; "pacto sucesorio en Cataluña/Galicia/País Vasco y venta de la cuota"; "vender vivienda heredada con deudas de comunidad"; "herencia con hermano fallecido (derecho de representación)"; "cuota de proindiviso en subasta judicial: cómo pujar"; "arras y contrato privado al vender una cuota". Mantener 1.100-1.500 palabras, FAQ con schema, callout a mitad y CTA final.
8. **Revisar cifras**: €/m² y tipos de ITP/AJD por comunidad están marcados como orientativos 2026; validar con Isra antes de campañas.
9. **Rendimiento**: medir Lighthouse móvil en home y una geo; si hace falta, reducir el número de ficheros CSS locales (Elementor › Ajustes › Rendimiento) y comprobar que la fuente Manrope se sirve con `font-display: swap`.
10. **Leads**: el correo de aviso llega a isra4772@gmail.com y el WhatsApp al alias "isra"; cuando Isra decida destino definitivo, cambiar `email.to` en los componentes 83 y 85 y el alias en el workflow n8n.

## 6. QA disponible (en `tools/wordpress/`)
- `cssqa.py`: coherencia HTML/CSS de todas las URL del sitemap.
- `geo_qa.sh` y `blog_qa.sh`: código 200, FAQPage, acordeón y extensión mínima.
- `cssmatch.sh <url> <id>`, `overflow.js` (elementos que desbordan en móvil), `shotm.js` (capturas por viewport).

## 7. Datos y fuentes
- `docs/datos/terminos-busqueda-6-cuentas-2024-2026.tsv` (1.906 términos con impresiones, clics, conversiones y coste; dos cuentas, 4630614423 y 7078242970, no respondieron por el gateway).
- `docs/datos/keyword-planner-*.csv`, `docs/investigacion-*.md`, `docs/ARQUITECTURA-URLS.md`, `docs/ENCARGO-WEB-PROINDIVISOS-v2.md`, `docs/PLAN-WORDPRESS.md` (bitácora de construcción e incidencias).
