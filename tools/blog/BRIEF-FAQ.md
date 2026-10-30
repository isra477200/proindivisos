# Brief: página «Preguntas frecuentes sobre el proindiviso» (30/10/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md` (posicionamiento, estilo), las reglas de Yoast de `BRIEF-PROGRAMADOS.md` y `EJEMPLO-spec.json`.

## Qué es
Una sola página `/preguntas-frecuentes-proindiviso/` (`plan_faq.json`: slug, focus_kw «preguntas sobre el proindiviso», title_corto) con
50 preguntas reales agrupadas en 6 bloques. Cada bloque es una sección con su H2 y un shortcode nuestro que pinta sus preguntas como
desplegables (con un único schema FAQPage para toda la página). Las preguntas son las que la gente escribe en Google y nos hacen al
teléfono, no inventadas para rellenar.

## Bloques (orden y número orientativo)
1. Lo básico del proindiviso (qué es, cuotas, derechos, decisiones, gastos) — 8-9
2. Vender tu parte (sin permiso, a quién, precio, plazos, documentos, retracto) — 9-10
3. Herencias en proindiviso (aceptar, impuesto, herederos que no firman, casa del pueblo) — 8-9
4. Extinción de condominio y división de cosa común (cuándo cada una, subasta, costes, plazos) — 8-9
5. Impuestos y gastos (AJD, ITP, plusvalía, IRPF, notaría; enlaza a `/impuestos-del-proindiviso/`) — 7-8
6. Cómo compramos nosotros (oferta en 48 h, de dónde sale el dinero, notaría, gastos, sin exclusividad, qué pasa con los demás) — 6-7

## Formato (JSON: lista con UN objeto)
- Esquema de BRIEF-BLOG para la página (slug, kind "page", category null, kicker, h1, sub, checks, card_title, card_text, faq_title,
  related, cta_title, cta_text, yoast_title, meta_desc, focus_kw, title_corto, imagen_prompt, imagen_alt) con `"faqs": []` (vacío: el
  schema lo pone nuestro shortcode).
- `sections`: primero una sección `text` breve (cómo usar la página, 80-150 palabras); después los 6 bloques, cada uno:
  `{"overline": "Bloque N", "h2": "...", "type": "tool", "intro": ["1-2 frases de entrada"], "shortcode": "[zp_faq_bloque n=\"N\"]",
  "preguntas": [["¿Pregunta?", "Respuesta de 40-90 palabras, 2-4 frases, que responde en la primera frase; puede llevar 1 enlace interno
  <a href=\"/ruta/\">texto</a> a la guía o entrada que lo amplía (urls_todas.txt)"], ...]}`; por último un `callout` con nuestra compra.
- Yoast: la keyphrase «preguntas sobre el proindiviso» completa en h1, sub, yoast_title (al principio), meta_desc e imagen_alt; en 3-4 de
  los H2 aparecen «preguntas» y «proindiviso» (p. ej. «Preguntas sobre el proindiviso y la herencia»); y en total al menos 14 frases
  (intros de bloque, sub, algunas respuestas) contienen «preguntas» y «proindiviso» de forma natural. Frases cortas (≤ 25 % de más de
  20 palabras), ≥ 30 % con palabra de transición, nunca 3 frases seguidas que empiecen igual, sin guion largo.
- Rigor: artículos del Código Civil cuando proceda, cifras prudentes y «según comunidad autónoma» en impuestos.
- Valida tú mismo: json válido; 6 bloques; 48-52 preguntas en total; ninguna respuesta con menos de 35 ni más de 95 palabras; ninguna
  pregunta repetida. Guarda en `tools/blog/faq.json`. No toques ningún otro fichero del repositorio ni ningún sistema externo.
