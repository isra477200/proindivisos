# Brief: 44 entradas «huecos de la competencia» (24/10/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md`, después `BRIEF-PROGRAMADOS.md` (TODAS sus reglas aplican: dos campos de imagen, Yoast en verde, contenido,
enlaces, entrega) y `EJEMPLO-spec.json`. Después esto.

## Diferencias respecto a las programadas
- El plan es `plan_competencia.json` (dividido en `plan_lote_12.json` … `plan_lote_15.json`). Se publican EN EL ACTO, no programadas.
- Validación: `python3 tools/blog/validar.py tools/blog/blog_12.json tools/blog/plan_competencia.json` hasta «N/N válidas».
- El `angulo` de cada tema dice qué competidor lo cubre y, cuando existe, qué artículo nuestro se le acerca: enlázalo y trata lo que
  aquel no trata. No copies estructura ni frases de nadie: escribe desde nuestra experiencia como compradores.
- Enlaces internos permitidos: URL de `urls_paginas.txt` y `urls_entradas.txt`, las 44 nuevas entre sí (`/blog/{slug}/`), las dos
  herramientas (`/cuanto-vale-mi-parte-de-un-piso/`, `/simulador-extincion-de-condominio/`) y el diccionario
  (`/diccionario-del-proindiviso/`). NO enlaces a las 47 programadas (`plan_programados.json`): aún no son públicas.
- Rigor extra en lo jurídico-fiscal: artículos del CC/LEC/LAU/LPH solo si estás seguro; cifras de impuestos siempre «orientativo» y
  «según comunidad autónoma»; horquillas, no precios exactos. Nada de sentencias con número ni fecha. Sin guion largo (—).
- Mantén el cierre comercial en primera persona del plural (compramos la cuota, oferta por escrito en 48 h, firma en notaría en 2-4
  semanas, gastos a nuestro cargo, 40-70 % del valor proporcional). Nunca «intermediarios».
