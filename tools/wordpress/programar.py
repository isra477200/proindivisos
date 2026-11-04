"""Entradas programadas: imagen MiniMax → adjunto → entrada (borrador) → composición Elementor → metas Yoast → QA Yoast → fecha futura.
Uso: python3 programar.py blog/blog_8.json [blog/blog_9.json ...] [--solo slug] [--sin-imagenes] [--sin-programar] [--solo-programar] [--plan blog/plan_X.json]
Con --sin-programar las entradas quedan publicadas en el acto (lotes de la competencia: plan blog/plan_competencia.json).
Las fechas salen de blog/plan_programados.json (campo `fecha`, hora local del sitio). El paso de composición publica la entrada unos
segundos (Elementor solo genera el CSS al publicar y Yoast solo se puede medir en una URL pública); después se pasa a «future».
Imágenes: usa gen.py/upload.py del scratchpad (MANIFEST=manifest_prog.json); la clave de MiniMax no está en el repo."""
import sys, os, json, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogbuilder as b
HERE=os.path.dirname(os.path.abspath(__file__))
IMGDIR=os.environ.get('ZP_IMGDIR','/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/img')
args=sys.argv[1:]
files=[a for i,a in enumerate(args) if a.endswith('.json') and (i==0 or args[i-1]!='--plan')]
solo=args[args.index('--solo')+1] if '--solo' in args else None
PLANF=args[args.index('--plan')+1] if '--plan' in args else 'blog/plan_programados.json'
plan={p['slug']:p for p in json.load(open(PLANF if os.path.isabs(PLANF) else os.path.join(HERE,PLANF)))}
S=[]
for f in files: S+=json.load(open(f if os.path.isabs(f) else os.path.join(HERE,f)))
if solo: S=[s for s in S if s['slug']==solo]
print(len(S),'entradas')
ids=b.load_ids()
IMG_F=os.path.join(HERE,'images.json'); IMG=json.load(open(IMG_F))
# A) imágenes
MF=os.path.join(IMGDIR,'manifest_prog.json'); MAP_F=os.path.join(IMGDIR,'media_map_prog.json')
if '--sin-imagenes' not in args and '--solo-programar' not in args:
    man=json.load(open(MF)) if os.path.exists(MF) else []
    have={m['key'] for m in man}
    for s in S:
        if s['slug'] in have: continue
        man.append({'key':s['slug'],'kind':'post','post_id':0,'filename':(s['slug'][:70])+'.webp','title':s['h1'][:120],'alt':s['imagen_alt'],'prompt':s['imagen_prompt']})
    json.dump(man,open(MF,'w'),ensure_ascii=False,indent=1)
    keys=[s['slug'] for s in S]
    r=subprocess.run(['python3','gen.py']+keys,cwd=IMGDIR,env={**os.environ,'MANIFEST':'manifest_prog.json'},capture_output=True,text=True); print(r.stdout[-400:])
    r=subprocess.run(['python3','upload.py']+keys,cwd=IMGDIR,env={**os.environ,'MANIFEST':'manifest_prog.json'},capture_output=True,text=True); print(r.stdout[-600:])
mm=json.load(open(MAP_F)) if os.path.exists(MAP_F) else {}
# B) entradas
hechos=[]
for s in S:
    pid=b.ensure(s,ids)
    if not pid: print('SIN ID',s['slug']); continue
    if '--solo-programar' in args: hechos.append((s,pid)); continue
    # si la entrada ya estaba programada, su fecha es futura y WP no la dejaría «publish» para la QA: se pasa a borrador con fecha de hoy
    b.api('POST',f'/wp/v2/posts/{pid}',{'status':'draft','date':time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime())})
    mid=mm.get(s['slug'],{}).get('media_id')
    if mid:
        IMG=json.load(open(IMG_F)); IMG[str(pid)]=mid; json.dump(IMG,open(IMG_F,'w'),indent=0)  # releer antes de escribir: otros procesos pueden estar añadiendo
        b.api('POST',f'/wp/v2/posts/{pid}',{'featured_media':mid}); s=dict(s,image_id=mid)  # la composición usa image_id del spec antes que images.json
    else: print('  sin imagen',s['slug'])
    ok=b.build_one(s,ids)
    print(pid,s['slug'],'OK' if ok else 'FAIL',flush=True)
    if ok: hechos.append((s,pid))
# C) QA Yoast sobre las URL publicadas
if hechos and '--solo-programar' not in args:
    urls=[f"https://zonaproindiviso.com/blog/{s['slug']}/" for s,_ in hechos]
    r=subprocess.run(['python3','yoastqa.py','--urls']+urls+['--save'],cwd=HERE,capture_output=True,text=True); print(r.stdout[-1500:])
# D) programar
if '--sin-programar' not in args:
    for s,pid in hechos:
        f=plan.get(s['slug'],{}).get('fecha')
        if not f: print('  sin fecha en el plan',s['slug']); continue
        r=b.api('POST',f'/wp/v2/posts/{pid}',{'status':'future','date':f})
        print(pid,s['slug'],'→',r.get('status'),r.get('date'))
