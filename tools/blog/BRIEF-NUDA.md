# Brief: «Calculadora de nuda propiedad» con página SEO completa (04/11/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md`, las reglas de imagen y de Yoast de `BRIEF-PROGRAMADOS.md` (mandan), `EJEMPLO-spec.json` y
`BRIEF-HERRAMIENTAS.md` + `herramientas.json` (cómo están hechas las otras calculadoras). Lee también
`tools/wordpress/snippet_calculadora_nuda.php`: es la calculadora real; el texto debe explicar EXACTAMENTE lo que calcula, con los mismos
nombres de campo y los mismos valores por defecto.

## Por qué existe
Search Console muestra búsquedas sin página propia: «calculadora nuda propiedad», «calcular valor nuda propiedad», «cálculo nuda
propiedad», «tabla cálculo nuda propiedad», «coeficiente nuda propiedad», «descuento nuda propiedad por edad», «a qué edad se puede
vender la nuda propiedad», «cuánto vale la nuda propiedad de mi casa», «vender nuda propiedad». Isra quiere la página con SEO a tope: no
solo la calculadora, sino la mejor página de España para calcular la nuda propiedad, que además lleve a quien quiere vender.

## Plan (`plan_nuda.json`)
`calculadora-nuda-propiedad` · keyphrase «calculadora de nuda propiedad» · title_corto «Calculadora de nuda propiedad» · `"kind": "page"`,
`"category": null`. Guarda la spec en `tools/blog/nuda.json` (lista con 1 objeto).

## Estructura
- Sección 1 OBLIGATORIA: `{"overline": "Herramienta", "h2": "<frase con la keyphrase>", "type": "tool", "intro": ["1-2 frases"],
  "shortcode": "[zp_calculadora_n]"}`.
- Después 6-8 secciones que cubran, con H2 que respondan a las búsquedas de arriba:
  1. Cómo se calcula (fórmula en palabras): usufructo vitalicio = 89 menos la edad del usufructuario, con un mínimo del 10 % y un
     máximo del 70 %; usufructo temporal = 2 % por cada año de duración, máximo 70 %; nuda propiedad = valor total menos usufructo.
     Base legal: artículo 26 de la Ley 29/1987 del Impuesto sobre Sucesiones y Donaciones y artículo 10.2 del texto refundido del ITP
     (Real Decreto Legislativo 1/1993). Verifica las dos en el BOE (WebFetch) y cita bien.
  2. TABLA (`type: table`) de porcentajes por edad: menos de 20, 20, 30, 40, 50, 60, 65, 70, 75, 79 o más → % usufructo / % nuda
     propiedad (calcúlala con la fórmula; comprueba cada fila).
  3. Ejemplos con cifras redondas: el de la calculadora con sus valores por defecto (piso de 200.000 €, usufructo vitalicio, usufructuario
     de 75 años, tu parte 100 % → usufructo 28.000 €, nuda propiedad 172.000 €), el temporal de 10 años (40.000 € / 160.000 €) y dos
     hermanos que heredan la nuda propiedad al 50 % con la madre viuda usufructuaria.
  4. Para qué sirve ese valor: impuesto de sucesiones o donaciones del nudo propietario; qué pasa al fallecer el usufructuario
     (consolidación del dominio: verifica en el artículo 26 de la Ley 29/1987 qué se paga entonces y explícalo bien); ITP si compras o
     vendes una nuda propiedad; valor de adquisición en el IRPF cuando vendas.
  5. Valor fiscal frente a precio de mercado: la fórmula sirve para impuestos; quien compra una nuda propiedad descuenta según esperanza
     de vida, tipo de interés y estado del inmueble, así que el precio suele ser menor. Cuándo se puede vender la nuda propiedad (a cualquier
     edad del usufructuario: el nudo propietario puede vender sin su permiso; el comprador espera a la consolidación) y el usufructo sigue
     intacto. Enlaza `/vender-nuda-propiedad/` y `/blog/cuanto-vale-la-nuda-propiedad-calculo/`.
  6. Nuda propiedad en proindiviso (varios hermanos nudos propietarios, viudo usufructuario): vender tu parte de la nuda propiedad,
     extinción con usufructo. Enlaza `/blog/puedo-vender-la-casa-de-mi-madre-con-usufructo/`,
     `/blog/testamento-con-usufructo-universal-puede-vender-el-viudo/`, `/diccionario-del-proindiviso/usufructo/`,
     `/diccionario-del-proindiviso/usufructo-viudal/` o `/diccionario-del-proindiviso/conmutacion-del-usufructo/` si viene a cuento.
  7. Errores habituales (usar la edad equivocada, aplicar la tabla a un usufructo temporal, confundir valor catastral con valor de
     referencia o de mercado, olvidar que hay varios nudos propietarios...).
  8. Callout con nuestra compra: compramos nudas propiedades y partes de nuda propiedad con fondos propios; precio por escrito en 48 horas.
- 1.300-1.900 palabras de cuerpo (la sección de la herramienta solo cuenta por su intro), 6-8 FAQ (las búsquedas de arriba en forma de
  pregunta: «¿A qué edad se puede vender la nuda propiedad?», «¿Qué coeficiente se aplica a la nuda propiedad?», «¿Cuánto vale la nuda
  propiedad de un piso si mi madre tiene 80 años?»...), `related` 4-6 enlaces internos (las otras calculadoras:
  `/calculadora-impuestos-vender-tu-parte/`, `/cuanto-vale-mi-parte-de-un-piso/`, `/simulador-extincion-de-condominio/`;
  `/vender-nuda-propiedad/`; `/impuestos-del-proindiviso/`).
- SOLO enlaces internos que estén en `tools/blog/urls_publicadas.txt`.
- Rigor fiscal y jurídico: «orientativo», «consulta tu caso». País Vasco y Navarra tienen normas forales: dilo en una frase (verifica si
  su regla de valoración del usufructo coincide o no; si no lo confirmas, di solo que pueden tener reglas propias).
- `yoast_title` 50-62 caracteres que EMPIEZA por la keyphrase exacta; `h1` 55-90 con la keyphrase; `meta_desc` 130-155.
- `imagen_prompt` sin personas ni texto (escena: salón de una vivienda española con un sillón vacío junto a una ventana, unas llaves sobre
  una mesa de madera...) con el cierre obligatorio; `imagen_alt` con la keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/nuda.json tools/blog/plan_nuda.json --herramienta-plus` hasta «1/1 válidas» y
  revisa con `python3 tools/wordpress/yoastpre.py tools/blog/nuda.json`. No toques ningún otro fichero ni sistema externo.
