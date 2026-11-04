"""QA SEO de todas las URL del sitemap: 200, og:image propia (no la de fachada por defecto), imagen en el contenido (banda Figura),
alt no vacío, TOC en entradas, fecha visible, FAQPage, coherencia HTML/CSS (como cssqa). Uso: python3 seoqa.py [--sample N]"""
import re, sys, json, random, subprocess
from concurrent.futures import ThreadPoolExecutor
DEFAULT='vender-proindiviso-fachada-edificio-espana.webp'
def get(u): return subprocess.run(['curl','-sS','--max-time','60',u],capture_output=True,text=True).stdout
urls=[]
for sm in ('page','post'):
    urls+=re.findall(r'<loc>([^<]+)',get(f'https://zonaproindiviso.com/{sm}-sitemap.xml?q={random.random()}'))
if '--sample' in sys.argv: urls=random.sample(urls,int(sys.argv[sys.argv.index('--sample')+1]))
def check(u):
    h=get(u+f'?q={random.random()}')
    if not h: return dict(u=u,err='sin respuesta')
    ids=[i for i in re.findall(r'data-elementor-id="(\d+)"',h) if i not in ('20','22','684','83','85')]
    r=dict(u=u)
    r['doc']=ids[0] if ids else None
    og=re.search(r'property="og:image" content="([^"]+)"',h); r['og']=og.group(1).split('/')[-1] if og else ''
    r['og_default']=r['og'].endswith(DEFAULT) or r['og']==''
    r['figura']=bool(re.search(r'<img[^>]+class="[^"]*e-image-base[^"]*"[^>]+uploads/2026/10/(?!zona-proindiviso-marca)[^"]+\.webp',h))
    r['alt_vacio']=len(re.findall(r'<img[^>]+alt=""',h))
    r['toc']='class="zp-toc"' in h
    r['fecha']='Actualizado el ' in h
    r['faq']=h.count('FAQPage')
    r['h1']=len(re.findall(r'<h1',h))
    r['noindex']='noindex' in h
    if r['doc']:
        i=h.find(f'data-elementor-id="{r["doc"]}"'); seg=h[i:]; j=seg.find('data-elementor-id="',30); seg=seg[:j] if j>0 else seg
        cls=set(re.findall(r'\be-([0-9a-f]{5,8}-[0-9a-f]{4})\b',seg))
        c=get(f'https://zonaproindiviso.com/wp-content/uploads/elementor/css/local-{r["doc"]}-frontend-desktop.css?x={random.random()}')
        hit=sum(1 for x in cls if f'e-{x}' in c); r['css']=f'{hit}/{len(cls)}'; r['css_ok']=bool(cls) and hit*100//len(cls)>=60
    else: r['css_ok']=False; r['css']='sin doc'
    return r
with ThreadPoolExecutor(8) as ex: R=list(ex.map(check,urls))
is_post=lambda u:'/blog/' in u and u.rstrip('/')!='https://zonaproindiviso.com/blog'
print('urls',len(R))
print('css mal:',[(r['u'],r['css']) for r in R if not r.get('css_ok')])
print('og por defecto:',[r['u'] for r in R if r.get('og_default') and r['u']!='https://zonaproindiviso.com/'])
print('sin figura:',[r['u'] for r in R if not r.get('figura') and r['u']!='https://zonaproindiviso.com/'])
print('alt vacío:',[(r['u'],r['alt_vacio']) for r in R if r.get('alt_vacio')])
print('posts sin TOC:',[r['u'] for r in R if is_post(r['u']) and not r.get('toc')])
print('posts sin fecha:',[r['u'] for r in R if is_post(r['u']) and not r.get('fecha')])
print('sin FAQPage (no legales/contacto/gracias/blog):',[r['u'] for r in R if not r.get('faq') and not re.search(r'/(aviso-legal|politica-de-privacidad|politica-de-cookies|contacto|gracias|blog)/$',r['u'])])
print('h1 != 1:',[(r['u'],r['h1']) for r in R if r.get('h1')!=1])
print('noindex:',[r['u'] for r in R if r.get('noindex')])
json.dump(R,open('/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/seoqa.json','w'),ensure_ascii=False,indent=0)
