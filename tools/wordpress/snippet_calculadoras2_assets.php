<?php
/* Zona Proindiviso — calculadoras 2 (snippet 225): CSS (wp_head) y JS (wp_footer), solo en páginas que llevan [zp_calculadora_x].
 * Va aparte de snippet_calculadoras2.php porque el WAF de Hostinger rechaza cuerpos REST de más de ~15 KB.
 * Datos 2026 (verificados el 30/10/2026, ver tools/blog/fiscal_comun.json): escala del ahorro 19/21/23/27/30 % y coeficientes máximos
 * de plusvalía de 2024 (RDL 8/2023), vigentes porque el RDL 16/2025 y el RDL 26/2026 no se convalidaron. Revisar cada enero. */
add_action( 'wp_head', function () {
	if ( ! function_exists( 'zp_calcx_pagina_lleva' ) || ! zp_calcx_pagina_lleva() ) { return; }
	$t = 'sty' . 'le';
	$css = <<<'CSS'
.zpcx{display:block;width:100%;font-family:Manrope,sans-serif;color:#1f2a33}.zpcx [hidden]{display:none!important}
.zpcx select{width:100%;padding:12px 14px;font:inherit;font-size:15px;font-weight:600;color:#1f2a33;background:#fff;border:1px solid #c3ccd3;border-radius:10px}
.zpcx input:focus,.zpcx select:focus,.zpcx button:focus{outline:2px solid #e87524;outline-offset:1px}
.zpcx-cop{margin-top:22px;padding:22px;background:#fff;border:1px solid #d8e0e6;border-radius:18px}
.zpcx-filas{display:flex;flex-direction:column;gap:12px;margin:12px 0}
.zpcx-fila{display:grid;grid-template-columns:2fr 1fr 1.3fr auto;gap:10px;align-items:end}
.zf-c{display:flex;flex-direction:column;gap:4px;font-size:12.5px;font-weight:700;color:#0d4f78}
.zf-c input{padding:10px 12px;font:inherit;font-size:15px;font-weight:700;color:#1f2a33;border:1px solid #c3ccd3;border-radius:10px;background:#fff;min-width:0;width:100%;box-sizing:border-box}
.zf-x{width:42px;height:44px;border:1px solid #c3ccd3;border-radius:10px;background:#fff;font-size:20px;color:#4f5b66;cursor:pointer}
.zpcx-add{margin-top:4px;padding:10px 16px;border:1px dashed #0d4f78;border-radius:999px;background:#eff5f8;color:#0d4f78;font:inherit;font-weight:800;font-size:14px;cursor:pointer}
.zpcx-aviso{margin:10px 0 0;font-size:13.5px;font-weight:700;color:#b3261e}
.zpcx-tabla{display:flex;flex-direction:column;background:#fff;border:1px solid #d8e0e6;border-radius:14px;overflow:hidden}
.zf-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:10px;padding:12px 18px;border-top:1px solid #eef2f5;font-size:15px}
.zf-row span:not(:first-child){text-align:right;font-weight:700}
.zf-head{background:#eff5f8;border-top:0;font-size:12px;font-weight:800;color:#0d4f78;text-transform:uppercase;letter-spacing:.03em}
.zf-pos{color:#3f8a1a}.zf-neg{color:#b3261e}
@media(max-width:767px){.zpcx-cop{padding:16px}.zpcx-fila{grid-template-columns:1fr 1fr}.zf-n-w{grid-column:1/-1}.zf-x{grid-column:2;justify-self:end}.zf-row{grid-template-columns:1.3fr 1fr 1fr 1fr;gap:6px;padding:10px 12px;font-size:13px}.zf-head{font-size:10.5px}}
CSS;
	echo '<' . $t . ' id="zpcx-css">' . $css . '</' . $t . '>';
}, 99 );
add_action( 'wp_footer', function () {
	if ( ! function_exists( 'zp_calcx_pagina_lleva' ) || ! zp_calcx_pagina_lleva() ) { return; }
	$t = 'scr' . 'ipt';
	$js = <<<'JS'
(function(){
var E=function(n){return new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR",maximumFractionDigits:0}).format(Math.round(n))};
var N=function(root,id){var el=root.querySelector("#"+id);if(!el)return 0;var v=parseFloat(String(el.value).replace(",","."));return isNaN(v)?0:v};
var S=function(root,id,t){var e=root.querySelector("#"+id);if(e)e.textContent=t};
var PC=function(x){return String(Math.round(x*10000)/100).replace(".",",")+" %"};
var tramo=function(v){return v<100000?"<100k":v<200000?"100-200k":v<400000?"200-400k":">400k"};
var COEF=[0.15,0.15,0.14,0.14,0.16,0.18,0.19,0.20,0.19,0.15,0.12,0.10,0.09,0.09,0.09,0.09,0.10,0.13,0.17,0.23,0.40];
var TR=[[6000,0.19],[50000,0.21],[200000,0.23],[300000,0.27],[Infinity,0.30]];
function escala(g){var t=0,prev=0,det=[];for(var i=0;i<TR.length;i++){if(g<=prev)break;var b=Math.min(g,TR[i][0])-prev;t+=b*TR[i][1];det.push(E(b)+" al "+Math.round(TR[i][1]*100)+" %");prev=TR[i][0];}return{t:t,det:det}}
function impuestos(root){
var V=N(root,"zpx-venta"),A=N(root,"zpx-adq"),Y=N(root,"zpx-anio"),G=N(root,"zpx-gastos"),SU=N(root,"zpx-suelo"),VT=Math.max(N(root,"zpx-vct"),1),P=Math.min(100,Math.max(0,N(root,"zpx-pct")))/100,T=Math.min(30,Math.max(0,N(root,"zpx-tipo")))/100;
var res=root.querySelector("#zpx-res").value,ex=(root.querySelector("input[name=exento]:checked")||{}).value==="si";
var n=Math.max(0,Math.floor(new Date().getFullYear()-Y)),c=COEF[Math.min(n,20)],plus=0,ft="";
if(V<=A){ft="No hay plusvalía: vendes por "+E(V)+", igual o menos de lo que te costó ("+E(A)+"). Sin incremento de valor no hay impuesto; guarda las escrituras para acreditarlo.";}
else{var obj=SU*P*c*T,real=(V-A)*Math.min(SU/VT,1)*T;plus=Math.min(obj,real);
ft="Método objetivo: "+E(SU)+" × "+Math.round(P*100)+" % × coeficiente "+String(c).replace(".",",")+" ("+n+(n===1?" año":" años")+") × "+PC(T)+" = "+E(obj)+". Método real: ganancia "+E(V-A)+" × "+PC(Math.min(SU/VT,1))+" de suelo × "+PC(T)+" = "+E(real)+". Se aplica el menor.";}
S(root,"zpx-plus",E(plus));S(root,"zpx-plus-f",ft);
var gan=V-G-plus-A,irpf=0,it="";
if(gan<=0){it="No hay ganancia ("+E(gan)+"): no pagas IRPF y, si hay pérdida, puedes compensarla con otras ganancias del ahorro.";}
else if(ex&&res==="es"){it="Ganancia de "+E(gan)+" exenta: vendes tu vivienda habitual con 65 años o más. Se declara igualmente en la renta.";}
else if(res==="no"){irpf=gan*0.19;it="Ganancia "+E(gan)+" × 19 % (no residentes, modelo 210). El comprador retiene el 3 % del precio ("+E(V*0.03)+") a cuenta de este impuesto.";}
else{var e=escala(gan);irpf=e.t;it=E(V)+" − "+E(G)+" de gastos − "+E(plus)+" de plusvalía − "+E(A)+" de adquisición = "+E(gan)+" de ganancia. Escala del ahorro 2026: "+e.det.join(" + ")+".";}
S(root,"zpx-irpf",E(irpf));S(root,"zpx-irpf-f",it);
S(root,"zpx-tot",E(plus+irpf));S(root,"zpx-tot-f","Plusvalía "+E(plus)+" + IRPF "+E(irpf)+". El ITP de la compra lo paga el comprador, no tú.");
S(root,"zpx-neto",E(V-G-plus-irpf));S(root,"zpx-neto-f",E(V)+" − "+E(G)+" de gastos − "+E(plus+irpf)+" de impuestos.");
return{calculadora:"impuestos",situacion:res==="no"?"no_residente":(ex?"exento_65":"residente"),valor_tramo:tramo(P>0?V/P:V)};}
function uso(root){
var R=N(root,"zpx-renta"),P=Math.min(100,Math.max(0,N(root,"zpx-pct")))/100,M=Math.max(0,Math.round(N(root,"zpx-meses"))),GM=N(root,"zpx-gm");
var m=Math.min(M,60),mes=R*P,ac=mes*m,de=GM*m,ne=Math.max(0,ac-de);
S(root,"zpx-mes",E(mes));S(root,"zpx-mes-f",E(R)+" de renta de mercado × "+Math.round(P*100)+" % de tu parte.");
S(root,"zpx-acum",E(ac));S(root,"zpx-acum-f",E(mes)+" × "+m+" meses"+(M>60?" (tope de 60 meses: lo anterior suele estar prescrito)":"")+".");
S(root,"zpx-desc",E(de));S(root,"zpx-desc-f",E(GM)+" al mes que pagó por tu parte × "+m+" meses.");
S(root,"zpx-neto",E(ne));S(root,"zpx-neto-f","Orientativo. Antes de reclamar, manda un burofax: fija la fecha desde la que cuenta y abre la puerta a un acuerdo.");
return{calculadora:"uso",situacion:"ocupa"};}
function mk(tag,txt,cls){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e}
function fila(n,p,g){var d=mk("div",undefined,"zpcx-fila");
var c=function(cls,type,val,label){var w=mk("label",undefined,"zf-c "+cls+"-w");w.appendChild(mk("span",label));var i=document.createElement("input");i.type=type;i.className=cls;i.value=val;if(type==="number"){i.min="0";i.step="any";i.inputMode="decimal";}w.appendChild(i);return w};
d.appendChild(c("zf-n","text",n,"Nombre"));d.appendChild(c("zf-p","number",p,"Porcentaje (%)"));d.appendChild(c("zf-g","number",g,"Pagado este año (€)"));
var x=mk("button","×","zf-x");x.type="button";x.setAttribute("aria-label","Quitar copropietario");d.appendChild(x);return d}
function gastos(root){
var tot=N(root,"zpx-ibi")+N(root,"zpx-com")*12+N(root,"zpx-seg")+N(root,"zpx-bas")+N(root,"zpx-obr")+N(root,"zpx-otr");
S(root,"zpx-total",E(tot));S(root,"zpx-total-f","IBI + comunidad × 12 + seguro + basuras + derramas u obras + otros.");
var filas=[].slice.call(root.querySelectorAll(".zpcx-fila")).map(function(f){var v=function(s){var x=parseFloat(String(f.querySelector(s).value).replace(",","."));return isNaN(x)?0:x};return{n:f.querySelector(".zf-n").value||"Copropietario",p:v(".zf-p"),g:v(".zf-g")}});
var sp=filas.reduce(function(a,f){return a+f.p},0),sg=filas.reduce(function(a,f){return a+f.g},0),av=root.querySelector("#zpx-aviso"),msg=[];if(Math.abs(sp-100)>=0.01)msg.push("Los porcentajes suman "+String(Math.round(sp*100)/100).replace(".",",")+" %; deberían sumar 100 %.");if(sg>0&&Math.abs(sg-tot)>=1)msg.push("Lo pagado entre todos ("+E(sg)+") no coincide con los gastos del año ("+E(tot)+"): el reparto sale sobre los gastos; revisa los importes.");if(av){av.hidden=!msg.length;av.textContent=msg.join(" ");}
var tb=root.querySelector("#zpx-tabla");while(tb.firstChild)tb.removeChild(tb.firstChild);
var h=mk("div",undefined,"zf-row zf-head");["Copropietario","Le corresponde","Ha pagado","Saldo"].forEach(function(t){h.appendChild(mk("span",t))});tb.appendChild(h);
var sal=[];filas.forEach(function(f){var co=tot*f.p/100,sa=f.g-co;sal.push({n:f.n,s:sa});var r=mk("div",undefined,"zf-row");r.appendChild(mk("span",f.n+" ("+String(f.p).replace(".",",")+" %)"));r.appendChild(mk("span",E(co)));r.appendChild(mk("span",E(f.g)));r.appendChild(mk("span",(sa>=0?"+":"−")+E(Math.abs(sa)),sa>=0?"zf-pos":"zf-neg"));tb.appendChild(r)});
var de=sal.filter(function(x){return x.s<-0.5}).map(function(x){return{n:x.n,s:-x.s}}),ac=sal.filter(function(x){return x.s>0.5}).map(function(x){return{n:x.n,s:x.s}}),pg=[],i=0,j=0;
while(i<de.length&&j<ac.length){var q=Math.min(de[i].s,ac[j].s);pg.push(de[i].n+" paga "+E(q)+" a "+ac[j].n);de[i].s-=q;ac[j].s-=q;if(de[i].s<0.5)i++;if(ac[j].s<0.5)j++;}
S(root,"zpx-quien",pg.length?(pg.length===1?"1 pago":pg.length+" pagos"):"Nadie debe nada");S(root,"zpx-quien-f",pg.length?pg.join(" · ")+".":"Cada uno ha pagado lo que le corresponde.");
return{calculadora:"gastos",situacion:filas.length+"_copropietarios"};}
document.querySelectorAll(".zpcx").forEach(function(root){var tipo=root.getAttribute("data-calcx"),fn=tipo==="uso"?uso:(tipo==="gastos"?gastos:impuestos),sent=false;
var run=function(ev){var d=fn(root);if(ev&&!sent){sent=true;(window.dataLayer=window.dataLayer||[]).push(Object.assign({event:"calculadora_usada"},d));}};
if(tipo==="gastos"){var cont=root.querySelector("#zpx-filas"),add=function(n,p,g){if(cont.children.length<6)cont.appendChild(fila(n,p,g))};add("Copropietario 1",50,1440);add("Copropietario 2",50,0);
root.querySelector("#zpx-add").addEventListener("click",function(){add("Copropietario "+(cont.children.length+1),0,0);run({});});
cont.addEventListener("click",function(e){var b=e.target.closest(".zf-x");if(b&&cont.children.length>2){cont.removeChild(b.closest(".zpcx-fila"));run({});}});}
run();root.addEventListener("input",run);root.addEventListener("change",run);});
})();
JS;
	echo '<' . $t . ' id="zpcx-js">' . $js . '</' . $t . '>';
}, 98 );
