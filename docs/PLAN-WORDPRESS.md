# Plan técnico WordPress — zonaproindiviso.com (v2, 23/10/2026)

Sustituye al stack Astro/Cloudflare del encargo v2 (decisión 6 de Isra) y a la v1 de este plan (tema y plugin propios). Decisiones de Isra del 23/10 por la tarde: **Elementor Pro con su MCP oficial, Yoast SEO, sin plugin propio, sin ACF**.

## 1. Hosting y base
- Hosting propio de WebSEO. PHP 8.2+, HTTPS, HTTP/2, caché de página (LiteSpeed Cache si el servidor es LiteSpeed; si no, WP Super Cache). Sin Cloudflare de pago.
- WordPress limpio, es_ES, enlaces permanentes `/%postname%/`.
- Dominio: zonaproindiviso.com (a 23/10 sin DNS ni RDAP: registrar).

## 2. Stack cerrado

| Pieza | Para qué | Coste |
|---|---|---|
| **Hello Elementor** (tema) | Base vacía, cero CSS/JS propio. | Gratis |
| **Elementor Pro** | Theme Builder (cabecera, pie, plantilla geo), widgets globales (barra fija móvil, pestaña "Te llamamos nosotros", botones de llamada/WhatsApp), Elementor Forms (leads), acordeón con schema FAQ, popup. | Licencia anual (la aporta Isra) |
| **Elementor MCP** (oficial, dentro de Elementor) | Claude/ChatGPT crean y editan páginas en el editor. Se activa en el admin y genera el prompt de conexión. | Incluido |
| **WordPress MCP** (Automattic, gratuito) | Lo que Elementor MCP no toca: ajustes, Yoast, leads, usuarios. Conectado a Claude y ChatGPT como conector remoto con token. | Gratis |
| **Yoast SEO** (gratuito) | Títulos, metas, canonical, Open Graph, sitemap, breadcrumbs, schema Organization/WebPage/Breadcrumb, noindex por página, robots. | Gratis |
| **Complianz** (gratuito) | Banner de cookies con Consent Mode v2 + carga de GTM condicionada. | Gratis |
| **WPCode** (gratuito) | Un snippet de ~50 líneas: ajuste único de **teléfono y WhatsApp** y sus dos etiquetas dinámicas para Elementor. Visible y editable desde el admin, sin plugin propio. | Gratis |

**Fuera:** ACF (Elementor Pro lee los campos personalizados nativos de WordPress; ACF solo aportaría una interfaz de edición, se añade si algún día el equipo quiere editar datos geo a mano), Web3Forms (lo sustituye Elementor Forms), Rank Math, packs de addons de Elementor, constructores adicionales, Google Fonts remotas, reCAPTCHA de Google.

## 3. Cómo se cumple cada punto del encargo

### 3.1 Teléfono y WhatsApp en un único sitio (encargo §7)
- Snippet WPCode: registra dos opciones (`zp_telefono`, `zp_whatsapp`), una página de ajustes mínima (Ajustes → Zona Proindiviso) y dos **etiquetas dinámicas de Elementor** ("Teléfono", "WhatsApp" con mensaje prerrellenado por página).
- En todos los widgets el número nunca se escribe: se elige Dinámico → Teléfono / WhatsApp. Los bloques que lo contienen (barra móvil, pestaña, botones) son **widgets globales**, así que el cambio es doble: un ajuste y, si hiciera falta, un global.
- Yoast toma el teléfono del mismo ajuste para el schema Organization (filtro en el mismo snippet).
- Cambio de propietario = cambiar dos campos + nombre/logo en Yoast.

### 3.2 Formularios y leads (encargo §5-6, decisión 4)
- **Elementor Forms**: formulario corto (nombre + teléfono) en la pestaña "Te llamamos nosotros" y en el hero; formulario completo (nombre, teléfono, provincia, origen del proindiviso, % de propiedad, comentario) al final de cada página.
- Campos ocultos con etiquetas dinámicas: URL de la página, título, UTM (parámetros de URL), dispositivo.
- Acciones tras enviar: **Guardar envío** (Submissions = backend propio, exportable a CSV), **Email** al gestor de leads, **Webhook** al n8n que avisa por WhatsApp (`whatsapp-send`) y redirección a `/gracias/`.
- Antispam: honeypot de Elementor + hCaptcha (gratuito, integración nativa de Elementor Forms).

### 3.3 Pestaña "Te llamamos nosotros" (encargo §6)
Widget global dentro de un popup de Elementor Pro anclado al lateral derecho en escritorio; en móvil se sustituye por la barra fija inferior (Llamar · WhatsApp · Formulario). Solo nombre y teléfono.

### 3.4 Páginas geo (arquitectura §5)
- Páginas normales de WordPress en jerarquía `/vender-proindiviso/{ccaa}/{provincia}/{ciudad}/`.
- Datos locales (registros de la propiedad, €/m², plusvalía orientativa, comarcas, FAQ locales) en **campos personalizados nativos** de cada página. Las 90 páginas las crea Claude por la API REST una sola vez a partir de `docs/datos/geo.json`, en borrador.
- Una **plantilla única del Theme Builder** (condición: páginas hijas de "Vender proindiviso") lee esos campos con la etiqueta dinámica "Campo personalizado". Una plantilla, 90 URLs, contenido propio en cada una.
- Publicación por lotes según `ARQUITECTURA-URLS.md` §8; solo se publica lo que pasa el checklist SEO.

### 3.5 SEO por URL (encargo §9)
- Yoast: title, meta, canonical, breadcrumbs, sitemap por tipo, noindex en `/gracias/`.
- Elementor: un solo H1 por página, acordeón FAQ con schema, imágenes con alt y dimensiones, widgets globales para no repetir CSS.
- Rendimiento: Hello + contenedores Flexbox, experimentos de Elementor activados (DOM optimizado, carga CSS mejorada, iconos inline, lazy de fondos), Manrope alojada en local, caché de página, sin addons. Objetivo LCP < 2,5 s e INP < 200 ms en móvil, medido página a página.
- Auditoría final con rastreador (Screaming Frog gratuito hasta 500 URLs): cero títulos duplicados, cero metas vacías, cero 4xx internos. Se entrega el informe; no se promete "SEO perfecto".

### 3.6 Medición (encargo v2 §7)
GTM cargado por Complianz tras consentimiento; GA4 con eventos `lead_corto`, `lead_completo`, `click_tel`, `click_whatsapp`, `abrir_pestana` (los clics se capturan en GTM por atributos de los widgets globales). Conversiones de Google Ads preparadas aunque no haya campaña. Search Console con sitemap de Yoast.

### 3.7 Imágenes (decisión 7)
12 piezas del encargo §11 generadas con la API de MiniMax, sin caras; WebP, nombre con keyword, alt manual. Geo: foto de ciudad vía webhook de Pixabay o ninguna.

### 3.8 MCP (encargo §8)
- Elementor MCP oficial: construir y editar páginas, plantillas y widgets globales desde Claude o ChatGPT.
- WordPress MCP (Automattic): ajustes del snippet (teléfono/WhatsApp vía REST), metas de Yoast, lectura de envíos de formularios, creación masiva de páginas geo.
- Ambos remotos (HTTP) con token; se conectan como conector en Claude y en ChatGPT.

## 4. QA antes de dar nada por terminado
Rastreo completo, Lighthouse móvil en 10 URLs de cada tipo, prueba real de lead (envío guardado + email + WhatsApp), prueba de cambio de teléfono desde ajustes y desde MCP, Rich Results Test, Search Console con sitemap enviado.

## 5. Qué necesito de Isra para la fase 3
1. **Registrar zonaproindiviso.com** y apuntarlo al hosting.
2. **WordPress instalado** en el dominio (o en `dev.zonaproindiviso.com`) con PHP 8.2+.
3. **Elementor Pro** con licencia activa en ese sitio.
4. **Usuario administrador** para mí + **Application Password** (Usuarios → Perfil → Contraseñas de aplicación). Con eso instalo el resto (Hello, Yoast, Complianz, WPCode) y trabajo por REST/MCP. SSH con WP-CLI si lo hay, mejor.
5. **Teléfono y WhatsApp** de la web y el **email** que recibe los leads.
6. **Clave de MiniMax** (o confirmación de usar la de n8n `panel-creativos`).
7. **ID de GTM y propiedad GA4**, o acceso para crearlos.
8. Claves de **hCaptcha** (gratuitas) o me dices que las cree con tu email.

Con 1-4 arranco; 5-8 se añaden después en ajustes sin tocar nada.

## Estado de construcción (23/10/2026, tarde)

- Publicadas 140 páginas: home, 15 de intención (hub extinción de condominio con 3 hijas, qué es, división de cosa común, etc.), contacto, 3 legales, hub geo `/vender-proindiviso/` y 118 páginas geo (19 CCAA y ciudades autónomas, 43 provincias, 56 ciudades) con texto local único (`tools/geo/geo_*.json`, 300-350 palabras propias por lugar) y FAQ local con schema FAQPage.
- Jerarquía geo real en WordPress (página hija), migas de Yoast en el hero, títulos cortos para las migas, metas únicas por página, sitemap en https (snippet para el proxy de Hostinger), archivos de autor desactivados.
- Pie v3 (site part 544) con enlace a las 19 comunidades. Cabecera 20, popup 22, componentes de formulario 83 (corto) y 85 (completo).
- Pendiente de Isra: teléfono y WhatsApp (ajustes de "Zona Proindiviso" en WP), NIF y correo para aviso legal/privacidad/cookies, GTM/GA4 y banner de cookies (Complianz), revocar las dos contraseñas de aplicación sobrantes.
- Siguiente: Search Console + envío del sitemap, Lighthouse móvil, y ampliar a municipios según consultas reales.
