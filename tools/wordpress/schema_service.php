// Schema Service (compra de proindivisos) en páginas e índice, enlazado a la Organization de Yoast.
add_filter( 'wpseo_schema_graph_pieces', function ( $pieces, $context ) {
	if ( ! class_exists( 'ZP_Schema_Service' ) ) {
		class ZP_Schema_Service extends \Yoast\WP\SEO\Generators\Schema\Abstract_Schema_Piece {
			public function is_needed() { return is_front_page() || is_page(); }
			public function generate() {
				$home = trailingslashit( home_url() );
				return [
					'@type'        => 'Service',
					'@id'          => $home . '#servicio-compra-proindivisos',
					'name'         => 'Compra de proindivisos y partes de herencias',
					'serviceType'  => 'Compra de participaciones indivisas de inmuebles',
					'description'  => 'Compramos tu parte de un piso, casa, local, garaje o terreno con fondos propios. Oferta por escrito en 48 horas, firma en notaría en 2 a 4 semanas, gastos a nuestro cargo, sin exclusividad.',
					'provider'     => [ '@id' => $home . '#organization' ],
					'areaServed'   => [ '@type' => 'Country', 'name' => 'España' ],
					'availableChannel' => [ '@type' => 'ServiceChannel', 'serviceUrl' => $home . 'contacto/', 'availableLanguage' => 'es' ],
					'termsOfService' => $home . 'aviso-legal/',
				];
			}
		}
	}
	$pieces[] = new ZP_Schema_Service( $context );
	return $pieces;
}, 11, 2 );
