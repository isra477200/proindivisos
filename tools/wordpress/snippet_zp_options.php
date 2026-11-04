<?php
// Snippet 135 (Code Snippets, global, solo admin): lectura/escritura de opciones por REST para configurar Yoast (Premium) desde fuera del panel.
// GET  /wp-json/zp/v1/option/<nombre>              → valor de la opción
// POST /wp-json/zp/v1/option/<nombre> {k: v, ...}  → en opciones de Yoast (wpseo*) usa WPSEO_Options::set() clave a clave; en el resto, array_merge o {"value": ...}
// POST /wp-json/zp/v1/redirect {"origin": "/vieja/", "target": "/nueva/", "type": 301} → redirección en el gestor de Yoast Premium
add_action( 'rest_api_init', function () {
	$admin = function () { return current_user_can( 'manage_options' ); };
	register_rest_route( 'zp/v1', '/option/(?P<name>[a-zA-Z0-9_\-]+)', [
		[ 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) { return rest_ensure_response( get_option( $r['name'] ) ); } ],
		[ 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$name = $r['name']; $body = $r->get_json_params(); $cur = get_option( $name );
			if ( ! is_array( $body ) ) { return new WP_Error( 'zp_body', 'JSON esperado', [ 'status' => 400 ] ); }
			if ( strpos( $name, 'wpseo' ) === 0 && class_exists( 'WPSEO_Options' ) ) {
				$res = [];
				foreach ( $body as $k => $v ) { $res[ $k ] = WPSEO_Options::set( $k, $v, $name ); }
				return rest_ensure_response( [ 'set' => $res, 'option' => get_option( $name ) ] );
			}
			if ( array_key_exists( 'value', $body ) && count( $body ) === 1 ) { update_option( $name, $body['value'] ); }
			else { update_option( $name, is_array( $cur ) ? array_merge( $cur, $body ) : $body ); }
			return rest_ensure_response( get_option( $name ) );
		} ],
	] );
	register_rest_route( 'zp/v1', '/redirect', [ 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
		$b = $r->get_json_params();
		if ( ! class_exists( 'WPSEO_Redirect_Manager' ) || ! class_exists( 'WPSEO_Redirect' ) ) { return new WP_Error( 'zp_premium', 'Yoast Premium no disponible', [ 'status' => 500 ] ); }
		$mgr = new WPSEO_Redirect_Manager();
		$redirect = new WPSEO_Redirect( $b['origin'], $b['target'] ?? '', (int) ( $b['type'] ?? 301 ), WPSEO_Redirect_Formats::PLAIN );
		$ok = $mgr->create_redirect( $redirect );
		return rest_ensure_response( [ 'ok' => (bool) $ok, 'origin' => $redirect->get_origin(), 'target' => $redirect->get_target(), 'type' => $redirect->get_type() ] );
	} ] );
} );
