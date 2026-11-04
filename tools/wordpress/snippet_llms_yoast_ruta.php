// Yoast escribe su llms.txt (más pobre) en uploads/zp-yoast-llms/ en lugar de la raíz: así la opción enable_llms_txt queda activa
// (tarea de Yoast completada) y el /llms.txt dinámico del snippet 166 sigue siendo el que se sirve.
add_filter( 'wpseo_llmstxt_filesystem_path', function () {
	$u = wp_upload_dir(); $d = trailingslashit( $u['basedir'] ) . 'zp-yoast-llms';
	if ( ! is_dir( $d ) ) { wp_mkdir_p( $d ); }
	return $d;
} );
