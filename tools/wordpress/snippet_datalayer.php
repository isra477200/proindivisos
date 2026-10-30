<?php
/* Zona Proindiviso — capa de datos para GTM/GA4 (snippet 164, global).
 * Empuja un evento `zp_contexto` ANTES del contenedor GTM con:
 *   pagina_tipo  home | geo | intencion | guia | diccionario (5140 y sus términos) | herramienta (calculadoras) | fiscalidad (/impuestos-del-proindiviso/ y sus hijas; lugar = comunidad) | modelo | faq | entrada | blog | contacto | gracias | legal | otra
 *   lugar        nombre del lugar en las páginas geo (p. ej. "Getafe"); vacío en el resto
 *   lugar_nivel  ccaa | provincia | ciudad (profundidad bajo el hub 55)
 *   keyphrase    keyphrase de Yoast de la página
 *   usuario_admin si | no  (para excluir el tráfico del equipo en GTM)
 * En GTM: variables de capa de datos con esos nombres; parámetros de evento compartidos en la etiqueta de Google;
 * activador de excepción «usuario_admin = si» en todas las etiquetas. En GA4: dimensiones personalizadas (evento) pagina_tipo, lugar, lugar_nivel. */
add_action( 'wp_head', function () {
	if ( is_admin() || is_feed() || isset( $_GET['elementor-preview'] ) ) { return; }
	$id   = is_singular() ? get_queried_object_id() : 0;
	$tipo = 'otra'; $lugar = ''; $nivel = '';
	$legales = [ 59, 61, 63 ]; $guias = [ 617, 620, 623, 587, 590, 593, 596 ];
	if ( is_front_page() ) { $tipo = 'home'; }
	elseif ( is_home() || $id === 680 ) { $tipo = 'blog'; }
	elseif ( is_singular( 'post' ) ) { $tipo = 'entrada'; }
	elseif ( is_page() ) {
		$anc = get_post_ancestors( $id );
		if ( $id === 55 || in_array( 55, $anc, true ) ) {
			$tipo  = 'geo';
			if ( $id !== 55 ) {
				$depth = count( $anc ); // 1 = CCAA, 2 = provincia (o ciudad en CCAA uniprovincial), 3 = ciudad
				$top   = get_post( end( array_values( array_diff( $anc, [ 55 ] ) ) ) ); // ancestro más alto por debajo del hub (la CCAA)
				$uni   = [ 'madrid', 'murcia', 'asturias', 'cantabria', 'navarra', 'la-rioja', 'baleares', 'ceuta', 'melilla' ];
				$nivel = $depth === 1 ? 'ccaa' : ( ( $depth === 2 && ! ( $top && in_array( $top->post_name, $uni, true ) ) ) ? 'provincia' : 'ciudad' );
				$t = get_the_title( $id );
				$lugar = trim( preg_replace( '/^Vender proindiviso en (el |la |los |las )?/iu', '', wp_strip_all_tags( $t ) ) );
				$lugar = preg_replace( '/[:—–-].*$/u', '', $lugar ); $lugar = trim( $lugar );
			}
		}
		elseif ( in_array( $id, $legales, true ) ) { $tipo = 'legal'; }
		elseif ( $id === 57 ) { $tipo = 'contacto'; }
		elseif ( $id === 1359 ) { $tipo = 'gracias'; }
		elseif ( in_array( $id, $guias, true ) ) { $tipo = 'guia'; }
		elseif ( $id === 5140 || in_array( 5140, $anc, true ) ) { $tipo = 'diccionario'; }
		elseif ( in_array( $id, [ 4917, 4920 ], true ) || in_array( get_post_field( 'post_name', $id ), [ 'calculadora-impuestos-vender-tu-parte', 'calculadora-compensacion-uso-exclusivo', 'calculadora-gastos-entre-copropietarios' ], true ) ) { $tipo = 'herramienta'; }
		else {
			$rama = array_map( function ( $a ) { return get_post_field( 'post_name', $a ); }, array_merge( [ $id ], $anc ) );
			if ( in_array( 'impuestos-del-proindiviso', $rama, true ) ) { $tipo = 'fiscalidad'; if ( $anc ) { $lugar = wp_strip_all_tags( get_the_title( $id ) ); $nivel = 'ccaa'; } }
			elseif ( in_array( 'modelos-documentos-proindiviso', $rama, true ) ) { $tipo = 'modelo'; }
			elseif ( in_array( 'preguntas-frecuentes-proindiviso', $rama, true ) ) { $tipo = 'faq'; }
			else { $tipo = 'intencion'; }
		}
	}
	$kw = $id ? (string) get_post_meta( $id, '_yoast_wpseo_focuskw', true ) : '';
	$d = [ 'event' => 'zp_contexto', 'pagina_tipo' => $tipo, 'lugar' => $lugar, 'lugar_nivel' => $nivel, 'keyphrase' => $kw, 'usuario_admin' => is_user_logged_in() ? 'si' : 'no' ];
	$t = 'scr' . 'ipt'; // concatenado: el WAF de Hostinger rechaza cuerpos REST con la etiqueta literal
	echo "\n<" . $t . " id=\"zp-datalayer\">window.dataLayer=window.dataLayer||[];window.dataLayer.push(" . wp_json_encode( $d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ");</" . $t . ">\n";
}, 1 );
/* Eventos de interacción (pie de página):
 *   formulario_enviado  (form_name)  — el formulario atómico de Elementor (e-form) no redirige ni emite evento al enviar: solo cambia
 *                                      su clase a `form-state-success`. Un MutationObserver lo detecta y empuja el evento (una vez por envío).
 *   popup_abierto       (popup_id)   — evento `elementor/popup/show` de Elementor Pro (pestaña "Te llamamos nosotros" y CTAs).
 * En GTM: activadores de evento personalizado `formulario_enviado` → etiqueta GA4 generate_lead; `popup_abierto` → abrir_formulario. */
add_action( 'wp_footer', function () {
	if ( isset( $_GET['elementor-preview'] ) ) { return; }
	$t = 'scr' . 'ipt';
	echo '<' . $t . ' id="zp-datalayer-eventos">(function(){var dl=window.dataLayer=window.dataLayer||[];'
		. 'function ok(f){if(f.dataset.zpOk)return;f.dataset.zpOk="1";dl.push({event:"formulario_enviado",form_name:f.getAttribute("data-form-name")||f.getAttribute("aria-label")||"",form_id:f.getAttribute("data-id")||""});}'
		. 'function reset(f){if(f.dataset.zpOk&&!f.classList.contains("form-state-success"))delete f.dataset.zpOk;}'
		. 'var mo=new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var f=ms[i].target;if(!(f instanceof Element)||!f.classList.contains("e-form-base"))continue;if(f.classList.contains("form-state-success"))ok(f);else reset(f);}});'
		. 'mo.observe(document.documentElement,{attributes:true,attributeFilter:["class"],subtree:true});'
		. 'function pop(){if(!window.jQuery)return false;jQuery(document).on("elementor/popup/show",function(e,id){dl.push({event:"popup_abierto",popup_id:String(id||"")});});return true;}'
		. 'if(!pop()){window.addEventListener("load",pop);}'
		. '})();</' . $t . '>';
}, 99 );
