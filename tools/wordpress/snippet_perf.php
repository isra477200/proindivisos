/* Zona Proindiviso — rendimiento: preconnect a Google Fonts y preload de la imagen de fondo del hero (elemento LCP en todas las páginas del patrón). */
add_action( 'wp_head', function () {
	if ( is_admin() ) { return; }
	echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
	echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
	echo '<link rel="preload" as="image" href="https://zonaproindiviso.com/wp-content/uploads/2026/10/vender-proindiviso-fachada-edificio-espana.webp" fetchpriority="high">' . "\n";
}, 1 );
