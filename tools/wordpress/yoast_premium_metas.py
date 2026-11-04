"""Yoast Premium por REST: sinónimos de la keyphrase (_yoast_wpseo_keywordsynonyms, JSON ["a, b, c"]) y keyphrases
relacionadas (_yoast_wpseo_focuskeywords, JSON [{"keyword":"...","score":""}]) en geo, intención y entradas.
Requiere el snippet 95 (expone ambos metas). Uso: python3 yoast_premium_metas.py [geo|intencion|blog] [--dry]"""
import sys, os, json, glob, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import intencion_kw as I
env=dict(l.strip().split('=',1) for l in open(os.path.join(HERE,'wp.env')) if '=' in l)
WP=env['WP']; AUTH=env['P1']
def post(ptype,pid,syn,rel):
    body={'meta':{'_yoast_wpseo_keywordsynonyms':json.dumps([syn],ensure_ascii=False,separators=(',',':')),'_yoast_wpseo_focuskeywords':json.dumps([{'keyword':r,'score':''} for r in rel],ensure_ascii=False,separators=(',',':'))}}
    out=subprocess.run(['curl','-sS','--max-time','90','-u',AUTH,'-X','POST','-H','Content-Type: application/json',f'{WP}/wp-json/wp/v2/{ptype}/{pid}','-d',json.dumps(body,ensure_ascii=False)],capture_output=True,text=True).stdout
    try: d=json.loads(out); return d['meta'].get('_yoast_wpseo_keywordsynonyms')==body['meta']['_yoast_wpseo_keywordsynonyms']
    except Exception: return False
def jobs_geo():
    P=[]
    for f in sorted(glob.glob(os.path.join(HERE,'geo','geo_[A-F].json'))): P+=json.load(open(f))
    ids=json.load(open(os.path.join(HERE,'geo','ids.json')))
    for p in P:
        en=p['en']; n=p['nombre']
        syn=f"vender mi parte de un piso {en}, vender cuota indivisa {en}, compramos proindiviso {en}"
        rel=[f"empresas que compran proindivisos {en}", f"precio proindiviso {n}"]
        yield ('pages',ids[p['slug']],syn,rel)
INT={
23:("vender mi parte de un piso, vender cuota indivisa, compramos proindivisos",["empresas que compran proindivisos","vender parte de una casa"]),
25:("compradores de proindivisos, empresas que compran partes de pisos, inversores en proindiviso",["vender proindiviso","opiniones empresas que compran proindivisos"]),
27:("precio de un proindiviso, cuánto vale mi parte de un piso, cuánto dan por un proindiviso",["cuánto me dan por mi parte de un piso","vender proindiviso"]),
29:("vender mi parte sin el consentimiento de los demás, vender cuota sin avisar a los copropietarios",["vender proindiviso","derecho de tanteo y retracto"]),
31:("vender mi parte de la herencia, vender parte de un piso heredado, vender cuota hereditaria",["vender derechos hereditarios","vender piso heredado entre hermanos"]),
33:("reseñas de empresas que compran proindivisos, experiencias vendiendo un proindiviso",["empresas que compran proindivisos","cuánto pagan por un proindiviso"]),
35:("vender mi parte de un piso, vender la mitad de un piso, vender cuota de un piso",["vender proindiviso","vender la mitad de una casa"]),
37:("vender mi parte de un piso con hipoteca, vender cuota hipotecada",["hipoteca para extinción de condominio","vender proindiviso"]),
39:("vender mi parte del piso tras el divorcio, vender la casa común tras separarse",["extinción de condominio por divorcio","vender proindiviso"]),
41:("vender mi parte de un piso heredado a mis hermanos, herencia entre hermanos vender",["un heredero no quiere vender","vender parte de una casa heredada"]),
43:("disolución de condominio, extinción de proindiviso, división de la cosa común",["extinción de condominio entre hermanos","escritura de extinción de condominio"]),
45:("disolución de condominio entre hermanos, extinción de proindiviso entre hermanos",["extinción de condominio","vender piso heredado entre hermanos"]),
47:("extinción de condominio con préstamo hipotecario, disolución de condominio hipoteca",["hipoteca para extinción de condominio","vender proindiviso con hipoteca"]),
49:("impuestos de la extinción de condominio, notario extinción de condominio, AJD extinción de condominio",["cuánto cobra el notario extinción de condominio","extinción de condominio"]),
51:("qué es el proindiviso, proindiviso significado, copropiedad de un inmueble",["proindiviso código civil","vender proindiviso"]),
53:("división de la cosa común, acción de división, subasta por división de cosa común",["se puede obligar a vender a un copropietario","extinción de condominio"]),
55:("compramos proindivisos en toda España, vender mi parte de un piso en cualquier provincia",["empresas que compran proindivisos","vender proindiviso"]),
57:("pedir precio por mi proindiviso, oferta por mi parte de un piso",["cuánto pagan por un proindiviso","vender proindiviso"]),
680:("guías sobre proindivisos, artículos sobre vender tu parte de un piso",["qué es un proindiviso","vender proindiviso"]),
}
def jobs_intencion():
    for pid,(syn,rel) in INT.items(): yield ('pages',pid,syn,rel)
def jobs_blog():
    ids=json.load(open(os.path.join(HERE,'blog','ids.json')))
    S=[]
    for f in sorted(glob.glob(os.path.join(HERE,'blog','blog_[0-9].json'))): S+=json.load(open(f))
    for s in S:
        kw=s['focus_kw'].lower(); t=s['title_corto'].lower().strip(' .¿?¡!')
        rel=[t] if t!=kw and 2<=len(t.split())<=8 else []
        syn=s.get('synonyms','')
        if not (syn or rel): continue
        yield ('posts' if s['kind']=='post' else 'pages',ids[s['slug']],syn,rel)
if __name__=='__main__':
    which=[a for a in sys.argv[1:] if not a.startswith('--')] or ['geo','intencion','blog']
    J=[]
    for w in which: J+=list({'geo':jobs_geo,'intencion':jobs_intencion,'blog':jobs_blog}[w]())
    if '--dry' in sys.argv:
        for j in J[:5]: print(j)
        print(len(J),'páginas'); sys.exit()
    with ThreadPoolExecutor(6) as ex: ok=list(ex.map(lambda j: post(*j),J))
    print('ok',sum(ok),'/',len(ok))
