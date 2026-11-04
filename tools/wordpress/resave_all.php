add_action( 'init', function () {
	if ( ! class_exists( '\Elementor\Plugin' ) ) { return; }
	global $wpdb;
	$done = (array) get_option( 'zp_resave_done', [] );
	$ids = $wpdb->get_col( "SELECT DISTINCT p.ID FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = '_elementor_data' WHERE p.post_status IN ('publish','draft','private') AND p.post_type NOT IN ('revision') ORDER BY p.ID ASC" );
	$ids = array_values( array_diff( array_map( 'intval', $ids ), array_map( 'intval', $done ) ) );
	$batch = array_slice( $ids, 0, 45 );
	$t0 = microtime( true );
	foreach ( $batch as $id ) {
		if ( microtime( true ) - $t0 > 50 ) { break; }
		$doc = \Elementor\Plugin::$instance->documents->get( $id, false );
		if ( ! $doc ) { $done[] = $id; continue; }
		$data = $doc->get_elements_data();
		if ( empty( $data ) ) { $done[] = $id; continue; }
		$doc->save( [ 'elements' => $data, 'settings' => $doc->get_settings() ] );
		$done[] = $id;
	}
	update_option( 'zp_resave_done', $done );
	update_option( 'zp_resave_left', count( $ids ) - count( array_intersect( $batch, $done ) ) );
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}, 20 );
