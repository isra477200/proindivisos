<?php
/* Zona Proindiviso — calculadoras 2 (snippet 224, global; CSS y JS en snippet_calculadoras2_assets.php).
 *   [zp_calculadora_x tipo="impuestos"] → «Calculadora de impuestos al vender tu parte»: plusvalía municipal (método objetivo con los
 *                                          coeficientes máximos vigentes y método real, se aplica el menor) e IRPF (escala del ahorro
 *                                          2026; no residentes 19 %; exención de mayores de 65 en vivienda habitual).
 *   [zp_calculadora_x tipo="uso"]       → «Calculadora de compensación por uso exclusivo»: renta de mercado × tu porcentaje × meses
 *                                          (tope de 60 meses, art. 1966 CC), menos los gastos de tu parte que haya pagado el ocupante.
 *   [zp_calculadora_x tipo="gastos"]    → «Calculadora de gastos entre copropietarios»: reparto por cuotas (art. 393 y 395 CC) y saldo
 *                                          de cada uno según lo que ya ha pagado, con quién debe a quién.
 * Igual que las calculadoras 1: el e-paragraph de Elementor pasa el shortcode por wp_kses, así que devolvemos un marcador y el filtro
 * lo sustituye por el HTML. La raíz es .zpcx (no .zpc) para que el JS de las calculadoras 1 no la toque; reutiliza sus clases de estilo
 * (zpc-form, zpc-campo, zpc-in, zpc-r...), cuyo CSS se imprime porque «zp_calculadora_x» contiene «zp_calculadora».
 * Capa de datos: `calculadora_usada` {calculadora: impuestos|uso|gastos, situacion, valor_tramo} la primera vez que se cambia un dato. */
function zp_calcx_pagina_lleva() {
	if ( ! is_singular() ) { return false; }
	$id = get_queried_object_id();
	return $id && strpos( (string) get_post_meta( $id, '_elementor_data', true ), 'zp_calculadora_x' ) !== false;
}
add_shortcode( 'zp_calculadora_x', function ( $atts ) {
	$a = shortcode_atts( [ 'tipo' => 'impuestos' ], $atts );
	$t = in_array( $a['tipo'], [ 'impuestos', 'uso', 'gastos' ], true ) ? $a['tipo'] : 'impuestos';
	return '[[ZP_CALCX:' . $t . ']]';
} );
function zp_calcx_html( $tipo ) {
	$lt = chr( 60 );
	$campo = function ( $id, $label, $input, $ayuda = '' ) use ( $lt ) { return $lt . 'div class="zpc-campo">' . $lt . 'label for="' . $id . '">' . $label . $lt . '/label>' . $input . ( $ayuda ? $lt . 'small>' . $ayuda . $lt . '/small>' : '' ) . $lt . '/div>'; };
	$num = function ( $id, $val, $min, $step, $suf ) use ( $lt ) { return $lt . 'div class="zpc-in">' . $lt . 'input type="number" inputmode="decimal" id="' . $id . '" name="' . $id . '" value="' . $val . '" min="' . $min . '" step="' . $step . '">' . $lt . 'span>' . $suf . $lt . '/span>' . $lt . '/div>'; };
	$r = function ( $id, $label, $cls = '' ) use ( $lt ) { return $lt . 'div class="zpc-r' . ( $cls ? ' ' . $cls : '' ) . '" id="' . $id . '-box">' . $lt . 'span class="zpc-l">' . $label . $lt . '/span>' . $lt . 'strong id="' . $id . '">—' . $lt . '/strong>' . $lt . 'small id="' . $id . '-f">' . $lt . '/small>' . $lt . '/div>'; };
	$pop = '#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6MjIsInRvZ2dsZSI6ZmFsc2V9';
	if ( $tipo === 'impuestos' ) {
		$y = (int) gmdate( 'Y' );
		$form = $campo( 'zpx-venta', 'Precio de venta de tu parte', $num( 'zpx-venta', 60000, 0, 500, '€' ), 'Lo que vas a cobrar por tu cuota.' )
			. $campo( 'zpx-adq', 'Valor de adquisición de tu parte', $num( 'zpx-adq', 45000, 0, 500, '€' ), 'Heredada: valor declarado en sucesiones más impuesto y gastos pagados. Comprada: precio más gastos e impuestos.' )
			. $campo( 'zpx-anio', 'Año en que la adquiriste', $num( 'zpx-anio', $y - 12, 1950, 1, 'año' ), 'En una herencia, el año del fallecimiento.' )
			. $campo( 'zpx-gastos', 'Gastos de la venta a tu cargo', $num( 'zpx-gastos', 0, 0, 50, '€' ), 'Notaría, gestoría, comisiones. Si compra una empresa como la nuestra, suelen ser 0.' )
			. $campo( 'zpx-suelo', 'Valor catastral del suelo (inmueble entero)', $num( 'zpx-suelo', 40000, 0, 500, '€' ), 'Viene en el recibo del IBI.' )
			. $campo( 'zpx-vct', 'Valor catastral total (inmueble entero)', $num( 'zpx-vct', 90000, 1, 500, '€' ), 'También en el recibo del IBI: suelo más construcción.' )
			. $campo( 'zpx-pct', 'Tu porcentaje de propiedad', $num( 'zpx-pct', 50, 1, 1, '%' ), 'Mitad = 50; un tercio = 33.' )
			. $campo( 'zpx-tipo', 'Tipo de plusvalía de tu ayuntamiento', $num( 'zpx-tipo', 29, 0, 0.5, '%' ), 'Máximo legal 30 %. Está en la ordenanza fiscal municipal.' )
			. $campo( 'zpx-res', '¿Dónde resides?', $lt . 'select id="zpx-res" name="residencia">' . $lt . 'option value="es">En España (IRPF)' . $lt . '/option>' . $lt . 'option value="no">Fuera de España (no residente)' . $lt . '/option>' . $lt . '/select>' )
			. $campo( 'zpx-65', '¿Tienes 65 años o más y es tu vivienda habitual?', $lt . 'div class="zpc-radios">' . $lt . 'label>' . $lt . 'input type="radio" name="exento" value="no" checked> No' . $lt . '/label>' . $lt . 'label>' . $lt . 'input type="radio" name="exento" value="si"> Sí, vivo en ella y tengo 65 o más' . $lt . '/label>' . $lt . '/div>' );
		$res = $lt . 'div class="zpc-res">' . $r( 'zpx-plus', 'Plusvalía municipal (la paga el vendedor)' ) . $r( 'zpx-irpf', 'IRPF o impuesto de no residentes' ) . $r( 'zpx-tot', 'Total de impuestos', 'zpc-r-teo' ) . $r( 'zpx-neto', 'Lo que te queda limpio', 'zpc-r-ok' ) . $lt . '/div>'
			. $lt . 'p class="zpc-nota">Cálculo orientativo con la escala del ahorro de 2026 y los coeficientes máximos de plusvalía vigentes; tu ayuntamiento puede aplicar otros menores y hay bonificaciones municipales. País Vasco y Navarra tienen normas forales propias. Confírmalo con tu asesor. Si quieres una cifra en firme por tu parte, ' . $lt . 'a href="' . $pop . '">pídenos oferta por escrito en 48 horas' . $lt . '/a>.' . $lt . '/p>';
	} elseif ( $tipo === 'uso' ) {
		$form = $campo( 'zpx-renta', 'Renta mensual de mercado del inmueble entero', $num( 'zpx-renta', 900, 0, 10, '€' ), 'Lo que se pagaría hoy de alquiler por la vivienda completa.' )
			. $campo( 'zpx-pct', 'Tu porcentaje de propiedad', $num( 'zpx-pct', 50, 1, 1, '%' ), 'La parte de la renta que te corresponde.' )
			. $campo( 'zpx-meses', 'Meses de uso exclusivo desde que lo reclamaste', $num( 'zpx-meses', 24, 0, 1, 'meses' ), 'Cuenta desde tu reclamación por escrito (burofax). Como máximo, 60 meses.' )
			. $campo( 'zpx-gm', 'Gastos de tu parte que paga el ocupante', $num( 'zpx-gm', 0, 0, 5, '€/mes' ), 'IBI, comunidad o seguro que adelanta por ti. Se descuentan.' );
		$res = $lt . 'div class="zpc-res">' . $r( 'zpx-mes', 'Compensación que te corresponde al mes' ) . $r( 'zpx-acum', 'Acumulado del periodo', 'zpc-r-teo' ) . $r( 'zpx-desc', 'A descontar por gastos que pagó por ti' ) . $r( 'zpx-neto', 'Lo que podrías reclamar', 'zpc-r-ok' ) . $lt . '/div>'
			. $lt . 'p class="zpc-nota">Cálculo orientativo. Los juzgados suelen reconocer la compensación desde que la reclamas de forma fehaciente y con el límite de cinco años de las prestaciones periódicas (art. 1966 CC); la renta de mercado se acredita con una tasación o testigos de alquiler. Si prefieres no pleitear, ' . $lt . 'a href="' . $pop . '">te compramos la parte' . $lt . '/a>.' . $lt . '/p>';
	} else {
		$form = $campo( 'zpx-ibi', 'IBI anual', $num( 'zpx-ibi', 450, 0, 5, '€' ) )
			. $campo( 'zpx-com', 'Comunidad de propietarios al mes', $num( 'zpx-com', 60, 0, 1, '€/mes' ) )
			. $campo( 'zpx-seg', 'Seguro del hogar anual', $num( 'zpx-seg', 180, 0, 5, '€' ) )
			. $campo( 'zpx-bas', 'Tasa de basuras anual', $num( 'zpx-bas', 90, 0, 5, '€' ) )
			. $campo( 'zpx-obr', 'Derramas u obras del año', $num( 'zpx-obr', 0, 0, 50, '€' ) )
			. $campo( 'zpx-otr', 'Otros gastos del año', $num( 'zpx-otr', 0, 0, 5, '€' ), 'Suministros mínimos, reparaciones, cerrajero...' );
		$res = $lt . 'div class="zpcx-cop">' . $lt . 'p class="zpc-h">Copropietarios: porcentaje y lo que ha pagado cada uno este año' . $lt . '/p>' . $lt . 'div class="zpcx-filas" id="zpx-filas">' . $lt . '/div>'
			. $lt . 'button type="button" class="zpcx-add" id="zpx-add">+ Añadir copropietario' . $lt . '/button>' . $lt . 'p class="zpcx-aviso" id="zpx-aviso" hidden>' . $lt . '/p>' . $lt . '/div>'
			. $lt . 'div class="zpc-res">' . $r( 'zpx-total', 'Gastos totales del año', 'zpc-r-teo' ) . $lt . 'div class="zpcx-tabla" id="zpx-tabla">' . $lt . '/div>' . $r( 'zpx-quien', 'Quién debe a quién', 'zpc-r-ok' ) . $lt . '/div>'
			. $lt . 'p class="zpc-nota">Reparto por cuotas según los artículos 393 y 395 del Código Civil: cada copropietario paga los gastos de conservación en proporción a su parte, aunque no use el inmueble. La hipoteca es otra cosa: responde quien la firmó. Si estás harto de pagar por algo que no usas, ' . $lt . 'a href="' . $pop . '">te compramos la parte' . $lt . '/a>.' . $lt . '/p>';
	}
	return $lt . 'div class="zpcx zpcx-' . $tipo . '" data-calcx="' . $tipo . '">' . $lt . 'form class="zpc-form" onsubmit="return false" autocomplete="off">' . $form . $lt . '/form>' . $res . $lt . '/div>';
}
function zp_calcx_sustituir( $content ) {
	if ( strpos( $content, '[[ZP_CALCX:' ) === false ) { return $content; }
	$lt = chr( 60 );
	return preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_CALCX:(impuestos|uso|gastos)\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_calcx_html( $m[2] ) . $lt . '/div>'; }, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_calcx_sustituir', 25 );
add_filter( 'the_content', 'zp_calcx_sustituir', 100 );
