"""Validación de un fichero de specs de entradas (lista JSON) antes de construir: estructura, extensión y heurísticas de Yoast.
Uso: python3 validar.py blog_8.json [plan_programados.json]
Comprueba por pieza: claves obligatorias; 5-8 secciones con h2 (salvo callout); 5-6 FAQ; 1.100-1.600 palabras (intro+items+outro, sin FAQ);
keyphrase en h1, en sub (primer párrafo), en meta_desc, en yoast_title; en el 30-75 % de los H2 con más de la mitad de sus palabras de
contenido; densidad 0,5-2,5 %; cada sección ≤ 300 palabras (Yoast: subtítulos cada 300); párrafos ≤ 150 palabras; ≤ 25 % de frases de más de
20 palabras; ≥ 30 % de frases con palabra de transición; no 3 frases seguidas que empiecen igual; yoast_title 50-62; meta_desc 130-155;
imagen_prompt e imagen_alt presentes (alt con la keyphrase). Imprime los fallos; sale con 1 si hay alguno."""
import json, re, sys, unicodedata
FUNC=set("""de la el los las un una unos unas y o u e a en con sin por para del al que como mi tu su mis tus sus se lo le les me te nos os es son ser estar hay si no más menos muy ya aún todo toda todos todas otro otra otros otras este esta estos estas ese esa esos esas aquel aquella cuando donde quien quién qué cuál cuánto cuánta cuántos cuántas cómo porque pero sino entre sobre hasta desde ante bajo tras hacia según ni también tan tanto cada algo alguien nada nadie poco mucho ser está están era eran fue fueron ha han he hemos puede pueden puedo debe deben hace hacer tener tiene tienen vender venta parte""".split())
# nota: "parte", "vender" y "venta" se tratan como palabras de contenido débiles pero cuentan; se quitan de FUNC abajo
FUNC-= {"parte","vender","venta"}
TRANS=["además","también","sin embargo","por eso","por tanto","por lo tanto","así","así que","es decir","en cambio","aunque","porque","por ejemplo","primero","segundo","después","antes","luego","mientras","entonces","en la práctica","de hecho","en resumen","al final","por un lado","por otro","en cualquier caso","si","cuando","como","pero","ya que","puesto que","incluso","sobre todo","en concreto","en general","a cambio","en consecuencia","de todos modos","hasta","desde","salvo","excepto","igual que","del mismo modo","a su vez","por último","finalmente","en primer lugar","en segundo lugar","por otra parte","no obstante","ahora bien","en ese caso","en este caso","si no","para","con todo","mientras tanto","a partir de","gracias a","debido a","a pesar de","por el contrario","en definitiva","dicho de otro modo","o sea","es más","ni siquiera","tampoco","también","asimismo","todavía","aun así","de ahí que","por consiguiente","en otras palabras"]
def norm(s): return unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode()
def words(t): return re.findall(r"[a-záéíóúñü0-9]+", t.lower())
def strip(h): return re.sub(r'<[^>]+>',' ',str(h))
def sentences(t):
    t=strip(t); return [x.strip() for x in re.split(r'(?<=[.!?])\s+',t) if x.strip()]
def text_of(sec):
    parts=[]
    for k in ('intro','outro'):
        v=sec.get(k,[]); parts+= v if isinstance(v,list) else [v]
    it=sec.get('items')
    if isinstance(it,list):
        for x in it:
            if isinstance(x,dict): parts+=[x.get('t',''),x.get('p','')]
            elif isinstance(x,(list,tuple)): parts+=[str(y) for y in x]
            else: parts.append(str(x))
    elif isinstance(it,dict): parts+=[it.get('t',''),it.get('p','')]
    return ' '.join(strip(p) for p in parts)
def has_kw(text,kw,ratio=0.5):
    cw=[w for w in words(kw) if w not in FUNC] or words(kw)
    tw=set(words(norm(text))); cwn=[norm(w) for w in cw]
    return sum(1 for w in cwn if w in tw)/len(cwn)>ratio if cwn else True
MODO={'min':1100,'max':1700,'secs':(5,8),'faqs':(5,6)}
def check(s, plan=None):
    err=[]; slug=s.get('slug','?')
    req=["slug","kind","category","kicker","h1","sub","checks","card_title","card_text","sections","faqs","faq_title","related","cta_title","cta_text","yoast_title","meta_desc","focus_kw","title_corto","imagen_prompt","imagen_alt"]
    for k in req:
        if k not in s: err.append(f'falta {k}')
    if err: return err
    kw=s['focus_kw']
    if plan and slug in plan:
        if norm(kw)!=norm(plan[slug]['focus_kw']): err.append(f'focus_kw distinta del plan: {kw!r} vs {plan[slug]["focus_kw"]!r}')
        if s['category']!=plan[slug].get('category'): err.append('categoría distinta del plan')
        if plan[slug].get('kind') and s.get('kind')!=plan[slug]['kind']: err.append('kind distinto del plan')
    elif plan: err.append('slug no está en el plan')
    secs=s['sections']
    if not MODO['secs'][0]<=len(secs)<=MODO['secs'][1]: err.append(f'secciones {len(secs)} ({MODO["secs"][0]}-{MODO["secs"][1]})')
    if not MODO['faqs'][0]<=len(s['faqs'])<=MODO['faqs'][1]: err.append(f'faqs {len(s["faqs"])} ({MODO["faqs"][0]}-{MODO["faqs"][1]})')
    for q,a in s['faqs']:
        if len(words(a))<25: err.append(f'respuesta FAQ corta: {q[:40]}')
    total=0; h2s=[]; textos=[]
    for i,sec in enumerate(secs):
        t=sec.get('type','text')
        if t!='callout' and not sec.get('h2'): err.append(f'sección {i} sin h2')
        if sec.get('h2'): h2s.append(sec['h2'])
        tx=text_of(sec); n=len(words(tx)); total+=n; textos.append(tx)
        if n>300 and t!='table': err.append(f'sección {i} «{sec.get("h2","")[:30]}» {n} palabras (>300: Yoast pide subtítulo cada 300)')
        for p in (sec.get('intro',[]) if isinstance(sec.get('intro',[]),list) else [sec.get('intro','')])+(sec.get('outro',[]) if isinstance(sec.get('outro',[]),list) else [sec.get('outro','')]):
            if len(words(strip(p)))>150: err.append(f'párrafo >150 palabras en sección {i}')
    if not MODO['min']<=total<=MODO['max']: err.append(f'{total} palabras de cuerpo ({MODO["min"]}-{MODO["max"]})')
    if not has_kw(s['h1'],kw,0.99): err.append('keyphrase no está completa en h1')
    if not has_kw(s['sub'],kw,0.99): err.append('keyphrase no está completa en sub (primer párrafo)')
    if not has_kw(s['meta_desc'],kw,0.99): err.append('keyphrase no está en meta_desc')
    if not has_kw(s['yoast_title'],kw,0.99): err.append('keyphrase no está en yoast_title')
    if not 50<=len(s['yoast_title'])<=62: err.append(f'yoast_title {len(s["yoast_title"])} car. (50-62)')
    if not 130<=len(s['meta_desc'])<=155: err.append(f'meta_desc {len(s["meta_desc"])} car. (130-155)')
    conkw=sum(1 for h in h2s if has_kw(h,kw,0.5)); r=conkw/len(h2s) if h2s else 0
    if not 0.3<=r<=0.75: err.append(f'H2 con keyphrase {conkw}/{len(h2s)} (debe ser 30-75 %)')
    cuerpo=' '.join(textos)+' '+s['sub']; cw=[norm(w) for w in words(kw) if w not in FUNC] or [norm(w) for w in words(kw)]
    nw=len(words(cuerpo))
    # Yoast (motor español sin formas de palabra): una aparición = una frase que contiene TODAS las palabras de contenido de la keyphrase
    oc=sum(1 for x in sentences(cuerpo) if all(w in set(words(norm(x))) for w in cw))
    dens=oc*100/max(nw,1)
    if dens<0.5: err.append(f'densidad {dens:.2f} % ({oc} frases con todas las palabras de la keyphrase en {nw} palabras): mínimo 0,5 %, hacen falta al menos {max(oc+1,int(nw*0.005)+1)}')
    if dens>3.0: err.append(f'densidad {dens:.2f} %: demasiada (máx 3 %)')
    sents=[x for tx in textos for x in sentences(tx)]+sentences(s['sub'])
    largas=sum(1 for x in sents if len(words(x))>20)
    if sents and largas/len(sents)>0.25: err.append(f'{largas}/{len(sents)} frases de más de 20 palabras (máx 25 %)')
    tr=sum(1 for x in sents if any(re.search(r'\b'+re.escape(t)+r'\b', norm(x)) for t in [norm(t) for t in TRANS]))
    if sents and tr/len(sents)<0.30: err.append(f'palabras de transición en {tr}/{len(sents)} frases (mín 30 %)')
    for tx in textos:
        ss=sentences(tx); ini=[norm(x).split()[0] if x.split() else '' for x in ss]
        for i in range(len(ini)-2):
            if ini[i] and ini[i]==ini[i+1]==ini[i+2]: err.append(f'3 frases seguidas empiezan por «{ini[i]}»'); break
    if not has_kw(s['imagen_alt'],kw,0.99): err.append('imagen_alt sin la keyphrase')
    if re.search(r'[A-Za-z]{3}', s['imagen_prompt']) is None: err.append('imagen_prompt vacío')
    if '—' in json.dumps(s,ensure_ascii=False): err.append('contiene guion largo —')
    for lab,url in s['related']:
        if not url.startswith('/'): err.append(f'related con url externa: {url}')
    return err
if __name__=='__main__':
    if '--diccionario' in sys.argv: MODO.update({'min':550,'max':1100,'secs':(4,7),'faqs':(3,6)}); sys.argv.remove('--diccionario')
    specs=json.load(open(sys.argv[1]))
    planj=json.load(open(sys.argv[2])) if len(sys.argv)>2 else None
    if isinstance(planj,dict): planj=planj.get('nuevos',[])
    plan={p['slug']:p for p in planj} if planj else None
    bad=0
    for s in specs:
        e=check(s,plan)
        if e: bad+=1; print('✗',s.get('slug')); [print('   -',x) for x in e]
        else: print('✓',s.get('slug'))
    print(f'{len(specs)-bad}/{len(specs)} válidas'); sys.exit(1 if bad else 0)
