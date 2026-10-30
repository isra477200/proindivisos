"""Aplica la 2ª tanda de imágenes (media_map2.json del cuaderno de imágenes) a los mapas que leen los builders:
- slot "hero" (provincias y 5 ciudades grandes): images.json[post_id] = media_id; las ciudades sin imagen propia heredan la de su provincia.
- slot "fig2" (segunda imagen antes del FAQ): images2.json[post_id] = media_id.
Imprime los IDs de página cuya imagen de cabecera cambia (hay que recomponerlos y fijar featured_media con set_featured.py).
Uso: python3 apply_images2.py <ruta media_map2.json> <ruta manifest2.json>"""
import sys, os, json, glob
HERE=os.path.dirname(os.path.abspath(__file__))
MAP=json.load(open(sys.argv[1])); MAN={m['key']:m for m in json.load(open(sys.argv[2]))}
IMG=json.load(open(os.path.join(HERE,'images.json')))
IMG2_F=os.path.join(HERE,'images2.json'); IMG2=json.load(open(IMG2_F)) if os.path.exists(IMG2_F) else {}
P=[]
for f in sorted(glob.glob(os.path.join(HERE,'geo','geo_[A-F].json'))): P+=json.load(open(f))
by={p['slug']:p for p in P}; gids=json.load(open(os.path.join(HERE,'geo','ids.json')))
own={}  # slug -> media_id propio
for key,m in MAP.items():
    it=MAN.get(key)
    if not it: continue
    if it['slot']=='hero' and key.startswith('geo-'): own[key[4:]]=m['media_id']
    elif it['slot']=='fig2': IMG2[str(it['post_id'])]=m['media_id']
changed=[]; changed_slugs=[]
def hero_for(p):
    q=p
    while q:
        if q['slug'] in own: return own[q['slug']]
        q=by.get(q['padre']) if q.get('padre') else None
    return None
for p in P:
    mid=hero_for(p)
    if mid and IMG.get(str(gids[p['slug']]))!=mid:
        IMG[str(gids[p['slug']])]=mid; changed.append(gids[p['slug']]); changed_slugs.append(p['slug'])
json.dump(IMG,open(os.path.join(HERE,'images.json'),'w'),indent=0); json.dump(IMG2,open(IMG2_F,'w'),indent=0)
print('cabecera cambiada en',len(changed),'páginas geo;','figura 2 en',len(IMG2),'páginas')
print(' '.join(str(x) for x in changed))
open(os.path.join(HERE,'.geo_changed_slugs.txt'),'w').write(' '.join(changed_slugs))
