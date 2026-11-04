// robots.txt: Yoast escribe la línea Sitemap con http:// (el sitio está detrás de un proxy que llega a WordPress por http).
// Se fuerza https para que Google lea la URL canónica del sitemap.
add_filter( 'robots_txt', function ( $out ) {
	return str_replace( 'http://zonaproindiviso.com', 'https://zonaproindiviso.com', $out );
}, PHP_INT_MAX );
