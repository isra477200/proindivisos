"""Baja la densidad de keyphrase en specs (Yoast marca en rojo si supera el máximo): sustituye apariciones en FAQ y en las últimas
secciones (nunca en h1, sub, H2, títulos, meta ni alt) por variantes que no contienen todas las palabras de la keyphrase.
Uso: python3 densfix.py blog/dic_2.json slug:N [slug:N ...]   (N = apariciones a quitar)"""
import sys, json, re
SUBS={
 'nota de afección fiscal':[(r'nota de afección fiscal','nota de afección')],
 'condominio':[(r'\bel condominio\b','la copropiedad'),(r'\bdel condominio\b','de la copropiedad'),(r'\bun condominio\b','una copropiedad'),(r'\ben condominio\b','en copropiedad'),(r'\bEl condominio\b','La copropiedad')],
 'cuota indivisa':[(r'\bcuotas indivisas\b','cuotas'),(r'\bcuota indivisa\b','cuota')],
 'cuota de participación':[(r'\bcuotas de participación\b','cuotas'),(r'\bcuota de participación\b','cuota')],
 'finca registral':[(r'\bfincas registrales\b','fincas'),(r'\bfinca registral\b','finca')],
 'usufructo':[(r'\bel usufructo\b','este derecho'),(r'\bdel usufructo\b','de este derecho'),(r'\bun usufructo\b','un derecho de uso'),(r'\bEl usufructo\b','Este derecho')],
 'valor catastral':[(r'\bvalor catastral\b','valor del Catastro'),(r'\bValor catastral\b','Valor del Catastro')],
}
def candidates(s):
    """Referencias (contenedor, clave) en orden de preferencia: FAQ (de la última a la primera), luego secciones de la última a la segunda."""
    refs=[]
    for i in range(len(s['faqs'])-1,-1,-1): refs.append(('faq',i))
    for si in range(len(s['sections'])-1,0,-1):
        sec=s['sections'][si]
        for k in ('outro','intro'):
            v=sec.get(k)
            if isinstance(v,list):
                for i in range(len(v)-1,-1,-1): refs.append((sec,k,i))
        it=sec.get('items')
        if isinstance(it,list):
            for i in range(len(it)-1,-1,-1):
                if isinstance(it[i],dict): refs.append((sec,'items',i,'p'))
                elif isinstance(it[i],list): refs.append((sec,'items',i,len(it[i])-1))
                else: refs.append((sec,'items',i))
        elif isinstance(it,dict): refs.append((sec,'items',None,'p'))
    # primera sección: solo outro e items (no la intro, que abre el texto)
    sec=s['sections'][0]
    for k in ('outro',):
        v=sec.get(k)
        if isinstance(v,list):
            for i in range(len(v)): refs.append((sec,k,i))
    return refs
def get(s,r):
    if r[0]=='faq': return s['faqs'][r[1]][1]
    sec,k=r[0],r[1]
    if k=='items':
        if r[2] is None: return sec['items'][r[3]]
        x=sec['items'][r[2]]
        return x[r[3]] if len(r)>3 else x
    return sec[k][r[2]]
def put(s,r,val):
    if r[0]=='faq': s['faqs'][r[1]]=[s['faqs'][r[1]][0],val]; return
    sec,k=r[0],r[1]
    if k=='items':
        if r[2] is None: sec['items'][r[3]]=val; return
        if len(r)>3: sec['items'][r[2]][r[3]]=val
        else: sec['items'][r[2]]=val
        return
    sec[k][r[2]]=val
if __name__=='__main__':
    f=sys.argv[1]; want={a.split(':')[0]:int(a.split(':')[1]) for a in sys.argv[2:]}
    S=json.load(open(f))
    for s in S:
        if s['slug'] not in want: continue
        subs=SUBS[s['focus_kw'].lower()]; left=want[s['slug']]; done=0
        for r in candidates(s):
            if left<=0: break
            t=get(s,r)
            if not isinstance(t,str): continue
            for pat,rep in subs:
                if left<=0: break
                t2,n=re.subn(pat,rep,t,count=1)
                if n: t=t2; left-=1; done+=1
            put(s,r,t)
        print(s['slug'],'quitadas',done,'de',want[s['slug']])
    json.dump(S,open(f,'w'),ensure_ascii=False,indent=1)
