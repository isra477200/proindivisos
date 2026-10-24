"""Diccionario del proindiviso (A-Z): páginas hijas de /diccionario-del-proindiviso/ + índice.
Uso: python3 diccionario.py blog/dic_1.json [blog/dic_2.json ...] [--solo slug] [--sin-imagenes] [--solo-indice]
Cada término: imagen MiniMax (manifest_dic.json en el scratchpad) → adjunto → página hija (parent = hub) → composición → metas Yoast → publicada.
Al final (o con --solo-indice) recompone el índice A-Z: una sección por grupo de letras con enlaces a los términos nuevos y a las
páginas/entradas ya existentes que hacen de entrada del diccionario (diccionario_plan.json → «existentes»)."""
import sys, os, json, subprocess, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogbuilder as b
from pagebuilder import run, meta
HERE=os.path.dirname(os.path.abspath(__file__))
IMGDIR=os.environ.get('ZP_IMGDIR','/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/img')
HUB_SLUG='diccionario-del-proindiviso'; HUB_KW='diccionario del proindiviso'
args=sys.argv[1:]; files=[a for a in args if a.endswith('.json')]
solo=args[args.index('--solo')+1] if '--solo' in args else None
PLAN=json.load(open(os.path.join(HERE,'blog','diccionario_plan.json')))
ids=b.load_ids(); IMG_F=os.path.join(HERE,'images.json'); IMG=json.load(open(IMG_F))
def ensure_hub():
    if HUB_SLUG in ids: return ids[HUB_SLUG]
    r=b.api('GET',f"/wp/v2/pages?slug={HUB_SLUG}&status=any&_fields=id")
    if isinstance(r,list) and r: pid=r[0]['id']
    else:
        out=subprocess.run(['./emcp.sh','elementor-create-page',json.dumps({'title':'Diccionario del proindiviso','post_type':'page'})],capture_output=True,text=True).stdout
        m=re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out); pid=int(m.group(1))
        b.api('POST',f'/wp/v2/pages/{pid}',{'title':'Diccionario del proindiviso','slug':HUB_SLUG,'status':'draft'})
    ids[HUB_SLUG]=pid; json.dump(ids,open(b.IDS_FILE,'w'),ensure_ascii=False,indent=0); return pid
def norm(t): return unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
def defin(s):
    sub=re.sub(r'<[^>]+>','',s['sub']); first=re.split(r'(?<=[.!?])\s+',sub)[0]
    return first if len(first)<220 else first[:200].rsplit(' ',1)[0]+'…'
hub=ensure_hub(); print('hub',hub)
S=[]
for f in files: S+=json.load(open(f if os.path.isabs(f) else os.path.join(HERE,f)))
if solo: S=[s for s in S if s['slug']==solo]
if '--solo-indice' not in args:
    print(len(S),'términos')
    MF=os.path.join(IMGDIR,'manifest_dic.json'); MAP_F=os.path.join(IMGDIR,'media_map_dic.json')
    if '--sin-imagenes' not in args:
        man=json.load(open(MF)) if os.path.exists(MF) else []; have={m['key'] for m in man}
        for s in S:
            if s['slug'] in have: continue
            man.append({'key':s['slug'],'kind':'page','post_id':0,'filename':('diccionario-'+s['slug'][:60])+'.webp','title':s['h1'][:120],'alt':s['imagen_alt'],'prompt':s['imagen_prompt']})
        json.dump(man,open(MF,'w'),ensure_ascii=False,indent=1)
        keys=[s['slug'] for s in S]
        r=subprocess.run(['python3','gen.py']+keys,cwd=IMGDIR,env={**os.environ,'MANIFEST':'manifest_dic.json'},capture_output=True,text=True); print(r.stdout[-300:])
        r=subprocess.run(['python3','upload.py']+keys,cwd=IMGDIR,env={**os.environ,'MANIFEST':'manifest_dic.json'},capture_output=True,text=True); print(r.stdout[-300:])
    mm=json.load(open(MAP_F)) if os.path.exists(MAP_F) else {}
    hechos=[]
    for s in S:
        pid=b.ensure(s,ids)
        if not pid: print('SIN ID',s['slug']); continue
        b.api('POST',f'/wp/v2/pages/{pid}',{'parent':hub,'excerpt':defin(s)})  # extracto = definición (schema DefinedTerm, snippet 175)
        mid=mm.get(s['slug'],{}).get('media_id')
        if mid:
            IMG[str(pid)]=mid; json.dump(IMG,open(IMG_F,'w'),indent=0); b.api('POST',f'/wp/v2/pages/{pid}',{'featured_media':mid})
        else: print('  sin imagen',s['slug'])
        sp=b.normalize(s); sp['post_id']=pid; sp['dated']=False
        ok=run(sp)
        if ok: meta(pid,title=s['title_corto'],yt=s['yoast_title'].strip(),yd=s['meta_desc'],kw=s['focus_kw'],status='publish',parent=hub,ptype='pages',bctitle=s['title_corto'])
        print(pid,s['slug'],'OK' if ok else 'FAIL',flush=True)
        if ok: hechos.append(s)
    if hechos:
        urls=[f"https://zonaproindiviso.com/{HUB_SLUG}/{s['slug']}/" for s in hechos]
        r=subprocess.run(['python3','yoastqa.py','--urls']+urls+['--save'],cwd=HERE,capture_output=True,text=True); print(r.stdout[-1200:])
# ---- índice A-Z ----
entradas=[]
allspecs=[]
for f in sorted(os.listdir(os.path.join(HERE,'blog'))):
    if re.match(r'dic_\d+\.json$',f): allspecs+=json.load(open(os.path.join(HERE,'blog',f)))
for s in allspecs:
    if s['slug'] in ids or b.api('GET',f"/wp/v2/pages?slug={s['slug']}&status=publish&_fields=id"):
        entradas.append((s['title_corto'],f'/{HUB_SLUG}/{s["slug"]}/',defin(s)))
DEF_EX={'Beneficio de inventario':'Aceptar la herencia respondiendo de las deudas solo con lo heredado.','Comunidad de bienes':'Nombre legal del proindiviso en el Código Civil (arts. 392 a 406).','Comunidad hereditaria':'La situación de los herederos antes de repartir la herencia.','Cuaderno particional':'Documento que reparte la herencia bien por bien y heredero por heredero.','Contador partidor':'Persona que reparte la herencia cuando los herederos no se ponen de acuerdo.','Cuota hereditaria':'La parte de la herencia que corresponde a cada heredero.','División de cosa común':'El juicio para salir de un proindiviso cuando no hay acuerdo; suele acabar en subasta.','Desahucio por precario':'Procedimiento para recuperar la casa que ocupa alguien sin título ni renta.','Donación de la cuota':'Regalar tu parte a otra persona: impuestos y límites.','Embargo de la cuota':'Un acreedor puede embargar y subastar la parte de un copropietario.','Extinción de condominio':'Uno se queda el inmueble y compensa a los demás; tributa por AJD.','Exceso de adjudicación':'Lo que recibe de más un comunero al repartir; tributa si no está justificado.','Escisión y cesación de condominio':'Otros nombres que se usan para la extinción de condominio.','Herencia yacente':'La herencia aún no aceptada ni repartida.','IBI y gastos':'Quién paga los impuestos y gastos de una casa compartida.','ITP':'Impuesto de Transmisiones Patrimoniales: lo paga quien compra una cuota.','IRPF (ganancia patrimonial)':'Lo que tributa el vendedor si gana dinero al vender su parte.','Multipropiedad':'Derecho a usar un inmueble por turnos; no es un proindiviso.','Nota simple':'Documento del Registro que dice quién es dueño y qué cargas hay.','Nuda propiedad':'Ser dueño sin poder usar el bien mientras dura el usufructo.','Okupa':'Ocupante sin título: cómo afecta a la venta de una cuota.','Proindiviso':'Propiedad de varios dueños sin dividir: la base de todo este diccionario.','Pacto de indivisión':'Acuerdo para no dividir durante un plazo (máximo diez años).','Prescripción del impuesto de sucesiones':'A los cuatro años y medio Hacienda ya no puede exigirlo.','Retracto de comuneros':'Derecho de los copropietarios a quedarse con la cuota vendida a un tercero (art. 1522 CC).','Retracto de coherederos':'Lo mismo entre herederos antes de la partición (art. 1067 CC).','Renuncia a la herencia':'Rechazar la herencia ante notario; alternativa a vender la parte.','Subasta judicial':'La venta forzosa del inmueble tras la división de cosa común.','Tanteo':'Derecho a comprar la cuota antes que un tercero, al mismo precio.','Uso exclusivo (compensación)':'Quien usa solo la casa común puede deber una compensación a los demás.','Valor de referencia':'Valor que fija Catastro y que Hacienda usa como mínimo en ITP y sucesiones.','VPO':'Vivienda protegida: límites de precio y permisos al vender una parte.'}
for e in PLAN['existentes']: entradas.append((e['termino'],e['url'],DEF_EX.get(e['termino'],'')))
entradas.sort(key=lambda x: norm(x[0]))
grupos=[('A','A'),('B-C','BC'),('D-E','DE'),('F-H','FGH'),('I-L','IJKL'),('M-N','MN'),('O-P','OP'),('R-S','QRS'),('T-U','TU'),('V-Z','VWXYZ')]
secs=[]
for i,(nombre,letras) in enumerate(grupos):
    items=[f'<strong><a href="{u}">{t}</a></strong>: {d}' for t,u,d in entradas if norm(t)[0].upper() in letras]
    if not items: continue
    secs.append({'overline':f'Letra {nombre}','h2':(f'Términos del proindiviso de la {nombre}' if i%2==0 else f'Diccionario del proindiviso: {nombre}'),'type':'list','items':items})
secs.insert(0,{'overline':'Cómo usarlo','h2':'Qué encontrarás en este diccionario del proindiviso','intro':['Cada término tiene su propia página con la definición, el artículo del Código Civil o la norma que lo regula, un ejemplo con cifras y lo que significa para quien quiere vender su parte. Están ordenados de la A a la Z; pulsa en cualquiera para abrirlo.','Si lo que buscas es una cifra, prueba la <a href="/cuanto-vale-mi-parte-de-un-piso/">calculadora de cuánto vale tu parte</a> o el <a href="/simulador-extincion-de-condominio/">simulador de gastos de extinción de condominio</a>.']})
secs.append({'overline':'Tu caso','h2':'Si prefieres hablar en lugar de leer','intro':['Un diccionario del proindiviso explica las palabras; tu caso lo resuelve una oferta. Cuéntanos qué inmueble es, qué parte tienes y cómo está, y en 48 horas te decimos por escrito cuánto pagamos por tu cuota.'],'type':'callout','items':{'t':'¿Quieres salir del proindiviso sin aprender todas estas palabras?','p':'Compramos tu parte con fondos propios, firma en notaría y gastos a nuestro cargo. Sin compromiso.','cta':'Pedir mi oferta'}})
hubspec={'post_id':hub,'kw':HUB_KW,'kicker':'Diccionario','h1':'Diccionario del proindiviso: todos los términos de la A a la Z','sub':'Este diccionario del proindiviso reúne, de la A a la Z, las palabras que aparecen cuando varias personas comparten un piso, una casa o una herencia: desde actio communi dividundo hasta vivienda habitual. Cada término explicado en claro, con su base legal y con lo que implica si quieres vender tu parte.','checks':[f'{len(entradas)} términos explicados','Con artículos del Código Civil','Actualizado por quienes compramos cuotas'],'card_title':'¿Una palabra no te cuadra con tu caso?','card_text':'Déjanos tu teléfono y te lo explicamos sobre tu situación concreta, con una oferta por tu parte si la quieres.','sections':secs,'faqs':[('¿Qué es un proindiviso en pocas palabras?','Es una propiedad con varios dueños y sin dividir: cada uno tiene un porcentaje (una cuota) sobre todo el inmueble, no una habitación concreta. El Código Civil lo llama comunidad de bienes y lo regula en los artículos 392 a 406.'),('¿Cuál es la diferencia entre proindiviso, condominio y comunidad de bienes?','En la práctica son lo mismo: proindiviso describe la situación (sin dividir), condominio el hecho de ser varios dueños y comunidad de bienes es el nombre que usa la ley. Cada término tiene su entrada en este diccionario del proindiviso con los matices.'),('¿Puedo vender mi parte sin el permiso de los demás?','Sí. El artículo 399 del Código Civil permite a cada copropietario vender, ceder o hipotecar su cuota sin consentimiento de los otros. Los demás solo tienen derecho de retracto: quedarse tu parte al mismo precio en el plazo legal.'),('¿Qué términos debo mirar si he heredado una casa con mis hermanos?','Empieza por herencia yacente, aceptación de la herencia, impuesto de sucesiones, partición, cuaderno particional y retracto de coherederos. Si uno no quiere vender, sigue por división de cosa común y venta de cuota indivisa.'),('¿Cada cuánto se actualiza el diccionario del proindiviso?','Añadimos términos cuando aparecen en los casos que compramos o cuando cambia la norma o el criterio de Hacienda. Las entradas llevan ejemplos con cifras redondas que se revisan al menos una vez al año.')],'faq_title':'Preguntas sobre el diccionario del proindiviso','related':[('Qué es un proindiviso','/que-es-un-proindiviso/'),('Guía de extinción de condominio','/extincion-de-condominio/'),('División de cosa común','/division-de-cosa-comun/'),('Cuánto vale mi parte','/cuanto-vale-mi-parte-de-un-piso/'),('Blog','/blog/')],'cta_title':'Diccionario del proindiviso leído: ahora, una oferta por tu parte','cta_text':'Rellena el formulario y te llamamos en menos de 24 horas laborables con una cifra en firme. Si lo prefieres, llámanos o escríbenos.','dated':True}
b_norm=b.normalize(dict(hubspec,kind='page',sections=hubspec['sections'],related=hubspec['related'],faqs=hubspec['faqs']))
b_norm['post_id']=hub; b_norm['dated']=True
ok=run(b_norm); print('hub',hub,'OK' if ok else 'FAIL', len(entradas),'términos en el índice')
if ok: meta(hub,title='Diccionario del proindiviso',yt='Diccionario del proindiviso: términos de la A a la Z',yd=f'Diccionario del proindiviso con {len(entradas)} términos explicados de la A a la Z: cuota indivisa, extinción de condominio, retracto, usufructo, AJD... Con base legal y ejemplos.',kw=HUB_KW,status='publish',ptype='pages',slug=HUB_SLUG)
