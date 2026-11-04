"""Fija la imagen destacada (featured_media) de cada documento según images.json (post_id -> media_id).
Yoast usa la destacada como og:image / twitter:image si no hay OG propia. Uso: python3 set_featured.py [ids...]"""
import json, os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__))
env={}
for l in open(os.path.join(HERE,'wp.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip()
WP=env['WP']; AUTH=env['P1']
IMG={int(k):v for k,v in json.load(open(os.path.join(HERE,'images.json'))).items()}
def api(method,path,body=None):
    args=['curl','-sS','--max-time','60','-u',AUTH,'-X',method,'-H','Content-Type: application/json',WP+'/wp-json'+path]
    if body is not None: args+=['-d',json.dumps(body)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:200]}
def one(pid):
    mid=IMG[pid]
    for ep in ('pages','posts'):
        r=api('GET',f'/wp/v2/{ep}/{pid}?context=edit&_fields=id,featured_media')
        if isinstance(r,dict) and r.get('id')==pid:
            if r.get('featured_media')==mid: return (pid,'ya')
            r2=api('POST',f'/wp/v2/{ep}/{pid}',{'featured_media':mid})
            return (pid,'ok' if r2.get('featured_media')==mid else 'FAIL '+str(r2)[:120])
    return (pid,'NOEXISTE')
if __name__=='__main__':
    ids=[int(x) for x in sys.argv[1:]] or sorted(IMG)
    with ThreadPoolExecutor(6) as ex: res=list(ex.map(one,ids))
    from collections import Counter
    print(Counter(r[1][:4] for r in res)); print([r for r in res if r[1] not in ('ok','ya')][:20])
