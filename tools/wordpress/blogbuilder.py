import sys, os, json, glob, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import run, meta
HERE=os.path.dirname(os.path.abspath(__file__))
env={}
for l in open(os.path.join(HERE,'wp.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip().strip('"').strip("'")
CATS={'herencias':17,'extincion-de-condominio':18,'copropiedad':19,'division-de-cosa-comun':20,'impuestos-y-tramites':21}
IDS_FILE=os.path.join(HERE,'blog','ids.json')
def api(method,path,body=None):
    args=['curl','-sS','--max-time','60','-u',env['P1'],'-X',method,'-H','Content-Type: application/json',env['WP']+'/wp-json'+path]
    if body is not None: args+=['-d',json.dumps(body,ensure_ascii=False)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:300]}
def load_specs(files=None):
    S=[]
    for f in sorted(files or glob.glob(os.path.join(HERE,'blog','blog_[0-9].json'))): S+=json.load(open(f))
    return S
def load_ids(): return json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}
def ensure(spec,ids):
    if spec['slug'] in ids: return ids[spec['slug']]
    pt='post' if spec['kind']=='post' else 'page'; ep='posts' if pt=='post' else 'pages'
    r=api('GET',f"/wp/v2/{ep}?slug={spec['slug']}&status=any&_fields=id")
    if isinstance(r,list) and r: pid=r[0]['id']
    else:
        out=subprocess.run(['./emcp.sh','elementor-create-page',json.dumps({'title':spec['title_corto'],'post_type':pt})],capture_output=True,text=True).stdout
        m=re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out)
        if not m: print('CREATE FAIL',spec['slug'],out[:200]); return None
        pid=int(m.group(1))
        body={'title':spec['title_corto'],'slug':spec['slug'],'status':'draft'}
        if pt=='post': body['categories']=[CATS[spec['category']]]; body['comment_status']='closed'; body['ping_status']='closed'
        r=api('POST',f'/wp/v2/{ep}/{pid}',body)
        if 'id' not in r: print('SET FAIL',spec['slug'],r); return None
    ids[spec['slug']]=pid; json.dump(ids,open(IDS_FILE,'w'),ensure_ascii=False,indent=0); return pid
def normalize(spec):
    s=dict(spec); s['faqs']=[tuple(x) for x in s.get('faqs',[])]; s['related']=[tuple(x) for x in s.get('related',[])]
    for sec in s['sections']:
        if sec.get('type')=='table': sec['items']=[tuple(x) for x in sec['items']]
    return s
def build_one(spec,ids):
    pid=ensure(spec,ids)
    if not pid: return False
    s=normalize(spec); s['post_id']=pid
    ok=run(s)
    if ok:
        ep='posts' if spec['kind']=='post' else 'pages'
        yt=spec['yoast_title'].strip()
        if 'Zona Proindiviso' not in yt: yt+=' · Zona Proindiviso'
        extra={}
        if spec['kind']=='post': extra={'categories':[CATS[spec['category']]]}
        meta(pid,title=spec['title_corto'],yt=yt,yd=spec['meta_desc'],kw=spec['focus_kw'],status='publish',ptype=ep,extra=extra)
    return ok
if __name__=='__main__':
    files=[a for a in sys.argv[1:] if a.endswith('.json')]; only=[a for a in sys.argv[1:] if not a.endswith('.json')]
    S=load_specs(files or None); ids=load_ids()
    for spec in S:
        if only and spec['slug'] not in only: continue
        build_one(spec,ids)
