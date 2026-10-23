import sys, os, json, glob, subprocess, hashlib, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import run, meta
HERE=os.path.dirname(os.path.abspath(__file__))
env={}
for l in open(os.path.join(HERE,'wp.env')):
    if '=' in l: k,v=l.strip().split("=",1); env[k]=v.strip().strip("\"").strip("'")
WP=env['WP']; AUTH=env['P1']
HUB=55
def api(method,path,body=None):
    args=['curl','-sS','--max-time','60','-u',AUTH,'-X',method,'-H','Content-Type: application/json',WP+'/wp-json'+path]
    if body is not None: args+=['-d',json.dumps(body,ensure_ascii=False)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:300]}
def load_places():
    P=[]
    for f in sorted(glob.glob(os.path.join(HERE,'geo','geo_[A-F].json'))): P+=json.load(open(f))
    by={p['slug']:p for p in P}
    for p in P:
        p['hijos']=[q for q in P if q.get('padre')==p['slug']]
    return P,by
IDS_FILE=os.path.join(HERE,'geo','ids.json')
def load_ids():
    return json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}
def ensure_pages(P,by):
    ids=load_ids()
    order=[p for p in P if p['tipo']=='ccaa']+[p for p in P if p['tipo']=='provincia']+[p for p in P if p['tipo']=='ciudad']
    for p in order:
        if p['slug'] in ids: continue
        parent=HUB if not p.get('padre') else ids[p['padre']]
        r=api('GET',f"/wp/v2/pages?slug={p['slug']}&parent={parent}&status=any&_fields=id,slug")
        if isinstance(r,list) and r: ids[p['slug']]=r[0]['id']
        else:
            out=subprocess.run(['./emcp.sh','elementor-create-page',json.dumps({'title':h1_corto(p),'post_type':'page'})],capture_output=True,text=True).stdout
            m=re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out)
            if not m: print('CREATE FAIL',p['slug'],out[:200]); continue
            pid=int(m.group(1)); r=api('POST',f'/wp/v2/pages/{pid}',{'title':h1_corto(p),'slug':p['slug'],'parent':parent,'status':'draft'})
            if 'id' in r: ids[p['slug']]=r['id']
            else: print('CREATE FAIL',p['slug'],r); continue
        json.dump(ids,open(IDS_FILE,'w'),ensure_ascii=False,indent=0)
        print('page',p['slug'],ids[p['slug']],flush=True)
    return ids
def excerpt(t,n=170):
    t=t.strip()
    first=t.split('. ')[0].rstrip('.')+'.'
    if len(first)<=n: return first
    cut=t[:n].rsplit(' ',1)[0].rstrip(',;:')
    return cut+'…'
def h(s,n): return int(hashlib.md5(s.encode()).hexdigest(),16)%n
def rompe_repeticion(text):
    """Si tres frases seguidas empiezan por la misma palabra (Yoast: "frases consecutivas"), antepone un conector a la tercera."""
    if not text: return text
    parts=re.split(r'(?<=[.!?])\s+',text.strip())
    first=lambda x: re.sub(r'[^\wáéíóúüñ]','',x.split()[0].lower()) if x.split() else ''
    ops=["Además, ","Por otro lado, ","Asimismo, "]; k=0
    for i in range(2,len(parts)):
        if first(parts[i]) and first(parts[i])==first(parts[i-1])==first(parts[i-2]):
            parts[i]=conecta(ops[k%3],parts[i]); k+=1
    return ' '.join(parts)
def conecta(op,ex):
    """Antepone un conector al extracto. Pasa a minúscula la primera palabra si es preposición/adverbio/verbo común, o un artículo seguido de
    minúscula; los nombres propios (Jerez, El Puerto, San Fernando) se quedan como están."""
    if not ex: return ex
    w=ex.split()
    SIEMPRE={'En','A','Con','Desde','Hasta','Por','Para','Sin','Sobre','Hoy','Aquí','Cada','Más','Menos','Pocos','Pocas','Varios','Varias','Todo','Toda','Todos','Todas','Media','Medio','Quien','Quienes','Cuando','Donde','Como','Si','No','Ni','Ya','Aún','Tras','Según','Hace','Hacen','Falta','Faltan','Sobran','Hay','Es','Son','Tiene','Tienen','Abundan','Predominan','Dominan','Conviven','Muchos','Muchas','Casi','Gran','Buena','Mucho','Mucha','Parte','Entre','Este','Esta','Estos','Estas','Su','Sus','Aunque','Mientras','Al','Del'}
    ARTICULOS={'El','La','Los','Las','Un','Una','Unos','Unas'}
    if w[0] in SIEMPRE or (w[0] in ARTICULOS and len(w)>1 and w[1][:1].islower()):
        ex=ex[0].lower()+ex[1:]
    return op+ex
def h1_corto(p):
    return f"Vender proindiviso en {p['nombre']}" if p['tipo']!='ccaa' or p['slug'] in ('ceuta','melilla') else f"Vender proindiviso en {nombre_h1(p)}"
def nombre_h1(p):
    return {'madrid':'Madrid','murcia':'Murcia','baleares':'Baleares','comunidad-valenciana':'la Comunidad Valenciana','pais-vasco':'el País Vasco','la-rioja':'La Rioja','castilla-la-mancha':'Castilla-La Mancha','castilla-y-leon':'Castilla y León','asturias':'Asturias'}.get(p['slug'],p['nombre'])
def url(p,by):
    parts=[]; q=p
    while q: parts.append(q['slug']); q=by.get(q.get('padre')) if q.get('padre') else None
    return '/vender-proindiviso/'+'/'.join(reversed(parts))+'/'
def spec_for(p,by):
    n=nombre_h1(p); en=p['en']; t=p['tipo']; k=h(p['slug'],4)
    H1=[f"Vender proindiviso {en}: compramos tu parte con oferta por escrito en 48 horas",
        f"Compramos tu proindiviso {en}: vender tu parte del piso o la casa sin esperar a los demás",
        f"Vender tu proindiviso {en}: precio en 48 horas y firma en notaría en semanas",
        f"Empresa que compra tu proindiviso {en}: vender tu cuota con precio en 48 horas"][k]
    zonas=p.get('zonas',[])
    z4=', '.join(zonas[:4]) if zonas else n
    SUB=[f"Tienes una parte de un piso, una casa o un terreno {en} y quieres venderla. Pues bien: vender tu proindiviso {en} es posible aunque el resto de copropietarios no esté de acuerdo, porque lo compramos nosotros con fondos propios. {z4} y el resto de la zona: precio por escrito en 48 horas.",
         f"Compramos cuotas indivisas de viviendas, locales, garajes y fincas {en}: {z4} y toda la zona. Así puedes vender tu proindiviso {en} sin intermediarios, sin exclusiva y sin que los demás copropietarios tengan que firmar. Además, la oferta llega en 48 horas y el pago es al contado en notaría.",
         f"Si heredaste una parte, te separaste o tienes un socio que no quiere vender, puedes vender tu proindiviso {en} directamente a nosotros. Precio neto por escrito en 48 horas; además, notaría y gestión corren de nuestra cuenta. Cubrimos {z4} y el resto de la zona.",
         f"Somos compradores, no un portal de contactos. Por eso vender tu proindiviso {en} con nosotros es rápido: pagamos tu parte al contado en notaría, en dos a cuatro semanas desde la oferta. {z4} y toda la zona."][k]
    kicker={'ccaa':f"Compramos en {n}",'provincia':f"Provincia de {p['nombre']}",'ciudad':f"{p['nombre']}"}[t]
    sections=[]
    # 1 por qué / mercado
    T1=[f"Por qué se vende tanto proindiviso {en}",f"Vender un proindiviso {en}: de dónde salen y qué compramos",f"El mercado del proindiviso {en}: por qué se vende",f"Situaciones habituales {en} que acaban en vender el proindiviso"][k]
    sections.append({"overline":"Contexto local","h2":T1,"intro":[rompe_repeticion(p['angulo']),rompe_repeticion(p['mercado'])]})
    # 2 zonas (cards) : qué compramos con nombres de zonas
    tipos=[("Pisos y viviendas",f"Cuotas del 10 % al 90 % de pisos y casas {en}; además, da igual que estén vacíos, alquilados u ocupados por otro copropietario."),("Herencias",f"Partes de inmuebles heredados, con o sin la herencia inscrita; también con usufructo de uno de los padres o con varios herederos."),("Locales, garajes y naves",f"Participaciones de locales comerciales, plazas de garaje, trasteros y naves {en} y alrededores; por ejemplo, la mitad de un local que nadie alquila."),("Terrenos y fincas",f"Cuotas de solares, fincas rústicas y parcelas; en este caso, la referencia catastral es el punto de partida.")]
    T2=[f"Qué compramos {en}",f"Tipos de inmueble que compramos {en}",f"Compramos cuotas de cualquier inmueble {en}",f"Lo que compramos {en}: pisos, herencias, locales y fincas"][k]
    sections.append({"overline":"Qué compramos","h2":T2,"type":"cards","items":[{"t":a,"p":b} for a,b in tipos]})
    # 3 municipios / barrios (list text)
    mun=p.get('municipios',[])
    if mun:
        T3=[f"Municipios donde compramos proindivisos {en}",f"Barrios y zonas de {p['nombre']} donde compramos",f"Dónde compramos {en}: municipios y zonas",f"Cobertura {en}"][k if t!='ciudad' else 1]
        if t=='ciudad': T3=[f"Barrios y zonas de {p['nombre']} donde compramos",f"Cobertura en {p['nombre']}: barrios y distritos",f"Dónde compramos en {p['nombre']}",f"Zonas de {p['nombre']} en las que compramos cuotas"][k]
        txt=', '.join(mun)
        intro=[f"Compramos en todo el territorio {en}. Por ejemplo, estas son las zonas en las que más operaciones cerramos: {txt}." if t!='ciudad' else f"Compramos en cualquier punto de {p['nombre']}. Por ejemplo, las zonas con más operaciones: {txt}.","Si tu municipio o barrio no aparece, compramos igual: el listado es orientativo y, además, se amplía con cada operación." if h(p['slug']+'x',2) else "No importa que tu zona no esté en la lista. En cualquier caso, el precio y el proceso son los mismos en cualquier punto."]
        sections.append({"overline":"Cobertura","h2":T3,"intro":intro})
    # 4 trámites + datos (table)
    T4=[f"Trámites e impuestos para vender tu proindiviso {en}",f"Notaría, Registro e impuestos al vender un proindiviso {en}",f"Qué hay que saber para vender un proindiviso {en}",f"Datos prácticos para vender tu proindiviso {en}"][k]
    rows=[("Dato","Detalle")]
    if p.get('poblacion'): rows.append(("Población",p['poblacion']))
    if p.get('precio_m2'): rows.append(("Precio medio de la vivienda",p['precio_m2']))
    rows.append(("Lo que pagamos por tu cuota","Por lo general, entre el 40 % y el 70 % del valor proporcional de tu parte, según zona, ocupación y cargas. Además, la cifra neta va por escrito en 48 h."))
    rows.append(("Plazo de firma","Por lo general, de 2 a 4 semanas desde la oferta, en una notaría cercana a ti."))
    rows.append(("Gastos para ti","Ninguno. Notaría, gestión e impuestos de la compra los asumimos nosotros; por tanto, tú solo tributas en tu IRPF si hay ganancia."))
    sections.append({"overline":"Trámites","h2":T4,"intro":[rompe_repeticion(p['tramites'])],"type":"table","items":rows,"outro":["En resumen: tú no adelantas nada; nosotros nos ocupamos de la notaría, el Registro y los impuestos de la compra."]})
    # 5 enlaces a hijos / hermanos
    links=[]
    if p['hijos']:
        T5={'ccaa':f"Provincias y ciudades de {n} donde compramos",'provincia':f"Ciudades de la provincia de {p['nombre']} con página propia",'ciudad':""}[t]
        if p['slug'] in ('madrid','murcia','asturias','cantabria','navarra','la-rioja','baleares'): T5=f"Ciudades de {n} con página propia"
        OP=["Además, ","Por ejemplo, ","Por su parte, ","Asimismo, "]  # conectores rotados en los extractos (palabras de transición para Yoast sin repetir inicio de frase)
        for j,q in enumerate(p['hijos']):
            links.append({"t":q['nombre'],"p":conecta(OP[j%4],excerpt(q.get('mercado',''))),"url":url(q,by),"cta":f"Vender en {q['nombre']} →"})
            continue
            links.append({"t":q['nombre'],"p":ex,"url":url(q,by),"cta":f"Vender en {q['nombre']} →"})
        sections.append({"overline":"Por zonas","h2":T5,"intro":[f"Además de {p['nombre'] if t!='ccaa' else 'la capital'}, estas son las zonas con página propia; en cada una explicamos el mercado, los trámites y lo que pagamos."],"type":"cards","items":links})
    elif p.get('padre'):
        par=by[p['padre']]; sib=[q for q in par['hijos'] if q['slug']!=p['slug']][:6]
        items=[{"t":par['nombre'] if par['tipo']!='ccaa' else nombre_h1(par),"p":f"Cobertura completa {par['en']}: municipios, trámites y precios.","url":url(par,by),"cta":"Ver →"}]
        OP=["Además, ","Por ejemplo, ","Por su parte, ","Asimismo, "]
        for j,q in enumerate(sib):
            items.append({"t":q['nombre'],"p":conecta(OP[j%4],excerpt(q.get('angulo',''))),"url":url(q,by),"cta":f"Vender en {q['nombre']} →"})
        sections.append({"overline":"Cerca de ti","h2":f"También compramos cerca de {p['nombre']}","intro":[f"Si tu inmueble no está exactamente en {p['nombre']}, también compramos en los municipios de alrededor; por ejemplo, en estos."],"type":"cards","items":items})
    # 5b guías del blog (solo CCAA y provincias): 3 entradas afines, rotadas por hash para que no se repitan en todas
    if t in ('ccaa','provincia'):
        G=[("Vender tu parte de un piso heredado entre hermanos cuando uno no quiere","Qué pasa con la herencia bloqueada y cómo cobras tu parte sin esperar a nadie.","/vender-proindiviso-entre-hermanos/"),
           ("¿Cuánto me dan por mi parte de un piso?","La fórmula, cuatro ejemplos con cifras y lo que pagamos nosotros.","/blog/cuanto-me-dan-por-mi-parte-de-un-piso/"),
           ("Cuánto tarda vender un proindiviso","Plazos reales paso a paso: de la nota simple a la firma en notaría.","/blog/cuanto-tarda-vender-un-proindiviso/"),
           ("Documentos para vender tu parte de un piso","La lista completa de papeles y dónde conseguir cada uno.","/blog/documentos-para-vender-tu-parte-de-un-piso/"),
           ("Vender un piso heredado: impuestos","Plusvalía, IRPF y sucesiones: qué paga quien vende su cuota heredada.","/blog/vender-un-piso-heredado-impuestos/"),
           ("Qué pasa si uno quiere vender y el otro no","Tus tres salidas cuando el otro copropietario se niega.","/blog/uno-quiere-vender-y-el-otro-no/"),
           ("Vender tu parte de una herencia desde el extranjero","Poderes, firma a distancia y cobro sin viajar a España.","/blog/vender-parte-herencia-desde-el-extranjero/"),
           ("Mi hermano vive en la casa de mis padres y no quiere vender","Qué puedes hacer y cómo compramos tu cuota aunque él siga dentro.","/blog/mi-hermano-vive-en-la-casa-de-mis-padres-y-no-quiere-vender/"),
           ("Nota simple: cómo pedirla y leer tu cuota","Dónde aparece tu porcentaje y qué cargas mirar antes de vender.","/blog/nota-simple-como-pedirla-y-leerla/"),
           ("Vender tu parte de un terreno rústico heredado","Fincas, olivar, viñedo y parcelas: cómo se valora y qué compramos.","/blog/vender-parte-de-un-terreno-rustico-heredado/"),
           ("Piso heredado con hipoteca: vender tu parte","Cómo salir sin asumir la deuda del resto.","/blog/piso-heredado-con-hipoteca-vender-mi-parte/"),
           ("Extinción de condominio o vender tu parte: qué conviene","Comparativa con cifras para decidir en tu caso.","/blog/vender-o-hacer-extincion-de-condominio/")]
        g0=h(p['slug']+'g',len(G)); pick=[G[(g0+j*5)%len(G)] for j in range(3)]
        sections.append({"overline":"Guías","h2":f"Guías para vender tu parte {en}","intro":[f"Antes de pedir precio, estas tres guías resuelven las dudas más habituales de quien vende una cuota {en}."],"type":"cards","items":[{"t":a,"p":b,"url":u,"cta":"Leer la guía →"} for a,b,u in pick]})
    # 6 callout
    sections.append({"type":"callout","items":{"t":[f"Pide precio para vender tu proindiviso {en}",f"Vender tu proindiviso {en} tiene precio hoy",f"Vender tu proindiviso {en} sin esperar a nadie",f"Vender tu proindiviso {en}: precio por escrito en 48 horas"][k],"p":"Dinos la dirección del inmueble, tu porcentaje y cómo llegaste a ser copropietario. Después, te llamamos en menos de 24 horas laborables.","cta":"Pedir oferta ahora"}})
    faqs=[(q,rompe_repeticion(a)) for q,a in p.get('faq',[])]
    rel=[("Cuánto pagamos","/cuanto-pagan-por-un-proindiviso/"),("Tu parte de una herencia","/vender-parte-casa-heredada/"),("Sin avisar a los demás","/vender-proindiviso-sin-avisar/"),("Extinción de condominio","/extincion-de-condominio/"),("Tu parte de un piso","/vender-parte-de-un-piso/"),("Cómo trabajamos","/empresas-que-compran-proindivisos/")]
    rel=rel[k:]+rel[:k]; rel=rel[:4]
    if p.get('padre'): rel.insert(0,(f"Vender proindiviso {by[p['padre']]['en']}",url(by[p['padre']],by)))
    else: rel.insert(0,("Toda España","/vender-proindiviso/"))
    return {"post_id":None,"kicker":kicker,"h1":H1,"sub":SUB,"checks":[f"Compramos {en}","Oferta por escrito en 48 h","Pago al contado en notaría"],
            "card_title":[f"Precio por tu parte {en}",f"Te llamamos y te damos precio",f"Oferta en 48 h, {en}",f"Cuéntanos tu caso {en}"][k],
            "card_text":"Nombre y teléfono. Te llamamos en menos de 24 horas laborables y, además, te decimos cuánto pagamos por tu cuota.",
            "sections":sections,"faqs":faqs,"faq_title":f"Preguntas sobre vender un proindiviso {en}","related":rel,
            "cta_title":[f"Vender tu proindiviso {en} en semanas, no en años",f"Vender tu proindiviso {en} sin esperar al acuerdo de nadie",f"Vender tu proindiviso {en}: precio neto por escrito en 48 horas",f"Compramos tu parte: vender tu proindiviso {en} sin compromiso"][k],
            "cta_text":"Rellena el formulario con la dirección y tu porcentaje. Así, en 48 horas tienes una oferta por escrito, válida 30 días y sin exclusiva.","kw":kw_for(p)}
def kw_for(p):
    # keyphrase exacta tal y como aparece en los textos (con acentos): "vender proindiviso en Cádiz"; Yoast ignora las palabras vacías (en, la, de)
    return f"vender proindiviso en {p['nombre']}"
def meta_for(p,by):
    n=p['nombre']; en=p['en']
    # título SEO: empieza por la keyphrase exacta y cabe en 600 px (≈ 60 caracteres); sin sufijo de marca (va en og:site_name)
    for tail in (": oferta por escrito en 48 h",": oferta en 48 h",": precio en 48 h",""):
        yt=f"Vender proindiviso {en}{tail}"
        if len(yt)<=60: break
    for tail in (" Oferta por escrito en 48 h, firma en notaría y gastos a nuestro cargo."," Oferta por escrito en 48 h y gastos a nuestro cargo."," Oferta en 48 h."):
        yd=f"Vender proindiviso {en}: compramos tu parte de piso, casa o terreno con fondos propios, aunque los demás no quieran.{tail}"
        if len(yd)<=156: break
    return dict(title=h1_corto(p),yt=yt,yd=yd,kw=kw_for(p))
if __name__=='__main__':
    P,by=load_places()
    only=sys.argv[1:]  # slugs opcionales
    ids=ensure_pages(P,by)
    for p in P:
        if only and p['slug'] not in only: continue
        if p['slug'] not in ids: continue
        s=spec_for(p,by); s['post_id']=ids[p['slug']]
        ok=run(s)
        if ok:
            m=meta_for(p,by); meta(ids[p['slug']],status='publish',**m)
