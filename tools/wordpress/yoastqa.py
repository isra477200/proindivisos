"""Puntuación Yoast real (SEO + legibilidad) de cada URL con la librería yoastseo (investigador español), alimentando
el HTML del documento principal de Elementor como hace la integración Yoast↔Elementor. Requiere node + yoastseo en YOAST_DIR.
Uso: python3 yoastqa.py [--sample N] [--urls u1 u2] [--save]  (--save escribe _yoast_wpseo_linkdex/_content_score por REST)"""
import re, sys, json, random, subprocess, os, html as H
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__))
YOAST_DIR=os.environ.get('YOAST_DIR','/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/yoast')
env={}
for l in open(os.path.join(HERE,'wp.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip()
WP=env['WP']; AUTH=env['P1']
def get(u,auth=False):
    a=['curl','-sS','--max-time','60']+(['-u',AUTH] if auth else [])+[u]
    return subprocess.run(a,capture_output=True,text=True).stdout
def main_doc(h):
    ids=[i for i in re.findall(r'data-elementor-id="(\d+)"',h) if i not in ('20','22','684','83','85')]
    if not ids: return None,''
    i=h.find(f'data-elementor-id="{ids[0]}"'); i=h.rfind('<div',0,i)
    # cortar hasta el cierre del div .elementor (siguiente documento o fin de main)
    j=h.find('data-elementor-type=',i+40); j=h.rfind('<div',0,j) if j>0 else h.find('</main>',i)
    return ids[0], h[i:j]
def fetch(u):
    h=get(u+f'?q={random.random()}')
    doc,seg=main_doc(h)
    if not doc: return dict(url=u,err='sin doc')
    seg=re.sub(r'<nav class="zp-toc".*?</nav>','',seg,flags=re.S)  # el índice no lo ve Yoast en el editor (lo inyecta un snippet)
    title=re.search(r'<title>(.*?)</title>',h,re.S); desc=re.search(r'<meta name="description" content="([^"]*)"',h)
    ptype='posts' if re.search(r'<body[^>]*\bsingle-post\b',h) else 'pages'
    m=get(f'{WP}/wp-json/wp/v2/{ptype}/{doc}?context=edit&_fields=id,slug,meta',auth=True)
    try: m=json.loads(m); kw=m['meta'].get('_yoast_wpseo_focuskw',''); slug=m['slug']
    except Exception: kw=''; slug=u.rstrip('/').split('/')[-1]
    return dict(url=u,doc=doc,ptype=ptype,html=seg,keyword=kw,title=H.unescape(title.group(1).strip()) if title else '',description=H.unescape(desc.group(1)) if desc else '',slug=slug,permalink=u)
def analyze(items):
    r=subprocess.run(['node',os.path.join(YOAST_DIR,'analyze.js')],input=json.dumps(items),capture_output=True,text=True,cwd=YOAST_DIR)
    if r.returncode!=0: print(r.stderr[:2000]); sys.exit(1)
    return json.loads(r.stdout)
def save_scores(res,items):
    by={i['url']:i for i in items}
    def one(r):
        it=by[r['url']]
        body={'meta':{'_yoast_wpseo_linkdex':str(r['seoScore']),'_yoast_wpseo_content_score':str(r['readabilityScore'])}}
        out=subprocess.run(['curl','-sS','--max-time','60','-u',AUTH,'-X','POST','-H','Content-Type: application/json',f"{WP}/wp-json/wp/v2/{it['ptype']}/{it['doc']}",'-d',json.dumps(body)],capture_output=True,text=True).stdout
        try: d=json.loads(out); return d['meta'].get('_yoast_wpseo_linkdex')==str(r['seoScore'])
        except Exception: return False
    with ThreadPoolExecutor(6) as ex: ok=list(ex.map(one,res))
    print('guardados',sum(ok),'/',len(ok))
if __name__=='__main__':
    args=sys.argv[1:]
    if '--urls' in args: urls=args[args.index('--urls')+1:]; urls=[u for u in urls if u.startswith('http')]
    else:
        urls=[]
        for sm in ('page','post'): urls+=re.findall(r'<loc>([^<]+)',get(f'https://zonaproindiviso.com/{sm}-sitemap.xml?q={random.random()}'))
        if '--sample' in args: urls=random.sample(urls,int(args[args.index('--sample')+1]))
    with ThreadPoolExecutor(8) as ex: items=[i for i in ex.map(fetch,urls) if 'err' not in i]
    res=[]
    for k in range(0,len(items),25): res+=analyze(items[k:k+25])
    json.dump(res,open(os.path.join(YOAST_DIR,'last_results.json'),'w'),ensure_ascii=False,indent=0)
    def color(s): return 'verde' if s>=71 else ('naranja' if s>=41 else 'rojo')
    from collections import Counter
    print('urls',len(res)); print('SEO',Counter(color(r['seoScore']) for r in res)); print('Legibilidad',Counter(color(r['readabilityScore']) for r in res))
    bad=Counter(); badr=Counter()
    for r in res:
        for a in r['seo']:
            if a['score']<9: bad[(a['id'],a['score'])]+=1
        for a in r['readability']:
            if a['score']<9: badr[(a['id'],a['score'])]+=1
    print('SEO: comprobaciones no verdes (id, puntos) → nº páginas'); [print('  ',k,v) for k,v in bad.most_common()]
    print('Legibilidad: comprobaciones no verdes'); [print('  ',k,v) for k,v in badr.most_common()]
    if '--save' in args: save_scores(res,items)
