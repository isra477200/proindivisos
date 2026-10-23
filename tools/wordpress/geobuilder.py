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
    for f in sorted(glob.glob(os.path.join(HERE,'geo','geo_[A-D].json'))): P+=json.load(open(f))
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
        f"Compramos proindivisos {en}: vende tu parte del piso o la casa sin esperar a los demás",
        f"Vender tu proindiviso {en}: precio en 48 horas y firma en notaría en semanas",
        f"Empresa que compra proindivisos {en}: te damos precio por tu cuota en 48 horas"][k]
    zonas=p.get('zonas',[])
    z4=', '.join(zonas[:4]) if zonas else n
    SUB=[f"Tienes una parte de un piso, una casa o un terreno {en} y quieres venderla. La compramos nosotros, con fondos propios, aunque el resto de copropietarios no esté de acuerdo. {z4} y el resto de la zona: precio por escrito en 48 horas.",
         f"Compramos cuotas indivisas de viviendas, locales, garajes y fincas {en}: {z4} y toda la zona. Sin intermediarios, sin exclusiva y sin que los demás copropietarios tengan que firmar. Oferta en 48 horas y pago al contado en notaría.",
         f"Si heredaste una parte, te separaste o tienes un socio que no quiere vender, {en} compramos tu cuota directamente. Precio neto por escrito en 48 horas, notaría y gestión a nuestro cargo. Cubrimos {z4} y el resto de la zona.",
         f"Somos compradores, no un portal de contactos. Pagamos tu parte del inmueble {en} al contado en notaría, en dos a cuatro semanas desde la oferta. {z4} y toda la zona."][k]
    kicker={'ccaa':f"Compramos en {n}",'provincia':f"Provincia de {p['nombre']}",'ciudad':f"{p['nombre']}"}[t]
    sections=[]
    # 1 por qué / mercado
    T1=[f"Por qué hay tantos proindivisos {en}",f"Proindivisos {en}: de dónde salen y qué compramos",f"El mercado de las cuotas indivisas {en}",f"Situaciones habituales {en} que acaban en proindiviso"][k]
    sections.append({"overline":"Contexto local","h2":T1,"intro":[p['angulo'],p['mercado']]})
    # 2 zonas (cards) : qué compramos con nombres de zonas
    tipos=[("Pisos y viviendas",f"Cuotas del 10 % al 90 % de pisos y casas {en}, vacíos, alquilados u ocupados por otro copropietario."),("Herencias",f"Partes de inmuebles heredados, con o sin la herencia inscrita, con usufructo de uno de los padres o con varios herederos."),("Locales, garajes y naves",f"Participaciones de locales comerciales, plazas de garaje, trasteros y naves {en} y alrededores."),("Terrenos y fincas",f"Cuotas de solares, fincas rústicas y parcelas, con la referencia catastral como punto de partida.")]
    T2=[f"Qué compramos {en}",f"Tipos de inmueble que compramos {en}",f"Compramos cuotas de cualquier inmueble {en}",f"Lo que compramos {en}: pisos, herencias, locales y fincas"][k]
    sections.append({"overline":"Qué compramos","h2":T2,"type":"cards","items":[{"t":a,"p":b} for a,b in tipos]})
    # 3 municipios / barrios (list text)
    mun=p.get('municipios',[])
    if mun:
        T3=[f"Municipios donde compramos proindivisos {en}",f"Barrios y zonas de {p['nombre']} donde compramos",f"Dónde compramos {en}: municipios y zonas",f"Cobertura {en}"][k if t!='ciudad' else 1]
        if t=='ciudad': T3=[f"Barrios y zonas de {p['nombre']} donde compramos",f"Cobertura en {p['nombre']}: barrios y distritos",f"Dónde compramos en {p['nombre']}",f"Zonas de {p['nombre']} en las que compramos cuotas"][k]
        txt=', '.join(mun)
        intro=[f"Compramos en todo el territorio {en}. Estas son las zonas en las que más operaciones cerramos: {txt}." if t!='ciudad' else f"Compramos en cualquier punto de {p['nombre']}. Las zonas con más operaciones: {txt}.","Si tu municipio o barrio no aparece, compramos igual: el listado es orientativo y se amplía con cada operación." if h(p['slug']+'x',2) else "No importa que tu zona no esté en la lista. El precio y el proceso son los mismos en cualquier punto."]
        sections.append({"overline":"Cobertura","h2":T3,"intro":intro})
    # 4 trámites + datos (table)
    T4=[f"Trámites, impuestos y datos útiles {en}",f"Notaría, Registro e impuestos {en}",f"Qué hay que saber de los trámites {en}",f"Datos prácticos para vender tu cuota {en}"][k]
    rows=[("Dato","Detalle")]
    if p.get('poblacion'): rows.append(("Población",p['poblacion']))
    if p.get('precio_m2'): rows.append(("Precio medio de la vivienda",p['precio_m2']))
    rows.append(("Lo que pagamos por tu cuota","Entre el 40 % y el 70 % del valor proporcional de tu parte, según zona, ocupación y cargas. Cifra neta por escrito en 48 h."))
    rows.append(("Plazo de firma","De 2 a 4 semanas desde la oferta, en una notaría cercana a ti."))
    rows.append(("Gastos para ti","Ninguno. Notaría, gestión e impuestos de la compra los asumimos nosotros. Tú solo tributas en tu IRPF si hay ganancia."))
    sections.append({"overline":"Trámites","h2":T4,"intro":[p['tramites']],"type":"table","items":rows})
    # 5 enlaces a hijos / hermanos
    links=[]
    if p['hijos']:
        T5={'ccaa':f"Provincias y ciudades de {n} donde compramos",'provincia':f"Ciudades de la provincia de {p['nombre']} con página propia",'ciudad':""}[t]
        if p['slug'] in ('madrid','murcia','asturias','cantabria','navarra','la-rioja','baleares'): T5=f"Ciudades de {n} con página propia"
        for q in p['hijos']: links.append({"t":q['nombre'],"p":excerpt(q.get('mercado','')),"url":url(q,by),"cta":f"Vender en {q['nombre']} →"})
        sections.append({"overline":"Por zonas","h2":T5,"type":"cards","items":links})
    elif p.get('padre'):
        par=by[p['padre']]; sib=[q for q in par['hijos'] if q['slug']!=p['slug']][:6]
        items=[{"t":par['nombre'] if par['tipo']!='ccaa' else nombre_h1(par),"p":f"Cobertura completa {par['en']}: municipios, trámites y precios.","url":url(par,by),"cta":"Ver →"}]
        items+=[{"t":q['nombre'],"p":excerpt(q.get('angulo','')),"url":url(q,by),"cta":f"Vender en {q['nombre']} →"} for q in sib]
        sections.append({"overline":"Cerca de ti","h2":f"También compramos cerca de {p['nombre']}","type":"cards","items":items})
    # 6 callout
    sections.append({"type":"callout","items":{"t":[f"Pide precio por tu parte {en}",f"Tu cuota {en} tiene precio hoy",f"Vende tu proindiviso {en} sin esperar a nadie",f"Precio por escrito en 48 horas, {en} y en toda la provincia"][k],"p":"Dinos la dirección del inmueble, tu porcentaje y cómo llegaste a ser copropietario. Te llamamos en menos de 24 horas laborables.","cta":"Pedir oferta ahora"}})
    faqs=[tuple(x) for x in p.get('faq',[])]
    rel=[("Cuánto pagamos","/cuanto-pagan-por-un-proindiviso/"),("Vender tu parte de una herencia","/vender-parte-casa-heredada/"),("Vender sin avisar a los demás","/vender-proindiviso-sin-avisar/"),("Extinción de condominio","/extincion-de-condominio/"),("Vender tu parte de un piso","/vender-parte-de-un-piso/"),("Cómo trabajamos","/empresas-que-compran-proindivisos/")]
    rel=rel[k:]+rel[:k]; rel=rel[:4]
    if p.get('padre'): rel.insert(0,(f"Vender proindiviso {by[p['padre']]['en']}",url(by[p['padre']],by)))
    else: rel.insert(0,("Toda España","/vender-proindiviso/"))
    return {"post_id":None,"kicker":kicker,"h1":H1,"sub":SUB,"checks":[f"Compramos {en}","Oferta por escrito en 48 h","Pago al contado en notaría"],
            "card_title":[f"Precio por tu parte {en}",f"Te llamamos y te damos precio",f"Oferta en 48 h, {en}",f"Cuéntanos tu caso {en}"][k],
            "card_text":"Nombre y teléfono. Te llamamos en menos de 24 horas laborables y te decimos cuánto pagamos por tu cuota.",
            "sections":sections,"faqs":faqs,"faq_title":f"Preguntas sobre vender un proindiviso {en}","related":rel,
            "cta_title":[f"Vende tu proindiviso {en} en semanas, no en años",f"Cobra por tu parte {en} sin esperar al acuerdo de nadie",f"Tu cuota {en}: precio neto por escrito en 48 horas",f"Compramos tu parte {en}: pide precio sin compromiso"][k],
            "cta_text":"Rellena el formulario con la dirección y tu porcentaje. En 48 horas tienes una oferta por escrito, válida 30 días, sin exclusiva."}
def meta_for(p,by):
    n=p['nombre']; en=p['en']; k=h(p['slug'],3)
    yt=[f"Vender proindiviso {en}: oferta en 48 h · Zona Proindiviso",f"Compramos proindivisos {en} · precio en 48 h · Zona Proindiviso",f"Vender tu parte de un piso {en} · Zona Proindiviso"][k]
    m1=p['mercado'].split('. ')[0]
    yd=(f"Compramos tu parte de piso, casa o terreno {en} con fondos propios. {m1}. Oferta por escrito en 48 h, firma en notaría y gastos a nuestro cargo.")
    if len(yd)>158: yd=f"Compramos tu parte de piso, casa o terreno {en} con fondos propios, aunque los demás no quieran vender. Oferta por escrito en 48 h y gastos a nuestro cargo."
    kw=f"vender proindiviso {en}".replace(' la provincia de ',' ').replace(' el ',' ').replace(' la ',' ')
    return dict(title=h1_corto(p),yt=yt,yd=yd,kw=kw.lower())
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
