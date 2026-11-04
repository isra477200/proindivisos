# Brief: entradas de blog y páginas nuevas de zonaproindiviso.com

## Quiénes somos (posicionamiento obligatorio)
Zona Proindiviso COMPRA proindivisos (cuotas indivisas de pisos, casas, locales, garajes, terrenos) y partes de herencias con fondos propios en toda España. NO somos intermediarios, ni comparador, ni abogados. Promesa que se repite en todas las piezas: oferta por escrito en 48 h, firma en notaría en 2-4 semanas, pago al contado en notaría, gastos de notaría y gestión a nuestro cargo, sin exclusividad, sin compromiso. Pagamos entre el 40 % y el 70 % del valor proporcional de la cuota. Siempre en primera persona del plural ("compramos", "te damos precio"). Nunca "te ponemos en contacto", "varias ofertas", "empresas colaboradoras".

## Objetivo SEO
Cada pieza responde a consultas reales que la gente escribe en Google (te damos las keywords exactas por pieza). Debe posicionar sola: título H1 con la consulta principal, primer párrafo que responde la pregunta en 2-3 frases (featured snippet), H2 con las variantes y preguntas relacionadas, tablas y listas cuando ayuden, FAQ con 5-6 preguntas reales (van con schema FAQPage), y cierre comercial natural hacia nuestra compra. Nada de relleno: contenido útil, concreto, con artículos del Código Civil cuando proceda (392-406 comunidad de bienes, 399 venta de cuota, 400 y 404 división, 1062 adjudicación, 1522 retracto de comuneros, 1067 retracto de coherederos), cifras orientativas y ejemplos con números.

## Estilo
Español de España, directo, frases cortas, tú. Sin emojis, sin guiones largos (—), sin paréntesis en cadena. Prudencia jurídica y fiscal: "orientativo", "según comunidad autónoma", "consulta tu caso". No inventes sentencias con número; puedes citar doctrina general del Tribunal Supremo sin fecha si no estás seguro. No prometas plazos judiciales exactos: usa horquillas.

## Extensión
Entradas de blog: 1.100 a 1.600 palabras de texto propio (sin contar FAQ). Páginas: 1.000 a 1.400. Cada pieza es ÚNICA: no reutilices párrafos ni estructuras idénticas entre piezas; cambia el orden y el tipo de secciones.

## Formato de entrega: JSON (lista de objetos), un objeto por pieza, con este esquema EXACTO
Mira el ejemplo completo en EJEMPLO-spec.json (es una página real ya publicada; copia su estructura, no su contenido).
- "slug": slug exacto que te damos.
- "kind": "post" o "page" (te lo damos).
- "category": slug de categoría para posts (herencias | extincion-de-condominio | copropiedad | division-de-cosa-comun | impuestos-y-tramites); null en páginas.
- "kicker": etiqueta corta sobre el H1 (2-4 palabras).
- "h1": H1 (55-90 caracteres), con la consulta principal.
- "sub": subtítulo de 2-3 frases que responde ya a la pregunta y presenta nuestra compra.
- "checks": 3 textos cortos (3-5 palabras) de confianza.
- "card_title" y "card_text": título y texto del formulario corto del hero, adaptados al tema.
- "sections": lista de 5 a 8 secciones. Cada una: {"overline": "...", "h2": "...", "type": "text"|"cards"|"steps"|"list"|"callout"|"table", "intro": ["párrafo", ...], "items": ..., "outro": ["párrafo"...]}.
  - text: solo intro (1-4 párrafos).
  - cards: items = lista de {"t": título, "p": párrafo, "url": opcional, "cta": opcional}. 3-6 tarjetas.
  - steps: items = lista de {"t","p"} (3-6 pasos numerados).
  - list: items = lista de strings (pueden llevar <strong>).
  - table: items = lista de pares [col1, col2]; la primera fila es la cabecera.
  - callout: items = {"t": título, "p": texto, "cta": texto del botón} (abre el formulario). Úsalo 1 vez, hacia el final.
  Puedes combinar intro + type + outro en la misma sección.
- "faqs": lista de 5-6 pares [pregunta, respuesta 2-4 frases]. Preguntas tal y como las escribiría la gente.
- "faq_title": título del bloque FAQ.
- "related": 3-5 pares [etiqueta, url] eligiendo entre las URLs existentes de abajo (y las nuevas de este encargo, con su ruta /blog/{slug}/ o /{slug}/).
- "cta_title" y "cta_text": CTA final con formulario completo.
- "yoast_title": 50-62 caracteres SIN el sufijo " · Zona Proindiviso" (se añade solo).
- "meta_desc": 130-155 caracteres, con la keyword y nuestra propuesta.
- "focus_kw": keyword principal en minúsculas.
- "title_corto": 2-5 palabras para las migas de pan.

## URLs existentes para enlazar (usa 3-6 enlaces internos por pieza, dentro de cards con "url" o en related)
/ (home) · /empresas-que-compran-proindivisos/ · /cuanto-pagan-por-un-proindiviso/ · /vender-proindiviso-sin-avisar/ · /vender-parte-casa-heredada/ · /opiniones-empresas-que-compran-proindivisos/ · /vender-parte-de-un-piso/ · /vender-proindiviso-con-hipoteca/ · /vender-proindiviso-divorcio/ · /vender-proindiviso-entre-hermanos/ · /extincion-de-condominio/ · /extincion-de-condominio/entre-hermanos/ · /extincion-de-condominio/hipoteca/ · /extincion-de-condominio/impuestos-y-notario/ · /que-es-un-proindiviso/ · /division-de-cosa-comun/ · /vender-proindiviso/ (toda España) · /vender-proindiviso/madrid/ · /vender-proindiviso/cataluna/barcelona/ · /vender-proindiviso/comunidad-valenciana/valencia/ · /vender-proindiviso/andalucia/sevilla/ · /vender-proindiviso/andalucia/malaga/ · /contacto/
Nuevas de este encargo (páginas): /empresas-que-compran-herencias/ · /vender-derechos-hereditarios/ · /un-heredero-no-quiere-vender/ · /vender-la-mitad-de-una-casa/ · /vender-nuda-propiedad/ · /vender-terreno-proindiviso/ · /vender-proindiviso-con-inquilino-u-okupa/. Entradas: /blog/{slug}/.

## Validación antes de entregar
python3: json.load del fichero, comprobar que cada objeto tiene todas las claves, que "faqs" tiene 5-6 pares, que cada sección tiene "h2" (salvo callout) y que el recuento de palabras de intro+items+outro está en el rango pedido. Guarda el fichero donde se te indique.
