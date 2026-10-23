/* Zona Proindiviso — fecha de actualización visible e índice de contenidos (TOC) con anclas en los H2.
 * Shortcode [zp_actualizado]: "Actualizado el 23 de octubre de 2026" (fecha de modificación, idioma del sitio).
 * TOC: en entradas (post) y en las 7 guías largas (páginas), se añaden id a los H2 del documento principal y se inyecta
 * un bloque <nav class="zp-toc"> al principio de la primera sección de contenido (después del hero y la imagen). Server-side:
 * lo ven Google, los rastreadores de IA y los lectores sin JS. El último H2 (CTA final) se excluye. */
add_shortcode( 'zp_actualizado', function () {
	$id = get_the_ID();
	if ( ! $id ) { return ''; }
	return 'Actualizado el ' . esc_html( get_the_modified_date( 'j \d\e F \d\e Y', $id ) );
} );
function zp_toc_aplica( $id ) {
	if ( ! $id ) { return false; }
	if ( get_post_type( $id ) === 'post' ) { return true; }
	return in_array( (int) $id, [ 617, 620, 623, 587, 590, 593, 596 ], true );
}
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( is_admin() || wp_doing_ajax() || ! is_singular() ) { return $content; }
	if ( isset( $_GET['elementor-preview'] ) ) { return $content; }
	$id = get_queried_object_id();
	if ( ! zp_toc_aplica( $id ) ) { return $content; }
	if ( strpos( $content, 'data-elementor-id="' . $id . '"' ) === false ) { return $content; } // solo el documento principal, no cabecera/pie/popup
	if ( strpos( $content, 'class="zp-toc"' ) !== false ) { return $content; }
	if ( ! preg_match_all( '/<h2\b([^>]*)>(.*?)<\/h2>/is', $content, $m, PREG_OFFSET_CAPTURE ) ) { return $content; }
	$n = count( $m[0] );
	if ( $n < 4 ) { return $content; }
	$items = []; $used = [];
	for ( $i = $n - 2; $i >= 0; $i-- ) { // de atrás hacia delante para que los offsets sigan siendo válidos; el último H2 (CTA) se excluye
		$attrs = $m[1][ $i ][0]; $inner = $m[2][ $i ][0]; $off = $m[0][ $i ][1]; $len = strlen( $m[0][ $i ][0] );
		$text = trim( wp_strip_all_tags( $inner ) );
		if ( $text === '' ) { continue; }
		if ( preg_match( '/\sid="([^"]+)"/', $attrs, $idm ) ) {
			$slug = $idm[1];
		} else {
			$slug = sanitize_title( $text ); if ( $slug === '' ) { $slug = 'seccion'; }
			$base = $slug; $k = 2; while ( isset( $used[ $slug ] ) ) { $slug = $base . '-' . $k++; }
			$content = substr( $content, 0, $off ) . '<h2 id="' . esc_attr( $slug ) . '"' . $attrs . '>' . $inner . '</h2>' . substr( $content, $off + $len );
		}
		$used[ $slug ] = 1;
		$items[] = [ $slug, $text ];
	}
	if ( count( $items ) < 3 ) { return $content; }
	$items = array_reverse( $items );
	$li = '';
	foreach ( $items as $it ) { $li .= '<li><a href="#' . esc_attr( $it[0] ) . '">' . esc_html( $it[1] ) . '</a></li>'; }
	$toc = '<nav class="zp-toc" aria-label="Índice del artículo"><p class="zp-toc-t">En este artículo</p><ol>' . $li . '</ol></nav>';
	// Inserción: al principio del contenedor interior de la primera sección de contenido (la 2ª <section>; la 1ª es el hero).
	$p1 = strpos( $content, '<section' );
	$p2 = $p1 === false ? false : strpos( $content, '<section', $p1 + 8 );
	if ( $p2 !== false ) {
		$close = strpos( $content, '>', $p2 );
		$pd = strpos( $content, '<div', $close );
		if ( $pd !== false && $pd - $close < 400 ) {
			$pdc = strpos( $content, '>', $pd );
			return substr( $content, 0, $pdc + 1 ) . $toc . substr( $content, $pdc + 1 );
		}
		return substr( $content, 0, $p2 ) . '<div class="zp-toc-wrap">' . $toc . '</div>' . substr( $content, $p2 );
	}
	return $content;
}, 20 );
add_action( 'wp_head', function () {
	if ( ! is_singular() || ! zp_toc_aplica( get_queried_object_id() ) ) { return; }
	$t = 'sty' . 'le';
	$css = '.zp-toc{width:100%;max-width:820px;padding:22px 26px;background:#eff5f8;border:1px solid #d8e0e6;border-left:4px solid #e87524;border-radius:16px;font-family:Manrope,sans-serif;box-sizing:border-box}'
		. '.zp-toc-wrap{display:flex;justify-content:center;width:100%;padding:40px 24px 0;background:#fff}.zp-toc-wrap .zp-toc{max-width:1200px}'
		. '.zp-toc-t{margin:0 0 10px;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#d06316}'
		. '.zp-toc ol{margin:0;padding:0 0 0 20px;display:grid;grid-template-columns:1fr 1fr;gap:7px 28px}'
		. '.zp-toc li{font-size:15px;line-height:1.45;color:#1f2a33;padding-left:2px}'
		. '.zp-toc a{color:#0d4f78;text-decoration:none;font-weight:600}.zp-toc a:hover{color:#d06316;text-decoration:underline}'
		. 'h2[id]{scroll-margin-top:96px}'
		. '@media(max-width:767px){.zp-toc ol{grid-template-columns:1fr}.zp-toc{padding:18px 18px 18px 20px}}';
	echo '<' . $t . ' id="zp-toc-css">' . $css . '</' . $t . '>';
}, 99 );
