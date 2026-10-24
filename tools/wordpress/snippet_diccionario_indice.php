// Índice A-Z del diccionario del proindiviso: shortcode [zp_diccionario] (se usa en la página /diccionario-del-proindiviso/ dentro de un
// e-paragraph de Elementor, que pasa la salida por wp_kses: por eso devuelve un marcador y el filtro de abajo lo sustituye por el HTML).
// Fuentes: páginas hijas publicadas del hub (título, extracto = definición) + entradas/páginas existentes que hacen de término
// (ZP_DIC_EXTRA; solo si están publicadas, así las programadas entran solas el día que se publican). Caché 10 min (transient).
const ZP_DIC_EXTRA = [
	[ 'Beneficio de inventario', '/blog/aceptar-herencia-a-beneficio-de-inventario-y-vender/', 'Aceptar la herencia respondiendo de las deudas solo con lo heredado.' ],
	[ 'Comunidad de bienes', '/blog/proindiviso-condominio-comunidad-de-bienes-diferencias/', 'Nombre legal del proindiviso en el Código Civil (arts. 392 a 406).' ],
	[ 'Comunidad hereditaria', '/blog/comunidad-hereditaria-vs-proindiviso/', 'La situación de los herederos antes de repartir la herencia.' ],
	[ 'Cuaderno particional', '/blog/cuaderno-particional-que-es-y-para-que-sirve/', 'Documento que reparte la herencia bien por bien y heredero por heredero.' ],
	[ 'Contador partidor', '/blog/contador-partidor-herencia-sin-acuerdo/', 'Persona que reparte la herencia cuando los herederos no se ponen de acuerdo.' ],
	[ 'Cuota hereditaria', '/blog/que-es-una-cuota-hereditaria/', 'La parte de la herencia que corresponde a cada heredero.' ],
	[ 'División de cosa común', '/division-de-cosa-comun/', 'El juicio para salir de un proindiviso cuando no hay acuerdo; suele acabar en subasta.' ],
	[ 'Desahucio por precario', '/blog/desahucio-por-precario-de-un-familiar-casa-heredada/', 'Procedimiento para recuperar la casa que ocupa alguien sin título ni renta.' ],
	[ 'Donación de la cuota', '/blog/donar-mi-parte-de-un-proindiviso/', 'Regalar tu parte a otra persona: impuestos y límites.' ],
	[ 'Embargo de la cuota', '/blog/embargo-de-una-cuota-de-proindiviso/', 'Un acreedor puede embargar y subastar la parte de un copropietario.' ],
	[ 'Extinción de condominio', '/extincion-de-condominio/', 'Uno se queda el inmueble y compensa a los demás; tributa por AJD.' ],
	[ 'Exceso de adjudicación', '/blog/exceso-de-adjudicacion-en-la-extincion-de-condominio/', 'Lo que recibe de más un comunero al repartir; tributa si no está justificado.' ],
	[ 'Escisión y cesación de condominio', '/blog/escision-cesacion-liquidacion-de-condominio-que-significan/', 'Otros nombres que se usan para la extinción de condominio.' ],
	[ 'Herencia yacente', '/blog/herencia-yacente-vender-antes-de-la-particion/', 'La herencia aún no aceptada ni repartida.' ],
	[ 'IBI y gastos', '/blog/ibi-y-gastos-en-un-proindiviso-quien-paga/', 'Quién paga los impuestos y gastos de una casa compartida.' ],
	[ 'ITP', '/blog/itp-al-comprar-la-parte-de-un-piso/', 'Impuesto de Transmisiones Patrimoniales: lo paga quien compra una cuota.' ],
	[ 'IRPF (ganancia patrimonial)', '/blog/irpf-al-vender-mi-parte-de-un-piso-heredado/', 'Lo que tributa el vendedor si gana dinero al vender su parte.' ],
	[ 'Multipropiedad', '/blog/multipropiedad-como-vender/', 'Derecho a usar un inmueble por turnos; no es un proindiviso.' ],
	[ 'Nota simple', '/blog/nota-simple-como-pedirla-y-leerla/', 'Documento del Registro que dice quién es dueño y qué cargas hay.' ],
	[ 'Nuda propiedad', '/vender-nuda-propiedad/', 'Ser dueño sin poder usar el bien mientras dura el usufructo.' ],
	[ 'Okupa', '/vender-proindiviso-con-inquilino-u-okupa/', 'Ocupante sin título: cómo afecta a la venta de una cuota.' ],
	[ 'Proindiviso', '/que-es-un-proindiviso/', 'Propiedad de varios dueños sin dividir: la base de todo este diccionario.' ],
	[ 'Pacto de indivisión', '/blog/pacto-de-indivision-que-es-y-cuanto-dura/', 'Acuerdo para no dividir durante un plazo (máximo diez años).' ],
	[ 'Prescripción del impuesto de sucesiones', '/blog/herencia-prescrita-impuesto-de-sucesiones/', 'A los cuatro años y medio Hacienda ya no puede exigirlo.' ],
	[ 'Retracto de comuneros', '/blog/derecho-de-tanteo-y-retracto-entre-copropietarios/', 'Derecho de los copropietarios a quedarse con la cuota vendida a un tercero (art. 1522 CC).' ],
	[ 'Retracto de coherederos', '/blog/retracto-de-coherederos-que-es/', 'Lo mismo entre herederos antes de la partición (art. 1067 CC).' ],
	[ 'Renuncia a la herencia', '/blog/renunciar-a-la-herencia-o-vender-mi-parte/', 'Rechazar la herencia ante notario; alternativa a vender la parte.' ],
	[ 'Subasta judicial', '/blog/subasta-division-de-cosa-comun/', 'La venta forzosa del inmueble tras la división de cosa común.' ],
	[ 'Tanteo', '/blog/derecho-de-tanteo-y-retracto-entre-copropietarios/', 'Derecho a comprar la cuota antes que un tercero, al mismo precio.' ],
	[ 'Uso exclusivo (compensación)', '/blog/compensacion-por-uso-exclusivo-de-la-vivienda-comun/', 'Quien usa solo la casa común puede deber una compensación a los demás.' ],
	[ 'Valor de referencia', '/blog/valor-de-referencia-catastral-venta-de-tu-parte/', 'Valor que fija Catastro y que Hacienda usa como mínimo en ITP y sucesiones.' ],
	[ 'VPO', '/blog/vender-parte-de-una-vpo/', 'Vivienda protegida: límites de precio y permisos al vender una parte.' ],
];
function zp_dic_norm( $t ) { $t = remove_accents( wp_strip_all_tags( $t ) ); return mb_strtolower( $t ); }
function zp_dic_entradas() {
	$c = get_transient( 'zp_dic_entradas' );
	if ( is_array( $c ) ) { return $c; }
	$out = [];
	$hub = get_page_by_path( 'diccionario-del-proindiviso' );
	if ( $hub ) {
		foreach ( get_pages( [ 'parent' => $hub->ID, 'post_status' => 'publish', 'number' => 500 ] ) as $p ) {
			$out[] = [ get_the_title( $p ), get_permalink( $p ), wp_strip_all_tags( $p->post_excerpt ) ];
		}
	}
	$home = untrailingslashit( home_url() );
	foreach ( ZP_DIC_EXTRA as $e ) {
		$id = url_to_postid( $home . $e[1] );
		if ( ! $id || get_post_status( $id ) !== 'publish' ) { continue; }
		$out[] = [ $e[0], $home . $e[1], $e[2] ];
	}
	usort( $out, function ( $a, $b ) { return strcmp( zp_dic_norm( $a[0] ), zp_dic_norm( $b[0] ) ); } );
	set_transient( 'zp_dic_entradas', $out, 10 * MINUTE_IN_SECONDS );
	return $out;
}
add_action( 'save_post', function () { delete_transient( 'zp_dic_entradas' ); } );
add_shortcode( 'zp_diccionario', function () { return '[[ZP_DIC]]'; } );
function zp_dic_html() {
	$lt = chr( 60 );
	$grupos = [ 'A' => 'A', 'B-C' => 'BC', 'D-E' => 'DE', 'F-H' => 'FGH', 'I-L' => 'IJKL', 'M-N' => 'MN', 'O-P' => 'OP', 'Q-S' => 'QRS', 'T-U' => 'TU', 'V-Z' => 'VWXYZ' ];
	$ent = zp_dic_entradas(); $n = count( $ent );
	$nav = ''; $secs = ''; $i = 0;
	foreach ( $grupos as $nombre => $letras ) {
		$items = array_filter( $ent, function ( $e ) use ( $letras ) { return strpos( $letras, strtoupper( substr( zp_dic_norm( $e[0] ), 0, 1 ) ) ) !== false; } );
		if ( ! $items ) { continue; }
		$id = 'letra-' . strtolower( str_replace( '-', '', $nombre ) );
		$nav .= $lt . 'a href="#' . $id . '">' . esc_html( $nombre ) . $lt . '/a>';
		$h = ( $i++ % 2 === 0 ) ? 'Términos del proindiviso de la ' . $nombre : 'Diccionario del proindiviso: ' . $nombre;
		$li = '';
		foreach ( $items as $e ) { $li .= $lt . 'li>' . $lt . 'a href="' . esc_url( $e[1] ) . '">' . esc_html( $e[0] ) . $lt . '/a>' . ( $e[2] ? ': ' . esc_html( $e[2] ) : '' ) . $lt . '/li>'; }
		$secs .= $lt . 'section class="zpd-grupo" id="' . $id . '">' . $lt . 'h2>' . esc_html( $h ) . $lt . '/h2>' . $lt . 'ul>' . $li . $lt . '/ul>' . $lt . '/section>';
	}
	return $lt . 'div class="zpd">' . $lt . 'p class="zpd-n">' . $n . ' términos explicados. Pulsa una letra:' . $lt . '/p>' . $lt . 'nav class="zpd-nav" aria-label="Letras del diccionario">' . $nav . $lt . '/nav>' . $secs . $lt . '/div>';
}
function zp_dic_sustituir( $content ) {
	if ( strpos( $content, '[[ZP_DIC]]' ) === false ) { return $content; }
	$lt = chr( 60 );
	return preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_DIC\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_dic_html() . $lt . '/div>'; }, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_dic_sustituir', 25 );
add_filter( 'the_content', 'zp_dic_sustituir', 100 );
add_action( 'wp_head', function () {
	if ( ! is_page( 'diccionario-del-proindiviso' ) ) { return; }
	$t = 'sty' . 'le';
	echo '<' . $t . ' id="zpd-css">'
		. '.zpd{display:block;width:100%;font-family:Manrope,sans-serif;color:#1f2a33}.zpd-n{font-size:15px;color:#4f5b66;margin:0 0 10px}'
		. '.zpd-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px}.zpd-nav a{display:inline-block;padding:8px 14px;border:1px solid #d8e0e6;border-radius:999px;font-weight:700;font-size:14px;color:#0d4f78;text-decoration:none;background:#fff}.zpd-nav a:hover{border-color:#e87524;color:#e87524}'
		. '.zpd-grupo{padding:28px 0 8px;border-top:1px solid #e3e8ec;margin-top:20px;scroll-margin-top:110px}.zpd-grupo h2{font-size:clamp(1.35rem,1.1rem+1vw,1.8rem);line-height:1.2;letter-spacing:-.01em;color:#0d4f78;margin:0 0 16px}'
		. '.zpd-grupo ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px 28px}.zpd-grupo li{font-size:16px;line-height:1.55;padding:10px 0 10px 16px;border-left:3px solid #e87524;color:#1f2a33}'
		. '.zpd-grupo li a{font-weight:800;color:#0d4f78;text-decoration:none}.zpd-grupo li a:hover{color:#e87524;text-decoration:underline}'
		. '@media(max-width:767px){.zpd-grupo ul{grid-template-columns:1fr}}'
		. '</' . $t . '>';
}, 97 );
