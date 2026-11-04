<?php
/* Zona Proindiviso — informe SEO semanal por REST (snippet global).
 * GET /wp-json/zp/v1/seo-informe?k=<clave>&dias=28
 * Lee Search Console y GA4 con las credenciales de Site Kit del usuario 1 (sin sesión: sirve para una tarea programada) y devuelve JSON:
 *   periodo actual (28 días que terminan hace 3, porque SC tarda 2-3 días) frente al anterior; totales; consultas con impresiones y CTR bajo
 *   (oportunidades de title); páginas sin impresiones con más de 90 días; páginas que más suben y bajan en clics; leads GA4 por tipo de página
 *   y por lugar; uso de las calculadoras. La clave se guarda en la opción `zp_informe_key` (la fija el que configura; comparación en tiempo constante).
 * Lo consume la tarea programada «Informe SEO semanal zonaproindiviso» (Claude), que redacta propuestas y lo deja en la Bitácora IA de Notion. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'zp/v1', '/seo-informe', [ 'methods' => 'GET', 'callback' => 'zp_seo_informe', 'permission_callback' => function ( $req ) {
		$k = get_option( 'zp_informe_key' ); $q = (string) $req->get_param( 'k' );
		return is_string( $k ) && $k !== '' && hash_equals( $k, $q );
	} ] );
} );
function zp_seo_sitekit( $slug ) {
	wp_set_current_user( 1 );
	$ctx  = new \Google\Site_Kit\Context( GOOGLESITEKIT_PLUGIN_MAIN_FILE );
	$opts = new \Google\Site_Kit\Core\Storage\Options( $ctx );
	$uo   = new \Google\Site_Kit\Core\Storage\User_Options( $ctx, 1 );
	$auth = new \Google\Site_Kit\Core\Authentication\Authentication( $ctx, $opts, $uo );
	return $slug === 'ga' ? new \Google\Site_Kit\Modules\Analytics_4( $ctx, $opts, $uo, $auth ) : new \Google\Site_Kit\Modules\Search_Console( $ctx, $opts, $uo, $auth );
}
function zp_seo_sc_rows( $sc, $ini, $fin, $dim, $limit ) {
	$r = $sc->get_data( 'searchanalytics', [ 'startDate' => $ini, 'endDate' => $fin, 'dimensions' => [ $dim ], 'limit' => $limit ] );
	if ( is_wp_error( $r ) ) { return [ 'error' => $r->get_error_message() ]; }
	$out = [];
	foreach ( (array) $r as $row ) { $row = json_decode( wp_json_encode( $row ), true ); $out[ $row['keys'][0] ] = [ 'clics' => (int) $row['clicks'], 'impresiones' => (int) $row['impressions'], 'ctr' => round( $row['ctr'] * 100, 2 ), 'posicion' => round( $row['position'], 1 ) ]; }
	return $out;
}
function zp_seo_ga_rows( $ga, $ini, $fin, $dims, $metric = 'eventCount', $limit = 1000 ) {
	$r = $ga->get_data( 'report', [ 'startDate' => $ini, 'endDate' => $fin, 'metrics' => [ [ 'name' => $metric ] ], 'dimensions' => array_map( function ( $d ) { return [ 'name' => $d ]; }, $dims ), 'limit' => $limit ] );
	if ( is_wp_error( $r ) ) { return [ 'error' => $r->get_error_message() ]; }
	$out = [];
	foreach ( (array) ( $r->rows ?? [] ) as $row ) { $row = json_decode( wp_json_encode( $row ), true ); $k = array_map( function ( $v ) { return $v['value']; }, $row['dimensionValues'] ); $out[] = [ 'k' => $k, 'v' => (float) $row['metricValues'][0]['value'] ]; }
	return $out;
}
function zp_seo_informe( $req ) {
	$dias = max( 7, min( 90, (int) ( $req->get_param( 'dias' ) ?: 28 ) ) );
	$cache = get_transient( 'zp_seo_informe_' . $dias );
	if ( $cache && ! $req->get_param( 'fresco' ) ) { return $cache; }
	$fin = gmdate( 'Y-m-d', strtotime( '-3 days' ) ); $ini = gmdate( 'Y-m-d', strtotime( "-3 days -" . ( $dias - 1 ) . " days" ) );
	$fin0 = gmdate( 'Y-m-d', strtotime( $ini . ' -1 day' ) ); $ini0 = gmdate( 'Y-m-d', strtotime( $fin0 . " -" . ( $dias - 1 ) . " days" ) );
	$sc = zp_seo_sitekit( 'sc' ); $ga = zp_seo_sitekit( 'ga' );
	$qa = zp_seo_sc_rows( $sc, $ini, $fin, 'query', 500 ); $pa = zp_seo_sc_rows( $sc, $ini, $fin, 'page', 1000 ); $p0 = zp_seo_sc_rows( $sc, $ini0, $fin0, 'page', 1000 );
	$err = [];
	foreach ( [ 'consultas' => $qa, 'paginas' => $pa, 'paginas_anterior' => $p0 ] as $n => $x ) { if ( isset( $x['error'] ) ) { $err[] = $n . ': ' . $x['error']; } }
	$tot = function ( $rows ) { $t = [ 'clics' => 0, 'impresiones' => 0 ]; foreach ( $rows as $k => $r ) { if ( $k === 'error' ) { continue; } $t['clics'] += $r['clics']; $t['impresiones'] += $r['impresiones']; } $t['ctr'] = $t['impresiones'] ? round( $t['clics'] / $t['impresiones'] * 100, 2 ) : 0; return $t; };
	// oportunidades de title: impresiones altas, CTR bajo, posición ≤ 15
	$oport = [];
	foreach ( $qa as $q => $r ) { if ( $q === 'error' ) { continue; } if ( $r['impresiones'] >= 30 && $r['ctr'] < 2 && $r['posicion'] <= 15 ) { $oport[ $q ] = $r; } }
	uasort( $oport, function ( $a, $b ) { return $b['impresiones'] <=> $a['impresiones']; } );
	// páginas publicadas hace más de 90 días sin impresiones
	$viejas = get_posts( [ 'post_type' => [ 'page', 'post' ], 'post_status' => 'publish', 'posts_per_page' => -1, 'date_query' => [ [ 'before' => '90 days ago' ] ], 'fields' => 'ids', 'post__not_in' => [ 59, 61, 63, 1359 ] ] );
	$sin = [];
	foreach ( $viejas as $id ) { $u = get_permalink( $id ); if ( empty( $pa[ $u ] ) && empty( $pa[ untrailingslashit( $u ) ] ) ) { $sin[] = [ 'id' => $id, 'url' => $u, 'titulo' => get_the_title( $id ) ]; } }
	// subidas y bajadas en clics
	$delta = [];
	foreach ( $pa as $u => $r ) { if ( $u === 'error' ) { continue; } $antes = $p0[ $u ]['clics'] ?? 0; $delta[ $u ] = [ 'clics' => $r['clics'], 'antes' => $antes, 'diff' => $r['clics'] - $antes, 'posicion' => $r['posicion'] ]; }
	foreach ( $p0 as $u => $r ) { if ( $u !== 'error' && ! isset( $delta[ $u ] ) ) { $delta[ $u ] = [ 'clics' => 0, 'antes' => $r['clics'], 'diff' => -$r['clics'], 'posicion' => null ]; } }
	uasort( $delta, function ( $a, $b ) { return $b['diff'] <=> $a['diff']; } );
	$top = array_slice( $delta, 0, 10, true ); $bottom = array_slice( array_reverse( $delta, true ), 0, 10, true );
	// GA4: eventos clave por tipo de página y por lugar; calculadoras; canales
	$ev = zp_seo_ga_rows( $ga, $ini, $fin, [ 'eventName', 'customEvent:pagina_tipo' ] );
	$lug = zp_seo_ga_rows( $ga, $ini, $fin, [ 'eventName', 'customEvent:lugar' ] );
	$calc = zp_seo_ga_rows( $ga, $ini, $fin, [ 'eventName', 'customEvent:calculadora' ] );
	$can = zp_seo_ga_rows( $ga, $ini, $fin, [ 'sessionDefaultChannelGroup' ], 'sessions', 20 );
	$claves = [ 'generate_lead', 'llamada', 'whatsapp', 'abrir_formulario', 'calculadora_usada' ];
	$leads_tipo = []; $leads_lugar = []; $uso_calc = [];
	foreach ( ( isset( $ev['error'] ) ? [] : $ev ) as $r ) { if ( in_array( $r['k'][0], $claves, true ) ) { $leads_tipo[ $r['k'][0] ][ $r['k'][1] ?: '(sin)' ] = (int) $r['v']; } }
	foreach ( ( isset( $lug['error'] ) ? [] : $lug ) as $r ) { if ( in_array( $r['k'][0], [ 'generate_lead', 'llamada', 'whatsapp' ], true ) && $r['k'][1] !== '' && $r['k'][1] !== '(not set)' ) { $leads_lugar[ $r['k'][1] ] = ( $leads_lugar[ $r['k'][1] ] ?? 0 ) + (int) $r['v']; } }
	foreach ( ( isset( $calc['error'] ) ? [] : $calc ) as $r ) { if ( $r['k'][0] === 'calculadora_usada' ) { $uso_calc[ $r['k'][1] ?: '(sin)' ] = (int) $r['v']; } }
	arsort( $leads_lugar );
	$out = [
		'generado' => gmdate( 'c' ), 'periodo' => [ 'ini' => $ini, 'fin' => $fin ], 'periodo_anterior' => [ 'ini' => $ini0, 'fin' => $fin0 ], 'errores' => $err,
		'totales' => [ 'actual' => $tot( $pa ), 'anterior' => $tot( $p0 ) ],
		'top_consultas' => array_slice( $qa, 0, 25, true ),
		'oportunidades_title' => array_slice( $oport, 0, 20, true ),
		'paginas_sin_impresiones_90d' => [ 'n' => count( $sin ), 'de' => count( $viejas ), 'lista' => array_slice( $sin, 0, 40 ) ],
		'suben' => $top, 'bajan' => $bottom,
		'ga4' => [ 'leads_por_tipo_pagina' => $leads_tipo, 'leads_por_lugar' => array_slice( $leads_lugar, 0, 20, true ), 'calculadoras' => $uso_calc, 'sesiones_por_canal' => isset( $can['error'] ) ? $can : array_map( function ( $r ) { return [ $r['k'][0] => (int) $r['v'] ]; }, $can ) ],
	];
	set_transient( 'zp_seo_informe_' . $dias, $out, 6 * HOUR_IN_SECONDS );
	return $out;
}
