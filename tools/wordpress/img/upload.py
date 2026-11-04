import json, os, sys, subprocess, glob
HERE=os.path.dirname(os.path.abspath(__file__))
TOOLS='/home/claude/isra477200/proindivisos/tools'
env={}
for l in open(os.path.join(TOOLS,'wordpress','wp.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip()
WP=env['WP']; AUTH=env['P1']
MF=os.environ.get('MANIFEST','manifest.json'); M=json.load(open(os.path.join(HERE,MF)))
MAP_F=os.path.join(HERE,MF.replace('manifest','media_map'))
MAP=json.load(open(MAP_F)) if os.path.exists(MAP_F) else {}
def api(method,path,body=None,extra=None):
    args=['curl','-sS','--max-time','120','-u',AUTH,'-X',method,WP+'/wp-json'+path]+(extra or [])
    if body is not None: args+=['-H','Content-Type: application/json','-d',json.dumps(body,ensure_ascii=False)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:300]}
only=sys.argv[1:]
for it in M:
    if only and it['key'] not in only: continue
    f=os.path.join(HERE,'out',it['filename'])
    if not os.path.exists(f): print('NOFILE',it['key']); continue
    if it['key'] in MAP and not only:
        continue
    if it['key'] in MAP and only:
        # reemplazo: borrar el adjunto anterior y subir el fichero actual
        api('DELETE',f"/wp/v2/media/{MAP[it['key']]['media_id']}?force=true"); del MAP[it['key']]
    # ¿existe ya un adjunto con ese nombre? (reintentos)
    r=api('GET',f"/wp/v2/media?search={it['filename'].replace('.webp','')}&per_page=5&_fields=id,source_url")
    mid=None
    if isinstance(r,list):
        for x in r:
            if x.get('source_url','').endswith('/'+it['filename']): mid=x['id']
    if mid and it['key'] in MAP: pass
    elif not mid:
        out=subprocess.run(['curl','-sS','--max-time','180','-u',AUTH,'-X','POST',WP+'/wp-json/wp/v2/media','-H',f'Content-Disposition: attachment; filename="{it["filename"]}"','-H','Content-Type: image/webp','--data-binary','@'+f],capture_output=True,text=True).stdout
        try: d=json.loads(out); mid=d['id']
        except Exception: print('UPLOAD FAIL',it['key'],out[:200]); continue
    r=api('POST',f'/wp/v2/media/{mid}',{'alt_text':it['alt'],'title':it['title'],'caption':'','description':it['alt']})
    MAP[it['key']]={'media_id':mid,'post_id':it['post_id'],'kind':it['kind'],'url':r.get('source_url')}
    json.dump(MAP,open(MAP_F,'w'),ensure_ascii=False,indent=0)
    print('OK',it['key'],mid,r.get('source_url','')[-60:],flush=True)
print(len(MAP),'adjuntos en el mapa')
