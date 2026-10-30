<?php
/* Zona Proindiviso — modelos descargables y bloques de preguntas frecuentes (snippet 226, global).
 *   [zp_modelo id="modelo-burofax-copropietario"] → caja con el texto completo del modelo (huecos [EN MAYÚSCULAS] resaltados), botón
 *       «Copiar el texto» y enlace «Descargar en Word». Datos en la opción zp_modelo_{id} = {titulo, texto, docx} (la escribe modelos.py).
 *   [zp_faq_bloque n="2"] → preguntas del bloque 2 como desplegables (pregunta en h3). Datos en la opción zp_faq_bloque_{n} = [[p, r], ...]
 *       (la escribe faq.py; una opción por bloque porque el WAF de Hostinger corta cuerpos REST de más de ~15 KB). En wp_head se imprime
 *       UN solo schema FAQPage con todas las preguntas de todos los bloques de la página.
 * Igual que las calculadoras: el e-paragraph de Elementor pasa el shortcode por wp_kses → marcador + filtro de contenido.
 * Capa de datos: `modelo_copiado` {modelo} al copiar (la descarga del .docx la mide sola la medición mejorada de GA4: file_download). */
function zp_mf_pagina( $que ) {
	if ( ! is_singular() ) { return false; }
	$id = get_queried_object_id();
	return $id && strpos( (string) get_post_meta( $id, '_elementor_data', true ), $que ) !== false;
}
add_shortcode( 'zp_modelo', function ( $a ) { $a = shortcode_atts( [ 'id' => '' ], $a ); return '[[ZP_MODELO:' . sanitize_key( $a['id'] ) . ']]'; } );
add_shortcode( 'zp_faq_bloque', function ( $a ) { $a = shortcode_atts( [ 'n' => '1' ], $a ); return '[[ZP_FAQ:' . absint( $a['n'] ) . ']]'; } );
function zp_mf_modelo_html( $id ) {
	$lt = chr( 60 ); $m = get_option( 'zp_modelo_' . $id );
	if ( ! is_array( $m ) || empty( $m['texto'] ) ) { return ''; }
	$ps = '';
	foreach ( preg_split( '/\n\s*\n/', trim( $m['texto'] ) ) as $p ) {
		$p = esc_html( trim( $p ) );
		$p = preg_replace( '/\[([^\]]{2,80})\]/u', $lt . 'mark>[$1]' . $lt . '/mark>', $p );
		$ps .= $lt . 'p>' . nl2br( $p ) . $lt . '/p>';
	}
	$dl = ! empty( $m['docx'] ) ? $lt . 'a class="zpm-dl" href="' . esc_url( $m['docx'] ) . '" download>Descargar en Word (.docx)' . $lt . '/a>' : '';
	return $lt . 'div class="zpm" data-modelo="' . esc_attr( $id ) . '">' . $lt . 'div class="zpm-bar">' . $lt . 'span class="zpm-t">' . esc_html( $m['titulo'] ?? '' ) . $lt . '/span>'
		. $lt . 'div class="zpm-acc">' . $lt . 'button type="button" class="zpm-copy">Copiar el texto' . $lt . '/button>' . $dl . $lt . '/div>' . $lt . '/div>'
		. $lt . 'div class="zpm-doc">' . $ps . $lt . '/div>' . $lt . 'p class="zpm-nota">Los huecos en ' . $lt . 'mark>[MAYÚSCULAS]' . $lt . '/mark> son los que tienes que rellenar. Modelo orientativo: revísalo con un abogado si hay importes altos o conflicto.' . $lt . '/p>' . $lt . '/div>';
}
function zp_mf_faq_items( $n ) {
	$b = get_option( 'zp_faq_bloque_' . $n );
	return is_array( $b ) ? $b : [];
}
function zp_mf_faq_html( $n ) {
	$lt = chr( 60 ); $h = '';
	foreach ( zp_mf_faq_items( $n ) as $i => $qa ) {
		$h .= $lt . 'details class="zpq-i"' . ( $i === 0 ? ' open' : '' ) . '>' . $lt . 'summary>' . $lt . 'h3>' . esc_html( $qa[0] ) . $lt . '/h3>' . $lt . '/summary>'
			. $lt . 'div class="zpq-a">' . $lt . 'p>' . wp_kses( $qa[1], [ 'a' => [ 'href' => [] ], 'strong' => [] ] ) . $lt . '/p>' . $lt . '/div>' . $lt . '/details>';
	}
	return $h ? $lt . 'div class="zpq">' . $h . $lt . '/div>' : '';
}
function zp_mf_sustituir( $content ) {
	if ( strpos( $content, '[[ZP_' ) === false ) { return $content; }
	$lt = chr( 60 );
	$content = preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_MODELO:([a-z0-9_\-]+)\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_mf_modelo_html( $m[2] ) . $lt . '/div>'; }, $content );
	return preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_FAQ:(\d+)\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_mf_faq_html( (int) $m[2] ) . $lt . '/div>'; }, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_mf_sustituir', 26 );
add_filter( 'the_content', 'zp_mf_sustituir', 101 );
add_action( 'wp_head', function () {
	$mod = zp_mf_pagina( 'zp_modelo' ); $faq = zp_mf_pagina( 'zp_faq_bloque' );
	if ( ! $mod && ! $faq ) { return; }
	$t = 'sty' . 'le';
	$css = <<<'CSS'
.zpm{display:block;width:100%;font-family:Manrope,sans-serif;color:#1f2a33;background:#fff;border:1px solid #d8e0e6;border-radius:18px;overflow:hidden}
.zpm-bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:16px 22px;background:#0d4f78;color:#fff}
.zpm-t{font-size:16px;font-weight:800}.zpm-acc{display:flex;flex-wrap:wrap;gap:10px}
.zpm-copy,.zpm-dl{display:inline-flex;align-items:center;padding:9px 16px;border-radius:999px;font:inherit;font-size:14px;font-weight:800;text-decoration:none;cursor:pointer}
.zpm-copy{background:#fff;color:#0d4f78;border:0}.zpm-dl{background:#e87524;color:#fff;border:0}.zpm-copy:hover{background:#eff5f8}.zpm-dl:hover{background:#d06316}
.zpm-doc{max-height:560px;overflow:auto;padding:24px 28px;font-size:15.5px;line-height:1.7;background:#fbfcfd}
.zpm-doc p{margin:0 0 14px}.zpm-doc mark{background:#fff1e5;color:#b45309;padding:0 3px;border-radius:4px;font-family:Manrope,sans-serif;font-size:.9em;font-weight:700}
.zpm-nota{margin:0;padding:12px 22px;font-size:13px;color:#4f5b66;border-top:1px solid #e3e8ec;background:#fff}.zpm-nota mark{background:#fff1e5;color:#b45309}
.zpq{display:flex;flex-direction:column;gap:10px;width:100%;font-family:Manrope,sans-serif}
.zpq-i{background:#fff;border:1px solid #d8e0e6;border-radius:14px;overflow:hidden}
.zpq-i summary{list-style:none;cursor:pointer;padding:16px 52px 16px 20px;position:relative}.zpq-i summary::-webkit-details-marker{display:none}
.zpq-i summary::after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:22px;font-weight:700;color:#e87524}
.zpq-i[open] summary::after{content:"−"}
.zpq-i summary h3{margin:0;font-size:17px;line-height:1.35;font-weight:800;color:#0d4f78}
.zpq-a{padding:0 20px 18px;font-size:16px;line-height:1.6;color:#1f2a33}.zpq-a p{margin:0}.zpq-a a{color:#d06316;font-weight:700}
@media(max-width:767px){.zpm-doc{padding:18px;font-size:14.5px;max-height:460px}.zpm-bar{padding:14px 16px}.zpq-i summary h3{font-size:16px}}
CSS;
	echo '<' . $t . ' id="zpmf-css">' . $css . '</' . $t . '>';
	if ( $faq ) {
		$main = [];
		for ( $n = 1; $n <= 12; $n++ ) {
			foreach ( zp_mf_faq_items( $n ) as $qa ) {
				$main[] = [ '@type' => 'Question', 'name' => wp_strip_all_tags( $qa[0] ), 'acceptedAnswer' => [ '@type' => 'Answer', 'text' => wp_kses( $qa[1], [ 'a' => [ 'href' => [] ] ] ) ] ];
			}
		}
		if ( $main ) {
			$s = 'scr' . 'ipt';
			echo '<' . $s . ' type="application/ld+json" id="zp-faqpage">' . wp_json_encode( [ '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $main ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</' . $s . '>';
		}
	}
}, 99 );
add_action( 'wp_footer', function () {
	if ( ! zp_mf_pagina( 'zp_modelo' ) ) { return; }
	$t = 'scr' . 'ipt';
	$js = <<<'JS'
document.querySelectorAll(".zpm").forEach(function(m){var b=m.querySelector(".zpm-copy");if(!b)return;b.addEventListener("click",function(){var txt=[].map.call(m.querySelectorAll(".zpm-doc p"),function(p){return p.innerText}).join("\n\n");var ok=function(){b.textContent="Copiado";setTimeout(function(){b.textContent="Copiar el texto"},2200);(window.dataLayer=window.dataLayer||[]).push({event:"modelo_copiado",modelo:m.getAttribute("data-modelo")})};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok,function(){})}else{var a=document.createElement("textarea");a.value=txt;document.body.appendChild(a);a.select();try{document.execCommand("copy");ok()}catch(e){}document.body.removeChild(a)}})});
JS;
	echo '<' . $t . ' id="zpm-js">' . $js . '</' . $t . '>';
}, 98 );
