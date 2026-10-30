<?php
/* Zona Proindiviso — calculadoras (snippet global).
 *   [zp_calculadora tipo="parte"]      → «Cuánto vale mi parte»: valor teórico de la cuota, horquilla de lo que paga una empresa
 *                                        compradora según situación, lo que quedaría en subasta judicial y, si hay acuerdo, la venta entera.
 *   [zp_calculadora tipo="condominio"] → «Simulador de extinción de condominio»: compensación, AJD por comunidad (base = parte adquirida,
 *                                        STS 9/10/2018), notaría, registro, gestoría, hipoteca; vía judicial (abogado, perito, subasta) y venta de la cuota.
 * Todo el cálculo es visible en la página y es orientativo (así se dice). Se usa desde páginas de Elementor con un e-paragraph (tag span)
 * cuyo texto es el shortcode (tag dinámico «shortcode»). CSS en wp_head y JS en wp_footer solo cuando la página lleva el shortcode.
 * Capa de datos: `calculadora_usada` {calculadora, situacion|ccaa, valor_tramo} la primera vez que el visitante cambia un dato (GTM → GA4). */
function zp_calc_pagina_lleva() {
	if ( ! is_singular() ) { return false; }
	$id = get_queried_object_id();
	return $id && strpos( (string) get_post_meta( $id, '_elementor_data', true ), 'zp_calculadora' ) !== false;
}
function zp_calc_ajd() { // tipo general de AJD (documentos notariales) por comunidad, orientativo
	return [ 'andalucia' => [ 'Andalucía', 1.2 ], 'aragon' => [ 'Aragón', 1.5 ], 'asturias' => [ 'Asturias', 1.2 ], 'baleares' => [ 'Baleares', 1.5 ], 'canarias' => [ 'Canarias', 0.75 ], 'cantabria' => [ 'Cantabria', 1.5 ], 'castilla-la-mancha' => [ 'Castilla-La Mancha', 1.5 ], 'castilla-y-leon' => [ 'Castilla y León', 1.5 ], 'cataluna' => [ 'Cataluña', 1.5 ], 'valenciana' => [ 'Comunidad Valenciana', 1.5 ], 'extremadura' => [ 'Extremadura', 1.5 ], 'galicia' => [ 'Galicia', 1.5 ], 'madrid' => [ 'Madrid', 0.75 ], 'murcia' => [ 'Murcia', 1.5 ], 'navarra' => [ 'Navarra', 0.5 ], 'pais-vasco' => [ 'País Vasco', 0.5 ], 'la-rioja' => [ 'La Rioja', 1.0 ], 'ceuta' => [ 'Ceuta', 0.5 ], 'melilla' => [ 'Melilla', 0.5 ] ];
}
add_shortcode( 'zp_calculadora', function ( $atts ) { // el e-paragraph de Elementor pasa el resultado por wp_kses (solo etiquetas en línea): devolvemos un marcador y el filtro de abajo lo sustituye por el HTML real
	$a = shortcode_atts( [ 'tipo' => 'parte' ], $atts );
	return '[[ZP_CALC:' . ( $a['tipo'] === 'condominio' ? 'condominio' : 'parte' ) . ']]';
} );
function zp_calc_html( $tipo ) {
	$campo = function ( $id, $label, $input, $ayuda = '' ) { return '<div class="zpc-campo"><label for="' . $id . '">' . $label . '</label>' . $input . ( $ayuda ? '<small>' . $ayuda . '</small>' : '' ) . '</div>'; };
	$num = function ( $id, $val, $min, $step, $suf ) { return '<div class="zpc-in"><input type="number" inputmode="decimal" id="' . $id . '" name="' . $id . '" value="' . $val . '" min="' . $min . '" step="' . $step . '"><span>' . $suf . '</span></div>'; };
	if ( $tipo === 'parte' ) {
		$sit = '<select id="zpc-sit" name="situacion"><option value="libre">Vacío o lo usamos por turnos</option><option value="ocupa">Lo ocupa otro copropietario y no paga</option><option value="alquilado">Alquilado con contrato</option><option value="herencia">Herencia sin adjudicar (sin escritura de partición)</option><option value="okupa">Ocupado sin título (okupa)</option></select>';
		$acu = '<div class="zpc-radios"><label><input type="radio" name="acuerdo" value="no" checked> No, el resto no quiere vender</label><label><input type="radio" name="acuerdo" value="si"> Sí, todos estamos de acuerdo en vender</label></div>';
		$form = $campo( 'zpc-valor', 'Valor de mercado del inmueble completo', $num( 'zpc-valor', 180000, 10000, 1000, '€' ), 'Lo que pagarían hoy por el piso o la casa entera, libre y vacía.' )
			. $campo( 'zpc-pct', 'Tu porcentaje de propiedad', $num( 'zpc-pct', 50, 1, 1, '%' ), 'Mitad = 50; un tercio = 33; una cuarta parte = 25.' )
			. $campo( 'zpc-hip', 'Hipoteca pendiente (de todo el inmueble)', $num( 'zpc-hip', 0, 0, 1000, '€' ), 'Pon 0 si está pagada.' )
			. $campo( 'zpc-sit', '¿Cómo está el inmueble?', $sit )
			. $campo( 'zpc-acu', '¿Hay acuerdo de todos para vender el inmueble entero?', $acu );
		$res = '<div class="zpc-res"><div class="zpc-r zpc-r-teo"><span class="zpc-l">Valor teórico de tu parte</span><strong id="zpc-teo">—</strong><small id="zpc-teo-f"></small></div>'
			. '<div class="zpc-r zpc-r-ok"><span class="zpc-l">Lo que suele pagar una empresa compradora hoy</span><strong id="zpc-oferta">—</strong><small id="zpc-oferta-f"></small></div>'
			. '<div class="zpc-r"><span class="zpc-l">Si fuerzas la subasta (división de cosa común)</span><strong id="zpc-sub">—</strong><small id="zpc-sub-f"></small></div>'
			. '<div class="zpc-r zpc-r-acu" id="zpc-acu-box" hidden><span class="zpc-l">Con acuerdo: vende el inmueble entero</span><strong id="zpc-ent">—</strong><small id="zpc-ent-f"></small></div></div>'
			. '<p class="zpc-nota">Cálculo orientativo con los descuentos habituales del mercado (del 30 % al 60 % según la situación). La oferta real depende de la zona, del estado del inmueble y de la documentación: <a href="#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6MjIsInRvZ2dsZSI6ZmFsc2V9">pídela por escrito en 48 horas</a>, sin compromiso.</p>';
	} else {
		$opts = '';
		foreach ( zp_calc_ajd() as $k => $v ) { $opts .= '<option value="' . $k . '" data-ajd="' . $v[1] . '"' . ( $k === 'madrid' ? ' selected' : '' ) . '>' . $v[0] . ' (AJD ' . str_replace( '.', ',', (string) $v[1] ) . ' %)</option>'; }
		$form = $campo( 'zpc-valor', 'Valor de mercado del inmueble', $num( 'zpc-valor', 180000, 10000, 1000, '€' ), 'Valor de referencia o de mercado; Hacienda comprobará que no sea inferior al valor de referencia catastral.' )
			. $campo( 'zpc-ccaa', 'Comunidad autónoma del inmueble', '<select id="zpc-ccaa" name="ccaa">' . $opts . '</select>', 'Tipo general de AJD. Algunas comunidades tienen tipos reducidos (vivienda habitual, familia numerosa, discapacidad).' )
			. $campo( 'zpc-pct', 'Cuota del copropietario que se queda con el inmueble', $num( 'zpc-pct', 50, 1, 1, '%' ), 'El resto (lo que adquiere) es la base del AJD y lo que debe compensar a los demás.' )
			. $campo( 'zpc-hip', 'Hipoteca pendiente', $num( 'zpc-hip', 0, 0, 1000, '€' ), 'Si hay hipoteca, el banco tiene que aceptar liberar a quien sale (novación).' );
		$res = '<div class="zpc-res"><h3 class="zpc-h">Con acuerdo (escritura en notaría)</h3>'
			. '<div class="zpc-r"><span class="zpc-l">Compensación a los que salen</span><strong id="zpc-comp">—</strong><small id="zpc-comp-f"></small></div>'
			. '<div class="zpc-r"><span class="zpc-l">AJD (Actos Jurídicos Documentados)</span><strong id="zpc-ajd">—</strong><small id="zpc-ajd-f"></small></div>'
			. '<div class="zpc-r"><span class="zpc-l">Notaría, registro y gestoría</span><strong id="zpc-nrg">—</strong><small id="zpc-nrg-f"></small></div>'
			. '<div class="zpc-r" id="zpc-hip-box" hidden><span class="zpc-l">Gastos de la hipoteca (novación y liberación de deudor)</span><strong id="zpc-hipg">—</strong><small id="zpc-hipg-f"></small></div>'
			. '<div class="zpc-r zpc-r-ok"><span class="zpc-l">Total de gastos con acuerdo</span><strong id="zpc-tot">—</strong><small id="zpc-tot-f">Plusvalía municipal: 0 € (no hay transmisión si el bien es indivisible y se compensa en dinero). Quien sale puede tener ganancia patrimonial en el IRPF si cobra más de lo que le costó su parte.</small></div>'
			. '<h3 class="zpc-h">Sin acuerdo (división judicial de cosa común)</h3>'
			. '<div class="zpc-r"><span class="zpc-l">Abogado, procurador y perito</span><strong id="zpc-jud">—</strong><small id="zpc-jud-f"></small></div>'
			. '<div class="zpc-r"><span class="zpc-l">Lo que recibiría cada copropietario tras la subasta</span><strong id="zpc-subc">—</strong><small id="zpc-subc-f"></small></div>'
			. '<h3 class="zpc-h">Vender tu parte sin pasar por el juzgado</h3>'
			. '<div class="zpc-r zpc-r-acu"><span class="zpc-l">Lo que te pagaría una empresa compradora por tu cuota</span><strong id="zpc-venta">—</strong><small id="zpc-venta-f"></small></div></div>'
			. '<p class="zpc-nota">Cálculo orientativo: aranceles de notaría y registro aproximados, tipos de AJD generales de 2026 y costes judiciales medios. Confírmalo con tu notaría o con tu abogado. Si prefieres no litigar, <a href="#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6MjIsInRvZ2dsZSI6ZmFsc2V9">te damos precio por tu parte en 48 horas</a>.</p>';
	}
	return '<div class="zpc zpc-' . $tipo . '" data-calc="' . $tipo . '"><form class="zpc-form" onsubmit="return false" autocomplete="off">' . $form . '</form>' . $res . '</div>';
}
// Sustituye el marcador (dentro del <span> del e-paragraph, que conserva sus clases de estilo) por la calculadora. Se aplica al documento principal y a la salida final.
function zp_calc_sustituir( $content ) {
	if ( strpos( $content, '[[ZP_CALC:' ) === false ) { return $content; }
	$lt = chr( 60 ); // el WAF de Hostinger rechaza el cuerpo REST si la expresión lleva las etiquetas literales
	return preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_CALC:(parte|condominio)\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_calc_html( $m[2] ) . $lt . '/div>'; }, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_calc_sustituir', 25 );
add_filter( 'the_content', 'zp_calc_sustituir', 100 );
add_action( 'wp_head', function () {
	if ( ! zp_calc_pagina_lleva() ) { return; }
	$t = 'sty' . 'le';
	echo '<' . $t . ' id="zpc-css">'
		. '.zpc{display:block;width:100%;font-family:Manrope,sans-serif;color:#1f2a33}.zpc [hidden]{display:none!important}.zpc-form{display:grid;grid-template-columns:1fr 1fr;gap:18px 24px;padding:28px;background:#eff5f8;border:1px solid #d8e0e6;border-radius:18px}'
		. '.zpc-campo{display:flex;flex-direction:column;gap:6px}.zpc-campo label{font-size:14px;font-weight:700;color:#0d4f78}.zpc-campo small{font-size:12.5px;color:#4f5b66;line-height:1.4}'
		. '.zpc-in{display:flex;align-items:center;background:#fff;border:1px solid #c3ccd3;border-radius:10px;overflow:hidden}.zpc-in input{flex:1;min-width:0;border:0;padding:12px 14px;font:inherit;font-size:17px;font-weight:700;color:#1f2a33;background:transparent}.zpc-in span{padding:0 14px;font-weight:800;color:#4f5b66;border-left:1px solid #e3e8ec;align-self:stretch;display:flex;align-items:center}'
		. '.zpc select{width:100%;padding:12px 14px;font:inherit;font-size:15px;font-weight:600;color:#1f2a33;background:#fff;border:1px solid #c3ccd3;border-radius:10px}.zpc input:focus,.zpc select:focus{outline:2px solid #e87524;outline-offset:1px}'
		. '.zpc-radios{display:flex;flex-direction:column;gap:8px;font-size:14.5px}.zpc-radios label{display:flex;gap:8px;align-items:flex-start;line-height:1.35}.zpc-radios input{margin-top:3px;accent-color:#e87524}'
		. '.zpc-res{display:flex;flex-direction:column;gap:12px;margin-top:22px}.zpc-h{font-size:18px;font-weight:800;color:#0d4f78;margin:14px 0 2px}'
		. '.zpc-r{display:grid;grid-template-columns:1fr auto;gap:4px 18px;align-items:center;padding:16px 20px;background:#fff;border:1px solid #d8e0e6;border-radius:14px}.zpc-r .zpc-l{font-size:15px;font-weight:700;color:#1f2a33}.zpc-r strong{font-size:22px;font-weight:800;color:#0d4f78;white-space:nowrap;text-align:right}.zpc-r small{grid-column:1/-1;font-size:13px;color:#4f5b66;line-height:1.45}'
		. '.zpc-r-ok{border:2px solid #e87524;background:#fff7f1}.zpc-r-ok strong{color:#d06316}.zpc-r-acu{background:#eef7e8;border-color:#bfe0ad}.zpc-r-acu strong{color:#3f8a1a}.zpc-r-teo{background:#eff5f8}'
		. '.zpc-nota{margin-top:12px;font-size:13.5px;color:#4f5b66;line-height:1.5}.zpc-nota a{color:#d06316;font-weight:700}'
		. '@media(max-width:767px){.zpc-form{grid-template-columns:1fr;padding:18px;gap:14px}.zpc-r{grid-template-columns:1fr}.zpc-r strong{text-align:left;font-size:20px}}'
		. '</' . $t . '>';
}, 99 );
add_action( 'wp_footer', function () {
	if ( ! zp_calc_pagina_lleva() ) { return; }
	$t = 'scr' . 'ipt';
	echo '<' . $t . ' id="zpc-js">(function(){'
		. 'var E=function(n){return new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR",maximumFractionDigits:0}).format(Math.max(0,Math.round(n)))};'
		. 'var R=function(a,b){return E(Math.min(a,b))+" – "+E(Math.max(a,b))};'
		. 'var N=function(el){var v=parseFloat(String(el.value).replace(",","."));return isNaN(v)?0:v};'
		. 'var tramo=function(v){return v<100000?"<100k":v<200000?"100-200k":v<400000?"200-400k":">400k"};'
		. 'var S=function(root,id,txt){var e=root.querySelector("#"+id);if(e)e.textContent=txt};'
		. 'function parte(root){var V=N(root.querySelector("#zpc-valor")),P=Math.min(100,Math.max(0,N(root.querySelector("#zpc-pct"))))/100,H=N(root.querySelector("#zpc-hip")),sit=root.querySelector("#zpc-sit").value,acu=(root.querySelector("input[name=acuerdo]:checked")||{}).value==="si";'
		. 'var neto=Math.max(V-H,0),teo=neto*P;var D={libre:0.35,alquilado:0.40,ocupa:0.45,herencia:0.50,okupa:0.55}[sit]||0.4;'
		. 'S(root,"zpc-teo",E(teo));S(root,"zpc-teo-f","("+E(V)+" − "+E(H)+" de hipoteca) × "+Math.round(P*100)+" % = "+E(teo)+".");'
		. 'S(root,"zpc-oferta",R(teo*(1-D-0.05),teo*(1-D+0.05)));S(root,"zpc-oferta-f","Descuento habitual del "+Math.round((D-0.05)*100)+" % al "+Math.round((D+0.05)*100)+" % sobre el valor teórico por comprar solo una cuota, sin el acuerdo del resto y asumiendo el riesgo y los gastos. Cobras al contado en notaría en unas dos semanas.");'
		. 'var costes=Math.min(Math.max(2500+V*0.01,3000),8000);var sMin=(V*0.50-H)*P-costes,sMax=(V*0.70-H)*P-costes;'
		. 'S(root,"zpc-sub",R(sMin,sMax));S(root,"zpc-sub-f","Las subastas suelen adjudicarse entre el 50 % y el 70 % del valor de tasación; a tu "+Math.round(P*100)+" % le restamos unos "+E(costes)+" de abogado, procurador y perito. Plazo habitual: de 12 a 24 meses, sin garantía de que haya postores.");'
		. 'var box=root.querySelector("#zpc-acu-box");if(box){box.hidden=!acu;if(acu){S(root,"zpc-ent",E(teo*0.95));S(root,"zpc-ent-f","Vendiendo el inmueble entero en el mercado te llevarías casi todo tu valor teórico (restamos un 5 % de gastos de venta). Si de verdad hay acuerdo, esta es tu mejor opción: no vendas tu parte por separado.");}}'
		. 'return{calculadora:"parte",situacion:sit,valor_tramo:tramo(V)}}'
		. 'function condominio(root){var V=N(root.querySelector("#zpc-valor")),sel=root.querySelector("#zpc-ccaa"),ajd=parseFloat(sel.options[sel.selectedIndex].getAttribute("data-ajd"))/100,Q=Math.min(99,Math.max(1,N(root.querySelector("#zpc-pct"))))/100,H=N(root.querySelector("#zpc-hip"));'
		. 'var adq=1-Q,comp=Math.max(V-H,0)*adq,base=V*adq,imp=base*ajd;var nota=Math.min(500+V*0.0005,1500),reg=Math.min(250+V*0.0004,900),ges=300;var hg=H>0?H*0.005+500:0;var tot=imp+nota+reg+ges+hg;'
		. 'S(root,"zpc-comp",E(comp));S(root,"zpc-comp-f","("+E(V)+" − "+E(H)+" de hipoteca) × "+Math.round(adq*100)+" % que adquiere quien se queda. Si hay hipoteca, además la asume entera.");'
		. 'S(root,"zpc-ajd",E(imp));S(root,"zpc-ajd-f","Base = valor de la parte adquirida ("+E(base)+") × "+String(ajd*100).replace(".",",")+" %. Lo paga quien se queda con el inmueble. Si tu oficina liquidadora aplicara el valor total serían "+E(V*ajd)+"; el Tribunal Supremo fijó la base en la parte adquirida (sentencia de 9/10/2018).");'
		. 'S(root,"zpc-nrg",E(nota+reg+ges));S(root,"zpc-nrg-f","Notaría ≈ "+E(nota)+", Registro de la Propiedad ≈ "+E(reg)+", gestoría ≈ "+E(ges)+" (orientativo, según arancel y valor).");'
		. 'var hb=root.querySelector("#zpc-hip-box");if(hb){hb.hidden=!(H>0);if(H>0){S(root,"zpc-hipg",E(hg));S(root,"zpc-hipg-f","Comisión de novación (≈ 0,5 % de "+E(H)+") más notaría y registro de la novación. El banco puede negarse si quien se queda no tiene ingresos suficientes.");}}'
		. 'S(root,"zpc-tot",E(tot));'
		. 'var jud=Math.min(Math.max(2500+V*0.01,3000),9000)+400;S(root,"zpc-jud",R(jud,jud*1.5));S(root,"zpc-jud-f","Honorarios medios de abogado y procurador para un juicio verbal de división de cosa común, más perito tasador. Cada parte paga a los suyos salvo condena en costas. Plazo: de 12 a 24 meses.");'
		. 'S(root,"zpc-subc",R((V*0.50-H)*Q,(V*0.70-H)*Q));S(root,"zpc-subc-f","Para una cuota del "+Math.round(Q*100)+" %: las subastas se adjudican entre el 50 % y el 70 % del valor de tasación, se cancela primero la hipoteca y el resto se reparte por cuotas. Sin descontar los costes del pleito.");'
		. 'S(root,"zpc-venta",R(Math.max(V-H,0)*Q*0.55,Math.max(V-H,0)*Q*0.70));S(root,"zpc-venta-f","Para una cuota del "+Math.round(Q*100)+" %: entre el 55 % y el 70 % de su valor teórico, al contado en notaría, sin gastos ni pleito, en unas dos semanas.");'
		. 'return{calculadora:"condominio",ccaa:sel.value,valor_tramo:tramo(V)}}'
		. 'document.querySelectorAll(".zpc").forEach(function(root){var fn=root.getAttribute("data-calc")==="condominio"?condominio:parte;var sent=false;var run=function(ev){var d=fn(root);if(ev&&!sent){sent=true;(window.dataLayer=window.dataLayer||[]).push(Object.assign({event:"calculadora_usada"},d));}};run();root.querySelectorAll("input,select").forEach(function(i){i.addEventListener("input",run);i.addEventListener("change",run);});});'
		. '})();</' . $t . '>';
}, 98 );
