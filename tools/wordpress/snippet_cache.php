<?php
/* Zona Proindiviso — caché de HTML corta con purga automática (snippet 21, global). Sustituye a «sin caché LiteSpeed de HTML».
 * Antes el HTML iba siempre con no-cache (la CDN de Hostinger había servido una copia vieja de la instalación por defecto) y el documento
 * raíz tardaba ~1 s en móvil. Ahora:
 *   - Visitante anónimo, GET, sin query string, página normal (no 404, no búsqueda, no vista previa): LiteSpeed y la CDN pueden guardar el
 *     HTML 10 minutos (X-LiteSpeed-Cache-Control: public,max-age=600; Cache-Control: public, max-age=0, s-maxage=600 → el navegador
 *     revalida siempre, solo cachean servidor y CDN). La caché varía por la cookie de sesión de WordPress, así los administradores
 *     nunca reciben la copia anónima (y la capa de datos usuario_admin sigue siendo fiable).
 *   - Usuario conectado, admin, REST, POST, query string, 404, búsqueda o vista previa de Elementor: no-cache, como antes.
 *   - Purga: al guardar cualquier entrada/página/plantilla, al cambiar un snippet o un menú, se manda X-LiteSpeed-Purge: * en esa misma
 *     respuesta y se deja una marca para repetirla en la siguiente petición pública (por si la primera no pasó por LiteSpeed).
 *     La CDN (hcdn) no se puede purgar desde aquí: como mucho 10 minutos de retraso tras un cambio. */
function zp_cache_marcar_purga() { update_option( 'zp_purga_pendiente', time(), false ); if ( ! headers_sent() ) { header( 'X-LiteSpeed-Purge: *' ); } }
foreach ( [ 'save_post', 'deleted_post', 'elementor/document/after_save', 'elementor/core/files/clear_cache', 'wp_update_nav_menu', 'code_snippets/update_snippet', 'code_snippets/create_snippet', 'code_snippets/activate_snippet', 'code_snippets/deactivate_snippet', 'update_option_zp_telefono', 'update_option_zp_whatsapp' ] as $h ) { add_action( $h, 'zp_cache_marcar_purga', 10, 0 ); }
add_action( 'send_headers', function () {
	if ( headers_sent() ) { return; }
	$pend = (int) get_option( 'zp_purga_pendiente', 0 );
	if ( $pend && time() - $pend < 900 ) { header( 'X-LiteSpeed-Purge: *' ); if ( ! is_user_logged_in() ) { delete_option( 'zp_purga_pendiente' ); } }
	$metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';
	$uri    = $_SERVER['REQUEST_URI'] ?? '/';
	$cacheable = $metodo === 'GET' && ! is_user_logged_in() && ! is_admin() && strpos( $uri, '?' ) === false && strpos( $uri, '/wp-json/' ) === false && strpos( $uri, '/wp-login' ) === false && empty( $_COOKIE[ 'wordpress_logged_in_' . COOKIEHASH ] ) && empty( $_COOKIE['comment_author_' . COOKIEHASH] );
	if ( $cacheable ) {
		header( 'X-LiteSpeed-Cache-Control: public,max-age=600' );
		header( 'X-LiteSpeed-Vary: cookie=wordpress_logged_in_' . COOKIEHASH );
		header( 'Cache-Control: public, max-age=0, s-maxage=600' );
		header( 'Vary: Cookie' );
	} else {
		header( 'X-LiteSpeed-Cache-Control: no-cache' );
		if ( ! is_admin() ) { header( 'Cache-Control: no-cache, no-store, must-revalidate, max-age=0' ); }
	}
}, 1 );
// 404, búsqueda y vista previa se deciden después de send_headers: se corrigen en template_redirect.
add_action( 'template_redirect', function () {
	if ( headers_sent() ) { return; }
	if ( is_404() || is_search() || isset( $_GET['elementor-preview'] ) || is_preview() ) { header( 'X-LiteSpeed-Cache-Control: no-cache' ); header( 'Cache-Control: no-cache, no-store, must-revalidate, max-age=0' ); }
}, 0 );
add_action( 'rest_api_init', function () { if ( ! headers_sent() ) { header( 'X-LiteSpeed-Cache-Control: no-cache' ); } } );
