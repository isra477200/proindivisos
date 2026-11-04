<?php
/* Zona Proindiviso — enlaces internos hacia las secciones nuevas del 30/10/2026 sin recomponer páginas (snippet 227, global).
 * Añade un botón al bloque «También te puede interesar» (mismas clases que el primer botón del bloque) en:
 *   - páginas geo (/vender-proindiviso/ y descendientes): «Impuestos en {comunidad}» → /impuestos-del-proindiviso/extincion-de-condominio-{ccaa}/
 *     (en el hub, «Impuestos por comunidad» → /impuestos-del-proindiviso/);
 *   - páginas y entradas de ZP_ENL_MAPA: el enlace indicado (calculadoras 2, modelos, preguntas frecuentes, impuestos).
 * Solo si el destino está publicado (los enlaces aparecen solos cuando se publica la sección) y si la página aún no enlaza a esa URL.
 * 04/11/2026: varios enlaces por página (un valor del mapa puede ser una lista de pares) y secciones nuevas: impuesto de sucesiones por
 * comunidad (geo → «Sucesiones en {comunidad}»; extinción de condominio de cada comunidad → su página de sucesiones; diccionario y blog de
 * herencias → índice de sucesiones), calculadora de nuda propiedad y 6 modelos nuevos (ZP_ENL_MAPA2). */
const ZP_ENL_MAPA = [
	'extincion-de-condominio/impuestos-y-notario' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'simulador-extincion-de-condominio' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'cuanto-vale-mi-parte-de-un-piso' => [ 'Impuestos al vender tu parte', 'calculadora-impuestos-vender-tu-parte' ],
	'division-de-cosa-comun' => [ 'Modelo de requerimiento', 'modelos-documentos-proindiviso/modelo-requerimiento-division-cosa-comun' ],
	'que-es-un-proindiviso' => [ 'Preguntas frecuentes', 'preguntas-frecuentes-proindiviso' ],
	'un-heredero-no-quiere-vender' => [ 'Modelo de burofax', 'modelos-documentos-proindiviso/modelo-burofax-copropietario' ],
	'vender-proindiviso-entre-hermanos' => [ 'Modelo de propuesta de venta', 'modelos-documentos-proindiviso/modelo-propuesta-venta-de-mi-parte' ],
	'vender-proindiviso-sin-avisar' => [ 'Modelo de notificación de venta', 'modelos-documentos-proindiviso/modelo-notificacion-venta-cuota-retracto' ],
	'blog/compensacion-por-uso-exclusivo-de-la-vivienda-comun' => [ 'Calcula tu compensación', 'calculadora-compensacion-uso-exclusivo' ],
	'blog/derecho-a-usar-la-casa-en-proindiviso' => [ 'Calcula tu compensación', 'calculadora-compensacion-uso-exclusivo' ],
	'blog/mi-hermano-vive-en-la-casa-de-mis-padres-y-no-quiere-vender' => [ 'Calcula tu compensación', 'calculadora-compensacion-uso-exclusivo' ],
	'blog/ibi-y-gastos-en-un-proindiviso-quien-paga' => [ 'Calcula el reparto de gastos', 'calculadora-gastos-entre-copropietarios' ],
	'blog/renunciar-a-mi-parte-de-un-proindiviso-para-no-pagar-gastos' => [ 'Calcula el reparto de gastos', 'calculadora-gastos-entre-copropietarios' ],
	'blog/irpf-al-vender-mi-parte-de-un-piso-heredado' => [ 'Calcula tus impuestos', 'calculadora-impuestos-vender-tu-parte' ],
	'blog/plusvalia-municipal-al-vender-mi-parte-heredada' => [ 'Calcula tus impuestos', 'calculadora-impuestos-vender-tu-parte' ],
	'blog/vender-un-piso-heredado-impuestos' => [ 'Calcula tus impuestos', 'calculadora-impuestos-vender-tu-parte' ],
	'blog/extincion-de-condominio-irpf-ganancia-patrimonial' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'blog/itp-al-comprar-la-parte-de-un-piso' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'blog/no-puedo-pagar-el-impuesto-de-sucesiones' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'blog/derecho-de-tanteo-y-retracto-entre-copropietarios' => [ 'Modelo de notificación de venta', 'modelos-documentos-proindiviso/modelo-notificacion-venta-cuota-retracto' ],
	'blog/pacto-de-indivision-que-es-y-cuanto-dura' => [ 'Modelo de pacto de indivisión', 'modelos-documentos-proindiviso/modelo-pacto-de-indivision' ],
	'blog/demanda-de-division-de-cosa-comun-requisitos' => [ 'Modelo de requerimiento', 'modelos-documentos-proindiviso/modelo-requerimiento-division-cosa-comun' ],
	'blog/conciliacion-notarial-para-dividir-un-proindiviso' => [ 'Modelo de requerimiento', 'modelos-documentos-proindiviso/modelo-requerimiento-division-cosa-comun' ],
	'blog/uno-quiere-vender-y-el-otro-no' => [ 'Modelo de burofax', 'modelos-documentos-proindiviso/modelo-burofax-copropietario' ],
	'blog/preguntas-antes-de-vender-tu-parte' => [ 'Preguntas frecuentes', 'preguntas-frecuentes-proindiviso' ],
	'diccionario-del-proindiviso/ajd-actos-juridicos-documentados' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'diccionario-del-proindiviso/impuesto-de-sucesiones' => [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ],
	'diccionario-del-proindiviso/plusvalia-municipal' => [ 'Calcula tus impuestos', 'calculadora-impuestos-vender-tu-parte' ],
	'diccionario-del-proindiviso/frutos-y-rentas-de-la-cosa-comun' => [ 'Calcula tu compensación', 'calculadora-compensacion-uso-exclusivo' ],
	'diccionario-del-proindiviso/indivision' => [ 'Modelo de pacto de indivisión', 'modelos-documentos-proindiviso/modelo-pacto-de-indivision' ],
];
const ZP_ENL_MAPA2 = [
	'impuestos-del-proindiviso' => [ 'Impuesto de sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'blog/no-puedo-pagar-el-impuesto-de-sucesiones' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'blog/herencia-prescrita-impuesto-de-sucesiones' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'blog/aceptar-la-herencia-y-vender-mi-parte-en-el-mismo-acto' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'diccionario-del-proindiviso/impuesto-de-sucesiones' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'diccionario-del-proindiviso/modelo-650' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'diccionario-del-proindiviso/bonificacion-del-impuesto-de-sucesiones' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'diccionario-del-proindiviso/aplazamiento-del-impuesto-de-sucesiones' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'diccionario-del-proindiviso/recargo-por-presentacion-fuera-de-plazo' => [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ],
	'vender-nuda-propiedad' => [ 'Calculadora de nuda propiedad', 'calculadora-nuda-propiedad' ],
	'blog/cuanto-vale-la-nuda-propiedad-calculo' => [ 'Calculadora de nuda propiedad', 'calculadora-nuda-propiedad' ],
	'blog/puedo-vender-la-casa-de-mi-madre-con-usufructo' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'blog/testamento-con-usufructo-universal-puede-vender-el-viudo' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'blog/extincion-de-condominio-con-usufructo' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'diccionario-del-proindiviso/usufructo' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'diccionario-del-proindiviso/usufructo-viudal' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'diccionario-del-proindiviso/conmutacion-del-usufructo' => [ 'Calcula la nuda propiedad', 'calculadora-nuda-propiedad' ],
	'calculadora-gastos-entre-copropietarios' => [ 'Modelo de reconocimiento de deuda', 'modelos-documentos-proindiviso/modelo-reconocimiento-de-deuda-entre-copropietarios' ],
	'blog/ibi-y-gastos-en-un-proindiviso-quien-paga' => [ 'Modelo de reconocimiento de deuda', 'modelos-documentos-proindiviso/modelo-reconocimiento-de-deuda-entre-copropietarios' ],
	'blog/copropietario-no-paga-la-hipoteca-que-hacer' => [ 'Modelo de reconocimiento de deuda', 'modelos-documentos-proindiviso/modelo-reconocimiento-de-deuda-entre-copropietarios' ],
	'calculadora-compensacion-uso-exclusivo' => [ 'Modelo de reclamación de rentas', 'modelos-documentos-proindiviso/modelo-reclamacion-rentas-copropietario' ],
	'diccionario-del-proindiviso/frutos-y-rentas-de-la-cosa-comun' => [ 'Modelo de reclamación de rentas', 'modelos-documentos-proindiviso/modelo-reclamacion-rentas-copropietario' ],
	'blog/alquilar-un-piso-en-proindiviso' => [ 'Modelo de reclamación de rentas', 'modelos-documentos-proindiviso/modelo-reclamacion-rentas-copropietario' ],
	'blog/alquilar-piso-compartido-en-airbnb-sin-permiso' => [ 'Modelo de reclamación de rentas', 'modelos-documentos-proindiviso/modelo-reclamacion-rentas-copropietario' ],
	'diccionario-del-proindiviso/contrato-de-arras' => [ 'Modelo de contrato de arras', 'modelos-documentos-proindiviso/modelo-contrato-de-arras-cuota-indivisa' ],
	'diccionario-del-proindiviso/cesion-de-derechos-hereditarios' => [ 'Modelo de cesión de derechos', 'modelos-documentos-proindiviso/modelo-cesion-de-derechos-hereditarios' ],
	'blog/vender-mi-parte-de-la-herencia-a-otro-heredero' => [ 'Modelo de cesión de derechos', 'modelos-documentos-proindiviso/modelo-cesion-de-derechos-hereditarios' ],
	'blog/vender-herencia-sin-escriturar' => [ 'Modelo de cesión de derechos', 'modelos-documentos-proindiviso/modelo-cesion-de-derechos-hereditarios' ],
	'blog/herencia-yacente-vender-antes-de-la-particion' => [ 'Modelo de cesión de derechos', 'modelos-documentos-proindiviso/modelo-cesion-de-derechos-hereditarios' ],
	'blog/como-se-reparte-una-herencia-de-una-casa-entre-hermanos' => [ 'Modelo de compraventa entre hermanos', 'modelos-documentos-proindiviso/modelo-contrato-compraventa-entre-hermanos' ],
	'blog/cuanto-tengo-que-pagar-a-mi-ex-por-la-casa' => [ 'Modelo de oferta de compra', 'modelos-documentos-proindiviso/modelo-oferta-compra-parte-copropietario' ],
];
function zp_enl_publicada( $ruta ) {
	static $c = [];
	if ( ! isset( $c[ $ruta ] ) ) { $p = get_page_by_path( $ruta ); $c[ $ruta ] = ( $p && $p->post_status === 'publish' ); }
	return $c[ $ruta ];
}
function zp_enl_lista( $v ) { return $v ? ( is_array( $v[0] ) ? $v : [ $v ] ) : []; }
function zp_enl_objetivo() {
	if ( ! is_singular() ) { return []; }
	$id = get_queried_object_id(); $anc = get_post_ancestors( $id );
	if ( is_page() && ( $id === 55 || in_array( 55, $anc, true ) ) ) {
		if ( $id === 55 ) { return [ [ 'Impuestos por comunidad', 'impuestos-del-proindiviso' ], [ 'Sucesiones por comunidad', 'impuestos-del-proindiviso/impuesto-de-sucesiones-por-comunidad' ] ]; }
		$sin = array_values( array_diff( $anc, [ 55 ] ) ); $top = $sin ? end( $sin ) : $id;
		$ccaa = get_post_field( 'post_name', $top );
		$nombre = trim( preg_replace( '/^Vender proindiviso en (el |la |los |las )?/iu', '', preg_replace( '/[:—–-].*$/u', '', wp_strip_all_tags( get_the_title( $top ) ) ) ) );
		return [ [ 'Impuestos en ' . $nombre, 'impuestos-del-proindiviso/extincion-de-condominio-' . $ccaa ], [ 'Sucesiones en ' . $nombre, 'impuestos-del-proindiviso/impuesto-de-sucesiones-' . $ccaa ] ];
	}
	$ruta = trim( wp_parse_url( get_permalink( $id ), PHP_URL_PATH ), '/' );
	if ( preg_match( '#^impuestos-del-proindiviso/extincion-de-condominio-([a-z-]+)$#', $ruta, $m ) ) {
		$nombre = trim( preg_replace( '/^.*? en (el |la )?/iu', '', wp_strip_all_tags( get_the_title( $id ) ) ) );
		return [ [ 'Sucesiones en ' . $nombre, 'impuestos-del-proindiviso/impuesto-de-sucesiones-' . $m[1] ] ];
	}
	return array_merge( zp_enl_lista( ZP_ENL_MAPA[ $ruta ] ?? null ), zp_enl_lista( ZP_ENL_MAPA2[ $ruta ] ?? null ) );
}
function zp_enl_insertar( $content ) {
	if ( is_admin() || strpos( $content, 'También te puede interesar' ) === false ) { return $content; }
	$lt = chr( 60 );
	foreach ( zp_enl_objetivo() as $o ) {
		if ( ! zp_enl_publicada( $o[1] ) ) { continue; }
		$url = '/' . $o[1] . '/';
		if ( strpos( $content, 'href="' . $url . '"' ) !== false || strpos( $content, 'href="' . home_url( $url ) . '"' ) !== false ) { continue; }
		$i = strpos( $content, 'También te puede interesar' );
		$d = strpos( $content, $lt . 'div', $i ); if ( $d === false ) { continue; }
		$e = strpos( $content, '>', $d ); if ( $e === false ) { continue; }
		$cls = 'e-button-base e-default-a';
		if ( preg_match( '/' . $lt . 'a [^>]*class="([^"]*e-button-base[^"]*)"/', substr( $content, $e, 3000 ), $m ) ) { $cls = $m[1]; }
		$btn = $lt . 'a href="' . esc_url( $url ) . '" target="_self" class="' . esc_attr( $cls ) . '">' . esc_html( $o[0] ) . $lt . '/a>';
		$content = substr( $content, 0, $e + 1 ) . $btn . substr( $content, $e + 1 );
	}
	return $content;
}
add_filter( 'elementor/frontend/the_content', 'zp_enl_insertar', 35 );
add_filter( 'the_content', 'zp_enl_insertar', 115 );
