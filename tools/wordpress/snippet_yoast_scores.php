/* Zona Proindiviso — puntuaciones de Yoast (SEO y legibilidad) escribibles por REST.
 * _yoast_wpseo_linkdex (0-100) y _yoast_wpseo_content_score (0-100) son las que pintan el semáforo en el listado y el editor.
 * Las calcula tools/wordpress/yoastqa.py con la propia librería yoastseo (investigador español) sobre el HTML del documento de Elementor. */
add_action( 'init', function () {
	foreach ( [ 'post', 'page' ] as $pt ) {
		foreach ( [ '_yoast_wpseo_linkdex', '_yoast_wpseo_content_score', '_yoast_wpseo_inclusive_language_score', '_yoast_wpseo_bctitle' ] as $k ) {
			register_post_meta( $pt, $k, [ 'show_in_rest' => true, 'single' => true, 'type' => 'string', 'default' => '', 'sanitize_callback' => 'sanitize_text_field', 'auth_callback' => function () { return current_user_can( 'edit_posts' ); } ] );
		}
		// Yoast Premium: sinónimos (JSON: ["..."]) y keyphrases relacionadas (JSON: [{"keyword":"...","score":""}]) — se guardan como texto JSON, sin sanitize_text_field (rompería las comillas)
		foreach ( [ '_yoast_wpseo_keywordsynonyms', '_yoast_wpseo_focuskeywords' ] as $k ) {
			register_post_meta( $pt, $k, [ 'show_in_rest' => true, 'single' => true, 'type' => 'string', 'default' => '', 'sanitize_callback' => function ( $v ) { return is_string( $v ) ? wp_kses( $v, [] ) : ''; }, 'auth_callback' => function () { return current_user_can( 'edit_posts' ); } ] );
		}
	}
}, 99 );
