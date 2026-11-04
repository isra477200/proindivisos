import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geobuilder import load_places, load_ids, nombre_h1
from pagebuilder import meta
P,by=load_places(); ids=load_ids()
for p in P:
    if p['slug'] in ids: meta(ids[p['slug']], title=(nombre_h1(p) if p['tipo']=='ccaa' else p['nombre']))
