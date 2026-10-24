# Brief: 47 entradas programadas (24/10/2026) — complementa a BRIEF-BLOG.md, que manda en todo lo que no se diga aquí

Lee primero `BRIEF-BLOG.md` (posicionamiento, estilo, esquema JSON) y `EJEMPLO-spec.json` (estructura real). Después esto.

## Encargo
Cada redactor recibe un subconjunto de `plan_programados.json` (slug, focus_kw, title_corto, category, angulo, fecha). Escribe UNA pieza por tema,
`"kind": "post"`, respetando exactamente `slug`, `focus_kw`, `title_corto` y `category` del plan. El `angulo` es el enfoque obligatorio:
desarróllalo; no lo cambies por otro tema. No existe aún ninguna de estas 47 URL: no las des por publicadas salvo para enlazarlas entre sí
(`/blog/{slug}/`), y enlaza sobre todo a las URL que ya existen (`urls_paginas.txt`, `urls_entradas.txt`).

## Dos campos nuevos por pieza (obligatorios)
- `"imagen_prompt"`: prompt EN INGLÉS para generar la foto de cabecera con un modelo de imagen (16:9, editorial inmobiliaria española, luz
  natural, paleta apagada con acentos azul oscuro y terracota, 35 mm). Escena concreta y pertinente al tema (una fachada, un portal, una llave,
  una mesa de notaría vacía, un paisaje urbano español, una casa de pueblo, un local, un garaje, un juzgado por fuera...). Termina SIEMPRE con:
  "No people, no visible faces, no text, no letters, no numbers, no signs, no logos, no watermark, no documents, no calendars, no maps."
  Prohibido pedir calendarios, mapas, papeles, pantallas, bancos o dinero: el modelo mete texto. Nada de personas.
- `"imagen_alt"`: alt en español, 8-14 palabras, que EMPIEZA por la keyphrase y describe la escena. Ej.: "Herencia con deudas: fachada de un
  edificio de viviendas al atardecer en una ciudad española".

## Yoast en verde, sin excepciones (lo valida `validar.py`; ejecútalo hasta que no quede ningún fallo)
1. La keyphrase exacta (`focus_kw`) aparece en `h1`, en `sub`, en `yoast_title`, en `meta_desc` y en `imagen_alt`.
2. Entre el 30 % y el 75 % de los H2 contienen más de la mitad de las palabras de contenido de la keyphrase (no hace falta la frase exacta;
   con 6-7 secciones: 2-4 H2). El resto de H2 varían el vocabulario.
3. Densidad: al menos una frase de cada 150-200 palabras contiene TODAS las palabras de contenido de la keyphrase (Yoast cuenta frases con
   todas las palabras, no solo la frase exacta). Para 1.300 palabras: 8-10 frases así, repartidas, naturales. Sin pasarse de 3 %.
4. Cada sección (intro + items + outro) ≤ 300 palabras. Párrafos ≤ 150 palabras. 5-8 secciones. Una sección `callout` hacia el final.
5. Legibilidad: frases cortas (como máximo el 25 % de las frases supera las 20 palabras); al menos el 30 % de las frases llevan una palabra de
   transición (además, por eso, sin embargo, es decir, por ejemplo, en cambio, aunque, porque, también, después, primero, en la práctica,
   de hecho, en resumen, por tanto...); nunca 3 frases seguidas que empiecen por la misma palabra; voz activa; sin guion largo (—).
6. `yoast_title` 50-62 caracteres SIN sufijo de marca (se añade solo). `meta_desc` 130-155 caracteres con la keyphrase y nuestra propuesta.
7. 5-6 FAQ con respuestas de 2-4 frases (mínimo 25 palabras cada una), escritas como las busca la gente.
8. 1.100-1.600 palabras de cuerpo (intro + items + outro de todas las secciones, sin FAQ ni CTA).

## Contenido
- Cada pieza responde en las 2-3 primeras frases del `sub` a la pregunta del título (featured snippet) y presenta nuestra compra.
- Datos concretos y prudentes: artículos del Código Civil cuando proceda (392-406, 399, 400, 404, 1005, 1057, 1062, 1067, 1522), horquillas,
  ejemplos con números redondos (piso de 180.000 €, mitad, tercio). Impuestos: siempre «orientativo» y «según comunidad autónoma». Sin
  sentencias con número ni fecha exacta; «doctrina del Tribunal Supremo» a secas.
- Cierre comercial coherente con el ángulo: compramos la cuota, oferta por escrito en 48 h, firma en notaría en 2-4 semanas, gastos a nuestro
  cargo, sin exclusividad. Entre el 40 % y el 70 % del valor proporcional. Primera persona del plural. Nunca «intermediarios».
- Enlaces internos: 3-6 por pieza (en `related` y en `cards` con `url`), hacia URL existentes relacionadas con el tema. Las dos herramientas
  nuevas son muy enlazables cuando encajen: `/cuanto-vale-mi-parte-de-un-piso/` (calculadora) y `/simulador-extincion-de-condominio/`.
- No repitas enfoques ni párrafos de `entradas_existentes.txt` (ahí tienes los 71 títulos ya publicados): si tu tema roza uno existente,
  enlázalo y trata lo que aquel no trata.
- Varía la estructura entre piezas (orden y tipo de secciones: text, cards, steps, list, table, callout).

## Entrega
Guarda la lista JSON en el fichero que se te indique (p. ej. `tools/blog/blog_8.json`), UTF-8, y ejecuta
`python3 tools/blog/validar.py tools/blog/blog_8.json tools/blog/plan_programados.json` hasta que imprima «N/N válidas». No toques ningún
otro fichero del repositorio ni ningún sistema externo.
