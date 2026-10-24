"""Pre-análisis Yoast de specs (sin publicar): aproxima el HTML que generará pagebuilder (H1, sub, H2 por sección, H3 de tarjetas y
de FAQ según las mismas reglas, CTA) y lo pasa por el motor yoastseo del scratchpad (analyze.js). Imprime las comprobaciones no verdes.
Uso: python3 yoastpre.py blog/blog_11.json [--solo slug]"""
import sys, os, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import _has_kw, _topic, _plan_subtitulos, _break_runs
YOAST_DIR=os.environ.get('YOAST_DIR','/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/yoast')
def _w(x): return len(re.findall(r"\w+",re.sub(r"<[^>]+>"," ",str(x))))
def html_of(s):
    kw=s['focus_kw']; h=[f"<h1>{s['h1']}</h1><p>{s['sub']}</p>"]
    pc,pf=_plan_subtitulos(s,kw)
    for si,sec in enumerate(s['sections']):
        t=sec.get('type','text')
        if sec.get('overline'): h.append(f"<p>{sec['overline']}</p>")
        if sec.get('h2'): h.append(f"<h2>{sec['h2']}</h2>")
        for p in (sec.get('intro',[]) if isinstance(sec.get('intro'),list) else [sec.get('intro','')]):
            if p: h.append(f"<p>{p}</p>")
        it=sec.get('items',[])
        if t in ('cards','steps'):
            secw=sum(_w(x) for x in (sec.get('intro',[]) if isinstance(sec.get('intro'),list) else [sec.get('intro','')]))+sum(_w(x.get('t',''))+_w(x.get('p','')) for x in it)
            for k,x in enumerate(it):
                h3=pc.get((si,k),False)
                h.append((f"<h3>{x['t']}</h3>" if h3 else f"<p><strong>{x['t']}</strong></p>")+f"<p>{x['p']}</p>")
        elif t=='list': h+= [f"<p>{x}</p>" for x in it]
        elif t=='table': h.append('<table>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in it)+'</table>')
        elif t=='callout': h.append(f"<p><strong>{it['t']}</strong></p><p>{it['p']}</p>")
        for p in (sec.get('outro',[]) if isinstance(sec.get('outro'),list) else [sec.get('outro','')]):
            if p: h.append(f"<p>{p}</p>")
    ft=s.get('faq_title','Dudas habituales')
    if kw and not _has_kw(ft,kw): ft=f"Preguntas sobre {kw}"
    h.append(f"<h2>{ft}</h2>")
    for i,(q,a) in enumerate(s['faqs'],1):
        fh3=pf.get(i,False)
        h.append((f"<h3>{q}</h3>" if fh3 else f"<p><strong>{q}</strong></p>")+f"<p>{a}</p>")
    ct=s.get('cta_title','')
    if kw and not _has_kw(ct,kw): ct=f"{kw[0].upper()+kw[1:]}: te damos precio por tu parte en 48 h"
    h.append(f"<h2>{ct}</h2><p>{s.get('cta_text','')}</p>")
    # enlaces internos (related + cards con url) como <a> para 'competing links' / 'internal links'
    rel=[tuple(x) for x in s.get('related',[])]
    if rel and not any('boe.es' in u for _,u in rel): rel.append(("Código Civil (BOE)","https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763"))
    for lab,u in _break_runs(rel): h.append(f'<p><a href="{u}">{lab}</a></p>')
    h.append('<p><img src="x.webp" alt="{}"></p>'.format(s.get('imagen_alt','')))
    return ''.join(h)
def analyze(specs):
    items=[dict(url=s['slug'],doc=0,ptype='posts',html=html_of(s),keyword=s['focus_kw'],title=s['yoast_title'].strip(),description=s['meta_desc'],slug=s['slug'],permalink=(f"https://zonaproindiviso.com/blog/{s['slug']}/" if s.get('kind')=='post' else f"https://zonaproindiviso.com/diccionario-del-proindiviso/{s['slug']}/")) for s in specs]
    r=subprocess.run(['node',os.path.join(YOAST_DIR,'analyze.js')],input=json.dumps(items),capture_output=True,text=True,cwd=YOAST_DIR)
    return json.loads(r.stdout)
if __name__=='__main__':
    args=sys.argv[1:]; files=[a for a in args if a.endswith('.json')]; solo=args[args.index('--solo')+1] if '--solo' in args else None
    S=[]
    for f in files: S+=json.load(open(f))
    if solo: S=[s for s in S if s['slug']==solo]
    res=analyze(S); n=0
    for r in res:
        bad=[(a['id'],a['score'],a['text'][:110]) for a in r['seo']+r.get('readability',[]) if 0<a['score']<=6 and a['id'] not in ('keyphraseLength',)]
        if bad: n+=1; print(r['url'],r['seoScore'],r['readabilityScore']); [print('   ',b) for b in bad]
    print(f'{len(res)-n}/{len(res)} sin comprobaciones naranjas/rojas')
