# Brief: «Modelos de documentos del proindiviso» (30/10/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md`, las reglas de imagen y de Yoast de `BRIEF-PROGRAMADOS.md` (mandan) y `EJEMPLO-spec.json`. Después esto.

## Qué es
Un índice `/modelos-documentos-proindiviso/` y 6 páginas hijas, una por modelo (`plan_modelos.json`: `slug`, `focus_kw`, `title_corto`,
`ruta` y el campo `modelo` con lo que debe resolver). Cada página explica cuándo usar el documento y cómo rellenarlo y enviarlo, y muestra
el modelo completo para copiar o descargar en Word (eso lo pinta un shortcode nuestro con el texto que tú escribes en el campo `modelo`).

## Cada página de modelo (`"kind": "page"`, `"category": null`)
- Spec normal de página (esquema de BRIEF-BLOG) con 4-7 secciones y 650-1.250 palabras de cuerpo SIN contar el modelo.
- La 2.ª sección es OBLIGATORIAMENTE la del modelo: `{"overline": "Modelo", "h2": "<frase con la keyphrase>", "type": "tool",
  "intro": ["1-2 frases: cómo usarlo"], "shortcode": "[zp_modelo id=\"{slug}\"]"}`.
- El resto: cuándo conviene y cuándo no (alternativas), base legal (artículos del Código Civil: 392-406, 395, 397, 398, 399, 400, 404,
  1522, 1524, 1067...), cómo enviarlo (burofax con certificación de contenido y acuse de recibo, requerimiento notarial; costes
  orientativos verificados en la web de Correos o con horquillas prudentes), qué pasa después (plazos, respuesta, siguientes pasos), y
  un callout con nuestra compra («si no quieres pelear, te compramos la parte»).
- 4-6 FAQ reales. `related` 3-5 enlaces internos (`urls_todas.txt`, más `/modelos-documentos-proindiviso/` y los otros modelos).
- Campo nuevo `"modelo"`: {"titulo": "Modelo de burofax a un copropietario", "texto": "texto COMPLETO del documento, párrafos separados
  por \n\n, con huecos entre corchetes en mayúsculas: [NOMBRE Y APELLIDOS], [DNI], [DOMICILIO], [DESCRIPCIÓN DEL INMUEBLE],
  [REFERENCIA CATASTRAL], [FINCA REGISTRAL N.º] [REGISTRO DE LA PROPIEDAD DE], [PORCENTAJE], [IMPORTE EN EUROS], [PLAZO], [FECHA],
  [LOCALIDAD]...", "instrucciones": ["3-6 consejos breves para rellenarlo"]}. El texto del modelo: 250-600 palabras, formal, claro,
  correcto según el Derecho español, sin datos reales, sin amenazas ni presiones indebidas, con el aviso inicial
  «Modelo orientativo. Revísalo con un abogado antes de enviarlo si hay importes altos o conflicto.» como primer párrafo.
- No inventes plazos legales: tanteo y retracto de comuneros, 9 días naturales (art. 1524 CC); pacto de indivisión, máximo 10 años
  prorrogables (art. 400 CC). Si dudas de una cifra, búscala.

## Índice `/modelos-documentos-proindiviso/` (primer objeto de la lista)
- Página normal (5-7 secciones, 650-1.250 palabras): para qué sirve cada modelo (sección `cards` con `url` a cada modelo, `t` = nombre del
  modelo, `p` = cuándo usarlo), en qué orden se usan normalmente (steps: propuesta amistosa → burofax → requerimiento → demanda o venta
  de la cuota), cómo enviarlos con prueba, y callout con nuestra compra. Sin campo `modelo`.

## Formato y validación
- `yoast_title` 50-62 caracteres que EMPIEZA por la keyphrase exacta; `h1` con la keyphrase; `imagen_prompt` sin personas ni papeles ni
  texto (una mesa de madera con una pluma estilográfica y un sobre cerrado sin nada escrito, un buzón de un portal antiguo, una oficina de
  correos vacía por fuera, una llave sobre una mesa...: escena distinta en cada modelo) con el cierre obligatorio; `imagen_alt` con la
  keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/modelos.json tools/blog/plan_modelos.json --modelo` hasta «7/7 válidas» y revisa
  con `python3 tools/wordpress/yoastpre.py tools/blog/modelos.json`.
- Guarda en `tools/blog/modelos.json`. No toques ningún otro fichero del repositorio ni ningún sistema externo.
