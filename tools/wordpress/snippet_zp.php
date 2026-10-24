/**
 * Zona Proindiviso — ajuste único de teléfono y WhatsApp.
 * Expone: opciones (REST), página de ajustes, shortcodes [zp_telefono] [zp_telefono_enlace] [zp_whatsapp] [zp_whatsapp_enlace] [zp_email],
 * etiquetas dinámicas de Elementor (grupo "Zona Proindiviso"), teléfono en el schema Organization de Yoast,
 * y metadatos de Yoast escribibles por REST (title, metadesc, focuskw, noindex, canonical).
 */

function zp_opt( $k, $d = '' ) { $v = get_option( $k, $d ); return is_string( $v ) ? trim( $v ) : $d; }
function zp_telefono() { return zp_opt( 'zp_telefono', '' ); }
function zp_telefono_enlace() { $n = preg_replace( '/[^0-9+]/', '', zp_telefono() ); if ( $n === '' ) return ''; if ( $n[0] !== '+' ) { $n = '+34' . ltrim( $n, '0' ); } return 'tel:' . $n; }
function zp_whatsapp() { return preg_replace( '/[^0-9]/', '', zp_opt( 'zp_whatsapp', '' ) ); }
function zp_whatsapp_mensaje( $post_id = 0 ) {
	$tpl = zp_opt( 'zp_wa_mensaje', 'Hola, quiero vender mi proindiviso. Vengo de la página: {pagina}' );
	$titulo = $post_id ? get_the_title( $post_id ) : ( is_singular() ? get_the_title() : get_bloginfo( 'name' ) );
	return str_replace( '{pagina}', $titulo, $tpl );
}
function zp_whatsapp_enlace( $post_id = 0 ) { $n = zp_whatsapp(); if ( $n === '' ) return ''; return 'https://wa.me/' . $n . '?text=' . rawurlencode( zp_whatsapp_mensaje( $post_id ) ); }

/* Opciones visibles por REST (/wp/v2/settings) y por MCP */
add_action( 'init', function () {
	$campos = [
		'zp_telefono'    => 'Teléfono visible (ej. 600 000 000)',
		'zp_whatsapp'    => 'WhatsApp en formato internacional sin + (ej. 34600000000)',
		'zp_email_leads' => 'Email que recibe los leads',
		'zp_wa_mensaje'  => 'Mensaje de WhatsApp prerrellenado ({pagina} = título de la página)',
		'zp_debug'       => 'Uso interno (diagnóstico)',
	];
	foreach ( $campos as $k => $desc ) {
		register_setting( 'zp_ajustes', $k, [ 'type' => 'string', 'show_in_rest' => true, 'default' => '', 'sanitize_callback' => 'sanitize_text_field', 'description' => $desc ] );
	}
}, 5 );

/* Página de ajustes: Ajustes → Zona Proindiviso */
add_action( 'admin_menu', function () {
	add_options_page( 'Zona Proindiviso', 'Zona Proindiviso', 'manage_options', 'zp-ajustes', function () {
		echo '<div class="wrap"><h1>Zona Proindiviso — teléfono y WhatsApp</h1><p>Estos valores se usan en toda la web (botones, barra móvil, pestaña "Te llamamos", schema). Cambiarlos aquí los cambia en todas las páginas.</p><form method="post" action="options.php">';
		settings_fields( 'zp_ajustes' );
		echo '<table class="form-table">';
		foreach ( [ 'zp_telefono' => 'Teléfono visible', 'zp_whatsapp' => 'WhatsApp (34600000000)', 'zp_email_leads' => 'Email de leads', 'zp_wa_mensaje' => 'Mensaje de WhatsApp' ] as $k => $label ) {
			echo '<tr><th scope="row"><label for="' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td><input class="regular-text" type="text" id="' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . esc_attr( get_option( $k, '' ) ) . '"></td></tr>';
		}
		echo '</table>';
		submit_button();
		echo '</form><p><strong>Enlace de llamada:</strong> ' . esc_html( zp_telefono_enlace() ) . '<br><strong>Enlace de WhatsApp:</strong> ' . esc_html( zp_whatsapp_enlace() ) . '</p></div>';
	} );
} );

/* Shortcodes (también usables desde la etiqueta dinámica "Shortcode" de Elementor) */
add_shortcode( 'zp_telefono', function () { return esc_html( zp_telefono() ); } );
add_shortcode( 'zp_telefono_enlace', function () { return esc_attr( zp_telefono_enlace() ); } );
add_shortcode( 'zp_whatsapp', function () { return esc_html( zp_whatsapp() ); } );
add_shortcode( 'zp_whatsapp_enlace', function () { return esc_url( zp_whatsapp_enlace() ); } );
add_shortcode( 'zp_email', function () { return esc_html( zp_opt( 'zp_email_leads' ) ); } );

/* Etiquetas dinámicas propias de Elementor (grupo Zona Proindiviso) */
add_action( 'elementor/dynamic_tags/register', function ( $dynamic_tags ) {
	if ( ! class_exists( '\Elementor\Core\DynamicTags\Tag' ) ) { return; }
	$dynamic_tags->register_group( 'zona-proindiviso', [ 'title' => 'Zona Proindiviso' ] );
	if ( ! class_exists( 'ZP_Tag_Telefono' ) ) {
		class ZP_Tag_Telefono extends \Elementor\Core\DynamicTags\Tag {
			public function get_name() { return 'zp-telefono'; }
			public function get_title() { return 'Teléfono (ZP)'; }
			public function get_group() { return [ 'zona-proindiviso' ]; }
			public function get_categories() { return [ \Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY ]; }
			public function render() { echo esc_html( zp_telefono() ); }
		}
		class ZP_Tag_Whatsapp_Numero extends \Elementor\Core\DynamicTags\Tag {
			public function get_name() { return 'zp-whatsapp-numero'; }
			public function get_title() { return 'WhatsApp número (ZP)'; }
			public function get_group() { return [ 'zona-proindiviso' ]; }
			public function get_categories() { return [ \Elementor\Modules\DynamicTags\Module::TEXT_CATEGORY ]; }
			public function render() { echo esc_html( zp_whatsapp() ); }
		}
		class ZP_Tag_Telefono_Enlace extends \Elementor\Core\DynamicTags\Data_Tag {
			public function get_name() { return 'zp-telefono-enlace'; }
			public function get_title() { return 'Llamar: enlace tel (ZP)'; }
			public function get_group() { return [ 'zona-proindiviso' ]; }
			public function get_categories() { return [ \Elementor\Modules\DynamicTags\Module::URL_CATEGORY ]; }
			public function get_value( array $options = [] ) { return zp_telefono_enlace(); }
		}
		class ZP_Tag_Whatsapp_Enlace extends \Elementor\Core\DynamicTags\Data_Tag {
			public function get_name() { return 'zp-whatsapp-enlace'; }
			public function get_title() { return 'WhatsApp: enlace con mensaje (ZP)'; }
			public function get_group() { return [ 'zona-proindiviso' ]; }
			public function get_categories() { return [ \Elementor\Modules\DynamicTags\Module::URL_CATEGORY ]; }
			public function get_value( array $options = [] ) { return zp_whatsapp_enlace( get_the_ID() ); }
		}
	}
	$dynamic_tags->register( new ZP_Tag_Telefono() );
	$dynamic_tags->register( new ZP_Tag_Whatsapp_Numero() );
	$dynamic_tags->register( new ZP_Tag_Telefono_Enlace() );
	$dynamic_tags->register( new ZP_Tag_Whatsapp_Enlace() );
} );

/* Teléfono en el schema Organization de Yoast */
add_filter( 'wpseo_schema_organization', function ( $data ) {
	$tel = zp_telefono_enlace();
	if ( $tel ) { $data['telephone'] = substr( $tel, 4 ); }
	$data['areaServed'] = 'ES';
	return $data;
} );

/* Metadatos de Yoast escribibles por REST/MCP */
add_action( 'init', function () {
	$claves = [ '_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw', '_yoast_wpseo_meta-robots-noindex', '_yoast_wpseo_canonical', '_yoast_wpseo_opengraph-title', '_yoast_wpseo_opengraph-description' ];
	foreach ( [ 'post', 'page' ] as $pt ) {
		foreach ( $claves as $k ) {
			register_post_meta( $pt, $k, [ 'show_in_rest' => true, 'single' => true, 'type' => 'string', 'default' => '', 'sanitize_callback' => 'sanitize_text_field', 'auth_callback' => function () { return current_user_can( 'edit_posts' ); } ] );
		}
	}
}, 99 );


/* CSS global del tema (menú de la cabecera, enlaces, formularios) */
add_action( 'wp_head', function () {
	echo '<style id="zp-css">
.elementor-nav-menu--main .elementor-item{font-family:var(--font-body,Manrope),sans-serif;font-size:15px;font-weight:700;color:#1f2a33;padding:10px 13px;letter-spacing:-0.005em}
.elementor-nav-menu--main .elementor-item:hover,.elementor-nav-menu--main .elementor-item.elementor-item-active{color:#0d4f78}
.elementor-nav-menu--main .elementor-item:before,.elementor-nav-menu--main .elementor-item:after{background-color:#e87524;height:2px}
.elementor-menu-toggle{color:#0d4f78;border:1px solid #d8e0e6;border-radius:10px;width:44px;height:44px;background:#fff}
.elementor-menu-toggle.elementor-active{color:#e87524}
.elementor-nav-menu--dropdown{background:#fff;border:1px solid #d8e0e6;border-radius:14px;box-shadow:0 18px 40px rgba(13,79,120,.14);margin-top:8px;overflow:hidden}
.elementor-nav-menu--dropdown .elementor-item{font-size:16px;font-weight:700;color:#1f2a33;padding:14px 18px;border-bottom:1px solid #eef2f5}
.elementor-nav-menu--dropdown .elementor-item:hover{background:#eff5f8;color:#0d4f78}
.e-form-base input::placeholder,.e-form-base textarea::placeholder{color:#8a96a3}
.e-form-base select{appearance:none;background-image:url(\"data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'14\' height=\'14\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%230d4f78\' stroke-width=\'3\'><path d=\'M6 9l6 6 6-6\'/></svg>\");background-repeat:no-repeat;background-position:right 14px center;padding-right:40px}
html{scroll-behavior:smooth}
body{-webkit-font-smoothing:antialiased}
</style>';
}, 99 );
