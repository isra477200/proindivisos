import json
MARK="https://zonaproindiviso.com/wp-content/uploads/2026/10/zona-proindiviso-marca-256.png"
HERO="https://zonaproindiviso.com/wp-content/uploads/2026/10/vender-proindiviso-fachada-edificio-espana.webp"
WA={"name":"shortcode","settings":{"shortcode":"[zp_whatsapp_enlace]"}}
TEL={"name":"shortcode","settings":{"shortcode":"[zp_telefono_enlace]"}}
POPUP={"name":"popup","settings":{"action":"open","popup":{"id":22,"label":"Te llamamos nosotros"}}}
BTN_BASE="font-family: var(--font-body); font-weight: 800; border-radius: 12px; text-decoration:none; text-align:center; display:inline-flex; align-items:center; justify-content:center; transition: all 0.15s ease; "
def btn_style(kind="accent", size="md", extra=""):
    pad={"sm":"padding: 10px 16px; font-size: 14px;","md":"padding: 14px 24px; font-size: 16px;","lg":"padding: 17px 30px; font-size: 17px;"}[size]
    k={"accent":"color: var(--white); background-color: var(--brand-accent); &:hover { background-color: var(--brand-accent-dark); transform: translateY(-1px); } ",
       "white":"color: var(--brand-primary); background-color: var(--white); &:hover { background-color: var(--surface-soft); } ",
       "outline-white":"color: var(--white); background-color: transparent; border: 2px solid rgba(255,255,255,0.55); &:hover { border-color: var(--white); background-color: rgba(255,255,255,0.08); } ",
       "outline":"color: var(--brand-primary); background-color: transparent; border: 2px solid var(--brand-primary); &:hover { background-color: var(--surface-soft); } ",
       "primary":"color: var(--white); background-color: var(--brand-primary); &:hover { background-color: var(--brand-primary-dark); } ",
       "wa":"color: var(--white); background-color: #25a05a; &:hover { background-color: #1e8a4c; } ",
       "link":"color: var(--brand-primary); background-color: transparent; padding: 0px; font-weight: 800; &:hover { color: var(--brand-accent-dark); } "}[kind]
    return BTN_BASE+pad+k+extra
class Comp:
    def __init__(self, post_id, mode="replace_children"):
        self.post_id=post_id; self.mode=mode; self.xml=[]; self.C={}; self.S={}
    def add(self,xml): self.xml.append(xml)
    def cfg(self,k,v): self.C[k]=v
    def st(self,k,v): self.S[k]=v
    def p(self,k,text,style="",tag="p"): self.C[k]={"tag":tag,"paragraph":text}; self.S[k]=style
    def h(self,k,text,tag="h2",style=""): self.C[k]={"tag":tag,"title":text}; self.S[k]=style
    def btn(self,k,text,dest,kind="accent",size="md",style=""): self.C[k]={"text":text,"link":{"destination":dest,"tag":"a"},"tag":"a"}; self.S[k]=btn_style(kind,size,style)
    def payload(self): return {"post_id":self.post_id,"mode":self.mode,"xml_structure":''.join(self.xml),"element_config":self.C,"style":self.S}
    def save(self,fn): json.dump(self.payload(),open(fn,'w'),ensure_ascii=False); return fn
def section(c,k,bg="var(--white)",pad="var(--space-xl)",extra=""):
    c.st(k,f"display:flex; flex-direction:column; align-items:center; width:100%; padding: {pad} 24px; background-color: {bg}; {extra} @media(--tablet){{ padding: var(--space-l) 24px; }} @media(--mobile){{ padding: 56px 18px; }}")
def inner(c,k,maxw="var(--container-max)",gap="var(--space-m)",extra=""):
    c.st(k,f"display:flex; flex-direction:column; gap: {gap}; width:100%; max-width: {maxw}; padding:0px; {extra}")
def overline(c,k,text,center=False,light=False):
    c.p(k,text,f"font-size: 12px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: {'rgba(255,255,255,0.75)' if light else 'var(--brand-accent-dark)'}; {'text-align:center;' if center else ''}")
