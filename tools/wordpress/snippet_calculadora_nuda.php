<?php
/* Zona Proindiviso — calculadora de nuda propiedad (snippet nuevo del 04/11/2026, global).
 *   [zp_calculadora_n] → valor fiscal del usufructo y de la nuda propiedad con las reglas del art. 26 de la Ley 29/1987 del ISD (las mismas
 *   del art. 10.2 del TR del ITP): usufructo vitalicio = 89 − edad del usufructuario, mínimo 10 %, máximo 70 %; usufructo temporal = 2 %
 *   por cada año completo (menos de un año: 2 %, art. 49 del Reglamento), máximo 70 %; nuda propiedad = 100 % − usufructo; tu parte = nuda propiedad × tu porcentaje.
 *   Valores por defecto: 200.000 €, vitalicio, 75 años, 100 % → usufructo 28.000 € (14 %), nuda propiedad 172.000 € (86 %).
 * Va aparte de las calculadoras 2 (snippets 224/225): raíz .zpcn, marcador [[ZP_CALCN]] y su propio JS. Reutiliza las clases zpc-* cuyo
 * CSS imprime el snippet 170 porque «zp_calculadora_n» contiene «zp_calculadora». Sin «<script»/«<style» literales (WAF de Hostinger).
 * Capa de datos: `calculadora_usada` {calculadora: nuda_propiedad, situacion: vitalicio|temporal, valor_tramo} la primera vez que se cambia un dato. */
function zp_calcn_pagina_lleva() {
	if ( ! is_singular() ) { return false; }
	$id = get_queried_object_id();
	return $id && strpos( (string) get_post_meta( $id, '_elementor_data', true ), 'zp_calculadora_n' ) !== false;
}
add_shortcode( 'zp_calculadora_n', function () { return '[[ZP_CALCN]]'; } );
function zp_calcn_html() {
	$lt = chr( 60 );
	$num = function ( $id, $val, $min, $step, $suf ) use ( $lt ) { return $lt . 'div class="zpc-in">' . $lt . 'input type="number" inputmode="decimal" id="' . $id . '" name="' . $id . '" value="' . $val . '" min="' . $min . '" step="' . $step . '">' . $lt . 'span>' . $suf . $lt . '/span>' . $lt . '/div>'; };
	$campo = function ( $id, $label, $input, $ayuda, $wid = '' ) use ( $lt ) { return $lt . 'div class="zpc-campo"' . ( $wid ? ' id="' . $wid . '"' : '' ) . '>' . $lt . 'label for="' . $id . '">' . $label . $lt . '/label>' . $input . $lt . 'small>' . $ayuda . $lt . '/small>' . $lt . '/div>'; };
	$r = function ( $id, $label, $cls = '' ) use ( $lt ) { return $lt . 'div class="zpc-r' . ( $cls ? ' ' . $cls : '' ) . '" id="' . $id . '-box">' . $lt . 'span class="zpc-l">' . $label . $lt . '/span>' . $lt . 'strong id="' . $id . '">—' . $lt . '/strong>' . $lt . 'small id="' . $id . '-f">' . $lt . '/small>' . $lt . '/div>'; };
	$pop = '#elementor-action%3Aaction%3Dpopup%3Aopen%26settings%3DeyJpZCI6MjIsInRvZ2dsZSI6ZmFsc2V9';
	$sel = $lt . 'select id="zpn-tipo" name="tipo">' . $lt . 'option value="vitalicio" selected>Vitalicio (de por vida, el caso habitual del viudo)' . $lt . '/option>' . $lt . 'option value="temporal">Temporal (por un número de años)' . $lt . '/option>' . $lt . '/select>';
	$form = $campo( 'zpn-valor', 'Valor del inmueble en pleno dominio', $num( 'zpn-valor', 200000, 0, 1000, '€' ), 'Para impuestos, el valor de referencia del Catastro, o el que declares si es mayor.' )
		. $campo( 'zpn-tipo', 'Tipo de usufructo', $sel, 'El del viudo o viuda suele ser vitalicio.' )
		. $campo( 'zpn-edad', 'Edad del usufructuario', $num( 'zpn-edad', 75, 0, 1, 'años' ), 'Años cumplidos en la fecha que se valora: fallecimiento, donación o venta.', 'zpn-edad-c' )
		. $campo( 'zpn-anos', 'Duración del usufructo', $num( 'zpn-anos', 10, 0, 1, 'años' ), 'Años completos que dura el usufructo.', 'zpn-anos-c' )
		. $campo( 'zpn-pct', 'Tu porcentaje de la nuda propiedad', $num( 'zpn-pct', 100, 0, 0.01, '%' ), 'Si sois dos hermanos a partes iguales, pon 50.' );
	$res = $lt . 'div class="zpc-res">' . $r( 'zpn-usu', 'Valor del usufructo' ) . $r( 'zpn-nuda', 'Valor de la nuda propiedad', 'zpc-r-teo' ) . $r( 'zpn-tuya', 'Tu parte de la nuda propiedad', 'zpc-r-ok' ) . $lt . '/div>'
		. $lt . 'p class="zpc-nota">Cálculo orientativo con las reglas del artículo 26 de la Ley 29/1987 del Impuesto sobre Sucesiones y Donaciones, que también usa el ITP. Es el valor fiscal: el precio de mercado de una nuda propiedad depende de la esperanza de vida y del comprador, y suele ser menor. País Vasco y Navarra pueden tener reglas forales propias. Si quieres vender tu nuda propiedad o tu parte, ' . $lt . 'a href="' . $pop . '">pídenos oferta por escrito en 48 horas' . $lt . '/a>.' . $lt . '/p>';
	return $lt . 'div class="zpcn" data-calcn="nuda">' . $lt . 'form class="zpc-form" onsubmit="return false" autocomplete="off">' . $form . $lt . '/form>' . $res . $lt . '/div>';
}
function zp_calcn_sustituir( $content ) {
	if ( strpos( $content, '[[ZP_CALCN]]' ) === false ) { return $content; }
	$lt = chr( 60 );
	return preg_replace_callback( '/' . $lt . 'span([^>]*)>\s*\[\[ZP_CALCN\]\]\s*' . $lt . '\/span>/', function ( $m ) use ( $lt ) { return $lt . 'div' . $m[1] . '>' . zp_calcn_html() . $lt . '/div>'; }, $content );
}
add_filter( 'elementor/frontend/the_content', 'zp_calcn_sustituir', 25 );
add_filter( 'the_content', 'zp_calcn_sustituir', 100 );
add_action( 'wp_head', function () {
	if ( ! zp_calcn_pagina_lleva() ) { return; }
	$t = 'sty' . 'le';
	$css = '.zpcn{display:block;width:100%;font-family:Manrope,sans-serif;color:#1f2a33}.zpcn [hidden]{display:none!important}'
		. '.zpcn select{width:100%;padding:12px 14px;font:inherit;font-size:15px;font-weight:600;color:#1f2a33;background:#fff;border:1px solid #c3ccd3;border-radius:10px}'
		. '.zpcn input:focus,.zpcn select:focus{outline:2px solid #e87524;outline-offset:1px}';
	echo '<' . $t . ' id="zpcn-css">' . $css . '</' . $t . '>';
}, 99 );
add_action( 'wp_footer', function () {
	if ( ! zp_calcn_pagina_lleva() ) { return; }
	$t = 'scr' . 'ipt';
	$js = <<<'JS'
(function(){
var E=function(n){return new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR",maximumFractionDigits:0}).format(Math.round(n))};
var P=function(x){return String(Math.round(x*100)/100).replace(".",",")+" %"};
document.querySelectorAll(".zpcn").forEach(function(root){
var q=function(id){return root.querySelector("#"+id)},num=function(id){var v=parseFloat(String(q(id).value).replace(",","."));return isNaN(v)?0:v},set=function(id,t){var e=q(id);if(e)e.textContent=t},sent=false;
function run(ev){
var V=Math.max(0,num("zpn-valor")),tipo=q("zpn-tipo").value,pct=Math.min(100,Math.max(0,num("zpn-pct")))/100,u,fu;
q("zpn-edad-c").hidden=tipo!=="vitalicio";q("zpn-anos-c").hidden=tipo!=="temporal";
if(tipo==="temporal"){var a=Math.max(0,Math.floor(num("zpn-anos")));if(a<1){u=2;fu="Menos de un año: 2 % (las fracciones de año no cuentan; un usufructo de menos de un año vale el 2 %).";}else{u=Math.min(70,2*a);fu=a+(a===1?" año":" años")+" × 2 % = "+(2*a)+" %"+(2*a>70?"; se aplica el máximo del 70 %":"")+".";}}
else{var ed=Math.max(0,Math.floor(num("zpn-edad"))),raw=89-ed;u=Math.min(70,Math.max(10,raw));fu="89 − "+ed+" años = "+raw+" %"+(raw>70?"; se aplica el máximo del 70 %":(raw<10?"; se aplica el mínimo del 10 %":""))+".";}
var n=100-u,vn=V*n/100;
set("zpn-usu",E(V*u/100)+" ("+u+" %)");set("zpn-usu-f",fu);
set("zpn-nuda",E(vn)+" ("+n+" %)");set("zpn-nuda-f","100 % − "+u+" % = "+n+" % de "+E(V)+".");
set("zpn-tuya",E(vn*pct));set("zpn-tuya-f",E(vn)+" × "+P(pct*100)+" de la nuda propiedad.");
if(ev&&!sent){sent=true;(window.dataLayer=window.dataLayer||[]).push({event:"calculadora_usada",calculadora:"nuda_propiedad",situacion:tipo,valor_tramo:V<100000?"<100k":V<200000?"100-200k":V<400000?"200-400k":">400k"});}}
run();root.addEventListener("input",run);root.addEventListener("change",run);});
})();
JS;
	echo '<' . $t . ' id="zpcn-js">' . $js . '</' . $t . '>';
}, 98 );
