"""Sube el porcentaje de frases con palabra de transición (Yoast: mínimo 30 %) en specs concretos, anteponiendo conectores neutros
(«Además», «En la práctica», «De hecho», «En concreto», «Asimismo») a frases de intro/outro/tarjetas que no tengan ninguno.
Uso: python3 transfix.py blog/dic_2.json slug [slug...]   (objetivo 34 %; reescribe el fichero)"""
import sys, os, json, re, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'blog'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validar import norm, sentences
import yoastpre as Y
TRANS=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'yoast_transition_words_es.json')))['single']
CON=["Además, ","En la práctica, ","De hecho, ","En concreto, ","Asimismo, "]
def has_trans(x):
    nx=norm(x); return any(re.search(r'\b'+re.escape(norm(t))+r'\b',nx) for t in TRANS)
def texts(s):
    for sec in s['sections']:
        for k in ('intro','outro'):
            v=sec.get(k)
            if isinstance(v,list):
                for i in range(len(v)): yield (sec,k,i)
        it=sec.get('items')
        if isinstance(it,list):
            for i,x in enumerate(it):
                if isinstance(x,dict) and x.get('p'): yield (sec,'items',i)
def get(ref):
    sec,k,i=ref; return sec[k][i]['p'] if k=='items' else sec[k][i]
def put(ref,val):
    sec,k,i=ref
    if k=='items': sec[k][i]['p']=val
    else: sec[k][i]=val
def ratio(s):
    """Ratio real del motor Yoast (findTransitionWords) sobre el HTML aproximado de la página."""
    it=dict(url=s['slug'],html=Y.html_of(s),keyword=s['focus_kw'],title=s['yoast_title'],description=s['meta_desc'],slug=s['slug'],permalink='https://zonaproindiviso.com/x/')
    r=subprocess.run(['node','research.js'],input=json.dumps([it]),capture_output=True,text=True,cwd=Y.YOAST_DIR); d=json.loads(r.stdout)['transition']
    return d['with']/max(d['total'],1), d['total']
def fix(s,target=0.34):
    r,n=ratio(s); c=0; k=0
    refs=list(texts(s))
    while r<target and k<200:
        done=False
        for ref in refs:
            t=get(ref); ss=sentences(t)
            for j,x in enumerate(ss):
                if has_trans(x) or not re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñü]',x): continue
                ss[j]=CON[c%len(CON)]+x[0].lower()+x[1:]; c+=1
                put(ref,' '.join(ss)); done=True; break
            if done: break
        if not done: break
        r,n=ratio(s); k+=1
    return r,c
if __name__=='__main__':
    f=sys.argv[1]; slugs=sys.argv[2:]; S=json.load(open(f))
    for s in S:
        if s['slug'] in slugs:
            r0,_=ratio(s); r,c=fix(s); print(s['slug'],f'{r0:.1%} → {r:.1%} ({c} conectores)')
    json.dump(S,open(f,'w'),ensure_ascii=False,indent=1)
