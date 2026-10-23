"""Crea y publica las entradas nuevas de tools/blog/blog_7.json: crea el post (elementor-create-page), asigna su imagen
(media_map de la sesión de imágenes -> images.json + featured_media), compone, publica y fija metas."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blogbuilder as b
HERE=os.path.dirname(os.path.abspath(__file__))
MEDIA=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/-home-claude/465a46cd-02da-53eb-bb5e-39c7569fb424/scratchpad/img/media_map.json'
mm=json.load(open(MEDIA))
S=json.load(open(os.path.join(HERE,'blog','blog_7.json')))
ids=b.load_ids()
IMG_F=os.path.join(HERE,'images.json'); IMG=json.load(open(IMG_F))
for spec in S:
    pid=b.ensure(spec,ids)
    if not pid: print('SIN ID',spec['slug']); continue
    mid=mm.get(spec['slug'],{}).get('media_id')
    if mid:
        IMG[str(pid)]=mid; json.dump(IMG,open(IMG_F,'w'),indent=0)
        r=b.api('POST',f'/wp/v2/posts/{pid}',{'featured_media':mid})
        print(pid,'featured',r.get('featured_media'))
    ok=b.build_one(spec,ids)
    print(pid,spec['slug'],'OK' if ok else 'FAIL',flush=True)
