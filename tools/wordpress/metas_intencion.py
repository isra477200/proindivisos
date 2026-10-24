import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagebuilder import meta
from intencion_kw import M
T={23:"Inicio",25:"Empresas que compran proindivisos",27:"Cuánto pagan",29:"Vender sin avisar",31:"Vender parte de una casa heredada",33:"Opiniones",35:"Vender parte de un piso",37:"Vender con hipoteca",39:"Vender tras un divorcio",41:"Vender piso heredado entre hermanos",43:"Extinción de condominio",45:"Entre hermanos",47:"Con hipoteca",49:"Impuestos y notario",51:"Qué es un proindiviso",53:"División de cosa común",55:"Dónde compramos",57:"Contacto",680:"Blog"}
BC={680:"Blog",55:"Dónde compramos",57:"Contacto"}  # migas más claras que la keyphrase en estas tres
for pid,(kw,yt,yd) in M.items():
    meta(pid,title=T.get(pid),yt=yt,yd=yd,kw=kw,ptype='pages',bctitle=BC.get(pid))
