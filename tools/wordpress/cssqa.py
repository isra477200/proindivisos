import re, sys, json, random, subprocess
from concurrent.futures import ThreadPoolExecutor
def get(u):
    return subprocess.run(['curl','-sS','--max-time','60',u],capture_output=True,text=True).stdout
urls=[]
for sm in ('page','post'):
    urls+=re.findall(r'<loc>([^<]+)',get(f'https://zonaproindiviso.com/{sm}-sitemap.xml?q={random.random()}'))
def check(u):
    h=get(u); ids=[i for i in re.findall(r'data-elementor-id="(\d+)"',h) if i not in ('20','22','684')]
    if not ids: return ('SIN ELEMENTOR',u,0,0,'')
    id=ids[0]; i=h.find(f'data-elementor-id="{id}"'); seg=h[i:]; j=seg.find('data-elementor-id="',30); seg=seg[:j] if j>0 else seg
    cls=set(re.findall(r'\be-([0-9a-f]{5,8}-[0-9a-f]{4})\b',seg))
    c=get(f'https://zonaproindiviso.com/wp-content/uploads/elementor/css/local-{id}-frontend-desktop.css?x={random.random()}')
    hit=sum(1 for x in cls if f'e-{x}' in c)
    faq=h.count('FAQPage'); det=h.count('<details')
    return ('OK' if cls and hit*100//len(cls)>=60 else 'MISMATCH',u,len(cls),hit,f'faq={faq} details={det} doc={id}')
with ThreadPoolExecutor(8) as ex: res=list(ex.map(check,urls))
bad=[r for r in res if r[0]!='OK']
print('urls',len(urls),'problemas',len(bad))
for r in bad: print(*r)
