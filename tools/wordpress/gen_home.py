import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from design import *
c=Comp(23)
# ---------- HERO oscuro ----------
c.add('<e-div-block configuration-id="Hero"><e-flexbox configuration-id="Hero inner"><e-flexbox configuration-id="Hero texto"><e-paragraph configuration-id="Hero overline"></e-paragraph><e-heading configuration-id="Hero titulo"></e-heading><e-paragraph configuration-id="Hero sub"></e-paragraph><e-flexbox configuration-id="Hero botones"><e-button configuration-id="Hero wa"></e-button><e-button configuration-id="Hero tel"></e-button></e-flexbox><e-flexbox configuration-id="Hero checks">'+''.join(f'<e-flexbox configuration-id="Hero check {i}"><e-paragraph configuration-id="Hero check {i} icono"></e-paragraph><e-paragraph configuration-id="Hero check {i} texto"></e-paragraph></e-flexbox>' for i in range(1,4))+'</e-flexbox></e-flexbox><e-flexbox configuration-id="Hero tarjeta"><e-div-block configuration-id="Hero tarjeta franja"></e-div-block><e-heading configuration-id="Hero tarjeta titulo"></e-heading><e-paragraph configuration-id="Hero tarjeta texto"></e-paragraph><e-component configuration-id="Hero formulario"/></e-flexbox></e-flexbox></e-div-block>')
c.cfg("Hero",{"tag":"section"})
c.st("Hero",f"display:flex; flex-direction:column; align-items:center; width:100%; padding: 88px 24px 120px 24px; background-color: var(--brand-primary-dark); background-image: linear-gradient(100deg, rgba(9,58,90,1) 0%, rgba(9,58,90,0.96) 48%, rgba(13,79,120,0.78) 100%), url('{HERO}'); background-size: cover; background-position: right center; @media(--tablet){{ padding: 64px 24px 110px 24px; }} @media(--mobile){{ padding: 44px 18px 96px 18px; background-image: linear-gradient(180deg, rgba(9,58,90,0.97) 0%, rgba(9,58,90,0.97) 100%), url('{HERO}'); }}")
c.st("Hero inner","display:flex; flex-direction:row; align-items:center; gap: 64px; width:100%; max-width: 1200px; padding:0px; @media(--tablet){ gap: 36px; } @media(--mobile){ flex-direction:column; gap: 36px; }")
c.st("Hero texto","display:flex; flex-direction:column; gap: 22px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding:0px;")
overline(c,"Hero overline","Vender proindiviso en toda España",light=True)
c.h("Hero titulo","Vende tu parte de un piso sin esperar al acuerdo de los demás","h1","font-size: clamp(2.3rem, 1.4rem + 3.4vw, 3.6rem); color: var(--white); max-width: 640px; line-height: 1.06;")
c.p("Hero sub","Compramos tu proindiviso directamente, con pago al contado en notaría. Te damos un precio por escrito en 48 horas. Sin agencias, sin gastos y sin compromiso.","font-size: 19px; line-height: 1.6; color: rgba(255,255,255,0.82); max-width: 560px; @media(--mobile){ font-size: 17px; }")
c.st("Hero botones","display:flex; flex-direction:row; flex-wrap:wrap; gap: 12px; width:100%; padding:0px;")
c.btn("Hero wa","Escribir por WhatsApp",WA,"wa","lg"); c.btn("Hero tel","Llamar ahora",TEL,"outline-white","lg")
c.st("Hero checks","display:flex; flex-direction:row; flex-wrap:wrap; gap: 8px 26px; width:100%; padding: 6px 0px 0px 0px;")
for i,t in enumerate(["Oferta en 48 h","Pago al contado en notaría","Gastos a nuestro cargo"],1):
    c.st(f"Hero check {i}","display:flex; flex-direction:row; align-items:center; gap: 6px; width:auto; padding:0px;")
    c.p(f"Hero check {i} icono","✓","font-size: 15px; font-weight: 800; color: var(--brand-accent);",tag="span")
    c.p(f"Hero check {i} texto",t,"font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.9);")
c.st("Hero tarjeta","display:flex; flex-direction:column; gap: 8px; flex-grow:0; flex-shrink:0; flex-basis: 440px; width: 440px; max-width:100%; padding: 0px 30px 30px 30px; background-color: var(--white); border-radius: 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.35); overflow:hidden; @media(--tablet){ flex-basis: 380px; width: 380px; } @media(--mobile){ flex-basis:auto; width:100%; padding: 0px 22px 24px 22px; }")
c.st("Hero tarjeta franja","width: calc(100% + 60px); height: 8px; margin: 0px 0px 22px -30px; padding:0px; background-color: var(--brand-accent); @media(--mobile){ width: calc(100% + 44px); margin-left: -22px; }")
c.h("Hero tarjeta titulo","Te llamamos nosotros","h3","font-size: 24px; color: var(--brand-primary);")
c.p("Hero tarjeta texto","Tu nombre y tu teléfono. Te llamamos en menos de 24 horas laborables con una oferta.","font-size: 14px; color: var(--ink-muted); margin-bottom: 8px;")
c.cfg("Hero formulario",{"component_id":83})
# ---------- DATOS flotantes ----------
c.add('<e-div-block configuration-id="Datos"><e-flexbox configuration-id="Datos fila"><e-flexbox configuration-id="Dato 1"><e-paragraph configuration-id="Dato 1 n"></e-paragraph><e-paragraph configuration-id="Dato 1 t"></e-paragraph></e-flexbox><e-flexbox configuration-id="Dato 2"><e-paragraph configuration-id="Dato 2 n"></e-paragraph><e-paragraph configuration-id="Dato 2 t"></e-paragraph></e-flexbox><e-flexbox configuration-id="Dato 3"><e-paragraph configuration-id="Dato 3 n"></e-paragraph><e-paragraph configuration-id="Dato 3 t"></e-paragraph></e-flexbox><e-flexbox configuration-id="Dato 4"><e-paragraph configuration-id="Dato 4 n"></e-paragraph><e-paragraph configuration-id="Dato 4 t"></e-paragraph></e-flexbox></e-flexbox></e-div-block>')
c.cfg("Datos",{"tag":"section"}); c.st("Datos","display:flex; flex-direction:column; align-items:center; width:100%; padding: 0px 24px; background-color: var(--white); @media(--mobile){ padding: 0px 18px; }")
c.st("Datos fila","display:flex; flex-direction:row; gap: 0px; width:100%; max-width: 1200px; margin-top: -56px; padding:0px; background-color: var(--white); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 20px 50px rgba(13,79,120,0.12); overflow:hidden; @media(--mobile){ flex-wrap:wrap; margin-top: -48px; }")
for i,(n,t) in enumerate([("48 h","para tener tu precio por escrito"),("0 €","de gastos: notaría a nuestro cargo"),("50","provincias donde compramos"),("Al contado","cobras el día de la firma")],1):
    c.st(f"Dato {i}","display:flex; flex-direction:column; gap: 4px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; padding: 26px 28px; border-right: 1px solid var(--line); @media(--mobile){ flex-basis: 50%; padding: 18px 16px; border-bottom: 1px solid var(--line); }")
    c.p(f"Dato {i} n",n,"font-family: var(--font-heading); font-size: 30px; font-weight: 800; letter-spacing: -0.02em; color: var(--brand-primary); line-height: 1;")
    c.p(f"Dato {i} t",t,"font-size: 14px; color: var(--ink-muted);")
c.st("Dato 4",c.S["Dato 4"].replace("border-right: 1px solid var(--line);","border-right: 0px;"))
# ---------- CÓMO FUNCIONA ----------
c.add('<e-div-block configuration-id="Como"><e-flexbox configuration-id="Como inner"><e-flexbox configuration-id="Como cabecera"><e-paragraph configuration-id="Como overline"></e-paragraph><e-heading configuration-id="Como titulo"></e-heading><e-paragraph configuration-id="Como sub"></e-paragraph></e-flexbox><e-flexbox configuration-id="Como pasos"><e-flexbox configuration-id="Paso 1"><e-paragraph configuration-id="Paso 1 n"></e-paragraph><e-heading configuration-id="Paso 1 t"></e-heading><e-paragraph configuration-id="Paso 1 p"></e-paragraph></e-flexbox><e-flexbox configuration-id="Paso 2"><e-paragraph configuration-id="Paso 2 n"></e-paragraph><e-heading configuration-id="Paso 2 t"></e-heading><e-paragraph configuration-id="Paso 2 p"></e-paragraph></e-flexbox><e-flexbox configuration-id="Paso 3"><e-paragraph configuration-id="Paso 3 n"></e-paragraph><e-heading configuration-id="Paso 3 t"></e-heading><e-paragraph configuration-id="Paso 3 p"></e-paragraph></e-flexbox></e-flexbox><e-button configuration-id="Como cta"></e-button></e-flexbox></e-div-block>')
c.cfg("Como",{"tag":"section"}); section(c,"Como","var(--white)"); inner(c,"Como inner",gap="40px",extra="align-items:center;")
c.st("Como cabecera","display:flex; flex-direction:column; align-items:center; gap: 12px; width:100%; max-width: 720px; padding:0px; text-align:center;")
overline(c,"Como overline","Así de simple",center=True)
c.h("Como titulo","Cómo vender tu proindiviso en tres pasos","h2","text-align:center;")
c.p("Como sub","Sin agencias, sin esperar a los demás propietarios y sin juicios.","font-size: 18px; color: var(--ink-muted); text-align:center;")
c.st("Como pasos","display:flex; flex-direction:row; gap: 24px; width:100%; padding:0px; @media(--mobile){ flex-direction:column; }")
for i,(t,d) in enumerate([("Cuéntanos tu caso","Dos minutos por teléfono o WhatsApp: qué inmueble es, qué parte tienes y si hay herencia, hipoteca o desacuerdo."),("Recibes tu oferta en 48 h","Valoramos tu parte por el inmueble, la zona, las cargas y la situación. Precio por escrito, sin compromiso."),("Firmamos en notaría y cobras","Preparamos la documentación, fijamos fecha y cobras el mismo día de la firma. Los gastos corren por nuestra cuenta.")],1):
    c.st(f"Paso {i}","display:flex; flex-direction:column; gap: 12px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; padding: 32px 28px; background-color: var(--surface-soft); border-radius: 18px; border-top: 4px solid var(--brand-accent);")
    c.p(f"Paso {i} n",f"0{i}","font-family: var(--font-heading); font-size: 15px; font-weight: 800; letter-spacing: 0.1em; color: var(--brand-accent-dark);")
    c.h(f"Paso {i} t",t,"h3","font-size: 21px;")
    c.p(f"Paso {i} p",d,"font-size: 16px; line-height: 1.65; color: var(--ink-muted);")
c.btn("Como cta","Pedir mi oferta ahora",POPUP,"accent","lg")
# ---------- CASOS ----------
casos=[("Has heredado una parte y los demás no venden","Un piso de los padres, tres hermanos y uno que bloquea. Tu parte se puede vender igual, sin su permiso.","/vender-parte-casa-heredada/"),
("Tras el divorcio la casa sigue a nombre de los dos","Si no hay acuerdo para vender o para que uno se quede, vender tu mitad corta el problema sin juicio.","/vender-proindiviso-divorcio/"),
("Quieres vender sin avisar al otro propietario","La ley te lo permite, con un derecho de retracto para el resto. Te contamos cómo hacerlo bien.","/vender-proindiviso-sin-avisar/"),
("La parte tiene hipoteca","La compramos igual. La deuda se liquida en la firma y tú te vas sin cargas.","/vender-proindiviso-con-hipoteca/"),
("Hay un inquilino o un okupa dentro","Es lo que más asusta a un particular y lo que menos nos frena. Cuéntanos el caso y te decimos un precio.","/contacto/"),
("Solo quieres saber cuánto te darían","Entre el 40 % y el 70 % del valor de tu parte. Te explicamos de qué depende y te lo decimos por escrito.","/cuanto-pagan-por-un-proindiviso/")]
cards=''.join(f'<e-flexbox configuration-id="Caso {i}"><e-heading configuration-id="Caso {i} t"></e-heading><e-paragraph configuration-id="Caso {i} p"></e-paragraph><e-button configuration-id="Caso {i} b"></e-button></e-flexbox>' for i in range(1,7))
c.add(f'<e-div-block configuration-id="Casos"><e-flexbox configuration-id="Casos inner"><e-flexbox configuration-id="Casos cabecera"><e-paragraph configuration-id="Casos overline"></e-paragraph><e-heading configuration-id="Casos titulo"></e-heading></e-flexbox><e-flexbox configuration-id="Casos grid">{cards}</e-flexbox></e-flexbox></e-div-block>')
c.cfg("Casos",{"tag":"section"}); section(c,"Casos","var(--surface-soft)"); inner(c,"Casos inner",gap="36px")
c.st("Casos cabecera","display:flex; flex-direction:column; gap: 12px; width:100%; max-width: 760px; padding:0px;")
overline(c,"Casos overline","¿Es tu caso?")
c.h("Casos titulo","Lo hemos comprado cientos de veces","h2")
c.st("Casos grid","display:flex; flex-direction:row; flex-wrap:wrap; gap: 20px; width:100%; padding:0px;")
for i,(t,d,u) in enumerate(casos,1):
    c.st(f"Caso {i}","display:flex; flex-direction:column; justify-content:space-between; gap: 10px; flex-grow:1; flex-shrink:1; flex-basis: 300px; width:auto; padding: 28px; background-color: var(--white); border: 1px solid var(--line); border-radius: 18px; transition: all 0.2s ease; &:hover { border-color: var(--brand-primary); transform: translateY(-3px); box-shadow: 0 18px 40px rgba(13,79,120,0.12); }")
    c.h(f"Caso {i} t",t,"h3","font-size: 19px; line-height: 1.3;")
    c.p(f"Caso {i} p",d,"font-size: 15px; line-height: 1.6; color: var(--ink-muted);")
    c.btn(f"Caso {i} b","Ver cómo se hace →",u,"link","sm","align-self:flex-start; margin-top: 8px; font-size: 15px;")
# ---------- POR QUÉ + PRECIO ----------
c.add('<e-div-block configuration-id="Porque"><e-flexbox configuration-id="Porque inner"><e-flexbox configuration-id="Porque texto"><e-paragraph configuration-id="Porque overline"></e-paragraph><e-heading configuration-id="Porque titulo"></e-heading><e-paragraph configuration-id="Porque p1"></e-paragraph><e-flexbox configuration-id="Porque lista"><e-paragraph configuration-id="Porque li 1"></e-paragraph><e-paragraph configuration-id="Porque li 2"></e-paragraph><e-paragraph configuration-id="Porque li 3"></e-paragraph><e-paragraph configuration-id="Porque li 4"></e-paragraph></e-flexbox><e-button configuration-id="Porque boton"></e-button></e-flexbox><e-flexbox configuration-id="Precio"><e-paragraph configuration-id="Precio overline"></e-paragraph><e-heading configuration-id="Precio n"></e-heading><e-paragraph configuration-id="Precio p"></e-paragraph><e-button configuration-id="Precio boton"></e-button></e-flexbox></e-flexbox></e-div-block>')
c.cfg("Porque",{"tag":"section"}); section(c,"Porque","var(--white)")
c.st("Porque inner","display:flex; flex-direction:row; align-items:stretch; gap: 56px; width:100%; max-width: 1200px; padding:0px; @media(--mobile){ flex-direction:column; gap: 32px; }")
c.st("Porque texto","display:flex; flex-direction:column; gap: 20px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding:0px;")
overline(c,"Porque overline","Por qué vendernos a nosotros")
c.h("Porque titulo","Compramos nosotros. Sin intermediarios, sin comisiones, sin esperas.","h2")
c.p("Porque p1","No somos una agencia ni vendemos tu contacto a nadie: compramos tu parte con fondos propios y firmamos en notaría. Por eso podemos darte un precio cerrado en 48 horas y una fecha de firma.","font-size: 17px; line-height: 1.7; color: var(--ink-muted);")
c.st("Porque lista","display:flex; flex-direction:column; gap: 12px; width:100%; padding:0px;")
for i,(b,t) in enumerate([("Sin gastos para ti.","Notaría, gestión y documentación corren por nuestra cuenta."),("Sin exclusividad ni permanencia.","Si encuentras mejor oferta, la aceptas y punto."),("Hasta la notaría.","Nos ocupamos de la escritura, la herencia pendiente o la hipoteca."),("Cualquier caso.","Herencias, divorcios, hipotecas, inquilinos, fincas rústicas.")],1):
    c.p(f"Porque li {i}",f"<strong>{b}</strong> {t}","font-size: 16px; line-height: 1.6; color: var(--ink); padding-left: 18px; border-left: 3px solid var(--brand-accent);")
c.btn("Porque boton","Pedir mi oferta",POPUP,"primary","md","align-self:flex-start; margin-top: 6px;")
c.st("Precio","display:flex; flex-direction:column; justify-content:center; gap: 12px; flex-grow:0; flex-shrink:0; flex-basis: 400px; width: 400px; max-width:100%; padding: 40px; background-color: var(--brand-primary); border-radius: 20px; @media(--tablet){ flex-basis: 340px; width: 340px; } @media(--mobile){ flex-basis:auto; width:100%; padding: 28px; }")
overline(c,"Precio overline","¿Cuánto pagamos?",light=True)
c.h("Precio n","Del 40 % al 70 % del valor de tu parte","h3","font-size: 32px; color: var(--white); line-height: 1.12;")
c.p("Precio p","Depende del inmueble, de la zona, de si hay cargas y de cuánto conflicto hay. Te decimos el precio por escrito en 48 horas, sin compromiso.","font-size: 15px; line-height: 1.6; color: rgba(255,255,255,0.85);")
c.btn("Precio boton","Ver de qué depende el precio","/cuanto-pagan-por-un-proindiviso/","accent","md","align-self:flex-start; margin-top: 8px;")
# ---------- FAQ ----------
faqs=[("¿Puedo vender mi parte si los demás propietarios no quieren?","Sí. Cada copropietario puede vender su cuota sin el consentimiento de los demás (artículo 399 del Código Civil). Los otros tienen derecho de retracto: pueden quedarse con tu parte al mismo precio en el plazo legal, pero no pueden impedir la venta."),
("¿Cuánto tarda todo el proceso?","La oferta, en 48 horas. La firma en notaría, entre dos y cuatro semanas, según la documentación (escrituras, herencia aceptada, cargas)."),
("¿Tiene algún coste para mí?","No. Nuestra oferta es neta: los gastos de notaría, gestión y documentación corren por nuestra cuenta. Si no vendes, no pagas nada."),
("¿Qué pasa si hay una hipoteca sobre el inmueble?","Compramos igual. La parte proporcional de la deuda se cancela en la firma con el dinero de la venta y tú recibes el resto."),
("¿Y si hay un inquilino o un okupa?","Compramos también en esos casos; es nuestra especialidad. El precio baja algo, pero vendes y dejas de pagar gastos de algo que no usas."),
("¿Puedo pedir una oferta solo para saber cuánto vale mi parte?","Sí. Pedir oferta no te compromete a nada. Muchas personas la usan para negociar con sus propios hermanos o con su expareja.")]
items=''.join(f'<e-accordion-item configuration-id="FAQ item {i}"><e-accordion-item-header configuration-id="FAQ header {i}"><e-accordion-item-title configuration-id="FAQ titulo {i}"><e-heading configuration-id="FAQ pregunta {i}"></e-heading></e-accordion-item-title><e-accordion-item-icon configuration-id="FAQ icono {i}"></e-accordion-item-icon></e-accordion-item-header><e-accordion-item-content configuration-id="FAQ contenido {i}"><e-paragraph configuration-id="FAQ respuesta {i}"></e-paragraph></e-accordion-item-content></e-accordion-item>' for i in range(1,len(faqs)+1))
c.add(f'<e-div-block configuration-id="FAQ"><e-flexbox configuration-id="FAQ inner"><e-flexbox configuration-id="FAQ cabecera"><e-paragraph configuration-id="FAQ overline"></e-paragraph><e-heading configuration-id="FAQ titulo"></e-heading></e-flexbox><e-accordion configuration-id="FAQ acordeon">{items}</e-accordion></e-flexbox></e-div-block>')
c.cfg("FAQ",{"tag":"section"}); section(c,"FAQ","var(--surface-soft)"); inner(c,"FAQ inner",maxw="860px",gap="28px")
c.st("FAQ cabecera","display:flex; flex-direction:column; gap: 12px; width:100%; padding:0px;")
overline(c,"FAQ overline","Preguntas frecuentes")
c.h("FAQ titulo","Preguntas sobre vender un proindiviso","h2")
c.cfg("FAQ acordeon",{"default_state":"all_collapsed","max_expanded":"one","show_icon":True,"faq_schema":True}); c.st("FAQ acordeon","display:flex; flex-direction:column; gap: 10px; width:100%;")
for i,(q,a) in enumerate(faqs,1):
    c.st(f"FAQ item {i}","width:100%; background-color: var(--white); border: 1px solid var(--line); border-radius: 14px; overflow:hidden;")
    c.st(f"FAQ header {i}","padding: 18px 22px; gap: 12px;")
    c.h(f"FAQ pregunta {i}",q,"h3","font-size: 17px; font-weight: 700; line-height: 1.4; color: var(--brand-primary); margin: 0px;")
    c.st(f"FAQ icono {i}","color: var(--brand-accent);"); c.st(f"FAQ contenido {i}","padding: 0px 22px 20px 22px;")
    c.p(f"FAQ respuesta {i}",a,"font-size: 16px; line-height: 1.7; color: var(--ink-muted);")
# ---------- CTA FINAL ----------
# ---------- GUÍAS Y BLOG ----------
guias=[("Qué es un proindiviso","Definición, derechos de cada copropietario y las tres salidas.","/que-es-un-proindiviso/"),("Extinción de condominio","Pasos, coste con cifras e impuestos. Y qué hacer si no hay acuerdo.","/extincion-de-condominio/"),("Compramos herencias","Tu parte de una herencia, con o sin acuerdo de los demás herederos.","/empresas-que-compran-herencias/"),("Un heredero no quiere vender","Qué puedes hacer y cómo vendemos tu parte igual.","/un-heredero-no-quiere-vender/"),("Dónde compramos","Todas las comunidades, provincias y grandes ciudades de España.","/vender-proindiviso/"),("Blog","Más de 30 respuestas a las dudas reales de quien tiene una parte de un inmueble.","/blog/")]
gcards=''.join(f'<e-flexbox configuration-id="Guia {i}"><e-heading configuration-id="Guia {i} t"></e-heading><e-paragraph configuration-id="Guia {i} p"></e-paragraph><e-button configuration-id="Guia {i} b"></e-button></e-flexbox>' for i in range(1,len(guias)+1))
c.add(f'<e-div-block configuration-id="Guias"><e-flexbox configuration-id="Guias inner"><e-flexbox configuration-id="Guias cabecera"><e-paragraph configuration-id="Guias overline"></e-paragraph><e-heading configuration-id="Guias titulo"></e-heading></e-flexbox><e-flexbox configuration-id="Guias grid">{gcards}</e-flexbox></e-flexbox></e-div-block>')
c.cfg("Guias",{"tag":"section"}); section(c,"Guias","var(--surface-soft)"); inner(c,"Guias inner",gap="36px")
c.st("Guias cabecera","display:flex; flex-direction:column; gap: 12px; width:100%; max-width: 760px; padding:0px;")
overline(c,"Guias overline","Infórmate antes de decidir"); c.h("Guias titulo","Guías claras sobre proindivisos, herencias y copropiedad","h2")
c.st("Guias grid","display:flex; flex-direction:row; flex-wrap:wrap; gap: 20px; width:100%; padding:0px;")
for i,(t,d,u) in enumerate(guias,1):
    c.st(f"Guia {i}","display:flex; flex-direction:column; justify-content:space-between; gap: 10px; flex-grow:1; flex-shrink:1; flex-basis: 300px; width:auto; padding: 26px; background-color: var(--white); border: 1px solid var(--line); border-radius: 18px; &:hover { border-color: var(--brand-primary); }")
    c.h(f"Guia {i} t",t,"h3","font-size: 19px; line-height: 1.3;"); c.p(f"Guia {i} p",d,"font-size: 15px; line-height: 1.6; color: var(--ink-muted);"); c.btn(f"Guia {i} b","Leer →",u,"link","sm","align-self:flex-start; margin-top: 8px; font-size: 15px;")
c.add('<e-div-block configuration-id="CTA final"><e-flexbox configuration-id="CTA inner"><e-flexbox configuration-id="CTA texto"><e-paragraph configuration-id="CTA overline"></e-paragraph><e-heading configuration-id="CTA titulo"></e-heading><e-paragraph configuration-id="CTA p"></e-paragraph><e-paragraph configuration-id="CTA tel"></e-paragraph><e-button configuration-id="CTA wa"></e-button></e-flexbox><e-flexbox configuration-id="CTA tarjeta"><e-component configuration-id="CTA formulario"/></e-flexbox></e-flexbox></e-div-block>')
c.cfg("CTA final",{"tag":"section"}); section(c,"CTA final","var(--white)")
c.st("CTA inner","display:flex; flex-direction:row; align-items:flex-start; gap: 56px; width:100%; max-width: 1200px; padding:0px; @media(--mobile){ flex-direction:column; gap: 28px; }")
c.st("CTA texto","display:flex; flex-direction:column; gap: 16px; flex-grow:0; flex-shrink:0; flex-basis: 40%; width: 40%; padding:0px; position: sticky; top: 100px; @media(--mobile){ flex-basis:auto; width:100%; position: static; }")
overline(c,"CTA overline","Pide tu oferta")
c.h("CTA titulo","Vender tu proindiviso: gratis, por escrito y sin compromiso","h2")
c.p("CTA p","Rellena el formulario y te llamamos en menos de 24 horas laborables con una oferta. Si lo prefieres, llámanos o escríbenos ahora. La venta de tu cuota la regula el <a href=\"https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763\" target=\"_blank\" rel=\"noopener\">artículo 399 del Código Civil</a>.","font-size: 17px; line-height: 1.6; color: var(--ink-muted);")
c.cfg("CTA tel",{"tag":"span","paragraph":{"name":"shortcode","settings":{"shortcode":"[zp_telefono]"}},"link":{"destination":TEL,"tag":"a"}}); c.st("CTA tel","font-family: var(--font-heading); font-size: 30px; font-weight: 800; color: var(--brand-primary); text-decoration:none; letter-spacing: -0.02em;")
c.btn("CTA wa","Escribir por WhatsApp",WA,"wa","md","align-self:flex-start;")
c.st("CTA tarjeta","display:flex; flex-direction:column; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding: 34px; background-color: var(--surface-soft); border: 1px solid var(--line); border-radius: 20px; @media(--mobile){ width:100%; padding: 20px; }")
c.cfg("CTA formulario",{"component_id":85})
c.save('comp_home.json'); print('home json ok')
if __name__=='__main__' and '--run' in sys.argv:
    import subprocess
    from pagebuilder import _to_draft
    _to_draft(23)
    out=subprocess.run(['./emcp.sh','elementor-build-composition','@comp_home.json'],capture_output=True,text=True).stdout
    print('home', 'OK' if '"success":true' in out else out[:300])
    if '"success":true' in out: subprocess.run(['./emcp.sh','elementor-publish-document',json.dumps({"post_id":23})],capture_output=True,text=True)
