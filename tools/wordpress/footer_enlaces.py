"""Añade enlaces a una columna del pie (site part 684) SIN reconstruirlo: build-composition en modo append bajo el flexbox de la
columna, así los elementos existentes conservan sus clases generadas (la pestaña fija «Te llamamos» tiene un arreglo CSS por clase
en el snippet 45). Uso: python3 footer_enlaces.py  (idempotente: no repite enlaces ya presentes en el pie)."""
import json, subprocess, re, urllib.request
COL='60f130d4'  # «Pie col 3» (Guías) en el pie 684
NUEVOS=[("Calculadora: cuánto vale tu parte","/cuanto-vale-mi-parte-de-un-piso/"),("Simulador de extinción de condominio","/simulador-extincion-de-condominio/"),("Diccionario del proindiviso","/diccionario-del-proindiviso/")]
STYLE="font-weight:500; font-size:15px; color:rgba(255,255,255,0.88); text-decoration:none; &:hover { color: var(--brand-accent); }"
def emcp(tool,args): return subprocess.run(['./emcp.sh',tool,json.dumps(args,ensure_ascii=False)],capture_output=True,text=True).stdout
html=urllib.request.urlopen('https://zonaproindiviso.com/?zpfoot=1').read().decode('utf8','ignore')
foot=html[html.find('<footer'):]
pend=[(l,u) for l,u in NUEVOS if f'href="{u}"' not in foot and f'href="https://zonaproindiviso.com{u}"' not in foot]
print('pendientes',pend)
if pend:
    x=''.join(f'<e-paragraph configuration-id="Pie col 3 extra {k}"></e-paragraph>' for k in range(len(pend)))
    C={f"Pie col 3 extra {k}":{"tag":"span","paragraph":l,"link":{"destination":u,"tag":"a"}} for k,(l,u) in enumerate(pend)}
    S={f"Pie col 3 extra {k}":STYLE for k in range(len(pend))}
    out=emcp('elementor-build-composition',{"post_id":684,"parent_id":COL,"mode":"append","xml_structure":x,"element_config":C,"style":S})
    print('build','"success":true' in out, out[:300] if '"success":true' not in out else '')
    print('publish',emcp('elementor-publish-document',{"post_id":684})[:100])
