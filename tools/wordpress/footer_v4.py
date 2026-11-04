import sys, os, json, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
COLS=[("Vender tu parte",[("Cómo trabajamos","/empresas-que-compran-proindivisos/"),("Cuánto pagamos","/cuanto-pagan-por-un-proindiviso/"),("Vender sin avisar","/vender-proindiviso-sin-avisar/"),("Parte de un piso","/vender-parte-de-un-piso/"),("La mitad de una casa","/vender-la-mitad-de-una-casa/"),("Con hipoteca","/vender-proindiviso-con-hipoteca/"),("Nuda propiedad","/vender-nuda-propiedad/"),("Terreno o finca","/vender-terreno-proindiviso/"),("Con inquilino u okupa","/vender-proindiviso-con-inquilino-u-okupa/")]),
("Herencias",[("Parte de una casa heredada","/vender-parte-casa-heredada/"),("Entre hermanos","/vender-proindiviso-entre-hermanos/"),("Compramos herencias","/empresas-que-compran-herencias/"),("Derechos hereditarios","/vender-derechos-hereditarios/"),("Un heredero no quiere vender","/un-heredero-no-quiere-vender/"),("Divorcio y separación","/vender-proindiviso-divorcio/")]),
("Guías",[("Qué es un proindiviso","/que-es-un-proindiviso/"),("Extinción de condominio","/extincion-de-condominio/"),("División de cosa común","/division-de-cosa-comun/"),("Opiniones sobre compradoras","/opiniones-empresas-que-compran-proindivisos/"),("Blog","/blog/")]),
("Dónde compramos",[("Toda España","/vender-proindiviso/"),("Contacto","/contacto/")])]
def emcp(tool,args): return subprocess.run(['./emcp.sh',tool,json.dumps(args,ensure_ascii=False)],capture_output=True,text=True).stdout
d=json.load(open('comp_footer_v3.json')); x=d['xml_structure']; C=d['element_config']; S=d['style']
tstyle=S['Pie col 1 t']; lstyle=S['Pie col 1 link 0']; cstyle=S['Pie col 1'].replace('flex-basis: 170px','flex-basis: 150px')
i=x.find('<e-flexbox configuration-id="Pie col 1">'); j=x.find('</e-flexbox><e-flexbox configuration-id="Pie zonas">')
for k in [k for k in list(C) if k.startswith('Pie col ')]: C.pop(k); S.pop(k,None)
cols=''
for ci,(t,links) in enumerate(COLS,1):
    cols+=f'<e-flexbox configuration-id="Pie col {ci}"><e-paragraph configuration-id="Pie col {ci} t"></e-paragraph>'+''.join(f'<e-paragraph configuration-id="Pie col {ci} link {k}"></e-paragraph>' for k in range(len(links)))+'</e-flexbox>'
    S[f'Pie col {ci}']=cstyle; C[f'Pie col {ci} t']={"tag":"p","paragraph":t}; S[f'Pie col {ci} t']=tstyle
    for k,(lab,url) in enumerate(links): C[f'Pie col {ci} link {k}']={"tag":"span","paragraph":lab,"link":{"destination":url,"tag":"a"}}; S[f'Pie col {ci} link {k}']=lstyle
x=x[:i]+cols+x[j:]
S['Pie columnas']=S['Pie columnas'].replace('gap: 48px','gap: 36px')
d['xml_structure']=x
if __name__=='__main__':
    out=emcp('elementor-manage-site-parts',{"operations":[{"action":"create","type":"footer","title":"Pie v4","conditions":[]}]})
    m=re.search(r'"id":\s*(\d+)',out); pid=int(m.group(1)); d['post_id']=pid; d['mode']='replace_children'
    json.dump(d,open('comp_footer_v4.json','w'),ensure_ascii=False)
    out=emcp('elementor-build-composition',d); ok='"success":true' in out; print('build',ok, '' if ok else out[:300])
    if ok:
        print('publish',emcp('elementor-publish-document',{"post_id":pid})[:80])
        print('delete 544',emcp('elementor-manage-site-parts',{"operations":[{"action":"delete","post_id":544}]})[:120])
    print('NEW FOOTER',pid)
