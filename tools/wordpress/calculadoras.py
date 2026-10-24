"""Páginas-herramienta: «Cuánto vale mi parte de un piso» y «Simulador de gastos de extinción de condominio».
Crea la página (elementor-create-page) si no existe, compone con pagebuilder.build (sección type=tool → shortcode del snippet
snippet_calculadoras.php), publica y fija metas. Uso: python3 calculadoras.py [parte|condominio]"""
import sys, os, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import run, meta, _env
env=_env()
def api(method,path,body=None):
    args=['curl','-sS','--max-time','60','-u',env['P1'],'-X',method,env['WP']+'/wp-json'+path]
    if body is not None: args+=['-H','Content-Type: application/json','-d',json.dumps(body,ensure_ascii=False)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:300]}
def ensure_page(slug,title):
    r=api('GET',f"/wp/v2/pages?slug={slug}&status=any&_fields=id")
    if isinstance(r,list) and r: return r[0]['id']
    out=subprocess.run(['./emcp.sh','elementor-create-page',json.dumps({'title':title,'post_type':'page'})],capture_output=True,text=True).stdout
    m=re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out)
    if not m: print('CREATE FAIL',slug,out[:200]); return None
    pid=int(m.group(1)); api('POST',f'/wp/v2/pages/{pid}',{'title':title,'slug':slug,'status':'draft'}); return pid
POP="#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6MjIsInRvZ2dsZSI6ZmFsc2V9"
SPECS={}
SPECS['parte']={"slug":"cuanto-vale-mi-parte-de-un-piso","title":"Cuánto vale mi parte de un piso","kw":"cuánto vale mi parte de un piso","image_id":4915,"dated":True,
"yt":"Cuánto vale mi parte de un piso: calculadora gratis (2026)","yd":"Calcula cuánto vale tu parte de un piso en un minuto: valor teórico de tu cuota, lo que paga una empresa compradora y lo que quedaría en subasta. Oferta real en 48 h.",
"kicker":"Calculadora","h1":"Cuánto vale mi parte de un piso: calcúlalo en un minuto",
"sub":"Pon el valor del piso, tu porcentaje y cómo está el inmueble. Te decimos cuánto vale tu parte sobre el papel, cuánto te pagaría hoy una empresa compradora y qué te quedaría si fueras a juicio.",
"checks":["Cálculo visible, sin registro","Horquillas reales del mercado","Oferta por escrito en 48 h"],
"card_title":"Prefieres el precio real","card_text":"La calculadora orienta. Si quieres una cifra en firme por tu parte, déjanos tu teléfono y te llamamos en menos de 24 horas laborables.",
"sections":[
 {"overline":"Herramienta","h2":"Calcula cuánto vale tu parte del piso","intro":["Los resultados cambian según escribes. Todo el cálculo está a la vista: nada de fórmulas ocultas ni de registrarte para ver la cifra."],"type":"tool","shortcode":'[zp_calculadora tipo="parte"]'},
 {"overline":"El método","h2":"Cómo se calcula el valor de tu parte de un piso","intro":["Hay dos números distintos y conviene no mezclarlos. El primero es el valor teórico: lo que vale tu cuota si el inmueble se vendiera entero hoy y se repartiera el dinero. Se calcula restando la hipoteca pendiente al valor de mercado y aplicando tu porcentaje. Con un piso de 180.000 €, sin hipoteca y con la mitad a tu nombre, tu parte vale 90.000 € sobre el papel.","El segundo número es lo que de verdad puedes cobrar sin el acuerdo de los demás. Nadie compra media vivienda para vivir en ella: quien compra tu parte compra el derecho a reclamarla, con el conflicto incluido, y por eso paga con descuento. La calculadora aplica las horquillas que se ven en el mercado español: del 30 % al 60 % de descuento según quién ocupe el inmueble, si hay contrato de alquiler, si la herencia está sin adjudicar o si hay un okupa."]},
 {"overline":"Factores","h2":"Por qué tu parte del piso vale menos que su porcentaje","type":"table","items":[
  ("Situación del inmueble","Descuento habitual sobre el valor teórico"),
  ("Vacío o de uso compartido","Del 30 % al 40 %. Es la mejor situación: el comprador puede negociar la venta del conjunto con rapidez."),
  ("Lo ocupa otro copropietario sin pagar","Del 40 % al 50 %. Quien está dentro no tiene prisa; muchas veces hay que ir al juzgado para desalojar o subastar."),
  ("Alquilado con contrato","Del 35 % al 45 %. La renta compensa en parte, pero el comprador no puede disponer del inmueble hasta que el contrato acabe."),
  ("Herencia sin adjudicar","Del 45 % al 55 %. Antes de vender hay que aceptar la herencia, liquidar el impuesto y escriturar; el comprador asume esa gestión."),
  ("Ocupado sin título (okupa)","Del 50 % al 60 %. El desalojo tarda y cuesta; el comprador descuenta ese tiempo y ese riesgo."),
  ("Porcentaje minoritario","Resta entre 5 y 10 puntos más. Un 25 % tiene menos fuerza para forzar la venta del conjunto que un 50 %.")],
  "outro":["La hipoteca no es un descuento: se resta antes de repartir, porque en cualquier venta o subasta el banco cobra primero. Lo que sí baja el precio es una hipoteca impagada con un procedimiento de ejecución en marcha."]},
 {"overline":"Opciones","h2":"Tres caminos para convertir tu parte del piso en dinero","type":"cards","items":[
  {"t":"Vender el piso entero con acuerdo","p":"Si todos los copropietarios quieren vender, es la mejor opción: cobráis el valor de mercado menos los gastos de venta. El problema es que casi nunca hay acuerdo, y por eso has llegado hasta aquí."},
  {"t":"Vender tu parte a una empresa compradora","p":"Cobras entre el 40 % y el 70 % del valor teórico de tu cuota, al contado y en unas dos semanas. Sin avisar a los demás, sin pleito y sin pagar notaría. Es lo que hacemos nosotros.","url":POP,"cta":"Pedir mi oferta →"},
  {"t":"Forzar la subasta (división de cosa común)","p":"Cualquier copropietario puede pedir al juzgado que se venda el inmueble. Tarda de 12 a 24 meses, cuesta varios miles de euros en abogado y procurador, y las subastas se adjudican entre el 50 % y el 70 % del valor de tasación."}],
  "outro":["La calculadora compara las tres salidas con tus números. Si el resultado de la subasta te parece parecido al de la venta directa, fíjate en lo que no sale en la cifra: dos años de espera, el riesgo de que no haya postores y el trato con la otra parte durante todo el proceso."]},
 {"overline":"Precio real","h2":"De la calculadora a una oferta en firme","intro":["La herramienta usa horquillas medias. La cifra exacta depende de la zona, del estado del inmueble, de las cargas inscritas y de la documentación que tengas. Para darte un precio real revisamos la nota simple del Registro y te enviamos la oferta por escrito en 48 horas, sin compromiso y sin que tengas que avisar a nadie."],
  "type":"callout","items":{"t":"¿Quieres saber cuánto te pagamos por tu parte?","p":"Cuéntanos el caso en dos minutos: qué inmueble es, qué porcentaje tienes y cómo está. Te llamamos con una oferta en menos de 24 horas laborables.","cta":"Pedir mi oferta"}}],
"faqs":[("¿Cómo sé cuánto vale el piso entero para hacer el cálculo?","Mira anuncios de pisos parecidos en tu misma zona y descuenta entre un 5 % y un 10 %, que es la diferencia habitual entre el precio de anuncio y el de cierre. También puedes usar el valor de referencia del Catastro como suelo: Hacienda no acepta valores inferiores en los impuestos."),
("¿Mi parte del piso vale lo mismo si yo vivo en él?","Para una empresa compradora, no: si tú ocupas el inmueble y sigues dentro después de vender, el comprador tiene que negociar o litigar contigo. Lo normal es pactar la entrega de llaves en la misma escritura, y entonces el precio sube."),
("¿Puedo vender mi parte si hay hipoteca?","Sí. La hipoteca sigue sobre el inmueble entero y se cancela cuando se venda o subaste. En la calculadora se resta del valor antes de aplicar tu porcentaje, que es como se reparte el dinero en cualquiera de las tres salidas."),
("¿Por qué una empresa paga menos que la subasta en algunos casos?","Porque en la subasta el precio sale de la calculadora sin contar el tiempo ni el riesgo: un pleito de uno o dos años, costas y la posibilidad de que la subasta quede desierta. La empresa te paga ahora y asume todo eso en tu lugar."),
("¿La calculadora guarda mis datos?","No. Todo se calcula en tu navegador y no se envía nada a ningún sitio. Solo nos escribes si quieres una oferta.")],
"related":[("Cuánto pagan por un proindiviso","/cuanto-pagan-por-un-proindiviso/"),("Vender tu parte de un piso","/vender-parte-de-un-piso/"),("Simulador de gastos de extinción de condominio","/simulador-extincion-de-condominio/"),("Empresas que compran proindivisos","/empresas-que-compran-proindivisos/"),("Vender con hipoteca","/vender-proindiviso-con-hipoteca/"),("División de cosa común","/division-de-cosa-comun/")],
"cta_title":"Cuánto vale mi parte de un piso: te lo decimos con una oferta real"}
SPECS['condominio']={"slug":"simulador-extincion-de-condominio","title":"Simulador de gastos de extinción de condominio","kw":"gastos de extinción de condominio","image_id":4916,"dated":True,
"yt":"Gastos de extinción de condominio: simulador 2026 (AJD, notaría)","yd":"Simula los gastos de una extinción de condominio: AJD por comunidad autónoma, notaría, registro, gestoría e hipoteca. Y lo que cuesta la vía judicial si no hay acuerdo.",
"kicker":"Simulador","h1":"Gastos de extinción de condominio: simulador con AJD por comunidad",
"sub":"Escribe el valor del inmueble, la comunidad autónoma y la cuota del que se queda. Te desglosamos la compensación, el impuesto, la notaría y el registro, y los comparamos con el coste de ir a juicio o de vender tu parte.",
"checks":["AJD de las 19 comunidades","Cálculo visible","Con y sin acuerdo"],
"card_title":"Si no hay acuerdo","card_text":"La extinción de condominio solo funciona cuando todos firman. Si alguien se niega, compramos tu parte: precio por escrito en 48 horas.",
"sections":[
 {"overline":"Herramienta","h2":"Simula los gastos de tu extinción de condominio","intro":["Los resultados se actualizan según escribes. Son orientativos: los aranceles de notaría y registro dependen de cada caso y algunas comunidades tienen tipos reducidos de AJD por vivienda habitual, familia numerosa o discapacidad."],"type":"tool","shortcode":'[zp_calculadora tipo="condominio"]'},
 {"overline":"Con acuerdo","h2":"Qué gastos tiene una extinción de condominio con acuerdo","intro":["La extinción de condominio es la escritura por la que uno de los copropietarios se queda con el inmueble entero y compensa a los demás en dinero. No es una compraventa, y por eso no paga ITP: tributa por Actos Jurídicos Documentados, que es más barato. Estos son los gastos que aparecen en la simulación."],
  "type":"table","items":[
  ("Concepto","Cuánto y quién lo paga"),
  ("Compensación a los que salen","El valor de la parte que adquiere quien se queda, descontada la hipoteca pendiente. No es un gasto: es el precio de la operación."),
  ("AJD (Actos Jurídicos Documentados)","Entre el 0,5 % y el 1,5 % según la comunidad, sobre el valor de la parte adquirida. Lo paga quien se queda con el inmueble."),
  ("Notaría","Arancel fijado por el Estado según el valor: de unos 500 € a 1.500 €. Se suele pactar que lo pague el adjudicatario."),
  ("Registro de la Propiedad","Inscripción de la nueva titularidad: de unos 250 € a 900 € según el valor."),
  ("Gestoría","Opcional si lo haces tú; obligatoria en la práctica si hay hipoteca, porque el banco la impone: unos 300 €."),
  ("Hipoteca","Si hay préstamo, el banco debe liberar al que sale (novación): comisión de novación más notaría y registro de esa escritura."),
  ("Plusvalía municipal","No se paga si el inmueble es indivisible y la compensación es en dinero: no hay transmisión a efectos del impuesto."),
  ("IRPF de quien sale","Puede haber ganancia patrimonial si cobra más de lo que le costó su parte (criterio del Tribunal Supremo desde 2022).")]},
 {"overline":"Impuesto","h2":"AJD de la extinción de condominio por comunidad autónoma","intro":["La base del impuesto es el valor de la parte que se adquiere, no el valor total del inmueble: lo fijó el Tribunal Supremo en su sentencia de 9 de octubre de 2018. Algunas oficinas liquidadoras siguen calculando sobre el total; si te ocurre, recurre. Tipos generales que usa el simulador:"],
  "type":"table","items":[
  ("Comunidad","Tipo general de AJD"),
  ("Navarra, País Vasco, Ceuta y Melilla","0,5 %"),
  ("Madrid y Canarias","0,75 %"),
  ("La Rioja","1 %"),
  ("Andalucía y Asturias","1,2 %"),
  ("Cataluña, Comunidad Valenciana, Galicia, Aragón, Baleares, Cantabria, Castilla y León, Castilla-La Mancha, Extremadura y Murcia","1,5 %")],
  "outro":["Con un piso de 200.000 € y una mitad que cambia de manos, el AJD va de 500 € en Navarra a 1.500 € en Cataluña. Si tu comunidad tiene un tipo reducido por vivienda habitual o por familia numerosa, el simulador se queda corto a tu favor."]},
 {"overline":"Sin acuerdo","h2":"Gastos de la extinción de condominio sin acuerdo: la vía judicial","type":"steps","items":[
  {"t":"Demanda de división de cosa común","p":"Si un copropietario no quiere firmar, no hay extinción posible: hay que pedir al juzgado la división. Abogado y procurador obligatorios; los honorarios medios van de 3.000 € a 9.000 € según el valor del inmueble."},
  {"t":"Tasación pericial y sentencia","p":"El juzgado declara el inmueble indivisible y ordena su venta en subasta. Entre la demanda y la sentencia pasan de 8 a 18 meses, según el juzgado."},
  {"t":"Subasta y reparto","p":"Las subastas se adjudican entre el 50 % y el 70 % del valor de tasación. Se cancela primero la hipoteca y el resto se reparte por cuotas. Si queda desierta, vuelta a empezar."}],
  "outro":["Por eso el simulador muestra, junto al pleito, una tercera salida: vender tu cuota a una empresa compradora, que se queda en tu lugar y es ella quien negocia o litiga con los demás."]},
 {"overline":"Alternativa","h2":"Cuándo compensa vender tu parte en lugar de pagar los gastos","intro":["Si hay acuerdo y quien se queda puede pagar, la extinción de condominio es casi siempre la salida más barata: entre el 1 % y el 3 % del valor en gastos. El problema aparece cuando uno no quiere firmar, no tiene el dinero para compensar o el banco no acepta la novación de la hipoteca. Ahí la alternativa al juzgado es vender tu parte: cobras entre el 55 % y el 70 % de su valor teórico, sin gastos, sin esperar y sin el conflicto."],
  "type":"callout","items":{"t":"¿Un copropietario se niega a firmar?","p":"Compramos tu parte aunque los demás no quieran vender. Oferta por escrito en 48 horas y firma en notaría en unas dos semanas.","cta":"Pedir mi oferta"}}],
"faqs":[("¿La extinción de condominio paga ITP o AJD?","Paga AJD, no ITP, siempre que el inmueble sea indivisible y la compensación a los demás sea en dinero. Si en lugar de dinero se entrega otro bien, o si hay excesos de adjudicación no justificados, Hacienda puede liquidar ITP sobre ese exceso."),
("¿Sobre qué valor se calcula el AJD de la extinción de condominio?","Sobre el valor de la parte que adquiere quien se queda, según el Tribunal Supremo. Si eran dos al 50 %, la base es la mitad del valor del inmueble. Hacienda comprobará que ese valor no sea inferior al valor de referencia del Catastro."),
("¿Quién paga los gastos de la extinción de condominio?","El AJD lo paga quien se queda con el inmueble (el adquirente). Notaría, registro y gestoría se pactan: lo habitual es que los asuma el adjudicatario, aunque los copropietarios pueden repartirlos como quieran en la escritura."),
("¿Hay plusvalía municipal en la extinción de condominio?","No, si el inmueble es indivisible y la compensación es en metálico: los tribunales consideran que no hay transmisión. Ojo con el IRPF: quien sale puede tener ganancia patrimonial si la compensación supera el valor por el que adquirió su parte."),
("¿Qué pasa con la hipoteca en la extinción de condominio?","La hipoteca no desaparece: quien se queda tiene que asumirla entera y el banco debe liberar al que sale mediante una novación. Si el banco no acepta, la extinción se complica, y es una de las razones por las que muchos copropietarios acaban vendiendo su parte.")],
"related":[("Extinción de condominio","/extincion-de-condominio/"),("Impuestos y notario en la extinción","/extincion-de-condominio/impuestos-y-notario/"),("Extinción de condominio con hipoteca","/extincion-de-condominio/hipoteca/"),("Cuánto vale mi parte de un piso","/cuanto-vale-mi-parte-de-un-piso/"),("División de cosa común","/division-de-cosa-comun/"),("Vender con hipoteca","/vender-proindiviso-con-hipoteca/")],
"cta_title":"Gastos de extinción de condominio o una oferta por tu parte: tú eliges"}
# ajustes de Yoast (palabras de transición y descripción ≤ 155) generados con transfix.py: blog/calculadoras_ajustes.json
_AJ=os.path.join(os.path.dirname(os.path.abspath(__file__)),'blog','calculadoras_ajustes.json')
if os.path.exists(_AJ):
    for _k,_v in json.load(open(_AJ)).items():
        if _k in SPECS: SPECS[_k]['sections']=_v['sections']; SPECS[_k]['faqs']=[tuple(x) for x in _v['faqs']]; SPECS[_k]['yd']=_v['yd']
if __name__=='__main__':
    only=sys.argv[1:]
    for key,s in SPECS.items():
        if only and key not in only: continue
        pid=ensure_page(s['slug'],s['title'])
        if not pid: continue
        s['post_id']=pid; print(key,'post_id',pid,flush=True)
        ok=run(s,publish=True)
        if ok: meta(pid,title=s['title'],yt=s['yt'],yd=s['yd'],kw=s['kw'],status='publish',slug=s['slug'],extra={'featured_media':s['image_id']})
