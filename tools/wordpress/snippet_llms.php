<?php
/* Zona Proindiviso — /llms.txt servido por WordPress (snippet global).
 * Yoast Premium no consigue escribir el archivo físico en Hostinger (quedaba en 404), así que se sirve dinámicamente:
 * home, páginas de intención, guías, comunidades y provincias (las ciudades se enlazan desde su provincia), entradas y legales,
 * con la descripción de Yoast de cada una. Formato llmstxt.org. Caché en transitorio de 12 h; se invalida al guardar cualquier entrada/página. */
add_action( 'template_redirect', function () {
	$path = strtok( $_SERVER['REQUEST_URI'] ?? '', '?' );
	if ( $path !== '/llms.txt' ) { return; }
	$out = get_transient( 'zp_llms_txt' );
	if ( ! $out ) { $out = zp_llms_build(); set_transient( 'zp_llms_txt', $out, 12 * HOUR_IN_SECONDS ); }
	status_header( 200 ); nocache_headers();
	header( 'Content-Type: text/plain; charset=utf-8' ); header( 'Cache-Control: public, max-age=3600' ); header( 'X-Robots-Tag: noindex' );
	echo $out; exit;
}, 0 );
add_action( 'save_post', function () { delete_transient( 'zp_llms_txt' ); } );
function zp_llms_desc( $id ) {
	$d = trim( (string) get_post_meta( $id, '_yoast_wpseo_metadesc', true ) );
	if ( $d === '' ) { $d = trim( wp_strip_all_tags( get_the_excerpt( $id ) ) ); }
	return preg_replace( '/\s+/', ' ', $d );
}
function zp_llms_line( $id ) {
	$t = html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ); $d = zp_llms_desc( $id );
	return '- [' . $t . '](' . get_permalink( $id ) . ')' . ( $d !== '' ? ': ' . $d : '' ) . "\n";
}
function zp_llms_build() {
	$home = 23; $hub = 55; $dicp = get_page_by_path( 'diccionario-del-proindiviso' ); $dic = $dicp ? (int) $dicp->ID : 0; $contacto = 57; $legales = [ 59, 61, 63 ]; $guias = [ 51, 43, 53, 617, 620, 623, 587, 590, 593, 596 ];
	$zp_id = function ( $slug ) { $p = get_page_by_path( $slug ); return ( $p && $p->post_status === 'publish' ) ? (int) $p->ID : 0; };
	$secc = array_filter( [ 'impuestos-del-proindiviso' => [ $zp_id( 'impuestos-del-proindiviso' ), 'Impuestos del proindiviso por comunidad autónoma (AJD, ITP, sucesiones, plusvalía e IRPF)' ], 'modelos-documentos-proindiviso' => [ $zp_id( 'modelos-documentos-proindiviso' ), 'Modelos de documentos para copropietarios (para copiar o descargar en Word)' ] ], function ( $x ) { return $x[0] > 0; } );
	$herr = array_values( array_filter( array_map( $zp_id, [ 'cuanto-vale-mi-parte-de-un-piso', 'simulador-extincion-de-condominio', 'calculadora-impuestos-vender-tu-parte', 'calculadora-compensacion-uso-exclusivo', 'calculadora-gastos-entre-copropietarios', 'preguntas-frecuentes-proindiviso' ] ) ) );
	$fuera = array_merge( $herr, array_map( function ( $x ) { return $x[0]; }, array_values( $secc ) ) );
	$o  = "# Zona Proindiviso\n\n";
	$o .= "> Compramos tu parte de un piso, casa, local o terreno en proindiviso en toda España: pago al contado en notaría, oferta por escrito en 48 horas, sin necesidad del acuerdo del resto de copropietarios y con los gastos a nuestro cargo. También compramos derechos hereditarios y cuotas con hipoteca, inquilino u ocupante.\n\n";
	$o .= "Sitio: " . home_url( '/' ) . " · Idioma: español (España) · Contacto: " . get_permalink( $contacto ) . "\n\n";
	$o .= "## Qué hacemos\n\n" . zp_llms_line( $home );
	$int = get_posts( [ 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1, 'post_parent' => 0, 'post__not_in' => array_merge( [ $home, $hub, $contacto, 680, 1359, $dic ], $legales, $guias, $fuera ), 'orderby' => 'menu_order title', 'order' => 'ASC' ] );
	foreach ( $int as $p ) { $o .= zp_llms_line( $p->ID ); }
	$o .= "\n## Guías\n\n";
	foreach ( $guias as $id ) { if ( get_post_status( $id ) === 'publish' ) { $o .= zp_llms_line( $id ); } }
	if ( $dic && get_post_status( $dic ) === 'publish' ) {
		$o .= "\n## Diccionario del proindiviso (un término por página)\n\n" . zp_llms_line( $dic );
		foreach ( get_posts( [ 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1, 'post_parent' => $dic, 'orderby' => 'title', 'order' => 'ASC' ] ) as $t ) { $o .= zp_llms_line( $t->ID ); }
	}
	if ( $herr ) { $o .= "\n## Herramientas y preguntas frecuentes\n\n"; foreach ( $herr as $id ) { $o .= zp_llms_line( $id ); } }
	foreach ( $secc as $x ) {
		$o .= "\n## " . $x[1] . "\n\n" . zp_llms_line( $x[0] );
		foreach ( get_posts( [ 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1, 'post_parent' => $x[0], 'orderby' => 'title', 'order' => 'ASC' ] ) as $t ) { $o .= zp_llms_line( $t->ID ); }
	}
	$o .= "\n## Dónde compramos (comunidades y provincias; cada provincia enlaza a sus municipios)\n\n" . zp_llms_line( $hub );
	$ccaa = get_posts( [ 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1, 'post_parent' => $hub, 'orderby' => 'title', 'order' => 'ASC' ] );
	$uni = [ 'madrid', 'murcia', 'asturias', 'cantabria', 'navarra', 'la-rioja', 'baleares', 'ceuta', 'melilla' ]; // uniprovinciales: sus hijas son ciudades, no provincias
	foreach ( $ccaa as $c ) {
		$o .= zp_llms_line( $c->ID );
		if ( in_array( $c->post_name, $uni, true ) ) { continue; }
		$prov = get_posts( [ 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1, 'post_parent' => $c->ID, 'orderby' => 'title', 'order' => 'ASC' ] );
		foreach ( $prov as $p ) { $o .= '  ' . zp_llms_line( $p->ID ); }
	}
	$o .= "\n## Blog\n\n";
	$posts = get_posts( [ 'post_type' => 'post', 'post_status' => 'publish', 'posts_per_page' => -1, 'orderby' => 'date', 'order' => 'DESC' ] );
	foreach ( $posts as $p ) { $o .= zp_llms_line( $p->ID ); }
	$o .= "\n## Legal\n\n";
	foreach ( $legales as $id ) { $o .= zp_llms_line( $id ); }
	$o .= "\n## Fuentes normativas que citamos\n\n- Código Civil, arts. 392-406 (comunidad de bienes) y 1062 (adjudicación de cosa indivisible): https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763\n- Ley de Enjuiciamiento Civil, arts. 643-675 (subasta): https://www.boe.es/buscar/act.php?id=BOE-A-2000-323\n";
	return $o;
}
