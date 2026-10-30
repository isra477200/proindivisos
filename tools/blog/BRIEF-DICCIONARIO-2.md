# Brief: ampliación del «Diccionario del proindiviso» de 94 a 181 entradas (30/10/2026)

Manda `BRIEF-DICCIONARIO.md` (léelo entero, y lo que él manda leer: `BRIEF-BLOG.md`, `BRIEF-PROGRAMADOS.md`, `EJEMPLO-spec.json`).
Esto solo añade lo nuevo.

- Tu lote: `tools/blog/dic_lote_N.json` (slug, focus_kw, title_corto, termino y `angulo`, que es el enfoque obligatorio). Respeta
  exactamente `slug`, `focus_kw` y `title_corto`. Escribe UNA página por término en `tools/blog/dic_N.json` (mismo N).
- El plan completo de términos (los 72 publicados, los 87 nuevos y los 32 que ya cubren otras páginas) está en
  `tools/blog/diccionario_plan.json`. Para enlazar a otro término usa `/diccionario-del-proindiviso/{slug}/` (todos los «nuevos»
  existirán) o la `url` de los «existentes».
- Todas las URL publicadas y programadas: `tools/blog/urls_todas.txt`. No repitas el enfoque de una entrada del blog que ya trate el tema:
  enlázala y define el término.
- Secciones nuevas que también puedes enlazar cuando encaje: `/impuestos-del-proindiviso/` (impuestos por comunidad autónoma),
  `/modelos-documentos-proindiviso/` (modelos de burofax, requerimiento de división, notificación de venta de cuota, pacto de indivisión,
  acuerdo entre copropietarios: rutas en `tools/blog/plan_modelos.json`), `/calculadora-impuestos-vender-tu-parte/`,
  `/calculadora-compensacion-uso-exclusivo/`, `/calculadora-gastos-entre-copropietarios/`, `/preguntas-frecuentes-proindiviso/`.
- Imagen: escena distinta en cada término y distinta de las del resto del diccionario (no repitas llave sobre mesa ni fachada genérica).
- Valida con `python3 tools/blog/validar.py tools/blog/dic_N.json tools/blog/diccionario_plan.json --diccionario` hasta «N/N válidas» y
  revisa con `python3 tools/wordpress/yoastpre.py tools/blog/dic_N.json` (corrige lo naranja o rojo). Si el validador marca densidad baja
  en una keyphrase de una palabra, mete la palabra en más frases naturales; si una keyphrase larga no encaja, reformula frases, nunca la
  cambies.
- No toques ningún otro fichero del repositorio ni ningún sistema externo.
