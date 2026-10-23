import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json, re, subprocess
from design import *
def build(spec):
    c=Comp(spec['post_id'])
    # HERO (azul oscuro, con tarjeta)
    c.add('<e-div-block configuration-id="Hero"><e-flexbox configuration-id="Hero inner"><e-flexbox configuration-id="Hero texto"><e-paragraph configuration-id="Hero migas"></e-paragraph><e-paragraph configuration-id="Hero overline"></e-paragraph><e-heading configuration-id="Hero titulo"></e-heading><e-paragraph configuration-id="Hero sub"></e-paragraph><e-flexbox configuration-id="Hero botones"><e-button configuration-id="Hero wa"></e-button><e-button configuration-id="Hero tel"></e-button></e-flexbox><e-flexbox configuration-id="Hero checks"><e-paragraph configuration-id="Hero check 1"></e-paragraph><e-paragraph configuration-id="Hero check 2"></e-paragraph><e-paragraph configuration-id="Hero check 3"></e-paragraph></e-flexbox></e-flexbox><e-flexbox configuration-id="Hero tarjeta"><e-div-block configuration-id="Hero tarjeta franja"></e-div-block><e-heading configuration-id="Hero tarjeta titulo"></e-heading><e-paragraph configuration-id="Hero tarjeta texto"></e-paragraph><e-component configuration-id="Hero formulario"/></e-flexbox></e-flexbox></e-div-block>')
    c.cfg("Hero",{"tag":"section"})
    c.st("Hero",f"display:flex; flex-direction:column; align-items:center; width:100%; padding: 72px 24px 80px 24px; background-color: var(--brand-primary-dark); background-image: linear-gradient(100deg, rgba(9,58,90,1) 0%, rgba(9,58,90,0.97) 50%, rgba(13,79,120,0.82) 100%), url('{HERO}'); background-size: cover; background-position: right center; @media(--tablet){{ padding: 56px 24px 64px 24px; }} @media(--mobile){{ padding: 40px 18px 48px 18px; background-image: linear-gradient(180deg, rgba(9,58,90,0.97) 0%, rgba(9,58,90,0.97) 100%), url('{HERO}'); }}")
    c.st("Hero inner","display:flex; flex-direction:row; align-items:center; gap: 56px; width:100%; max-width: 1200px; padding:0px; @media(--tablet){ gap: 32px; } @media(--mobile){ flex-direction:column; gap: 32px; }")
    c.st("Hero texto","display:flex; flex-direction:column; gap: 20px; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding:0px;")
    c.cfg("Hero migas",{"tag":"p","paragraph":{"name":"shortcode","settings":{"shortcode":"[wpseo_breadcrumb]"}}}); c.st("Hero migas","font-size: 13px; color: rgba(255,255,255,0.7); margin-bottom: 4px; @media(--mobile){ font-size: 12px; }")
    overline(c,"Hero overline",spec['kicker'],light=True)
    c.h("Hero titulo",spec['h1'],"h1","font-size: clamp(2rem, 1.3rem + 2.8vw, 3.1rem); color: var(--white); max-width: 640px; line-height: 1.08;")
    c.p("Hero sub",spec['sub'],"font-size: 18px; line-height: 1.6; color: rgba(255,255,255,0.84); max-width: 580px;")
    c.st("Hero botones","display:flex; flex-direction:row; flex-wrap:wrap; gap: 12px; width:100%; padding:0px;")
    c.btn("Hero wa","Escribir por WhatsApp",WA,"wa","md"); c.btn("Hero tel","Llamar ahora",TEL,"outline-white","md")
    c.st("Hero checks","display:flex; flex-direction:row; flex-wrap:wrap; gap: 8px 24px; width:100%; padding: 4px 0px 0px 0px;")
    for i,t in enumerate(spec.get('checks',["Oferta en 48 h","Pago al contado en notaría","Gastos a nuestro cargo"]),1):
        c.p(f"Hero check {i}",f"<strong>✓</strong>&nbsp; {t}","font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.9);")
    c.st("Hero tarjeta","display:flex; flex-direction:column; gap: 8px; flex-grow:0; flex-shrink:0; flex-basis: 420px; width: 420px; max-width:100%; padding: 0px 28px 28px 28px; background-color: var(--white); border-radius: 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.35); overflow:hidden; @media(--tablet){ flex-basis: 360px; width: 360px; } @media(--mobile){ flex-basis:auto; width:100%; padding: 0px 22px 22px 22px; }")
    c.st("Hero tarjeta franja","width: calc(100% + 56px); height: 8px; margin: 0px 0px 20px -28px; padding:0px; background-color: var(--brand-accent); @media(--mobile){ width: calc(100% + 44px); margin-left: -22px; }")
    c.h("Hero tarjeta titulo",spec.get('card_title',"Te llamamos nosotros"),"h3","font-size: 23px; color: var(--brand-primary);")
    c.p("Hero tarjeta texto",spec.get('card_text',"Tu nombre y tu teléfono. Te llamamos en menos de 24 horas laborables con una oferta."),"font-size: 14px; color: var(--ink-muted); margin-bottom: 6px;")
    c.cfg("Hero formulario",{"component_id":83})
    # SECCIONES
    for si,sec in enumerate(spec['sections']):
        bg="var(--white)" if si%2==0 else "var(--surface-soft)"
        sc=f"Seccion {si+1}"; ic=f"{sc} inner"; parts=[]
        t=sec.get('type','text')
        if sec.get('overline') or sec.get('h2'):
            parts.append(f'<e-flexbox configuration-id="{sc} cab"></e-flexbox>')  # placeholder reemplazado abajo
            cab=[]
            if sec.get('overline'): cab.append(f'<e-paragraph configuration-id="{sc} overline"></e-paragraph>'); overline(c,f"{sc} overline",sec['overline'])
            if sec.get('h2'): cab.append(f'<e-heading configuration-id="{sc} titulo"></e-heading>'); c.h(f"{sc} titulo",sec['h2'],"h2","max-width: 820px;")
            parts[-1]=f'<e-flexbox configuration-id="{sc} cab">{"".join(cab)}</e-flexbox>'; c.st(f"{sc} cab","display:flex; flex-direction:column; gap: 10px; width:100%; padding:0px;")
        for k,para in enumerate(sec.get('intro',[]) if isinstance(sec.get('intro',[]),list) else [sec['intro']]):
            cc=f"{sc} intro {k}"; parts.append(f'<e-paragraph configuration-id="{cc}"></e-paragraph>'); c.p(cc,para,"font-size: 17px; line-height: 1.75; color: var(--ink); max-width: 820px;")
        if t in ('cards','steps'):
            cards=[]
            for k,it in enumerate(sec['items']):
                cc=f"{sc} card {k}"; inn=''
                if t=='steps': inn+=f'<e-paragraph configuration-id="{cc} n"></e-paragraph>'; c.p(f"{cc} n",f"0{k+1}","font-family: var(--font-heading); font-size: 15px; font-weight: 800; letter-spacing: 0.1em; color: var(--brand-accent-dark);")
                inn+=f'<e-heading configuration-id="{cc} t"></e-heading><e-paragraph configuration-id="{cc} p"></e-paragraph>'
                c.h(f"{cc} t",it['t'],"h3","font-size: 19px; line-height: 1.3;"); c.p(f"{cc} p",it['p'],"font-size: 15px; line-height: 1.65; color: var(--ink-muted);")
                if it.get('url'): inn+=f'<e-button configuration-id="{cc} b"></e-button>'; c.btn(f"{cc} b",it.get('cta',"Ver más →"),it['url'],"link","sm","align-self:flex-start; margin-top: 6px; font-size: 15px;")
                cards.append(f'<e-flexbox configuration-id="{cc}">{inn}</e-flexbox>')
                c.st(cc,"display:flex; flex-direction:column; justify-content:flex-start; gap: 10px; flex-grow:1; flex-shrink:1; flex-basis: 260px; width:auto; padding: 26px; background-color: "+("var(--surface-soft)" if bg=="var(--white)" else "var(--white)")+"; border: 1px solid var(--line); border-radius: 18px;"+(" border-top: 4px solid var(--brand-accent);" if t=='steps' else ""))
            parts.append(f'<e-flexbox configuration-id="{sc} grid">{"".join(cards)}</e-flexbox>'); c.st(f"{sc} grid","display:flex; flex-direction:row; flex-wrap:wrap; gap: 18px; width:100%; padding:0px;")
        elif t=='list':
            cc=f"{sc} lista"; parts.append(f'<e-flexbox configuration-id="{cc}">'+''.join(f'<e-paragraph configuration-id="{cc} {k}"></e-paragraph>' for k in range(len(sec['items'])))+'</e-flexbox>')
            c.st(cc,"display:flex; flex-direction:column; gap: 12px; width:100%; max-width: 820px; padding:0px;")
            for k,x in enumerate(sec['items']): c.p(f"{cc} {k}",x,"font-size: 16px; line-height: 1.65; color: var(--ink); padding-left: 18px; border-left: 3px solid var(--brand-accent);")
        elif t=='callout':
            cc=f"{sc} callout"; it=sec['items']
            parts.append(f'<e-flexbox configuration-id="{cc}"><e-heading configuration-id="{cc} t"></e-heading><e-paragraph configuration-id="{cc} p"></e-paragraph><e-button configuration-id="{cc} b"></e-button></e-flexbox>')
            c.st(cc,"display:flex; flex-direction:column; gap: 10px; width:100%; max-width: 820px; padding: 32px; background-color: var(--brand-primary); border-radius: 18px;")
            c.h(f"{cc} t",it['t'],"h3","font-size: 24px; color: var(--white);"); c.p(f"{cc} p",it['p'],"font-size: 16px; line-height: 1.6; color: rgba(255,255,255,0.88);"); c.btn(f"{cc} b",it['cta'],it.get('url',POPUP),"accent","md","align-self:flex-start; margin-top: 6px;")
        elif t=='table':
            cc=f"{sc} tabla"; rows=sec['items']
            parts.append(f'<e-flexbox configuration-id="{cc}">'+''.join(f'<e-flexbox configuration-id="{cc} fila {k}"><e-paragraph configuration-id="{cc} fila {k} a"></e-paragraph><e-paragraph configuration-id="{cc} fila {k} b"></e-paragraph></e-flexbox>' for k in range(len(rows)))+'</e-flexbox>')
            c.st(cc,"display:flex; flex-direction:column; gap: 0px; width:100%; max-width: 820px; padding:0px; border: 1px solid var(--line); border-radius: 14px; overflow:hidden;")
            for k,(a,b) in enumerate(rows):
                hdr = (k==0)
                c.st(f"{cc} fila {k}","display:flex; flex-direction:row; gap: 16px; width:100%; padding: 14px 18px; background-color: "+("var(--brand-primary)" if hdr else ("var(--white)" if k%2 else "var(--surface-soft)"))+"; @media(--mobile){ flex-direction:column; gap: 4px; }")
                c.p(f"{cc} fila {k} a",a,("font-size: 14px; font-weight: 800; color: var(--white); flex-basis: 40%; flex-shrink:0;" if hdr else "font-size: 15px; font-weight: 700; color: var(--ink); flex-basis: 40%; flex-shrink:0;"))
                c.p(f"{cc} fila {k} b",b,("font-size: 14px; font-weight: 800; color: var(--white);" if hdr else "font-size: 15px; color: var(--ink-muted); line-height: 1.5;"))
        for k,para in enumerate(sec.get('outro',[]) if isinstance(sec.get('outro',[]),list) else [sec['outro']]):
            cc=f"{sc} outro {k}"; parts.append(f'<e-paragraph configuration-id="{cc}"></e-paragraph>'); c.p(cc,para,"font-size: 17px; line-height: 1.75; color: var(--ink); max-width: 820px;")
        c.add(f'<e-div-block configuration-id="{sc}"><e-flexbox configuration-id="{ic}">{"".join(parts)}</e-flexbox></e-div-block>')
        c.cfg(sc,{"tag":"section"}); section(c,sc,bg,pad="var(--space-l)"); inner(c,ic,gap="24px")
    # FAQ
    faqs=spec.get('faqs',[])
    if faqs:
        items=''.join(f'<e-accordion-item configuration-id="FAQ item {i}"><e-accordion-item-header configuration-id="FAQ header {i}"><e-accordion-item-title configuration-id="FAQ titulo {i}"><e-paragraph configuration-id="FAQ pregunta {i}"></e-paragraph></e-accordion-item-title><e-accordion-item-icon configuration-id="FAQ icono {i}"></e-accordion-item-icon></e-accordion-item-header><e-accordion-item-content configuration-id="FAQ contenido {i}"><e-paragraph configuration-id="FAQ respuesta {i}"></e-paragraph></e-accordion-item-content></e-accordion-item>' for i in range(1,len(faqs)+1))
        c.add(f'<e-div-block configuration-id="FAQ"><e-flexbox configuration-id="FAQ inner"><e-flexbox configuration-id="FAQ cab"><e-paragraph configuration-id="FAQ overline"></e-paragraph><e-heading configuration-id="FAQ titulo"></e-heading></e-flexbox><e-accordion configuration-id="FAQ acordeon">{items}</e-accordion></e-flexbox></e-div-block>')
        c.cfg("FAQ",{"tag":"section"}); section(c,"FAQ","var(--surface-soft-2)",pad="var(--space-l)"); inner(c,"FAQ inner",maxw="860px",gap="24px")
        c.st("FAQ cab","display:flex; flex-direction:column; gap: 10px; width:100%; padding:0px;")
        overline(c,"FAQ overline","Preguntas frecuentes"); c.h("FAQ titulo",spec.get('faq_title',"Dudas habituales"),"h2")
        c.cfg("FAQ acordeon",{"default_state":"all_collapsed","max_expanded":"one","show_icon":True,"faq_schema":True}); c.st("FAQ acordeon","display:flex; flex-direction:column; gap: 10px; width:100%;")
        for i,(q,a) in enumerate(faqs,1):
            c.st(f"FAQ item {i}","width:100%; background-color: var(--white); border: 1px solid var(--line); border-radius: 14px; overflow:hidden;")
            c.st(f"FAQ header {i}","padding: 16px 20px; gap: 12px;"); c.p(f"FAQ pregunta {i}",q,"font-size: 17px; font-weight: 700; color: var(--brand-primary);")
            c.st(f"FAQ icono {i}","color: var(--brand-accent);"); c.st(f"FAQ contenido {i}","padding: 0px 20px 18px 20px;")
            c.p(f"FAQ respuesta {i}",a,"font-size: 16px; line-height: 1.7; color: var(--ink-muted);")
    # RELACIONADO
    rel=spec.get('related',[])
    if rel:
        c.add('<e-div-block configuration-id="Relacionado"><e-flexbox configuration-id="Relacionado inner"><e-paragraph configuration-id="Relacionado titulo"></e-paragraph><e-flexbox configuration-id="Relacionado lista">'+''.join(f'<e-button configuration-id="Rel {i}"></e-button>' for i in range(len(rel)))+'</e-flexbox></e-flexbox></e-div-block>')
        c.cfg("Relacionado",{"tag":"section"}); c.st("Relacionado","display:flex; flex-direction:column; align-items:center; width:100%; padding: 32px 24px; background-color: var(--white); border-top: 1px solid var(--line);")
        c.st("Relacionado inner","display:flex; flex-direction:column; gap: 12px; width:100%; max-width: 1200px; padding:0px;")
        overline(c,"Relacionado titulo","También te puede interesar"); c.st("Relacionado lista","display:flex; flex-direction:row; flex-wrap:wrap; gap: 10px; width:100%; padding:0px;")
        for i,(label,url) in enumerate(rel): c.btn(f"Rel {i}",label,url,"outline","sm","font-size: 14px; padding: 9px 16px;")
    # CTA
    c.add('<e-div-block configuration-id="CTA final"><e-flexbox configuration-id="CTA inner"><e-flexbox configuration-id="CTA texto"><e-paragraph configuration-id="CTA overline"></e-paragraph><e-heading configuration-id="CTA titulo"></e-heading><e-paragraph configuration-id="CTA p"></e-paragraph><e-paragraph configuration-id="CTA tel"></e-paragraph><e-button configuration-id="CTA wa"></e-button></e-flexbox><e-flexbox configuration-id="CTA tarjeta"><e-component configuration-id="CTA formulario"/></e-flexbox></e-flexbox></e-div-block>')
    c.cfg("CTA final",{"tag":"section"}); section(c,"CTA final","var(--white)",pad="var(--space-l)")
    c.st("CTA inner","display:flex; flex-direction:row; align-items:flex-start; gap: 48px; width:100%; max-width: 1200px; padding:0px; @media(--mobile){ flex-direction:column; gap: 28px; }")
    c.st("CTA texto","display:flex; flex-direction:column; gap: 14px; flex-grow:0; flex-shrink:0; flex-basis: 40%; width: 40%; padding:0px; position: sticky; top: 100px; @media(--mobile){ flex-basis:auto; width:100%; position: static; }")
    overline(c,"CTA overline","Pide tu oferta"); c.h("CTA titulo",spec.get('cta_title',"Gratis, por escrito y sin compromiso"),"h2")
    c.p("CTA p",spec.get('cta_text',"Rellena el formulario y te llamamos en menos de 24 horas laborables con una oferta. Si lo prefieres, llámanos o escríbenos ahora."),"font-size: 17px; line-height: 1.6; color: var(--ink-muted);")
    c.cfg("CTA tel",{"tag":"span","paragraph":{"name":"shortcode","settings":{"shortcode":"[zp_telefono]"}},"link":{"destination":TEL,"tag":"a"}}); c.st("CTA tel","font-family: var(--font-heading); font-size: 30px; font-weight: 800; color: var(--brand-primary); text-decoration:none; letter-spacing: -0.02em;")
    c.btn("CTA wa","Escribir por WhatsApp",WA,"wa","md","align-self:flex-start;")
    c.st("CTA tarjeta","display:flex; flex-direction:column; flex-grow:1; flex-shrink:1; flex-basis:0px; width:auto; min-width:0; padding: 32px; background-color: var(--surface-soft); border: 1px solid var(--line); border-radius: 20px; @media(--mobile){ width:100%; padding: 20px; }")
    c.cfg("CTA formulario",{"component_id":85})
    return c.payload()
def _env():
    import os
    env={}
    for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wp.env')):
        if '=' in l: k,v=l.strip().split('=',1); env[k]=v.strip().strip('"').strip("'")
    return env
def _to_draft(post_id):
    # build-composition sobre un documento publicado no actualiza la versión publicada: pasar a borrador antes de componer.
    env=_env()
    for ep in ('pages','posts'):
        out=subprocess.run(['curl','-sS','--max-time','60','-u',env['P1'],'-X','POST','-H','Content-Type: application/json',f"{env['WP']}/wp-json/wp/v2/{ep}/{post_id}",'-d','{"status":"draft"}'],capture_output=True,text=True).stdout
        try:
            if json.loads(out).get('status')=='draft': return ep
        except Exception: pass
    return None
def run(spec, publish=True):
    _to_draft(spec['post_id'])
    payload=build(spec)
    out=subprocess.run(['./emcp.sh','elementor-build-composition',json.dumps(payload,ensure_ascii=False)],capture_output=True,text=True).stdout
    ok='"success":true' in out
    warn=re.findall(r'"warnings":\[(.*?)\]',out)
    print(spec['post_id'], 'OK' if ok else 'FAIL', '' if ok else out[:400], ('WARN '+warn[0][:300]) if warn else '', flush=True)
    if ok and publish:
        subprocess.run(['./emcp.sh','elementor-publish-document',json.dumps({"post_id":spec['post_id']})],capture_output=True,text=True)
    return ok
def meta(post_id, title=None, yt=None, yd=None, kw=None, parent=None, status=None, slug=None, ptype='pages', extra=None):
    import os
    env={}
    for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wp.env')):
        if '=' in l: k,v=l.strip().split("=",1); env[k]=v.strip().strip("\"").strip("'")
    body={}
    if title: body['title']=title
    if parent is not None: body['parent']=parent
    if status: body['status']=status
    if slug: body['slug']=slug
    m={}
    if yt: m['_yoast_wpseo_title']=yt
    if yd: m['_yoast_wpseo_metadesc']=yd
    if kw is not None: m['_yoast_wpseo_focuskw']=kw
    if m: body['meta']=m
    if extra: body.update(extra)
    out=subprocess.run(['curl','-sS','--max-time','60','-u',env['P1'],'-X','POST','-H','Content-Type: application/json',f"{env['WP']}/wp-json/wp/v2/{ptype}/{post_id}",'-d',json.dumps(body,ensure_ascii=False)],capture_output=True,text=True).stdout
    try:
        d=json.loads(out); print(post_id,'META OK' if 'id' in d else 'META FAIL '+str(d)[:200],d.get('link'))
    except Exception: print(post_id,'META FAIL',out[:300])

def build_simple(spec):
    c=Comp(spec['post_id'])
    c.add('<e-div-block configuration-id="Hero"><e-flexbox configuration-id="Hero inner"><e-paragraph configuration-id="Hero migas"></e-paragraph><e-paragraph configuration-id="Hero overline"></e-paragraph><e-heading configuration-id="Hero titulo"></e-heading><e-paragraph configuration-id="Hero sub"></e-paragraph></e-flexbox></e-div-block>')
    c.cfg("Hero",{"tag":"section"}); c.st("Hero","display:flex; flex-direction:column; align-items:center; width:100%; padding: 56px 24px 56px 24px; background-color: var(--brand-primary-dark); @media(--mobile){ padding: 36px 18px 40px 18px; }")
    c.st("Hero inner","display:flex; flex-direction:column; gap: 14px; width:100%; max-width: 860px; padding:0px;")
    c.cfg("Hero migas",{"tag":"p","paragraph":{"name":"shortcode","settings":{"shortcode":"[wpseo_breadcrumb]"}}}); c.st("Hero migas","font-size: 13px; color: rgba(255,255,255,0.7);")
    overline(c,"Hero overline",spec.get('kicker',''),light=True)
    c.h("Hero titulo",spec['h1'],"h1","font-size: clamp(1.8rem, 1.2rem + 2vw, 2.6rem); color: var(--white); line-height: 1.12;")
    c.p("Hero sub",spec.get('sub',''),"font-size: 17px; line-height: 1.6; color: rgba(255,255,255,0.84);")
    parts=[]
    for si,sec in enumerate(spec['sections']):
        sc=f"S{si}"
        if sec.get('h2'): parts.append(f'<e-heading configuration-id="{sc} h"></e-heading>'); c.h(f"{sc} h",sec['h2'],"h2","font-size: 24px; margin-top: 12px;")
        for k,para in enumerate(sec.get('p',[])):
            cc=f"{sc} p{k}"; parts.append(f'<e-paragraph configuration-id="{cc}"></e-paragraph>'); c.p(cc,para,"font-size: 16px; line-height: 1.75; color: var(--ink);")
        for k,x in enumerate(sec.get('items',[])):
            cc=f"{sc} i{k}"; parts.append(f'<e-paragraph configuration-id="{cc}"></e-paragraph>'); c.p(cc,x,"font-size: 16px; line-height: 1.65; color: var(--ink); padding-left: 16px; border-left: 3px solid var(--brand-accent);")
    c.add(f'<e-div-block configuration-id="Cuerpo"><e-flexbox configuration-id="Cuerpo inner">{"".join(parts)}</e-flexbox></e-div-block>')
    c.cfg("Cuerpo",{"tag":"section"}); section(c,"Cuerpo","var(--white)",pad="56px"); c.st("Cuerpo inner","display:flex; flex-direction:column; gap: 14px; width:100%; max-width: 860px; padding:0px;")
    return c.payload()
def run_simple(spec, publish=True):
    payload=build_simple(spec)
    out=subprocess.run(['./emcp.sh','elementor-build-composition',json.dumps(payload,ensure_ascii=False)],capture_output=True,text=True).stdout
    ok='"success":true' in out
    print(spec['post_id'], 'OK' if ok else 'FAIL', '' if ok else out[:400], flush=True)
    if ok and publish: subprocess.run(['./emcp.sh','elementor-publish-document',json.dumps({"post_id":spec['post_id']})],capture_output=True,text=True)
    return ok
