global $wpdb;
$wpdb->query( "DELETE FROM {$wpdb->postmeta} WHERE meta_key IN ( '_elementor_css', '_elementor_page_assets', '_elementor_element_cache' )" );
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_elementor%' OR option_name LIKE '_transient_timeout_elementor%' OR option_name LIKE '_site_transient_elementor%'" );
if ( class_exists( '\Elementor\Plugin' ) ) { \Elementor\Plugin::$instance->files_manager->clear_cache(); }
$dir = wp_upload_dir()['basedir'] . '/elementor/css';
if ( is_dir( $dir ) ) { foreach ( glob( $dir . '/*.css' ) as $f ) { @unlink( $f ); } }
update_option( 'zp_css_cleared', current_time( 'mysql' ) );
