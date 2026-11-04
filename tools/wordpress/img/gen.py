import json, os, sys, time, subprocess, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
MF=os.environ.get('MANIFEST','manifest.json'); M=json.load(open(os.path.join(HERE,MF)))
URL='https://n8n-wmlc.srv1480016.hstgr.cloud/webhook/panel-img'
K=os.environ["PANEL_IMG_KEY"]  # clave del webhook n8n panel-img (no va en el repo)
LOG=os.path.join(HERE,MF.replace('.json','')+'.log')
def log(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); open(LOG,'a').write(s+'\n')
def one(it):
    dst=os.path.join(OUT,it['filename'])
    if os.path.exists(dst) and os.path.getsize(dst)>20000: return (it['key'],'skip')
    for attempt in range(3):
        try:
            r=subprocess.run(['curl','-sS','-m','220','-X','POST',URL,'-H','Content-Type: application/json','-d',json.dumps({"k":K,"prompt":it['prompt'],"aspect":"16:9","n":1,"optimiza":False})],capture_output=True,text=True,timeout=240)
            d=json.loads(r.stdout)
            if not d.get('ok'): log('FAIL',it['key'],d.get('error')); time.sleep(5); continue
            u=d['imagenes'][0]
            raw=subprocess.run(['curl','-sS','-m','90','-L',u],capture_output=True,timeout=120).stdout
            im=Image.open(io.BytesIO(raw)).convert('RGB')
            if im.size[0]<1000: log('SMALL',it['key'],im.size)
            if im.size!=(1280,720): im=im.resize((1280,720),Image.LANCZOS)
            im.save(dst,'WEBP',quality=82,method=6)
            log('OK',it['key'],os.path.getsize(dst)//1024,'KB')
            return (it['key'],'ok')
        except Exception as e:
            log('ERR',it['key'],repr(e)[:200]); time.sleep(8)
    return (it['key'],'fail')
only=sys.argv[1:]
work=[it for it in M if not only or it['key'] in only or it['kind'] in only]
log('inicio',len(work),'imágenes')
with ThreadPoolExecutor(3) as ex: res=list(ex.map(one,work))
from collections import Counter
log('fin',Counter(r[1] for r in res))
