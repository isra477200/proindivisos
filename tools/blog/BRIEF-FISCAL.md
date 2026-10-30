# Brief: «Impuestos del proindiviso por comunidad autónoma» (30/10/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md` (posicionamiento, estilo, esquema JSON), las reglas de imagen y de Yoast de `BRIEF-PROGRAMADOS.md`
(«Dos campos nuevos» y «Yoast en verde»: mandan) y `EJEMPLO-spec.json`. Después esto.

## Qué es
Una página por comunidad autónoma (y Ceuta y Melilla) colgando de `/impuestos-del-proindiviso/` (el índice lo escribimos nosotros).
URL de cada una: el campo `ruta` de `plan_fiscal.json`. Cada página: `"kind": "page"`, `"category": null`, `slug`, `focus_kw` y
`title_corto` EXACTOS del plan. La keyphrase es «extinción de condominio en {comunidad}» porque es como se busca, pero la página cubre
TODOS los impuestos del proindiviso en esa comunidad.

## Contenido obligatorio de cada página (2026, cifras VERIFICADAS)
1. AJD de la extinción de condominio: tipo general de AJD para documentos notariales en 2026 y tipos reducidos relevantes (vivienda
   habitual, jóvenes, familia numerosa, discapacidad...). Base imponible: solo el valor de la parte que adquiere quien se queda el inmueble
   (doctrina del Tribunal Supremo desde 2018: dilo así, sin número de sentencia). Si la comunidad tiene una regla propia para la extinción
   de condominio o los excesos de adjudicación, explícala.
2. ITP si vendes tu cuota a un tercero o a una empresa: tipo general 2026 y reducidos relevantes. Lo paga el comprador.
3. Impuesto de sucesiones si la cuota viene de una herencia: reducciones y bonificaciones de esa comunidad para hijos, cónyuge y
   hermanos/sobrinos (grupos I a III), reducción por vivienda habitual del fallecido (porcentaje, límite y años de mantenimiento) y plazo de
   presentación (6 meses, prorrogable).
4. Plusvalía municipal e IRPF: breve, son estatales (salvo País Vasco y Navarra, con normativa foral propia: explícala en esas dos).
   Enlaza a `/calculadora-impuestos-vender-tu-parte/` (nueva) y a las entradas existentes de IRPF y plusvalía.
5. Ejemplo con cifras redondas de un piso en esa comunidad (p. ej. 200.000 €, dos hermanos al 50 %): AJD de la extinción, compensación, y
   alternativa de vender la cuota a una empresa (ITP lo paga ella).
6. Organismo donde se presenta (nombre exacto de la agencia tributaria autonómica o de la Hacienda foral) y modelo/vía.
7. Sección «Fuentes oficiales» (type `list`) con 2-4 enlaces externos `<a href="https://...">` a la agencia tributaria autonómica, a la
   ley o decreto legislativo de tributos cedidos vigente o al BOE. Solo fuentes oficiales.
8. Enlaces internos: la página geo de la comunidad (campo `geo` del plan), `/extincion-de-condominio/`,
   `/extincion-de-condominio/impuestos-y-notario/`, `/simulador-extincion-de-condominio/`, `/impuestos-del-proindiviso/` y 1-2 entradas
   del blog relacionadas (elige en `urls_todas.txt`).

## Rigor (lo más importante)
- Busca cada cifra en la web (WebSearch/WebFetch) en fuentes oficiales de 2026 (agencia tributaria autonómica, boletín oficial, BOE).
  Si una cifra solo la encuentras de 2025 o anterior y no consta cambio, úsala y dilo con prudencia («tipo vigente en 2026 salvo cambio
  normativo»). Nada de memoria.
- Añade a cada objeto dos campos internos (no se publican): `"datos"` = {"ajd_general": "1,2 %", "ajd_reducidos": "...",
  "itp_general": "7 %", "itp_reducidos": "...", "isd_hijos_conyuge": "...", "isd_hermanos": "...", "isd_vivienda_habitual": "...",
  "organismo": "...", "url_organismo": "https://..."} y `"fuentes_verificacion"` = lista de [qué cifra, URL consultada].
  Y `"dudas"`: lista de cifras que no hayas podido confirmar (vacía si todo está confirmado).
- Prudencia: «orientativo», «consulta tu caso»; cero promesas fiscales.

## Formato y validación
- Extensión de página: 1.000-1.600 palabras de cuerpo, 5-8 secciones, 5-6 FAQ (respuestas de 2-4 frases, mínimo 25 palabras).
- `h1` 55-90 caracteres con la keyphrase (p. ej. «Extinción de condominio en Aragón: impuestos y gastos en 2026»). `yoast_title`
  50-62 caracteres y EMPIEZA por la keyphrase exacta. Varía H2 y estructura entre comunidades: no son plantillas con el nombre cambiado.
- Al menos una tabla (`type: table`) con los impuestos de esa comunidad.
- `imagen_prompt`: escena reconocible de esa comunidad SIN monumentos famosos ni texto (arquitectura típica, calle, patio, paisaje urbano
  o rural característico), con el cierre obligatorio de BRIEF-PROGRAMADOS. `imagen_alt` empieza por la keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/FICHERO.json tools/blog/plan_fiscal.json --pagina` hasta «N/N válidas» y
  revisa con `python3 tools/wordpress/yoastpre.py tools/blog/FICHERO.json` (corrige lo que salga en naranja o rojo).
- No toques ningún otro fichero del repositorio ni ningún sistema externo.
