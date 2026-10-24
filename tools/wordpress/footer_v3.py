import sys, os, json, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CCAA=[("Andalucía","andalucia"),("Aragón","aragon"),("Asturias","asturias"),("Baleares","baleares"),("Canarias","canarias"),("Cantabria","cantabria"),("Castilla-La Mancha","castilla-la-mancha"),("Castilla y León","castilla-y-leon"),("Cataluña","cataluna"),("C. Valenciana","comunidad-valenciana"),("Extremadura","extremadura"),("Galicia","galicia"),("Madrid","madrid"),("Murcia","murcia"),("Navarra","navarra"),("País Vasco","pais-vasco"),("La Rioja","la-rioja"),("Ceuta","ceuta"),("Melilla","melilla")]
def emcp(tool,args):
    return subprocess.run(['./emcp.sh',tool,json.dumps(args,ensure_ascii=False)],capture_output=True,text=True).stdout
d=json.load(open('comp_footer.json'))
x=d['xml_structure']; C=d['element_config']; S=d['style']
# fila de comunidades entre "Pie columnas" y "Pie inferior"
links=''.join(f'<e-paragraph configuration-id="Pie ccaa {i}"></e-paragraph>' for i in range(len(CCAA)))
row=f'<e-flexbox configuration-id="Pie zonas"><e-paragraph configuration-id="Pie zonas t"></e-paragraph><e-flexbox configuration-id="Pie zonas lista">{links}</e-flexbox></e-flexbox>'
assert '<e-flexbox configuration-id="Pie inferior">' in x
x=x.replace('<e-flexbox configuration-id="Pie inferior">',row+'<e-flexbox configuration-id="Pie inferior">',1)
S["Pie zonas"]="display:flex; flex-direction:column; gap: 10px; width:100%; max-width: 1200px; padding: 28px 0px 28px 0px; border-bottom: 1px solid rgba(255,255,255,0.12);"
C["Pie zonas t"]={"tag":"p","paragraph":"Compramos proindivisos en"}; S["Pie zonas t"]="font-size: 12px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.6);"
S["Pie zonas lista"]="display:flex; flex-direction:row; flex-wrap:wrap; gap: 6px 18px; width:100%; padding:0px;"
for i,(n,s) in enumerate(CCAA):
    C[f"Pie ccaa {i}"]={"tag":"span","paragraph":n,"link":{"destination":f"/vender-proindiviso/{s}/","tag":"a"}}
    S[f"Pie ccaa {i}"]="font-size: 14px; color: rgba(255,255,255,0.78); text-decoration:none; &:hover { color: var(--brand-accent); }"
d['xml_structure']=x
if __name__=='__main__':
    out=emcp('elementor-manage-site-parts',{"operations":[{"action":"create","type":"footer","title":"Pie v3","conditions":[]}]})
    print(out[:400])
    m=re.search(r'"post_id":\s*(\d+)',out) or re.search(r'"id":\s*(\d+)',out)
    pid=int(m.group(1)); d['post_id']=pid; d['mode']='replace_children'
    json.dump(d,open('comp_footer_v3.json','w'),ensure_ascii=False)
    out=emcp('elementor-build-composition',d); print('build', '"success":true' in out, out[:300] if '"success":true' not in out else '')
    out=emcp('elementor-publish-document',{"post_id":pid}); print('publish',out[:200])
    print('NEW FOOTER',pid,'-> luego borrar 105 con manage-site-parts delete')
