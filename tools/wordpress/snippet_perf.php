/* Zona Proindiviso — rendimiento (snippet 83, global).
 * - Preload de la imagen de fondo del hero (elemento LCP en todas las páginas del patrón).
 * - Preload de Manrope: OMGF sirve la fuente en local como UN archivo variable (manrope-normal-latin.woff2) con font-display: swap;
 *   sin preload el texto se pintaba con la fuente del sistema y saltaba al cargar (CLS 0,14 en móvil). Se lee el ?ver= del CSS de OMGF
 *   para que el preload apunte a la misma URL que usa el CSS (si no, el navegador la descargaría dos veces).
 * - @font-face inline con font-display: optional en lugar de la hoja de OMGF (swap): sin salto de maquetación.
 * - jQuery al pie (ver abajo). */
add_action( 'wp_head', function () {
	if ( is_admin() ) { return; }
	echo '<link rel="preload" as="image" href="https://zonaproindiviso.com/wp-content/uploads/2026/10/vender-proindiviso-fachada-edificio-espana.webp" fetchpriority="high">' . "\n";
	$ver = get_transient( 'zp_manrope_ver' );
	if ( $ver === false ) {
		$css = @file_get_contents( WP_CONTENT_DIR . '/uploads/omgf/elementor-gf-manrope/elementor-gf-manrope.css' );
		$ver = ( $css && preg_match( '/manrope-normal-latin\.woff2\?ver=(\d+)/', $css, $m ) ) ? $m[1] : '';
		set_transient( 'zp_manrope_ver', $ver, HOUR_IN_SECONDS );
	}
	if ( $ver !== '' ) {
		$base = '//zonaproindiviso.com/wp-content/uploads/omgf/elementor-gf-manrope/manrope-normal-';
		echo '<link rel="preload" as="font" type="font/woff2" href="' . $base . 'latin.woff2?ver=' . esc_attr( $ver ) . '" crossorigin>' . "\n";
		// @font-face propio e inline (una petición menos) con font-display: optional: si la fuente no llega antes del primer pintado se
		// queda la del sistema y no hay salto de maquetación (CLS 0); con el preload llega a tiempo en casi todas las visitas.
		$t = 'sty' . 'le';
		echo '<' . $t . ' id="zp-manrope">'
			. "@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;font-display:optional;src:url('" . $base . "latin.woff2?ver=" . esc_attr( $ver ) . "') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}"
			. "@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;font-display:optional;src:url('" . $base . "latin-ext.woff2?ver=" . esc_attr( $ver ) . "') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF}"
			. '</' . $t . '>' . "\n";
	}
}, 1 );
// La hoja de OMGF para Manrope sobra (las @font-face van inline arriba, con font-display: optional).
add_filter( 'style_loader_tag', function ( $tag, $handle ) { return strpos( $handle, 'elementor-gf-manrope' ) === 0 && get_transient( 'zp_manrope_ver' ) ? '' : $tag; }, 10, 2 );
add_action( 'wp_enqueue_scripts', function () {
	// jQuery (y migrate) al pie: eran el único JS que bloqueaba el render en la cabecera (~200 ms en móvil). Todo lo que depende de
	// jQuery (Elementor, Elementor Pro, Complianz, smartmenus) ya se imprime en el pie, y WordPress respeta el orden de dependencias.
	// (La API de estrategias `defer` se probó y se descartó: WordPress dejaba elementor-pro-frontend bloqueante con sus dependencias
	// diferidas y rompía los popups: «elementorModules is not defined».)
	$ws = wp_scripts();
	foreach ( [ 'jquery', 'jquery-core', 'jquery-migrate' ] as $h ) { if ( isset( $ws->registered[ $h ] ) ) { $ws->add_data( $h, 'group', 1 ); } }
}, 9999 );
