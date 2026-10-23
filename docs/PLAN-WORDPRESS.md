# Plan técnico WordPress — zonaproindiviso.com (23/10/2026)

Sustituye al stack Astro/Cloudflare del encargo v2 (decisión 6 de Isra). Todo lo que pide el encargo se cumple dentro de WordPress con un tema propio y un plugin propio; no se depende de constructores ni de servicios de pago.

## 1. Hosting y base
- Hosting propio de WebSEO (el que usáis con clientes). PHP 8.2+, HTTPS, HTTP/2, caché de página (LiteSpeed Cache si el servidor es LiteSpeed; si no, WP Super Cache). Sin Cloudflare de pago; el plan gratuito de Cloudflare como DNS/CDN es opcional.
- WordPress limpio, idioma es_ES, enlaces permanentes `/%postname%/`, sin plugins de constructor.
- Dominio: zonaproindiviso.com (a 23/10 sin DNS ni RDAP: registrar).

## 2. Piezas que construyo yo
### 2.1 Tema propio `zonaproindiviso` (ligero, sin jQuery)
- Plantillas: portada, página transaccional, página hub, página geo (jerárquica), legales, 404, gracias.
- Patrón de landing del encargo §5: hero + formulario corto, barra fija móvil (Llamar · WhatsApp · Formulario), pestaña lateral "Te llamamos nosotros" en escritorio, cómo funciona, confianza, bloque específico, FAQ, CTA final.
- Colores de compramostucoche.es (`#0d4f78`, `#e87524`, `#eff5f8`) sobre blanco; tipografía Manrope (self-hosted, no Google Fonts para evitar cookies y latencia).
- CSS crítico inline, un solo CSS, un JS mínimo (formularios, pestaña, consent). Objetivo LCP < 2,5 s móvil.

### 2.2 Plugin propio `zp-core` (toda la lógica, independiente del tema)
- **Ajustes únicos** (una pantalla): teléfono, WhatsApp, email de leads, titular legal, clave Web3Forms, claves hCaptcha, ID de GTM, URL del webhook n8n. Se exponen como `[zp_telefono]`, `[zp_whatsapp]` y funciones de tema. **Cambiar el teléfono aquí lo cambia en toda la web** (incluidos schema y botones).
- **Leads**: tipo de contenido `zp_lead` (privado) con nombre, teléfono, provincia/ciudad, origen del proindiviso, % propiedad, comentario, URL de origen, página, UTM, dispositivo, IP anonimizada, consentimiento y fecha. Listado y exportación CSV desde el admin. **Este es "su propio backend" (decisión 4).**
- **Endpoint** `POST /wp-json/zp/v1/lead`: valida (nonce, honeypot, hCaptcha, teléfono ES), guarda el lead, envía email al gestor **vía Web3Forms** (transporte pedido en el encargo), dispara el webhook n8n para el aviso por WhatsApp (`whatsapp-send`, ya operativo) y devuelve la URL de `/gracias/`.
- **Formularios**: bloque/shortcode corto (nombre + teléfono) y completo. Mismo endpoint.
- **SEO en el propio plugin**: title y meta por página (campos propios), canonical, Open Graph, JSON-LD (Organization/WebSite en todo, Service en transaccionales, FAQPage donde hay FAQ, BreadcrumbList en geo), `noindex` por página, sitemap por secciones (core WP + filtro), robots.txt. Sin Yoast ni Rank Math: menos peso y nada que se desincronice.
- **Generador geo**: comando WP-CLI `wp zp geo generar` que lee `docs/datos/geo.json` (CCAA → provincias → ciudades con sus datos locales) y crea/actualiza la jerarquía de páginas en borrador. Las páginas se publican por lotes cuando pasan el checklist.
- **Consent Mode v2 + GTM**: banner propio mínimo (aceptar/rechazar/configurar) que fija `gtag('consent', ...)` antes de cargar GTM. Eventos: `lead_corto`, `lead_completo`, `click_tel`, `click_whatsapp`, `abrir_pestana`.

### 2.3 Conexión MCP (decisión del encargo §8)
- Opción A (recomendada): plugin **WordPress MCP de Automattic** (gratuito, código abierto). Expone la REST de WordPress como servidor MCP remoto con token. Se conecta a Claude (conector personalizado) y a ChatGPT (conectores en modo desarrollador). Con él, Claude/ChatGPT crean y editan páginas, cambian ajustes del plugin (teléfono/WhatsApp vía REST de `zp-core`) y leen leads.
- Opción B (si A no cubre algo): servidor MCP propio en el VPS de Hostinger (junto a n8n) que envuelve la REST de WordPress con una Application Password. Mismas herramientas: `get_config`, `set_config`, `list_pages`, `update_page`, `create_geo_page`, `seo_check`, `list_leads`.
- En ambos casos la REST de `zp-core` registra sus ajustes y metadatos SEO con `show_in_rest`, así que cualquier cliente MCP puede tocarlos.

### 2.4 Imágenes (MiniMax, decisión 7)
- 12 piezas del encargo §11, generadas con la API de MiniMax (clave: la que ya vive en n8n para `panel-creativos`, o una clave nueva que me pases). Sin caras. Conversión a WebP/AVIF, nombres con keyword, `alt` escrito a mano, dimensiones declaradas, lazy salvo hero.
- Páginas geo: foto de la ciudad vía webhook de Pixabay (ya operativo) o ninguna.

## 3. Lo que NO se instala
Constructores (Elementor, Divi), plugins de SEO, plugins de formularios, sliders, Google Fonts remotas, reCAPTCHA de Google (se usa hCaptcha, gratuito y sin cookies de perfilado).

## 4. QA antes de dar nada por terminado
Rastreo completo (Screaming Frog gratuito hasta 500 URLs o `wp zp seo auditar`), Lighthouse móvil en 10 URLs de cada tipo, prueba real de lead (email + WhatsApp + fila en Leads), prueba de cambio de teléfono desde ajustes y desde MCP, validación de schema en Rich Results Test, Search Console con sitemap enviado.

## 5. Qué necesito de Isra para la fase 3
1. **Registrar zonaproindiviso.com** y apuntarlo al hosting.
2. **WordPress instalado** en el dominio (o en un subdominio de pruebas, p. ej. `dev.zonaproindiviso.com`) con PHP 8.2+.
3. **Usuario administrador** para mí + **Application Password** (Usuarios → Perfil → Contraseñas de aplicación). Con eso subo tema y plugin por la REST/WP-CLI sin pedir SFTP. Si el hosting tiene WP-CLI por SSH, mejor: dame acceso SSH.
4. **Teléfono y WhatsApp** que irán en la web, y el **email** que recibe los leads.
5. **Clave de Web3Forms** (gratuita, se crea con el email de leads en web3forms.com).
6. **Clave de MiniMax** (o confirmación de que use la de n8n `panel-creativos`).
7. **ID de GTM y propiedad GA4** (si quieres que los cree yo, acceso a la cuenta de Google de WebSEO).
8. Claves de **hCaptcha** (gratuitas, 2 minutos en hcaptcha.com) o me dices que las cree con tu email.

Con 1-3 arranco el tema, el plugin y el contenido; 4-8 se pueden añadir después en la pantalla de ajustes sin tocar código.
