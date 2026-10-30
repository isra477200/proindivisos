# Brief: 3 páginas-herramienta nuevas (30/10/2026) — complementa a BRIEF-BLOG.md y BRIEF-PROGRAMADOS.md

Lee primero `BRIEF-BLOG.md`, las reglas de imagen y de Yoast de `BRIEF-PROGRAMADOS.md` (mandan) y `EJEMPLO-spec.json`. Mira también cómo
están planteadas las dos calculadoras que ya existen: `tools/wordpress/calculadoras.py` (specs en el propio fichero) y
`tools/blog/calculadoras_ajustes.json`. Las calculadoras ya están programadas (`tools/wordpress/snippet_calculadoras2.php` y
`snippet_calculadoras2_assets.php`: léelos para que el texto explique EXACTAMENTE lo que calculan, con los mismos nombres de campo).

## Plan (`plan_herramientas.json`): slug, focus_kw, title_corto y `tool`
1. `calculadora-impuestos-vender-tu-parte` · «calculadora de impuestos al vender tu parte» · tool `impuestos`: plusvalía municipal (método
   objetivo con coeficientes máximos vigentes en 2026 y método real; se aplica el menor; sin incremento no hay impuesto) e IRPF (escala del
   ahorro 2026: 19 % hasta 6.000 €, 21 % hasta 50.000 €, 23 % hasta 200.000 €, 27 % hasta 300.000 €, 30 % por encima; no residentes 19 %
   con retención del 3 % por el comprador; exención de mayores de 65 en su vivienda habitual). Datos y fuentes: `fiscal_comun.json`.
2. `calculadora-compensacion-uso-exclusivo` · «calculadora de compensación por uso exclusivo» · tool `uso`: renta de mercado × tu % × meses
   desde la reclamación (tope 60 meses, art. 1966 CC) − gastos de tu parte que pagó el ocupante.
3. `calculadora-gastos-entre-copropietarios` · «calculadora de gastos entre copropietarios» · tool `gastos`: reparto por cuotas de IBI,
   comunidad, seguro, basuras, derramas y otros (arts. 393 y 395 CC), saldo de cada copropietario según lo que ha pagado y quién debe a quién.

## Cada página (`"kind": "page"`, `"category": null`, JSON: lista de 3 objetos en `tools/blog/herramientas.json`)
- Sección 1 OBLIGATORIA: `{"overline": "Herramienta", "h2": "<frase con la keyphrase>", "type": "tool", "intro": ["1-2 frases"],
  "shortcode": "[zp_calculadora_x tipo=\"impuestos\"]"}` (o `uso` / `gastos`).
- Después 3-6 secciones: cómo se calcula (con la fórmula en palabras y un ejemplo con cifras redondas que dé el mismo resultado que la
  calculadora con sus valores por defecto: compruébalo leyendo el JS), qué datos necesitas y dónde encontrarlos (recibo del IBI, escritura,
  autoliquidación de sucesiones...), errores habituales, qué hacer con el resultado (reclamar con burofax: enlaza a
  `/modelos-documentos-proindiviso/modelo-burofax-copropietario/`; o vender la parte), y un callout con nuestra compra.
- 650-1.250 palabras de cuerpo (la sección de la herramienta solo cuenta por su intro), 5-6 FAQ, `related` 3-5 enlaces internos
  (`urls_todas.txt`; las otras calculadoras: `/cuanto-vale-mi-parte-de-un-piso/`, `/simulador-extincion-de-condominio/` y estas tres;
  `/impuestos-del-proindiviso/`). Rigor fiscal y jurídico: «orientativo», «según ayuntamiento/comunidad».
- `yoast_title` 50-62 caracteres que EMPIEZA por la keyphrase exacta; `imagen_prompt` sin personas ni texto ni papeles (escenas: una
  calculadora no, una mesa de trabajo con una lámpara y una taza junto a una ventana con vistas a tejados, un patio de vecinos, la entrada
  de un piso con un perchero...) con el cierre obligatorio; `imagen_alt` con la keyphrase.
- Valida con `python3 tools/blog/validar.py tools/blog/herramientas.json tools/blog/plan_herramientas.json --herramienta` hasta «3/3
  válidas» y revisa con `python3 tools/wordpress/yoastpre.py tools/blog/herramientas.json`. No toques ningún otro fichero ni sistema externo.
