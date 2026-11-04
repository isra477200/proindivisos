# Brief: «Impuesto de sucesiones por comunidad autónoma» (04/11/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md` (posicionamiento, estilo, esquema JSON), las reglas de imagen y de Yoast de `BRIEF-PROGRAMADOS.md`
(«Dos campos nuevos» y «Yoast en verde»: mandan), `EJEMPLO-spec.json` y, como referencia de formato y tono, una página ya publicada del
mismo tipo: `fiscal_1.json` (impuestos de la extinción de condominio por comunidad; posiciona en el top 5 de Google). Después esto.

## Por qué existe
Search Console muestra búsquedas de herederos («modelo 650», «modelo 650 cataluña», «no puedo pagar los impuestos de la herencia»,
«impuesto sucesiones»...). Quien hereda una parte de un piso y no puede o no quiere pagar sucesiones es nuestro vendedor ideal. Las páginas
deben ser la mejor respuesta a «cuánto pago de sucesiones al heredar en {comunidad}» y llevar, sin forzar, a vender la parte.

## Qué es
Una página por comunidad autónoma (y Ceuta y Melilla) colgando de `/impuestos-del-proindiviso/` (el índice de sucesiones lo hace otra
persona). `plan_sucesiones.json`: `slug`, `focus_kw` y `title_corto` EXACTOS; `ruta` es la URL; `geo` y `fiscal` son enlaces internos
obligatorios. `"kind": "page"`, `"category": null`. La keyphrase es «impuesto de sucesiones en {comunidad}».

## Contenido obligatorio de cada página (normativa vigente en 2026, cifras VERIFICADAS)
1. Cómo se calcula en esa comunidad: base (valor real; valor de referencia del Catastro como mínimo en inmuebles), reducciones por
   parentesco (grupos I, II, III y IV) estatales o autonómicas, tarifa (estatal o propia), coeficientes por patrimonio preexistente si la
   comunidad los cambia, y bonificaciones en cuota. Di con claridad cuánto paga en la práctica un hijo o el cónyuge (muchas comunidades
   bonifican el 99 % o tienen reducciones enormes) y cuánto un hermano o sobrino (ahí suele doler).
2. Vivienda habitual del fallecido: reducción (porcentaje, límite por heredero, beneficiarios y años de mantenimiento).
3. Tabla (`type: table`) con lo esencial de esa comunidad: grupo I, grupo II, grupo III, grupo IV, vivienda habitual, plazo, organismo.
4. Ejemplo con cifras redondas: piso de 200.000 € (valor de referencia) que heredan dos hijos al 50 %, sin otros bienes; y, si cambia
   mucho, el mismo piso heredado por dos sobrinos. Cuota orientativa de cada uno. Haz las cuentas con la tarifa y reducciones reales;
   anota el cálculo en `datos.ejemplo` para que se pueda revisar.
5. Plazo (6 meses desde el fallecimiento, prórroga de otros 6 si se pide dentro de los 5 primeros), organismo exacto donde se presenta
   (agencia tributaria autonómica u Hacienda foral), modelo o vía (650 u otro propio), recargos si te pasas
   (enlaza `/diccionario-del-proindiviso/recargo-por-presentacion-fuera-de-plazo/`) y aplazamiento o fraccionamiento
   (enlaza `/diccionario-del-proindiviso/aplazamiento-del-impuesto-de-sucesiones/`).
6. Heredar una parte de un inmueble (proindiviso): se tributa por el valor de tu cuota; después del impuesto quedáis en copropiedad.
   Salidas: extinción de condominio (enlaza a la página `fiscal` del plan), vender tu parte (enlaza `/vender-parte-casa-heredada/` o
   `/vender-derechos-hereditarios/` si aún no hay partición), y qué pasa con la plusvalía municipal por herencia y con el IRPF cuando
   vendas (el valor declarado en sucesiones es tu valor de adquisición: enlaza `/calculadora-impuestos-vender-tu-parte/`). Si hay usufructo
   del viudo, enlaza `/calculadora-nuda-propiedad/` (nueva, existirá al publicar).
7. «Si no puedes pagar el impuesto»: aplazar, fraccionar, aceptar a beneficio de inventario, vender tu parte para pagarlo
   (enlaza `/blog/no-puedo-pagar-el-impuesto-de-sucesiones/` y `/blog/aceptar-la-herencia-y-vender-mi-parte-en-el-mismo-acto/`).
   Callout con nuestra compra: «compramos tu parte de la herencia con fondos propios, precio por escrito en 48 horas».
8. Sección «Fuentes oficiales» (type `list`) con 2-4 enlaces externos `<a href="https://...">` a la agencia tributaria autonómica u
   Hacienda foral, a la ley o decreto legislativo de tributos cedidos vigente o al BOE/boletín autonómico. Solo fuentes oficiales.
9. Enlaces internos además de los de arriba: `geo` del plan, `/impuestos-del-proindiviso/`,
   `/impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad/`, `/diccionario-del-proindiviso/impuesto-de-sucesiones/`,
   `/diccionario-del-proindiviso/modelo-650/` y, si viene a cuento, `/diccionario-del-proindiviso/bonificacion-del-impuesto-de-sucesiones/`.
   SOLO enlaces que estén en `urls_publicadas.txt` (más las rutas nuevas de `plan_sucesiones.json` y `/calculadora-nuda-propiedad/`).
   Nada de `urls_todas.txt`: incluye entradas programadas que aún no existen.

## Casos especiales
- País Vasco: normativa foral distinta en Álava, Bizkaia y Gipuzkoa (una sola página que explique las tres; las diputaciones forales,
  no el modelo 650 estatal). Navarra: normativa foral propia (Hacienda Foral de Navarra).
- Ceuta y Melilla: normativa estatal con bonificación propia de las ciudades autónomas; explica qué se aplica y dónde se presenta.
- Cataluña, Canarias, Galicia, Madrid, Andalucía, etc. tienen reglas muy distintas: nada de plantillas con el nombre cambiado. Varía H2,
  orden y ejemplos.

## Rigor (lo más importante: es dinero de la gente)
- Busca cada cifra en la web (WebSearch/WebFetch) en fuentes oficiales vigentes en 2026 (agencia tributaria autonómica, boletín oficial,
  BOE, Hacienda foral). Comprueba si hubo cambios en 2025 o 2026 (leyes de presupuestos y de medidas fiscales). Si una cifra solo la
  encuentras de 2025 y no consta cambio, úsala y dilo con prudencia («vigente en 2026 salvo cambio normativo»). Nada de memoria.
- Campos internos (no se publican) en cada objeto:
  `"datos"` = {"grupo_I": "...", "grupo_II": "...", "grupo_III": "...", "grupo_IV": "...", "vivienda_habitual": "...", "tarifa": "...",
  "patrimonio_preexistente": "...", "plazo": "...", "organismo": "...", "modelo": "...", "url_organismo": "https://...",
  "ejemplo": "cálculo paso a paso del ejemplo"},
  `"fuentes_verificacion"` = lista de [qué cifra, URL consultada], y `"dudas"` = cifras que no hayas podido confirmar (vacía si todo está
  confirmado). Si algo no lo confirmas, en el texto usa una formulación prudente y genérica, nunca una cifra inventada.
- Tono prudente: «orientativo», «consulta tu caso con un asesor»; cero promesas fiscales.

## Formato y validación
- 1.000-1.600 palabras de cuerpo, 5-8 secciones, 5-6 FAQ (respuestas de 2-4 frases, mínimo 25 palabras). Pregunta tipo en las FAQ:
  «¿Cuánto paga un hijo por heredar un piso en {comunidad}?», «¿Cuánto tengo para presentar el impuesto?», «¿Qué pasa si no puedo
  pagarlo?», «¿Pagan lo mismo los hermanos y los sobrinos?»... variadas.
- `h1` 55-90 caracteres con la keyphrase (p. ej. «Impuesto de sucesiones en Aragón: cuánto se paga al heredar en 2026»). `yoast_title`
  50-62 caracteres que EMPIEZA por la keyphrase exacta. `meta_desc` 130-155 con la keyphrase.
- `imagen_prompt`: escena reconocible de esa comunidad SIN monumentos famosos, SIN personas y SIN texto (arquitectura típica, calle, patio,
  interior de una casa de la zona, paisaje urbano o rural característico), distinta de la que ya usa su página `fiscal`, con el cierre
  obligatorio de BRIEF-PROGRAMADOS. `imagen_alt` empieza por la keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/FICHERO.json tools/blog/plan_sucesiones.json --pagina` hasta «N/N válidas» y
  revisa con `python3 tools/wordpress/yoastpre.py tools/blog/FICHERO.json` (corrige lo que salga en naranja o rojo).
- No toques ningún otro fichero del repositorio ni ningún sistema externo (nada de WordPress, nada de publicar).
