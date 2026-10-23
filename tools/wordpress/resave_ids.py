"""Regraba documentos de Elementor por ID (regla 4.1: tras build-composition + publish, el CSS local no coincide con el HTML
hasta que el documento se vuelve a guardar con la API de Elementor). Uso: python3 resave_ids.py 14 23 55 ...  (lotes de 40)."""
import sys, os, json, subprocess, time
HERE=os.path.dirname(os.path.abspath(__file__))
env={}
for l in open(os.path.join(HERE,'wp.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip()
WP=env['WP']; AUTH=env['P1']
PHP=r'''add_action( 'init', function () {
	if ( ! class_exists( '\Elementor\Plugin' ) ) { return; }
	wp_set_current_user( 1 ); // Document::save() exige permiso de edición; en init aún no hay usuario autenticado (REST_REQUEST se define después)
	$ids = %s; $t0 = microtime( true ); $log = (array) get_option( 'zp_resave3_log', [] );
	foreach ( $ids as $id ) {
		if ( microtime( true ) - $t0 > 50 ) { $log[] = "$id: sin tiempo"; continue; }
		try {
			$doc = \Elementor\Plugin::$instance->documents->get( $id, false );
			if ( ! $doc ) { $log[] = "$id: sin documento"; continue; }
			$data = $doc->get_elements_data();
			if ( empty( $data ) ) { $log[] = "$id: vacío"; continue; }
			$payload = [ 'elements' => $data, 'settings' => $doc->get_settings() ];
			try { $doc->save( $payload ); $log[] = "$id: save"; }
			catch ( \Throwable $e ) { do_action( 'elementor/document/after_save', $doc, $payload ); $log[] = "$id: after_save (" . substr( $e->getMessage(), 0, 60 ) . ")"; } // la validación atómica rechaza algún párrafo en algunos documentos: con after_save se regenera el CSS local igualmente
		} catch ( \Throwable $e ) { $log[] = "$id: EXC " . substr( $e->getMessage(), 0, 80 ); }
	}
	update_option( 'zp_resave3_log', array_slice( $log, -400 ) );
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}, 20 );'''
def api(method,path,body=None):
    args=['curl','-sS','--max-time','120','-u',AUTH,'-X',method,'-H','Content-Type: application/json',WP+'/wp-json'+path]
    if body is not None: args+=['-d',json.dumps(body,ensure_ascii=False)]
    out=subprocess.run(args,capture_output=True,text=True).stdout
    try: return json.loads(out)
    except Exception: return {'_raw':out[:300]}
def trigger():
    # Petición AUTENTICADA (admin): Document::save() exige un usuario con permiso de edición; una visita anónima no regraba nada.
    subprocess.run(['curl','-sS','-o','/dev/null','--max-time','170','-u',AUTH,f'{WP}/wp-json/wp/v2/users/me?r={time.time()}'],capture_output=True)
    time.sleep(1)
def resave(ids):
    ids=[int(x) for x in ids]
    for i in range(0,len(ids),25):
        batch=ids[i:i+25]
        code=PHP % json.dumps(batch)
        r=api('POST','/code-snippets/v1/snippets',{"name":f"ZP una vez — regrabar {len(batch)} documentos","desc":"Regraba documentos por ID (lote).","code":code,"tags":["zona-proindiviso"],"scope":"single-use","active":True,"priority":10})
        if 'id' not in r: print('SNIPPET FAIL',r); return False
        trigger()
        api('DELETE',f"/code-snippets/v1/snippets/{r['id']}?force=true")  # el snippet de un solo uso ya se ejecutó: se borra para no acumular basura
        print('lote',i//25+1,'ids',batch[0],'..',batch[-1],flush=True)
    return True
if __name__=='__main__':
    resave(sys.argv[1:])
