"""Reemplazo de textos en páginas ya construidas sin recomponerlas (Elementor): str_replace en _elementor_data (texto literal y escapado en
JSON), en post_content y en la metadescripción de Yoast; borra _elementor_element_cache y limpia la caché de CSS de Elementor.
Uso: python3 reemplazar.py pares.json ID [ID...]      (pares.json = [["texto viejo", "texto nuevo"], ...])
Lo hace un snippet de un solo uso (se crea, se ejecuta con una petición anónima y se borra); el registro queda en la opción zp_reemplazo_log.
Sirve también para entradas programadas (no las publica). Úsalo solo para cambios de texto: los cambios de estructura, con el constructor."""
import json, subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(l.strip().split('=', 1) for l in open(os.path.join(HERE, 'wp.env')) if '=' in l)
pares = json.load(open(sys.argv[1])); ids = [int(x) for x in sys.argv[2:]]
def curl(*a): return subprocess.run(['curl', '-sS', '-u', env['P1']] + list(a), capture_output=True, text=True).stdout
curl('-X', 'POST', '-H', 'Content-Type: application/json', env['WP'] + '/wp-json/zp/v1/option/zp_reemplazo', '-d', json.dumps({'value': {'ids': ids, 'pairs': pares}}, ensure_ascii=False), '-o', '/dev/null')
tag = int(time.time())
PHP = ("add_action( 'init', function () { if ( get_option( 'zp_reemplazo_hecho_%d' ) ) { return; } $cfg = get_option( 'zp_reemplazo' ); if ( ! is_array( $cfg ) ) { return; } update_option( 'zp_reemplazo_hecho_%d', 1, false ); wp_set_current_user( 1 ); global $wpdb; $log = [];"
       " foreach ( $cfg['ids'] as $id ) { $n = 0; $data = get_post_meta( $id, '_elementor_data', true ); $md = get_post_meta( $id, '_yoast_wpseo_metadesc', true ); $pc = get_post_field( 'post_content', $id );"
       " foreach ( $cfg['pairs'] as $p ) { foreach ( [ [ $p[0], $p[1] ], [ substr( wp_json_encode( $p[0] ), 1, -1 ), substr( wp_json_encode( $p[1] ), 1, -1 ) ], [ substr( json_encode( $p[0] ), 1, -1 ), substr( json_encode( $p[1] ), 1, -1 ) ] ] as $q ) {"
       " $c = 0; $data = str_replace( $q[0], $q[1], $data, $c ); $n += $c; $md = str_replace( $q[0], $q[1], (string) $md ); $pc = str_replace( $q[0], $q[1], $pc ); } }"
       " if ( $n ) { update_post_meta( $id, '_elementor_data', wp_slash( $data ) ); if ( $md ) { update_post_meta( $id, '_yoast_wpseo_metadesc', $md ); } delete_post_meta( $id, '_elementor_element_cache' ); $wpdb->update( $wpdb->posts, [ 'post_content' => $pc ], [ 'ID' => $id ] ); clean_post_cache( $id ); }"
       " $log[ $id ] = $n; } update_option( 'zp_reemplazo_log', $log, false ); if ( class_exists( '\\\\Elementor\\\\Plugin' ) ) { \\Elementor\\Plugin::$instance->files_manager->clear_cache(); } } );") % (tag, tag)
d = json.loads(curl('-X', 'POST', '-H', 'Content-Type: application/json', env['WP'] + '/wp-json/code-snippets/v1/snippets', '-d', json.dumps({'name': 'ZP una vez — reemplazo de textos', 'code': PHP, 'scope': 'global', 'active': True, 'priority': 10})))
subprocess.run(['curl', '-sS', '-o', '/dev/null', env['WP'] + f'/?zrun={tag}']); time.sleep(3)
print('reemplazos por página:', curl(env['WP'] + '/wp-json/zp/v1/option/zp_reemplazo_log'))
curl('-X', 'DELETE', env['WP'] + f"/wp-json/code-snippets/v1/snippets/{d['id']}?force=true", '-o', '/dev/null')
