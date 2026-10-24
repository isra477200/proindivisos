import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, subprocess
from design import *
from pagebuilder import meta, _to_draft, _env
# Página /gracias/ (1359; la 14 original no era de Elementor y se retiró): confirmación tras el formulario. Sin formulario, con "qué pasa ahora" y WhatsApp. noindex.
PID=1359
c=Comp(PID)
c.add('<e-div-block configuration-id="Hero"><e-flexbox configuration-id="Hero inner"><e-paragraph configuration-id="Hero check"></e-paragraph><e-paragraph configuration-id="Hero overline"></e-paragraph><e-heading configuration-id="Hero titulo"></e-heading><e-paragraph configuration-id="Hero sub"></e-paragraph><e-flexbox configuration-id="Hero botones"><e-button configuration-id="Hero wa"></e-button><e-button configuration-id="Hero home"></e-button></e-flexbox></e-flexbox></e-div-block>')
c.cfg("Hero",{"tag":"section"})
c.st("Hero",f"display:flex; flex-direction:column; align-items:center; width:100%; padding: 96px 24px 104px 24px; background-color: var(--brand-primary-dark); background-image: linear-gradient(100deg, rgba(9,58,90,1) 0%, rgba(9,58,90,0.97) 50%, rgba(13,79,120,0.82) 100%), url('{HERO}'); background-size: cover; background-position: right center; @media(--mobile){{ padding: 56px 18px 64px 18px; }}")
c.st("Hero inner","display:flex; flex-direction:column; align-items:center; gap: 18px; width:100%; max-width: 760px; padding:0px; text-align:center;")
c.p("Hero check","✓","display:flex; align-items:center; justify-content:center; width: 72px; height: 72px; border-radius: 50%; background-color: var(--success); box-shadow: 0 0 0 10px rgba(88,167,40,0.22); color: var(--white); font-size: 38px; font-weight: 800; line-height: 1; margin-bottom: 6px;")
overline(c,"Hero overline","Solicitud recibida",center=True,light=True)
c.h("Hero titulo","Gracias. Hemos recibido tus datos","h1","font-size: clamp(2rem, 1.3rem + 2.8vw, 3.1rem); color: var(--white); line-height: 1.08; text-align:center;")
c.p("Hero sub","Te llamamos en menos de 24 horas laborables para confirmar los datos del inmueble y darte precio. Si prefieres adelantarlo, escríbenos ahora por WhatsApp con la dirección y tu porcentaje.","font-size: 18px; line-height: 1.6; color: rgba(255,255,255,0.84); max-width: 640px; text-align:center;")
c.st("Hero botones","display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; gap: 12px; width:100%; padding: 6px 0px 0px 0px;")
c.btn("Hero wa","Escribir por WhatsApp",WA,"wa","md"); c.btn("Hero home","Volver al inicio","/","outline-white","md")
# QUÉ PASA AHORA
pasos=[("Revisamos tu caso","Comprobamos la nota simple, la cuota que figura en ella y el valor de mercado de la zona."),("Te llamamos","En menos de 24 horas laborables, desde un número español, para confirmar los datos y resolver tus dudas."),("Oferta por escrito en 48 h","Precio neto por tu parte, válido 30 días. Sin exclusiva y sin compromiso."),("Firma en notaría","En 2 a 4 semanas, en una notaría cercana a ti. Gastos a nuestro cargo. Cobras al contado el día de la firma.")]
cards=''.join(f'<e-flexbox configuration-id="Paso {i}"><e-paragraph configuration-id="Paso {i} n"></e-paragraph><e-heading configuration-id="Paso {i} t"></e-heading><e-paragraph configuration-id="Paso {i} p"></e-paragraph></e-flexbox>' for i in range(1,5))
c.add(f'<e-div-block configuration-id="Ahora"><e-flexbox configuration-id="Ahora inner"><e-flexbox configuration-id="Ahora cab"><e-paragraph configuration-id="Ahora overline"></e-paragraph><e-heading configuration-id="Ahora titulo"></e-heading></e-flexbox><e-flexbox configuration-id="Ahora grid">{cards}</e-flexbox></e-flexbox></e-div-block>')
c.cfg("Ahora",{"tag":"section"}); section(c,"Ahora","var(--white)",pad="var(--space-l)"); inner(c,"Ahora inner",gap="28px")
c.st("Ahora cab","display:flex; flex-direction:column; gap: 10px; width:100%; padding:0px;")
overline(c,"Ahora overline","Qué pasa ahora"); c.h("Ahora titulo","Los cuatro pasos hasta cobrar tu parte","h2","max-width: 820px;")
c.st("Ahora grid","display:flex; flex-direction:row; flex-wrap:wrap; gap: 18px; width:100%; padding:0px;")
for i,(t,p) in enumerate(pasos,1):
    c.st(f"Paso {i}","display:flex; flex-direction:column; gap: 10px; flex-grow:1; flex-shrink:1; flex-basis: 240px; width:auto; padding: 26px; background-color: var(--surface-soft); border: 1px solid var(--line); border-top: 4px solid var(--brand-accent); border-radius: 18px;")
    c.p(f"Paso {i} n",f"0{i}","font-family: var(--font-heading); font-size: 15px; font-weight: 800; letter-spacing: 0.1em; color: var(--brand-accent-dark);")
    c.h(f"Paso {i} t",t,"h3","font-size: 19px; line-height: 1.3;"); c.p(f"Paso {i} p",p,"font-size: 15px; line-height: 1.65; color: var(--ink-muted);")
# MIENTRAS TANTO (guías)
guias=[("Cuánto pagamos por un proindiviso","La horquilla real y de qué depende la cifra.","/cuanto-pagan-por-un-proindiviso/"),("Documentos para vender tu parte","Qué papeles necesitamos y dónde conseguir cada uno.","/blog/documentos-para-vender-tu-parte-de-un-piso/"),("Cuánto tarda la venta","Plazos reales paso a paso hasta la firma.","/blog/cuanto-tarda-vender-un-proindiviso/"),("Las 20 preguntas más habituales","Lo que nos preguntan antes de vender, con respuestas claras.","/blog/preguntas-antes-de-vender-tu-parte/")]
gc=''.join(f'<e-flexbox configuration-id="Guia {i}"><e-heading configuration-id="Guia {i} t"></e-heading><e-paragraph configuration-id="Guia {i} p"></e-paragraph><e-button configuration-id="Guia {i} b"></e-button></e-flexbox>' for i in range(1,5))
c.add(f'<e-div-block configuration-id="Guias"><e-flexbox configuration-id="Guias inner"><e-flexbox configuration-id="Guias cab"><e-paragraph configuration-id="Guias overline"></e-paragraph><e-heading configuration-id="Guias titulo"></e-heading><e-paragraph configuration-id="Guias intro"></e-paragraph></e-flexbox><e-flexbox configuration-id="Guias grid">{gc}</e-flexbox></e-flexbox></e-div-block>')
c.cfg("Guias",{"tag":"section"}); section(c,"Guias","var(--surface-soft)",pad="var(--space-l)"); inner(c,"Guias inner",gap="28px")
c.st("Guias cab","display:flex; flex-direction:column; gap: 10px; width:100%; padding:0px;")
overline(c,"Guias overline","Mientras tanto"); c.h("Guias titulo","Lo que conviene saber antes de que te llamemos","h2","max-width: 820px;")
c.p("Guias intro","Cuatro lecturas cortas para llegar a la llamada con las ideas claras.","font-size: 17px; line-height: 1.75; color: var(--ink); max-width: 820px;")
c.st("Guias grid","display:flex; flex-direction:row; flex-wrap:wrap; gap: 18px; width:100%; padding:0px;")
for i,(t,p,u) in enumerate(guias,1):
    c.st(f"Guia {i}","display:flex; flex-direction:column; gap: 10px; flex-grow:1; flex-shrink:1; flex-basis: 240px; width:auto; padding: 26px; background-color: var(--white); border: 1px solid var(--line); border-radius: 18px;")
    c.h(f"Guia {i} t",t,"h3","font-size: 19px; line-height: 1.3;"); c.p(f"Guia {i} p",p,"font-size: 15px; line-height: 1.65; color: var(--ink-muted);")
    c.btn(f"Guia {i} b","Leer →",u,"link","sm","align-self:flex-start; margin-top: 6px; font-size: 15px;")
# HABLAR AHORA
c.add('<e-div-block configuration-id="Ya"><e-flexbox configuration-id="Ya inner"><e-flexbox configuration-id="Ya texto"><e-heading configuration-id="Ya titulo"></e-heading><e-paragraph configuration-id="Ya p"></e-paragraph></e-flexbox><e-flexbox configuration-id="Ya botones"><e-button configuration-id="Ya wa"></e-button><e-paragraph configuration-id="Ya tel"></e-paragraph></e-flexbox></e-flexbox></e-div-block>')
c.cfg("Ya",{"tag":"section"}); section(c,"Ya","var(--white)",pad="var(--space-l)")
c.st("Ya inner","display:flex; flex-direction:row; align-items:center; justify-content:space-between; gap: 32px; width:100%; max-width: 1200px; padding: 36px 40px; background-color: var(--brand-primary); border-radius: 20px; @media(--mobile){ flex-direction:column; align-items:flex-start; padding: 26px 22px; }")
c.st("Ya texto","display:flex; flex-direction:column; gap: 8px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding:0px;")
c.h("Ya titulo","¿Prefieres hablar ahora?","h2","font-size: 26px; color: var(--white);"); c.p("Ya p","Escríbenos por WhatsApp o llámanos en horario laboral. Te atendemos nosotros, no un contestador.","font-size: 16px; line-height: 1.6; color: rgba(255,255,255,0.88);")
c.st("Ya botones","display:flex; flex-direction:column; align-items:flex-end; gap: 10px; flex-grow:0; flex-shrink:0; width:auto; padding:0px; @media(--mobile){ align-items:flex-start; width:100%; }")
c.btn("Ya wa","Escribir por WhatsApp",WA,"wa","md")
c.cfg("Ya tel",{"tag":"span","paragraph":{"name":"shortcode","settings":{"shortcode":"[zp_telefono]"}},"link":{"destination":TEL,"tag":"a"}}); c.st("Ya tel","font-family: var(--font-heading); font-size: 24px; font-weight: 800; color: var(--white); text-decoration:none; letter-spacing: -0.02em;")
if __name__=='__main__':
    _to_draft(PID)
    fn=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.gracias_payload.json'); c.save(fn)
    out=subprocess.run(['./emcp.sh','elementor-build-composition','@'+fn],capture_output=True,text=True).stdout; os.unlink(fn)
    print(out[:600])
    if '"success":true' in out:
        print(subprocess.run(['./emcp.sh','elementor-publish-document',json.dumps({"post_id":PID})],capture_output=True,text=True).stdout[:200])
        meta(PID,title="Gracias, hemos recibido tu solicitud",yt="Gracias · Zona Proindiviso",yd="Hemos recibido tu solicitud. Te llamamos en menos de 24 horas laborables.",kw="",status="publish",slug="gracias",extra={"meta":{"_yoast_wpseo_title":"Gracias · Zona Proindiviso","_yoast_wpseo_metadesc":"Hemos recibido tu solicitud. Te llamamos en menos de 24 horas laborables.","_yoast_wpseo_meta-robots-noindex":"1"}})
