// Enlaces a entradas programadas: hasta que una entrada se publica, su URL da 404. Este filtro convierte en texto (span con las mismas
// clases) cualquier enlace del contenido que apunte a una entrada programada o en borrador, y lo vuelve a dejar como enlace solo cuando
// la entrada se publica (lista de rutas en caché 10 min; se vacía al cambiar el estado de cualquier entrada).
function zp_rutas_no_publicadas() {
	$c = get_transient( 'zp_rutas_no_pub' );
	if ( is_array( $c ) ) { return $c; }
	$r = [];
	foreach ( get_posts( [ 'post_type' => 'post', 'post_status' => [ 'future', 'draft', 'pending' ], 'posts_per_page' => -1 ] ) as $p ) {
		if ( $p->post_name ) { $r[] = '/blog/' . $p->post_name . '/'; }
	}
	set_transient( 'zp_rutas_no_pub', $r, 10 * MINUTE_IN_SECONDS );
	return $r;
}
add_action( 'transition_post_status', function () { delete_transient( 'zp_rutas_no_pub' ); } );
function zp_desenlazar_programadas( $content ) {
	if ( is_admin() || strpos( $content, '/blog/' ) === false ) { return $content; }
	$rutas = zp_rutas_no_publicadas();
	if ( ! $rutas ) { return $content; }
	$lt = chr( 60 );
	return preg_replace_callback( '/' . $lt . 'a\b([^>]*)\bhref="([^"]+)"([^>]*)>(.*?)' . $lt . '\/a>/is', function ( $m ) use ( $rutas, $lt ) {
		$path = wp_parse_url( $m[2], PHP_URL_PATH );
		if ( ! $path || ! in_array( trailingslashit( $path ), $rutas, true ) ) { return $m[0]; }
		$cls = preg_match( '/\bclass="([^"]*)"/', $m[1] . ' ' . $m[3], $c ) ? ' class="' . esc_attr( $c[1] ) . '"' : '';
		return $lt . 'span' . $cls . ' data-zp-pendiente="1">' . $m[4] . $lt . '/span>';
	}, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_desenlazar_programadas', 30 );
add_filter( 'the_content', 'zp_desenlazar_programadas', 110 );
