# Brief: «Diccionario del proindiviso» (A-Z) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md` (posicionamiento, estilo, esquema JSON), después las reglas de Yoast y de imagen de `BRIEF-PROGRAMADOS.md`
(apartados «Dos campos nuevos» y «Yoast en verde»), y `EJEMPLO-spec.json`. Después esto.

## Qué es
Un glosario de términos jurídicos, fiscales y prácticos alrededor del proindiviso. Cada término es UNA página propia en
`/diccionario-del-proindiviso/{slug}/` (`"kind": "page"`, `"category": null`). Un índice A-Z (lo montamos nosotros) enlaza a todas.

## Cada entrada del diccionario
- `focus_kw` exacta del plan (`dic_lote_N.json`): es el término tal y como se busca. `title_corto` = el término.
- `h1`: «Qué es {término}» o «{Término}: qué es y cómo afecta a tu parte» (55-90 caracteres, con la keyphrase).
- `sub`: 2-3 frases. La PRIMERA es la definición limpia, de diccionario, que Google pueda sacar como fragmento destacado. La segunda o
  tercera dice qué significa para alguien que quiere vender su parte.
- `kicker`: «Diccionario del proindiviso».
- 4-7 secciones, 550-1.000 palabras de cuerpo. Estructura recomendada (varíala): «Definición y base legal» (artículo del Código Civil o ley
  cuando exista) → «Cómo funciona en la práctica» (ejemplo con números: piso de 180.000 €, dos o tres hermanos) → «Qué significa si quieres
  vender tu parte» → tabla o lista «{Término} frente a términos parecidos» (enlaza a las entradas vecinas del diccionario con
  `/diccionario-del-proindiviso/{slug}/` o a las URL existentes) → callout breve con nuestra compra. Sin paja.
- 3-5 FAQ reales (como se buscan: «¿Hace falta...?», «¿Cuánto cuesta...?», «¿Qué pasa si...?»).
- `related`: 3-5 enlaces: otros términos del diccionario (ruta `/diccionario-del-proindiviso/{slug}/`, slugs en `diccionario_plan.json`,
  tanto «nuevos» como los «existentes» con su URL), la guía o entrada profunda relacionada (`urls_paginas.txt`, `urls_entradas.txt`) y,
  si encaja, `/cuanto-vale-mi-parte-de-un-piso/` o `/simulador-extincion-de-condominio/`.
- `yoast_title` 50-62 caracteres con la keyphrase (p. ej. «Cuota indivisa: qué es, qué derechos da y cómo se vende»). `meta_desc` 130-155.
- `imagen_prompt` (inglés, sin personas ni texto, escena concreta y distinta en cada término: un portal, una fachada, un pasillo de juzgado
  vacío, una llave en una mesa de madera, un patio de vecinos, un tejado, una calle de pueblo, un local con persiana bajada, un garaje,
  una finca con olivos, una escalera de edificio antiguo...) e `imagen_alt` que empieza por la keyphrase.
- Rigor: prudencia jurídica («orientativo», «según comunidad autónoma»), artículos del CC cuando procedan (392-406, 397, 398, 399, 400,
  401, 404, 1005, 1057, 1062, 1067, 1522, 96, 806-808, 1931-1959), nada de sentencias con número ni fecha. Sin guion largo (—).
- Validación: `python3 tools/blog/validar.py tools/blog/dic_N.json tools/blog/diccionario_plan.json --diccionario` hasta «15/15 válidas».
