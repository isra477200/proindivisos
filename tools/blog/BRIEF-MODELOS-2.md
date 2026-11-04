# Brief: 6 modelos nuevos de documentos del proindiviso (04/11/2026) — complementa a BRIEF-MODELOS.md

Lee primero `BRIEF-MODELOS.md` (manda en todo lo que no cambie aquí), `BRIEF-BLOG.md`, las reglas de imagen y de Yoast de
`BRIEF-PROGRAMADOS.md`, y `modelos.json` (los 6 modelos ya publicados: mismo formato, mismo tono, sin repetir contenido).

## Qué hay que hacer
1. 6 páginas nuevas, una por modelo, en `tools/blog/modelos2.json` (lista de 6 objetos), según `plan_modelos2.json`: `slug`, `focus_kw`,
   `title_corto` EXACTOS; el campo `modelo` del plan dice qué debe resolver cada documento. Cuelgan de `/modelos-documentos-proindiviso/`.
2. Actualizar en `tools/blog/modelos.json` SOLO el primer objeto (el índice `/modelos-documentos-proindiviso/`): añade las 6 tarjetas nuevas
   (url, t, p) a la sección `cards` (o una segunda sección `cards` si queda mejor: «Comprar, vender y reclamar dinero»), ajusta el texto
   para que el índice presente 12 modelos y revalida. No toques los otros objetos de `modelos.json`.

## Rigor jurídico (Derecho civil común español; si el modelo cambia en Cataluña, Aragón, Navarra, País Vasco, Galicia o Baleares, dilo en
el texto de la página en una frase prudente)
- Compraventa entre hermanos: contrato privado válido entre las partes; para inscribir en el Registro hace falta escritura pública. Si con
  la compra uno pasa a tener el 100 %, Hacienda la trata como extinción de condominio (AJD sobre la parte adquirida, doctrina del Tribunal
  Supremo); si quedan más copropietarios, ITP. Si hay otros copropietarios, tienen derecho de retracto (arts. 1522 y 1524 CC).
- Cesión de derechos hereditarios: la cesión de derechos hereditarios debe constar en documento público (art. 1280 CC); los demás
  coherederos pueden subrogarse en el lugar del comprador extraño reembolsándole el precio en el plazo de un mes desde que se les haga
  saber (art. 1067 CC). Verifica ambos en el BOE. El modelo es un documento previo/borrador para llevar a la notaría: dilo.
- Arras: arras penitenciales del art. 1454 CC (quien las da las pierde si desiste; quien las recibe las devuelve duplicadas). Retracto de
  comuneros: nueve días (art. 1524 CC) desde la inscripción o, en su defecto, desde que el retrayente tuvo conocimiento de la venta.
- Reconocimiento de deuda y reclamación de rentas: arts. 393 y 395 CC (gastos y frutos en proporción a la cuota); prescripción: verifica
  qué plazo aplica (art. 1964 CC, acciones personales, 5 años; art. 1966 CC para pagos periódicos) y dilo con prudencia.
- Oferta de compra: si el comprador se queda el 100 %, AJD de la extinción de condominio; el que vende no paga ITP; plusvalía municipal e
  IRPF del que vende (enlaza `/calculadora-impuestos-vender-tu-parte/`).
- Nada de plazos inventados: si dudas de una cifra, búscala (WebSearch/WebFetch, fuentes oficiales: BOE, notariado, Correos para el
  burofax).

## Enlaces internos
SOLO URL que estén en `tools/blog/urls_publicadas.txt` (incluye los modelos ya publicados, las calculadoras y el blog). Enlaza cada modelo
con 1-2 modelos relacionados (nuevos o existentes) y con su calculadora natural: reconocimiento de deuda →
`/calculadora-gastos-entre-copropietarios/`; reclamación de rentas → `/calculadora-compensacion-uso-exclusivo/`; compraventa y oferta →
`/cuanto-vale-mi-parte-de-un-piso/` y `/calculadora-impuestos-vender-tu-parte/`; cesión de derechos → `/vender-derechos-hereditarios/`.

## Formato y validación
- Igual que BRIEF-MODELOS: 2.ª sección type `tool` con `"shortcode": "[zp_modelo id=\"{slug}\"]"`, campo `modelo` {titulo, texto con huecos
  [EN MAYÚSCULAS] y el aviso inicial, instrucciones}, 650-1.250 palabras sin contar el modelo, 4-6 FAQ, related 3-5.
- `yoast_title` 50-62 caracteres que EMPIEZA por la keyphrase exacta; `imagen_prompt` sin personas ni papeles ni texto, escena distinta en
  cada modelo y distinta de las de `modelos.json`, con el cierre obligatorio; `imagen_alt` con la keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/modelos2.json tools/blog/plan_modelos2.json --modelo` hasta «6/6 válidas» y con
  `python3 tools/blog/validar.py tools/blog/modelos.json tools/blog/plan_modelos.json --modelo` (el índice sigue válido); revisa con
  `python3 tools/wordpress/yoastpre.py` ambos ficheros. No toques ningún otro fichero ni sistema externo.
