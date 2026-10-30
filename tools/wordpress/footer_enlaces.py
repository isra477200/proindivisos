"""Añade enlaces a una columna del pie (site part 684) SIN reconstruirlo: build-composition en modo append bajo el flexbox de la
columna, así los elementos existentes conservan sus clases generadas (la pestaña fija «Te llamamos» tiene un arreglo CSS por clase
en el snippet 45). Uso: python3 footer_enlaces.py  (idempotente: no repite enlaces ya presentes en el pie).
OJO (24/10/2026): sobre un documento publicado, build-composition escribe en un autoguardado y publish-document no lo publica; además
el pie tiene caché de elementos (_elementor_element_cache, 24 h). Tras el build, este script ejecuta un snippet de un solo uso que
guarda el autoguardado como versión publicada, borra _elementor_element_cache y limpia el CSS."""
import json, subprocess, re, urllib.request
COL='60f130d4'  # «Pie col 3» (Guías) en el pie 684
NUEVOS=[("Calculadora: cuánto vale tu parte","/cuanto-vale-mi-parte-de-un-piso/"),("Simulador de extinción de condominio","/simulador-extincion-de-condominio/"),("Diccionario del proindiviso","/diccionario-del-proindiviso/"),("Impuestos por comunidad","/impuestos-del-proindiviso/"),("Modelos de documentos","/modelos-documentos-proindiviso/"),("Preguntas frecuentes","/preguntas-frecuentes-proindiviso/")]
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
    import time
    env=dict(l.strip().split('=',1) for l in open('wp.env') if '=' in l)
    PHP=("add_action( 'init', function () { if ( get_option( 'zp_pie_pub_%d' ) ) { return; } if ( ! class_exists( '\\Elementor\\Plugin' ) ) { return; }"
         " wp_set_current_user( 1 ); update_option( 'zp_pie_pub_%d', 1, false ); $doc = \\Elementor\\Plugin::$instance->documents->get( 684, false );"
         " $a = $doc->get_newer_autosave(); if ( $a ) { $doc->save( [ 'elements' => $a->get_elements_data(), 'settings' => $doc->get_settings() ] ); wp_delete_post( $a->get_post()->ID, true ); }"
         " delete_post_meta( 684, '_elementor_element_cache' ); \\Elementor\\Plugin::$instance->files_manager->clear_cache(); } );") % (int(time.time()),int(time.time()))
    body={"name":"ZP una vez — pie: publicar y limpiar caché","code":PHP,"scope":"global","active":True,"priority":10}
    d=json.loads(subprocess.run(['curl','-sS','-u',env['P1'],'-X','POST','-H','Content-Type: application/json',f"{env['WP']}/wp-json/code-snippets/v1/snippets",'-d',json.dumps(body)],capture_output=True,text=True).stdout)
    subprocess.run(['curl','-sS','-o','/dev/null',f"{env['WP']}/?zrun={time.time()}"]); time.sleep(3)
    subprocess.run(['curl','-sS','-u',env['P1'],'-X','DELETE',f"{env['WP']}/wp-json/code-snippets/v1/snippets/{d['id']}?force=true",'-o','/dev/null'])
