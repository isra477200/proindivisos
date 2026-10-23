import sys, os, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import run, meta
from blogbuilder import load_specs, load_ids, api, CATS
CATNAMES={'herencias':('Herencias','Vender tu parte de una herencia: hermanos, usufructo, derechos hereditarios e impuestos.'),'extincion-de-condominio':('Extinción de condominio','Compensación, hipoteca, notario, escritura y ejemplos con cifras.'),'copropiedad':('Copropiedad y proindiviso','Qué es, tus derechos como copropietario y cómo salir cuando los demás no quieren.'),'division-de-cosa-comun':('División de cosa común','Juicio, abogado, subasta y alternativas para salir del proindiviso.'),'impuestos-y-tramites':('Impuestos y trámites','Notaría, Registro, AJD, plusvalía e IRPF al vender tu parte.')}
S=load_specs(); ids=load_ids()
posts=[s for s in S if s['kind']=='post' and s['slug'] in ids]
pages=[s for s in S if s['kind']=='page' and s['slug'] in ids]
sections=[{"overline":"Para empezar","h2":"Guías para vender tu parte","intro":["Si tu situación es una de estas, empieza por la guía: resuelve la duda principal y te dice cuánto pagamos y cómo."],"type":"cards","items":[{"t":p['title_corto'],"p":p['sub'].split('. ')[0]+'.',"url":f"/{p['slug']}/","cta":"Leer la guía →"} for p in pages]}] if pages else []
for cslug,(cname,cdesc) in CATNAMES.items():
    items=[{"t":p['h1'],"p":(p['sub'].split('. ')[0]+'.'),"url":f"/blog/{p['slug']}/","cta":"Leer →"} for p in posts if p['category']==cslug]
    if items: sections.append({"overline":cname,"h2":f"{cname}: artículos","intro":[cdesc],"type":"cards","items":items})
sections.append({"type":"callout","items":{"t":"¿Tu caso no está aquí?","p":"Cuéntanoslo. Te decimos en 48 horas si compramos tu parte y por cuánto.","cta":"Pedir oferta"}})
spec={"post_id":None,"kicker":"Blog","h1":"Blog de Zona Proindiviso: respuestas claras para vender tu parte de un inmueble","sub":"Herencias bloqueadas, extinción de condominio, división de cosa común, impuestos y copropiedad, explicados con cifras y sin rodeos. Y siempre con la salida más rápida: compramos tu parte.","checks":["Guías actualizadas en 2026","Con artículos del Código Civil","Escritas por quien compra"],"card_title":"¿Prefieres hablar con nosotros?","card_text":"Déjanos tu teléfono y te llamamos en menos de 24 horas laborables.","sections":sections,"faqs":[("¿Quién escribe estos artículos?","El equipo de Zona Proindiviso, que compra cuotas indivisas y partes de herencias en toda España. Lo que explicamos es lo que vemos cada semana en notarías y registros."),("¿Puedo consultaros mi caso aunque no quiera vender todavía?","Sí. Te damos precio por escrito sin compromiso. Muchas personas lo usan como referencia para negociar con sus hermanos o su expareja."),("¿Los contenidos sustituyen a un abogado?","No. Son orientación general. Para un pleito o una herencia compleja, consulta a un profesional. Para vender tu parte, nosotros nos ocupamos de todo.")],"faq_title":"Sobre este blog","related":[("Qué es un proindiviso","/que-es-un-proindiviso/"),("Cuánto pagamos","/cuanto-pagan-por-un-proindiviso/"),("Dónde compramos","/vender-proindiviso/")],"cta_title":"Pide precio por tu parte","cta_text":"Rellena el formulario con la dirección y tu porcentaje. En 48 horas tienes una oferta por escrito, válida 30 días."}
# página /blog/
r=api('GET','/wp/v2/pages?slug=blog&status=any&_fields=id')
if isinstance(r,list) and r: pid=r[0]['id']
else:
    out=subprocess.run(['./emcp.sh','elementor-create-page',json.dumps({'title':'Blog','post_type':'page'})],capture_output=True,text=True).stdout
    pid=int((re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out)).group(1))
    api('POST',f'/wp/v2/pages/{pid}',{'title':'Blog','slug':'blog','status':'draft'})
spec['post_id']=pid
if run(spec): meta(pid,title='Blog',yt='Blog: guías para vender tu parte de un inmueble · Zona Proindiviso',yd='Herencias, extinción de condominio, división de cosa común, impuestos y copropiedad explicados con cifras. Y la salida rápida: compramos tu parte.',kw='blog proindiviso',status='publish',slug='blog')
print('blog page',pid,len(posts),'posts',len(pages),'pages')
