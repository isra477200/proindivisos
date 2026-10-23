# Encargo v2 — Web nacional de captación de proindivisos

Versión revisada del encargo inicial (ChatGPT, v1). Mantiene todo lo pedido y añade lo que faltaba para que el proyecto sea ejecutable sin volver a preguntar. Las decisiones que solo puede tomar Isra están marcadas como **[DECISIÓN]**.

Fecha: 23/10/2026 · Repo: `isra477200/isra` · Rama: `claude/proindivisos-research-structure-37kcwt`

---

## 0. Qué cambia respecto a la v1

| Punto v1 | Qué faltaba o qué se mejora |
|---|---|
| 1 Objetivo | No decía qué pasa con el lead después de captarlo (routing, exclusividad, segmentación por origen). Añadido §1. |
| 2 Cobertura nacional | "Muchas URLs por poblaciones" sin criterio = riesgo de doorway pages. Añadido modelo por niveles con contenido mínimo real por página (§4). |
| 3 Investigación | Ya tenemos las 7 cuentas y sus IDs; la Google Ads API da volumen nacional por geo (Keyword Planner), que resuelve "observado vs volumen general". Añadido §3. |
| 5 Formularios | Web3Forms solo manda emails. Falta registro de leads, aviso inmediato, antispam y campos ocultos de atribución. Añadido §6. |
| 7 Panel | Se define como un único `site.config.json` + panel mínimo + rebuild automático (§8-9). |
| 8 MCP | Se concreta: servidor MCP remoto (HTTP) en el VPS de Hostinger, mismas operaciones que el panel (§9). |
| 9 SEO | Se convierte en checklist verificable por URL (§10) + reglas de indexación progresiva. |
| 10 Imágenes | Lista mínima cerrada (12 piezas) y regla de no generar una imagen por ciudad (§11). Conflicto con la norma "OpenRouter por defecto" del Contexto Maestro: ver [DECISIÓN]. |
| 11 Diseño | Tonos ya extraídos de compramostucoche.es. Falta tipografía: aplica la norma de marca de Isra (§12). |
| Nuevo | Medición (GA4, Ads, consent), legal RGPD (cesión de datos a terceros), marca/dominio/titular, fases con entregables, riesgos. |

---

## 1. Objetivo y modelo de negocio

- **Qué es:** web de captación para particulares que quieren vender su parte de un proindiviso. Los contactos se pasan a empresas compradoras. No vende servicios de marketing.
- **Posicionamiento recomendado:** "recibe ofertas de varias empresas compradoras" (intermediario/comparador). Es honesto, diferencia de las webs de un solo comprador y convierte mejor (el usuario percibe más precio). Evita prometer cosas que dependen del comprador ("pago en 48 h", "hasta el 95 %").
- **Qué hace falta decidir del lead:**
  - **[DECISIÓN] Destino de los leads:** a qué empresas, en exclusiva o compartido, por provincia o nacional, precio por lead o comisión.
  - **Segmentación por origen** (herencia / divorcio / compra conjunta / otros): no todos los compradores aceptan herencias (Soluciones Proindiviso, según su ficha, no las trabaja). El formulario captura el origen para enrutar.
  - **Registro de cada lead** con fecha, URL de origen, ciudad, origen del proindiviso, dispositivo y UTM, para poder demostrar calidad al comprador.
- **Conflicto a tener en cuenta:** la web competirá en orgánico con los 7 clientes de proindivisos de RedVitalia (Virginia y Pilar). **[DECISIÓN]** si se les informa y si pueden ser compradores de estos leads.

## 2. Marca, dominio y titular

- **[DECISIÓN] Nombre y dominio.** Recomendación: dominio de marca corto con palabra clave ("…proindiviso.es" o similar), `.es` o `.com`, sin guiones. Un EMD puro no aporta ventaja de ranking y limita la venta futura.
- **[DECISIÓN] Titular legal** que figura en aviso legal y política de privacidad (RedVitalia, WebSEO u otra). Condiciona el texto de cesión de datos.
- **Cambio de propietario:** todo lo "de marca" (nombre, teléfono, WhatsApp, email de leads, titular legal, logo) vive en un único fichero de configuración. Cambiar de dueño = cambiar ese fichero y redesplegar.

## 3. Investigación previa (fase 1)

Fuentes, en este orden:

1. **Búsquedas observadas (campañas).** Las 9 cuentas de proindivisos (8 en el MCC + Proindiviso Directo, que está fuera de este MCC; ver docs/investigacion-cuentas-proindivisos.md), vía Google Ads API (skill `google-ads-api`, n8n). Query a `search_term_view` y `keyword_view` de los últimos 12 meses: término, impresiones, clics, coste, conversiones, geo. Cuentas:

   | Cliente | Web | CID |
   |---|---|---|
   | Expertos en Proindivisos (Virginia) | expertosenproindivisos.com | 120-143-7650 |
   | Vender mi Proindiviso (Virginia) | vendermiproindiviso.com | 431-279-2125 |
   | Valora tu Proindiviso (Virginia) | valoratuproindiviso.net | 615-393-8152 |
   | Proindiviso Directo (Virginia) | proindivisodirecto.com | 408-846-3488 |
   | Proindivisos Gestión Propiedades (Virginia) | proindivisosgestionpropiedades.com | 851-660-5362 |
   | Sal del Proindiviso (Pilar) | saldelproindiviso.com | 930-792-9427 |
   | Soluciones Proindiviso (Pilar) | solucionesproindiviso.com | 707-824-2970 |
   | Compramos Proindivisos (no está en Notion) | ? | 463-061-4423 |
   | Fin del Proindiviso (no está en Notion) | ? | 746-018-9091 |

   Limitaciones a declarar: las campañas están muy centradas en Madrid (sesgo geográfico), Google oculta términos de poco volumen, y las conversiones de estas cuentas no están validadas como contacto real (aviso repetido en las rondas del Ads Center).
2. **Volumen general nacional.** `KeywordPlanIdeaService` de la misma API (1 petición/segundo): volumen mensual por provincia y a nivel España de cada término semilla y sus ideas. Esto separa "lo que compran los clientes en Ads" de "lo que busca España".
3. **Webs de los clientes.** Rastreo de las 7 webs: estructura de URLs, títulos, H1, FAQs, qué páginas tienen y cuáles no. Sirve para no copiar y para detectar huecos.
4. **Competencia orgánica.** Top 10 de Google para 10-15 consultas clave (nacional + 3 ciudades): quién posiciona, tipo de página, extensión, schema.
5. **Search Console de las webs de clientes** solo si hay acceso (consultas reales con impresiones). **[PENDIENTE DE VALIDAR]** si existe acceso.

**Entregable fase 1:** hoja "keyword → URL" con volumen nacional, volumen observado en campañas, intención (transaccional / informativa / local), página destino y prioridad. Con ella se cierra la arquitectura.

## 4. Arquitectura por niveles

| Nivel | Páginas | Criterio |
|---|---|---|
| Home | 1 | "Vender proindiviso" nacional. |
| Intención | 5-8 | vender parte de piso/casa, vender proindiviso heredado, vender proindiviso con hipoteca, proindiviso con okupas/inquilino, valorar proindiviso (lead magnet), comprar mi parte el otro propietario, extinción de condominio (informativa con CTA). Se cierra con datos de fase 1. |
| Situación | 4-6 | herencia, divorcio/separación, copropiedad con desconocidos, desacuerdo entre hermanos. |
| Informativa | 8-15 | qué es un proindiviso, cuánto vale mi parte, impuestos (plusvalía, IRPF), división de cosa común, usufructo, subasta, etc. Cada una con CTA y enlazado al nivel intención. |
| Geo nivel 1 | 17 CCAA + 50 provincias | Página real: datos de la provincia, tiempos, plusvalía orientativa, enlace a ciudades. |
| Geo nivel 2 | ciudades > 50.000 hab (aprox. 150) | Solo si la página tiene al menos 300 palabras únicas y datos locales reales (barrios, Registro de la Propiedad, precio medio m², ayuntamiento/plusvalía). |
| Geo nivel 3 | resto de municipios | **No se crean** salvo que la fase 1 muestre búsqueda. Si se crean, `noindex` hasta tener contenido propio. |

Reglas fijas: ninguna página geo es la plantilla con el nombre cambiado; cada una tiene título, H1, meta, FAQ y bloque de datos locales distintos. Breadcrumb CCAA → provincia → ciudad. Sitemap por secciones. Publicación progresiva (lotes de 50-100 URLs) para que Google no la lea como contenido escalado.

## 5. Patrón de landing (todas las páginas)

Orden fijo, mobile first:

1. Hero: H1 con la keyword, subtítulo con el beneficio, formulario corto o botón WhatsApp visible sin scroll.
2. Barra fija inferior en móvil: Llamar · WhatsApp · Formulario. En escritorio, pestaña lateral derecha "Te llamamos nosotros" (nombre + teléfono).
3. Cómo funciona (3 pasos).
4. Señales de confianza reales: número de empresas compradoras, zonas cubiertas, proceso, sin testimonios inventados.
5. Bloque específico de la keyword (situación, ciudad, datos).
6. FAQ (schema FAQPage) con 4-6 preguntas de la keyword.
7. CTA final + formulario completo.

WhatsApp: enlace `wa.me` con mensaje prerrellenado que incluye la página y la ciudad ("Hola, quiero vender mi proindiviso en Sevilla").

## 6. Formularios y leads

- **Dos formularios:** corto (nombre + teléfono, pestaña "Te llamamos") y completo (nombre, teléfono, provincia/ciudad, origen del proindiviso, % de propiedad, comentario opcional). Mínimo de fricción; lo demás lo pregunta el comprador.
- **Campos ocultos:** URL de la página, keyword/sección, ciudad, UTM, dispositivo, fecha/hora.
- **Web3Forms** como transporte (clave pública en config). Antispam: honeypot + hCaptcha (ambos soportados por Web3Forms).
- **Después del envío:** Web3Forms → webhook n8n → (a) fila en una BD de leads (Notion o Sheet; **[DECISIÓN]** cuál), (b) aviso inmediato por WhatsApp a quien gestione los leads usando el webhook `whatsapp-send` ya operativo, (c) email al comprador asignado según provincia/origen.
- **Alternativa a valorar:** el "Visor de Oportunidades" ya desplegado en el VPS (visor.srv1480016.hstgr.cloud) tiene widget de WhatsApp/llamada y registro de origen por lead. Si se reutiliza, el formulario puede apuntar directamente a él en vez de a Web3Forms. **[DECISIÓN]**.
- **Página de gracias** propia (`/gracias`) para medir conversión y con `noindex`.

## 7. Medición

- GTM + GA4 con Consent Mode v2 (obligatorio en UE si se usan Ads/Analytics).
- Eventos: envío de formulario corto, envío completo, clic en teléfono, clic en WhatsApp, apertura de la pestaña.
- Conversiones de Google Ads preparadas desde el día 1 (aunque no haya campaña), para poder encender Ads sobre la web sin tocar nada.
- Search Console y sitemap enviados el día del lanzamiento. Bing Webmaster opcional.
- Prueba de entrega del formulario a producción (email, WhatsApp y BD) antes de dar por lanzado.

## 8. Stack técnico

**Recomendación:** sitio estático generado (Astro) + contenido y configuración en este repo de GitHub + despliegue automático en Cloudflare Pages (gratis, CDN global, HTTPS).

Motivo: cientos de URLs con Core Web Vitals perfectos sin servidor que mantener; todo el contenido es texto en el repo, así que Claude/ChatGPT lo editan por MCP y cada cambio queda versionado; el teléfono/WhatsApp se inyecta en el HTML en el build (Google lo ve en el código, no en JavaScript).

Alternativa: WordPress (lo mantiene Cristopher, más fácil de vender a un comprador "normal"). Más lento, más mantenimiento, peor para generar cientos de páginas con calidad controlada. **[DECISIÓN]** confirmar Astro o volver a WordPress.

Estructura:

```
site.config.json        teléfono, WhatsApp, email leads, titular, marca, colores, claves públicas
content/paginas/*.md    páginas intención/situación/informativas
content/geo/*.json      datos por CCAA/provincia/ciudad
src/                    plantillas Astro
public/                 imágenes, robots.txt
```

## 9. Panel y conexión MCP (misma capa)

Una sola API (en el VPS de Hostinger, junto a n8n, con token) que expone:

- `get_config` / `set_config` (teléfono, WhatsApp, email de leads, titular…)
- `list_pages`, `get_page`, `update_page`, `create_page` (incluida creación de página geo desde plantilla + datos)
- `publish` (commit en GitHub → Cloudflare reconstruye en 1-2 min)
- `seo_check(url)` (devuelve título, meta, H1, canonical, enlaces, imágenes sin alt)

Encima de esa API:

- **Panel web mínimo** con contraseña: cambiar teléfono/WhatsApp y ver estado del último despliegue. Nada más.
- **Servidor MCP remoto (HTTP streamable)** con las mismas operaciones, para conectarlo a Claude y a ChatGPT como conector. Local (stdio) no sirve para ChatGPT.

Cambiar el teléfono desde el panel o desde Claude = mismo resultado: edición de `site.config.json` + redespliegue de toda la web.

## 10. Checklist SEO por URL (se pasa a todas, sin excepción)

- Título único (50-60 car.) con keyword al principio; meta description única con CTA.
- Un H1 con la keyword; H2 que responden a las búsquedas relacionadas.
- URL corta, en minúsculas, con guiones, sin stopwords innecesarias.
- Canonical propia; sin duplicados entre ciudad/provincia.
- Breadcrumb visible + schema BreadcrumbList. Schema Organization en todo el sitio, FAQPage donde haya FAQ, Service en páginas de intención.
- Enlazado interno: cada página enlaza a su padre, a 3-5 hermanas y a 2-3 informativas relacionadas; ninguna huérfana.
- Imágenes: WebP/AVIF, tamaño declarado, lazy salvo hero, alt descriptivo, nombre de archivo con keyword.
- Core Web Vitals: LCP < 2,5 s, CLS < 0,1, INP < 200 ms, medido en móvil (Lighthouse + PageSpeed real).
- Sin render dependiente de JavaScript para contenido o teléfonos.
- robots.txt, sitemap.xml por secciones, 404 propia, redirecciones 301 si cambia alguna URL.
- Auditoría final con rastreador (Screaming Frog o equivalente) sobre el sitio entero: cero títulos duplicados, cero metas vacías, cero 4xx internos.

Se entrega el informe del rastreo. No se llama "SEO perfecto": se entrega la lista de comprobaciones pasadas y las que no.

## 11. Imágenes

Lista mínima (12 piezas, sin caras reconocibles):

1. Hero home (fachada/llaves/documento, sin personas o de espaldas).
2-4. Tres ilustraciones del proceso (contacto, oferta, firma en notaría).
5-9. Cinco situacionales: herencia, divorcio, piso con hipoteca, vivienda ocupada/alquilada, desacuerdo entre copropietarios.
10. Imagen Open Graph genérica.
11. Favicon/logo (vector, no generado por IA).
12. Fondo/pattern suave para secciones.

Regla: no se genera una imagen por ciudad. Las páginas geo usan una foto de la ciudad del webhook de Pixabay (ya operativo) o ninguna.

Herramienta: API de MiniMax, como pide el encargo. **[DECISIÓN]** el Contexto Maestro fija OpenRouter como norma para todas las imágenes; aquí se usa MiniMax. Confirmar si es excepción de este proyecto o cambio de norma (y entonces actualizar el Contexto Maestro).

## 12. Diseño

- Tonos extraídos de compramostucoche.es (23/10/2026): azul principal `#0d4f78`, naranja CTA `#e87524` (hover `#d06316`), fondo azul claro `#eff5f8` / `#deeef4`, grises `#f0f0f0` `#e9e9e9` `#4a4a4a`, verde de confirmación `#58a728`. Blanco dominante; azul para cabecera/secciones de confianza; naranja solo en botones y acentos.
- Tipografía: norma de marca de Isra (Geist, Manrope, Satoshi, DM Sans, General Sans, Plus Jakarta Sans). Recomendación: Manrope. Nada clásico ni Inter ni Open Sans.
- Móvil primero; botones de 48 px; contraste AA.

## 13. Legal

- Aviso legal, política de privacidad y cookies con el titular de §2.
- Consentimiento explícito en el formulario para la **cesión de datos a empresas compradoras** (finalidad, destinatarios, derechos). Sin esto el modelo de negocio no es legal en RGPD.
- Banner de cookies con Consent Mode v2.
- Textos de marketing sin promesas que no se puedan cumplir.

## 14. Fases y entregables

| Fase | Entregable | Depende de |
|---|---|---|
| 1 Investigación | Hoja keyword → URL + informe de búsquedas (observado vs nacional) + rastreo de las 7 webs | n8n MCP operativo (en las sesiones programadas lleva fallando desde el 24/09) |
| 2 Estructura | Árbol de URLs definitivo + lista de ciudades nivel 2 + plantilla de landing + copy base | Fase 1 y decisiones §15 |
| 3 Construcción | Sitio Astro en el repo, config única, formularios, tracking, legal, imágenes | Dominio, titular, MiniMax, Web3Forms key, Cloudflare |
| 4 Panel + MCP | API + panel + servidor MCP conectado a Claude y ChatGPT | VPS |
| 5 QA SEO | Rastreo completo, CWV móvil, checklist por URL, informe | Fase 3 |
| 6 Lanzamiento | DNS, Search Console, sitemap, prueba real de leads, publicación progresiva | Todo lo anterior |

## 15. Decisiones de Isra antes de la fase 2

1. Nombre y dominio.
2. Titular legal.
3. Destino de los leads (empresas, exclusividad, precio) y quién recibe el aviso por WhatsApp.
4. Dónde se registran los leads (Notion / Sheet / Visor de Oportunidades).
5. Informar o no a los 7 clientes de proindivisos; si pueden comprar leads.
6. Stack: Astro + Cloudflare (recomendado) o WordPress.
7. MiniMax para imágenes: excepción o nueva norma.
8. Acceso a Search Console de las webs de clientes (si existe).

## 16. Riesgos y expectativas

- SEO nacional desde cero: primeros resultados orgánicos en 3-6 meses; las páginas geo tardan más. Si se quieren leads antes, Ads sobre esta web (tracking ya preparado).
- Páginas geo masivas sin contenido propio = riesgo de que Google las ignore o penalice el dominio. Por eso los niveles y la publicación progresiva.
- Competencia directa con clientes propios.
- Dependencia del conector n8n para la fase 1: si sigue caído, la investigación se hace con el GAQL runner por webhook o se pide el export manual.
