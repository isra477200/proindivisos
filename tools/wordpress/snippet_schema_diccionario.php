// Schema del diccionario del proindiviso en el grafo de Yoast: DefinedTermSet en el índice (/diccionario-del-proindiviso/) y
// DefinedTerm en cada término (páginas hijas). La definición sale del extracto de la página (lo fija diccionario.py: primera frase del sub).
add_filter( 'wpseo_schema_graph_pieces', function ( $pieces, $context ) {
	if ( ! class_exists( 'ZP_Schema_Diccionario' ) ) {
		class ZP_Schema_Diccionario extends \Yoast\WP\SEO\Generators\Schema\Abstract_Schema_Piece {
			public static function hub() {
				static $h = null;
				if ( $h === null ) { $p = get_page_by_path( 'diccionario-del-proindiviso' ); $h = ( $p && $p->post_status === 'publish' ) ? (int) $p->ID : 0; }
				return $h;
			}
			public function is_needed() {
				if ( ! is_page() ) { return false; }
				$id = get_queried_object_id(); $hub = self::hub();
				return $hub && ( $id === $hub || (int) wp_get_post_parent_id( $id ) === $hub );
			}
			public function generate() {
				$id = get_queried_object_id(); $hub = self::hub(); $hub_url = get_permalink( $hub );
				if ( $id === $hub ) {
					$terms = get_pages( [ 'parent' => $hub, 'post_status' => 'publish', 'sort_column' => 'post_title', 'number' => 500 ] );
					$list = [];
					foreach ( $terms as $t ) {
						$item = [ '@type' => 'DefinedTerm', '@id' => get_permalink( $t ) . '#termino', 'name' => get_the_title( $t ), 'url' => get_permalink( $t ) ];
						if ( $t->post_excerpt ) { $item['description'] = wp_strip_all_tags( $t->post_excerpt ); }
						$list[] = $item;
					}
					return [ '@type' => 'DefinedTermSet', '@id' => $hub_url . '#diccionario', 'name' => 'Diccionario del proindiviso', 'description' => 'Términos jurídicos, fiscales y prácticos del proindiviso explicados de la A a la Z.', 'url' => $hub_url, 'inLanguage' => 'es', 'hasDefinedTerm' => $list ];
				}
				$p = get_post( $id );
				$desc = $p && $p->post_excerpt ? wp_strip_all_tags( $p->post_excerpt ) : get_post_meta( $id, '_yoast_wpseo_metadesc', true );
				return [ '@type' => 'DefinedTerm', '@id' => get_permalink( $id ) . '#termino', 'name' => get_the_title( $id ), 'description' => $desc, 'url' => get_permalink( $id ), 'inLanguage' => 'es', 'inDefinedTermSet' => [ '@id' => $hub_url . '#diccionario' ], 'mainEntityOfPage' => [ '@id' => get_permalink( $id ) ] ];
			}
		}
	}
	$pieces[] = new ZP_Schema_Diccionario( $context );
	return $pieces;
}, 11, 2 );
