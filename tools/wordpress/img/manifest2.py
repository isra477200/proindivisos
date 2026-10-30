"""Segunda tanda de imágenes (MiniMax image-01 vía n8n): provincias y 5 ciudades grandes (imagen propia; las ciudades heredan
la de su provincia) y una segunda imagen editorial (antes del FAQ) en páginas de intención, guías y entradas.
Genera manifest2.json con el mismo formato que manifest.json (gen.py / upload.py lo leen con MANIFEST=manifest2.json)."""
import json, glob, os, sys, re
sys.path.insert(0,'/home/claude/isra477200/proindivisos/tools/wordpress')
REPO='/home/claude/isra477200/proindivisos/tools'
import intencion_kw as I
STYLE=(" Editorial real-estate photograph taken in Spain, natural daylight, realistic, calm composition, muted palette with deep blue and warm terracotta accents, "
       "35mm lens, shallow depth of field. No people, no visible faces, no text, no letters, no numbers, no signs, no logos, no watermark.")
items=[]
def add(key, kind, pid, filename, scene, alt, title, slot):
    items.append({"key":key,"kind":kind,"post_id":pid,"filename":filename,"prompt":scene+STYLE,"alt":alt,"title":title,"slot":slot})

# ---------- Provincias (43): arquitectura residencial típica, sin monumentos reconocibles ----------
PROV={
"almeria":("Whitewashed cube houses with flat roofs on a dry hillside near the sea in Almería, intense light, cacti and a blue door.","Casas blancas de tejado plano en una ladera de Almería"),
"cadiz":("A narrow street of white houses with ochre trim, wooden shutters and a glimpse of the Atlantic in a Cádiz town, bright light.","Calle de casas blancas con ribetes ocres en un pueblo de Cádiz"),
"cordoba":("A Cordoban patio with whitewashed walls, blue flower pots, a small fountain and a wrought-iron gate, dappled sunlight.","Patio cordobés con macetas azules y fuente"),
"granada":("Carmen houses with whitewashed walls and gardens on a hill in Granada, snowy mountains in the distance, evening light.","Cármenes encalados en una ladera de Granada con montañas nevadas"),
"huelva":("Low white houses with blue trim on a coastal village street in Huelva, pine trees and dunes behind, soft light.","Casas blancas con ribetes azules en un pueblo costero de Huelva"),
"jaen":("A hilltop village of white houses surrounded by endless olive groves in Jaén, warm late afternoon light.","Pueblo blanco rodeado de olivares en Jaén"),
"malaga":("Mediterranean apartment buildings with terraces and bougainvillea above a beach promenade on the Málaga coast, palm trees.","Edificios con terrazas y buganvillas junto al paseo marítimo en Málaga"),
"sevilla":("A Sevillian street of ochre and white facades with wrought-iron balconies and orange trees, morning light.","Calle sevillana con fachadas ocres, balcones de forja y naranjos"),
"badajoz":("Whitewashed single-storey houses with wide doorways on a quiet street in a Badajoz town, dehesa fields at the end of the street.","Casas bajas encaladas en un pueblo de Badajoz"),
"caceres":("Golden stone houses with arched doorways and wooden balconies in a Cáceres town, warm evening light.","Casas de piedra dorada con balcones de madera en Cáceres"),
"las-palmas":("Colourful flat-roofed houses stacked on a hillside in Gran Canaria with the ocean behind, bright Atlantic light.","Casas de colores en una ladera de Gran Canaria frente al océano"),
"santa-cruz-de-tenerife":("Canarian houses with carved wooden balconies and pastel facades on a sunny street in Tenerife, volcanic peak in the distance.","Casas canarias con balcones de madera en Tenerife"),
"barcelona":("Modernist apartment facades with ornate stone balconies and wooden shutters on a Barcelona street corner, morning light.","Fachadas modernistas con balcones de piedra en Barcelona"),
"girona":("Colourful riverside houses with wooden shutters reflected in the water in a Girona town, soft light.","Casas de colores junto al río en Girona"),
"lleida":("Brick and stone apartment buildings around a quiet plaza with plane trees in a Lleida town, fruit orchards on the horizon.","Edificios de ladrillo y piedra en una plaza de Lleida"),
"tarragona":("Mediterranean townhouses with ochre facades and green shutters on a street leading to the sea in Tarragona, bright sky.","Casas de fachada ocre en una calle que baja al mar en Tarragona"),
"alicante":("White Mediterranean houses with blue doors on a hillside street in Alicante province, palm trees and sea view.","Casas blancas con puertas azules en una ladera de Alicante"),
"castellon":("Orange groves in front of a village of white and ochre houses with a church tower in Castellón, mountains behind.","Naranjos frente a un pueblo de casas blancas en Castellón"),
"valencia":("Apartment blocks with long balconies and awnings on a wide avenue lined with palm and orange trees in Valencia, clear sky.","Bloques de pisos con balcones y toldos en una avenida de Valencia"),
"huesca":("Stone houses with slate roofs and wooden balconies in a Pyrenean village of Huesca, green meadows and peaks.","Casas de piedra con tejados de pizarra en un pueblo del Pirineo de Huesca"),
"teruel":("Brick Mudejar-style facades with green ceramic details on a quiet street in Teruel, warm afternoon light.","Fachadas de ladrillo mudéjar en una calle de Teruel"),
"zaragoza":("Brick apartment buildings with wide balconies on a tree-lined avenue in Zaragoza, dry hills in the distance.","Edificios de ladrillo con balcones en una avenida de Zaragoza"),
"avila":("Granite houses with small windows and wooden doors on a cobbled street in Ávila, cold clear light.","Casas de granito en una calle empedrada de Ávila"),
"burgos":("Stone houses with glazed white galleries along a riverside promenade with poplars in Burgos, soft light.","Casas con galerías acristaladas junto al río en Burgos"),
"leon":("Houses with wooden galleries and stone arcades on a plaza in a León town, mountains behind, morning light.","Casas con galerías de madera y soportales en León"),
"palencia":("Adobe and brick houses with a dovecote on the edge of a Tierra de Campos village in Palencia, golden wheat fields.","Casas de adobe y palomar en un pueblo de Palencia"),
"salamanca":("Golden sandstone facades with carved balconies on a street in Salamanca, warm evening light.","Fachadas de piedra dorada con balcones labrados en Salamanca"),
"segovia":("Houses with sgraffito facades and wooden eaves on a sloping street in Segovia, blue sky.","Casas con fachadas esgrafiadas en una calle de Segovia"),
"soria":("Stone and timber houses with wooden porticoes on a quiet plaza in Soria, pine forests on the hills behind.","Casas de piedra con soportales de madera en Soria"),
"valladolid":("Brick apartment buildings with balconies along a wide boulevard with plane trees in Valladolid, autumn light.","Edificios de ladrillo con balcones en un bulevar de Valladolid"),
"zamora":("Romanesque-style stone houses and a quiet street leading down to a river with a stone bridge in Zamora.","Casas de piedra en una calle que baja al río en Zamora"),
"albacete":("Low white houses with wrought-iron window grilles on a flat village street in Albacete, wide open sky.","Casas bajas con rejas en un pueblo de Albacete"),
"ciudad-real":("Whitewashed houses with blue window frames on a La Mancha village street in Ciudad Real, vineyards at the end.","Casas blancas con ventanas azules en un pueblo de Ciudad Real"),
"cuenca":("Houses with timber balconies clinging to a rocky gorge edge in Cuenca province, pines and river below.","Casas con balcones de madera al borde de una hoz en Cuenca"),
"guadalajara":("Black slate houses with stone walls in a mountain village of Guadalajara, autumn colours.","Casas de pizarra negra en un pueblo de la sierra de Guadalajara"),
"toledo":("Brick and stone houses with wooden doors on a steep cobbled street in Toledo province, warm afternoon light.","Casas de ladrillo y piedra en una calle empedrada de Toledo"),
"a-coruna":("White glazed galleries on a row of houses facing a harbour in A Coruña, grey-blue Atlantic light.","Galerías blancas de casas frente al puerto en A Coruña"),
"lugo":("Granite houses with slate roofs and a stone wall in a green Lugo countryside village, misty morning.","Casas de granito con tejados de pizarra en un pueblo de Lugo"),
"ourense":("Stone houses with wooden galleries on terraced slopes above a river with a stone bridge in Ourense.","Casas de piedra con galerías sobre el río en Ourense"),
"pontevedra":("Granite houses with white galleries beside a quiet ría with fishing boats in Pontevedra, soft light.","Casas de granito con galerías junto a una ría en Pontevedra"),
"alava":("Stone houses with red wooden balconies on a plaza in an Álava town, vineyards and mountains behind.","Casas de piedra con balcones rojos en un pueblo de Álava"),
"bizkaia":("Basque townhouses with green and red glazed galleries on a street above a river estuary in Bizkaia, overcast soft light.","Casas con miradores verdes y rojos sobre la ría en Bizkaia"),
"gipuzkoa":("Belle-époque apartment buildings with white balconies facing a bay with a green hill in Gipuzkoa, soft light.","Edificios con balcones blancos frente a la bahía en Gipuzkoa"),
}
CITY={
"palma":("Sandstone townhouses with green shutters and a courtyard with palm trees in Palma, Mediterranean light.","Casas de piedra con persianas verdes y patio con palmeras en Palma"),
"bilbao":("Apartment buildings with glazed white galleries along the river in Bilbao, green hills behind, soft light.","Edificios con miradores blancos junto a la ría de Bilbao"),
"las-palmas-de-gran-canaria":("Colourful flat-roofed houses on a hill above a city beach in Las Palmas de Gran Canaria, bright light.","Casas de colores sobre la playa en Las Palmas de Gran Canaria"),
"vigo":("Granite apartment buildings with white galleries on a steep street with a view of the ría in Vigo, grey-blue light.","Edificios de granito con galerías en una calle de Vigo frente a la ría"),
"gijon":("Houses with white glazed galleries along a seaside promenade in Gijón, Cantabrian sea and cloudy sky.","Casas con galerías blancas en el paseo marítimo de Gijón"),
}
P=[]
for f in sorted(glob.glob(f'{REPO}/geo/geo_[A-F].json')): P+=json.load(open(f))
by={p['slug']:p for p in P}
gids=json.load(open(f'{REPO}/geo/ids.json'))
for slug,(sc,alt) in {**PROV,**CITY}.items():
    p=by[slug]; en=p['en']
    add('geo-'+slug,'page',gids[slug],'vender-proindiviso-'+slug+'.webp',sc,f"Vender proindiviso {en}: {alt[0].lower()+alt[1:]}",f"Vender proindiviso {en}",'hero')

# ---------- Segunda imagen: páginas de intención ----------
INT2={
23:("A signed written offer in a deep blue folder next to house keys and a pen on a notary table in Spain, morning light.","Oferta por escrito en una carpeta azul junto a unas llaves"),
25:("Glass facade of a modern office building in Spain reflecting apartment blocks, clean sky, street level.","Fachada de oficinas reflejando bloques de pisos"),
27:("A bank transfer receipt-style blank paper, a calculator and euro coins on a Spanish kitchen table, soft light.","Papel, calculadora y monedas de euro sobre una mesa"),
29:("A quiet staircase of an old Spanish apartment building with a wooden handrail and light from a window above.","Escalera de un edificio antiguo con barandilla de madera"),
31:("A sideboard with family photo frames turned face down and a brass key, inherited Spanish house, soft afternoon light.","Aparador con marcos de fotos y una llave en una casa heredada"),
33:("A handshake-free scene: two chairs facing a desk with a signed folder in a bright Spanish meeting room, no people.","Dos sillas frente a una mesa con una carpeta firmada"),
35:("Floor plan of an apartment on a desk with one room highlighted by a coloured sticky note, pencil and ruler.","Plano de un piso con una habitación marcada"),
37:("A bank's glass door and a mortgage folder on a bench outside, Spanish city street, soft light.","Puerta de un banco y carpeta de hipoteca en un banco de la calle"),
39:("A moving box with a few books and a plant beside the door of a Spanish flat, afternoon light.","Caja de mudanza y una planta junto a la puerta de un piso"),
41:("A worn family dining table with four place mats and only one chair pulled out, inherited Spanish home.","Mesa familiar con cuatro manteles individuales y una silla apartada"),
43:("A notary's brass seal and an open deed folder on a dark wooden desk, warm lamp light, Spanish office.","Sello de notaría y carpeta de escritura sobre un escritorio"),
45:("Two front door keys, one tagged with a plain ribbon, on a hallway table of a Spanish family house.","Dos llaves de la casa familiar, una con un lazo"),
47:("A mortgage amortisation folder and a house key on a bank desk with a glass partition, blurred office.","Carpeta de hipoteca y llave sobre la mesa de un banco"),
49:("A tax office-style counter with a numbered ticket dispenser without digits, folders and a pen, Spanish interior.","Mostrador con carpetas y bolígrafo en una oficina"),
51:("A cross-section style view of a Spanish apartment building facade with several balconies, each with a different awning colour.","Fachada de un edificio con toldos de distintos colores"),
53:("A courtroom wooden bench and a gavel seen from the side, tall window light, Spanish court interior, no people.","Banco de madera y mazo en una sala de juzgado"),
55:("A paper map of Spain on a desk with brass keys placed on several regions, soft daylight, no readable text.","Mapa de España sobre un escritorio con llaves en varias regiones"),
57:("A desk phone handset off the hook next to a notebook and a cup of coffee, bright Spanish office, no readable screen.","Teléfono descolgado junto a un cuaderno y un café"),
680:("A stack of folded newspapers and property guides with reading glasses on a wooden bench, Spanish patio light.","Guías y periódicos apilados con unas gafas sobre un banco"),
}
SLUG_INT={23:'vender-proindiviso-home',25:'empresas-que-compran-proindivisos',27:'cuanto-pagan-por-un-proindiviso',29:'vender-proindiviso-sin-avisar',31:'vender-parte-casa-heredada',33:'opiniones-empresas-que-compran-proindivisos',35:'vender-parte-de-un-piso',37:'vender-proindiviso-con-hipoteca',39:'vender-proindiviso-divorcio',41:'vender-proindiviso-entre-hermanos',43:'extincion-de-condominio',45:'extincion-de-condominio-entre-hermanos',47:'extincion-de-condominio-hipoteca',49:'extincion-de-condominio-impuestos-y-notario',51:'que-es-un-proindiviso',53:'division-de-cosa-comun',55:'vender-proindiviso-espana',57:'contacto-zona-proindiviso',680:'blog-zona-proindiviso'}
for pid,(sc,alt) in INT2.items():
    kw=I.M[pid][0]; kwc=kw[0].upper()+kw[1:]
    add(f'int2-{pid}','page',pid,SLUG_INT[pid]+'-2.webp',sc,f"{kwc}: {alt[0].lower()+alt[1:]}",kwc,'fig2')

# ---------- Segunda imagen: entradas y guías ----------
POST2={
"empresas-que-compran-herencias":("A deep blue folder with a signed purchase offer and a brass key on a notary desk, Spanish office, soft light.","Carpeta azul con una oferta firmada y una llave"),
"vender-derechos-hereditarios":("An old family house seen through an open wrought-iron gate, overgrown garden, late afternoon, Spain.","Casa familiar vista a través de una verja abierta"),
"un-heredero-no-quiere-vender":("Two armchairs facing away from each other in an inherited Spanish living room, light through shutters.","Dos sillones dándose la espalda en un salón heredado"),
"vender-herencia-sin-escriturar":("A Spanish Property Registry style building entrance with stone steps and a wooden door, no readable signs.","Entrada de un edificio oficial con escalinata de piedra"),
"vender-mi-parte-de-la-herencia-a-otro-heredero":("A kitchen table with a folded document and a single key pushed across to the other side, morning light.","Documento doblado y una llave empujada al otro lado de la mesa"),
"herencia-cuatro-hermanos-dos-quieren-vender":("A set of four house keys on a ring, two of them separated on a wooden table, Spanish interior.","Cuatro llaves en un llavero, dos separadas"),
"como-se-reparte-una-herencia-de-una-casa-entre-hermanos":("A cake-style wooden house model cut into unequal slices on a table, Spanish kitchen light.","Casa de madera cortada en porciones desiguales"),
"vender-un-piso-heredado-impuestos":("A desk with a laptop, printed tax forms and a coffee, a Spanish balcony with plants behind the window.","Escritorio con portátil, impresos y café"),
"vender-parte-herencia-desde-el-extranjero":("A laptop open to a video call frame left blank, a passport and a key on a desk by a window with Spanish rooftops.","Portátil, pasaporte y llave junto a una ventana"),
"no-quiero-vender-mi-parte-de-la-casa":("A cosy lived-in Spanish living room with a reading lamp and a half-read book, evening warmth.","Salón habitado con lámpara de lectura y un libro"),
"extincion-de-condominio-con-compensacion-economica":("A bank cheque book and a fountain pen on a notary table beside a folded deed, dark wood, warm light.","Talonario y pluma junto a una escritura doblada"),
"extincion-de-condominio-sin-compensacion-economica":("A see-saw style wooden balance with two equal small houses perfectly level, white background.","Balanza de madera con dos casas iguales en equilibrio"),
"escritura-de-extincion-de-condominio":("A stack of notarial folios bound with a ribbon, a brass seal and reading glasses, Spanish notary desk.","Folios notariales atados con cinta, sello y gafas"),
"extincion-parcial-de-condominio":("A row of five mailboxes, one removed leaving a clean gap, Spanish building hallway.","Hilera de buzones con un hueco"),
"ejemplo-de-extincion-de-condominio-con-cifras":("A whiteboard with blank boxes and arrows drawn, a marker and a small house model on the desk below.","Pizarra con esquema de cajas y flechas y una casita"),
"hipoteca-para-extincion-de-condominio":("A bank branch interior with a desk, two chairs and a mortgage folder, afternoon light through blinds, Spain.","Interior de una sucursal bancaria con carpeta de hipoteca"),
"disolucion-de-condominio-entre-hermanos":("A family house doorway with two doormats side by side, warm evening light, Spain.","Entrada de una casa familiar con dos felpudos"),
"cuanto-cobra-el-notario-extincion-de-condominio":("A notary's waiting room with leather chairs, a low table with folders and a brass lamp, no people.","Sala de espera de una notaría"),
"valor-de-la-vivienda-en-la-extincion-de-condominio":("A tape measure and an appraisal clipboard on a windowsill of an empty Spanish flat, city view.","Metro y carpeta de tasación en el alféizar de un piso vacío"),
"extincion-de-condominio-por-divorcio":("Two coffee mugs on a kitchen counter, one packed into an open moving box, morning light, Spain.","Dos tazas, una guardada en una caja de mudanza"),
"vender-o-hacer-extincion-de-condominio":("Two doors side by side in a Spanish hallway, one wooden and one painted blue, both closed.","Dos puertas en un pasillo, una de madera y otra azul"),
"escision-cesacion-liquidacion-de-condominio-que-significan":("An open legal dictionary with a brass key as a bookmark, reading lamp, no readable text.","Diccionario abierto con una llave como marcapáginas"),
"que-significa-proindiviso-en-una-escritura":("A property deed folder with a percentage-style pie drawn on a sticky note, reading glasses, no digits.","Carpeta de escritura con un esquema circular en una nota"),
"proindiviso-ventajas-y-desventajas":("A two-column notebook page with ticks and crosses drawn in pencil, next to a coffee and keys, no readable words.","Cuaderno con dos columnas de ticks y cruces"),
"proindiviso-condominio-comunidad-de-bienes-diferencias":("Three doors of different colours in a Spanish courtyard building, morning light.","Tres puertas de colores en un patio"),
"proindiviso-codigo-civil":("A row of leather-bound law books on a shelf with a small house model in front, warm library light, no readable spines.","Libros de leyes y una casita en una estantería"),
"como-se-calcula-la-cuota-de-un-proindiviso":("A pie chart drawn in chalk on a slate with four unequal slices beside a brass key, Spanish kitchen.","Gráfico circular con porciones desiguales en una pizarra"),
"riesgos-de-un-proindiviso":("A pile of unopened letters and a dusty key on the floor behind the door of an abandoned Spanish flat.","Cartas sin abrir y una llave en el suelo de un piso abandonado"),
"merece-la-pena-comprar-un-proindiviso":("A magnifying glass over a floor plan with a calculator beside it, investor desk, Spanish office light.","Lupa sobre un plano y una calculadora"),
"abogado-proindiviso-cuando-hace-falta":("A leather briefcase and a legal folder on a bench in a Spanish courthouse corridor, tall windows.","Maletín y carpeta legal en el pasillo de un juzgado"),
"subasta-division-de-cosa-comun":("A numbered-style blank paddle and a gavel on a courtroom table, Spanish court interior, soft light.","Paleta y mazo sobre la mesa de una sala judicial"),
"se-puede-obligar-a-vender-a-un-copropietario":("A stone courthouse staircase with a brass handrail leading to tall wooden doors, Spain, no people.","Escalinata de un juzgado con barandilla de latón"),
"derecho-de-tanteo-y-retracto-entre-copropietarios":("An envelope with a wax-style seal and a brass key on a doormat inside a Spanish apartment door.","Sobre lacrado y llave sobre el felpudo"),
"vender-la-mitad-de-una-casa":("A semi-detached Spanish house with one half freshly painted and the other weathered, clear sky.","Casa pareada con una mitad pintada y otra desgastada"),
"vender-nuda-propiedad":("A rocking chair by a sunlit window with a folded blanket and a cane, Spanish living room, no people.","Mecedora junto a la ventana con una manta y un bastón"),
"vender-terreno-proindiviso":("A surveyor's stakes and string marking a boundary on a dry rural plot with almond trees in Spain.","Estacas y cuerda marcando un lindero en una finca"),
"vender-proindiviso-con-inquilino-u-okupa":("A padlocked metal door reinforced with a chain on a Spanish apartment entrance, hallway light.","Puerta metálica con candado y cadena"),
"vender-tu-parte-de-la-casa-a-tu-pareja":("A single house key on a kitchen counter next to a handwritten-style blank note and a flower, soft morning light.","Llave y nota en blanco sobre la encimera"),
"uno-quiere-vender-y-el-otro-no":("Two balconies of the same building, one tidy with flowers, one closed with lowered blinds, Spain.","Dos balcones del mismo edificio, uno con flores y otro cerrado"),
"como-salir-de-una-propiedad-compartida":("An exit door of a Spanish apartment building propped open to a sunny street, keys on the hall table.","Portal abierto a una calle soleada"),
"embargo-de-una-cuota-de-proindiviso":("A stack of registered letters with red edges and a padlock on a desk, dramatic side light, Spain.","Cartas certificadas y un candado sobre un escritorio"),
"donar-mi-parte-de-un-proindiviso":("A brass key tied with a ribbon resting on an open hand-sized gift box on a Spanish living room table.","Llave con lazo sobre una caja de regalo abierta"),
"soy-copropietario-y-quiero-vender":("A tidy desk with a to-do notebook, a phone face down and house keys, bright Spanish flat by a window.","Escritorio con cuaderno, móvil y llaves"),
"urge-vender-por-herencia":("An hourglass almost run out beside a folded deed on a wooden table, warm window light, Spain.","Reloj de arena casi vacío junto a una escritura"),
"que-hacen-las-empresas-que-compran-proindivisos":("A property analyst's desk with a tablet showing a blurred map, folders and a model house, Spanish office.","Mesa de analista con tablet, carpetas y una casita"),
"mi-hermano-vive-en-la-casa-de-mis-padres-y-no-quiere-vender":("A lit window of a family house at dusk seen from the garden gate, Spanish town, no people.","Ventana iluminada de la casa de los padres vista desde la verja"),
"puedo-vender-la-casa-de-mi-madre-con-usufructo":("A kitchen of an older Spanish home with a kettle, a chair and a sunlit tiled wall, no people.","Cocina de una casa familiar con tetera y azulejos al sol"),
"piso-heredado-con-hipoteca-vender-mi-parte":("A bank statement folder and an inherited flat's keys on an entryway console with a mirror, Spain.","Carpeta bancaria y llaves en la consola de la entrada"),
"vender-casa-heredada-sin-testamento":("An empty frame and a closed folder on a notary desk, light from a tall window, Spanish office.","Marco vacío y carpeta cerrada en una notaría"),
"herencia-yacente-vender-antes-de-la-particion":("Furniture under dust sheets and a shaft of light through closed shutters in an inherited Spanish flat.","Muebles tapados y un rayo de luz en un piso heredado"),
"heredero-ilocalizable-o-en-el-extranjero":("A stack of returned envelopes with blank labels and a globe on a Spanish study desk, soft light.","Sobres devueltos y un globo terráqueo sobre un escritorio"),
"heredero-menor-o-incapacitado-venta-de-la-casa":("A child's drawing of a house pinned on a fridge in a Spanish kitchen, soft daylight, no readable words.","Dibujo infantil de una casa en la nevera"),
"cuanto-tarda-vender-un-proindiviso":("A small desk clock without digits and a brass house key on a wooden table, soft window light, Spanish office.","Reloj de mesa y llave de casa sobre un escritorio"),
"documentos-para-vender-tu-parte-de-un-piso":("An open folder with tabbed sections and a passport-style blank card on a desk, Spanish flat, daylight.","Carpeta con separadores sobre un escritorio"),
"nota-simple-como-pedirla-y-leerla":("A printed registry extract style sheet with a magnifying glass and a highlighter on a desk, no readable text.","Documento impreso con lupa y rotulador"),
"valor-de-referencia-catastral-venta-de-tu-parte":("Aerial view of a Spanish residential block grid with rooftops and courtyards at golden hour.","Vista aérea de manzanas de pisos al atardecer"),
"vender-parte-de-un-garaje-trastero-o-local-heredado":("A closed shop front with a metal shutter and a storage room door in a Spanish residential street, morning.","Local con persiana metálica y puerta de trastero"),
"vender-parte-de-una-vpo":("A modern Spanish social housing courtyard with coloured balconies and a playground, clear sky, no people.","Patio de vivienda protegida con balcones de colores"),
"cuanto-me-dan-por-mi-parte-de-un-piso":("Euro banknotes-free scene: a wooden house model on a scale with euro coins on the other pan, Spanish table.","Casita de madera en una balanza con monedas"),
"pacto-de-indivision-que-es-y-cuanto-dura":("A handshake-free scene: two pens crossed over a signed agreement folder on a Spanish desk, warm light.","Dos bolígrafos cruzados sobre una carpeta firmada"),
"comunidad-hereditaria-vs-proindiviso":("An old photo album and a new property folder side by side on a Spanish dining table, soft light.","Álbum antiguo y carpeta nueva sobre la mesa"),
"compensacion-por-uso-exclusivo-de-la-vivienda-comun":("A lived-in Spanish bedroom with a made bed and personal items next to an empty bare bedroom, split view.","Dormitorio habitado junto a otro vacío"),
"ibi-y-gastos-en-un-proindiviso-quien-paga":("A pile of bills clipped together, a calculator and a brass key on a Spanish kitchen table, no readable text.","Recibos con clip, calculadora y llave"),
"alquilar-un-piso-en-proindiviso":("A bright empty Spanish flat with an open balcony door and a tenancy folder on the windowsill.","Piso vacío con puerta de balcón abierta y carpeta de alquiler"),
"vender-proindiviso-a-un-familiar-o-a-una-empresa":("A family kitchen table on one side and a glass office desk on the other, split composition, Spanish light.","Mesa familiar y escritorio de oficina en composición dividida"),
"vender-parte-de-un-garaje-o-trastero":("An underground parking level in a Spanish building with painted bays and a storage door, fluorescent light.","Planta de garaje con plazas pintadas y puerta de trastero"),
"vender-parte-de-un-terreno-rustico-heredado":("An old stone boundary wall and an olive grove with a gate on a rural Spanish plot, late afternoon.","Muro de piedra y olivar con una cancela"),
"proindiviso-por-divorcio-sin-acuerdo":("A hallway of a Spanish flat with two suitcases, one packed and one empty, afternoon light.","Pasillo con dos maletas, una hecha y otra vacía"),
"multipropiedad-como-vender":("A coastal apartment complex balcony view with a pool below, off-season, Spanish Mediterranean, no people.","Balcón de un complejo turístico con piscina fuera de temporada"),
"testamento-con-usufructo-universal-puede-vender-el-viudo":("A wedding photo frame turned to the wall and a key on a bedside table in a Spanish bedroom, soft light.","Marco de boda girado y una llave en la mesilla"),
"que-es-una-cuota-hereditaria":("A set of wooden house blocks of different sizes lined up on a table, Spanish kitchen light.","Bloques de madera de distintos tamaños en fila"),
"vender-casa-con-deudas-o-embargo-mi-parte":("A rusted padlock on a garden gate of a Spanish house with mail overflowing from the box.","Candado oxidado en una verja y buzón lleno"),
"preguntas-antes-de-vender-tu-parte":("A notebook with blank bullet points, a pen and a cup of coffee on a Spanish balcony table, morning.","Cuaderno con viñetas en blanco, bolígrafo y café en un balcón"),
"comprar-la-parte-de-mi-hermano":("Two house keys exchanged across a kitchen table with a folded document, Spanish interior, soft light.","Dos llaves intercambiadas sobre la mesa con un documento"),
"indivisos-inmobiliarios-que-son-y-quien-los-compra":("A property investment desk with a folder, a model house and a map of a Spanish city blurred in the background.","Mesa con carpeta, casita y mapa desenfocado"),
"inmobiliarias-que-compran-pisos-al-contado-o-empresa-de-proindivisos":("Two office doors in a Spanish business building corridor, one glass and modern, one wooden and classic.","Dos puertas de oficina en un pasillo, una moderna y otra clásica"),
"vender-una-casa-con-problemas-quien-la-compra":("A Spanish house facade with a cracked wall, peeling paint and a blooming lemon tree, soft overcast light.","Fachada con grietas y un limonero en flor"),
"cuanto-vale-la-nuda-propiedad-calculo":("A calculator, an hourglass and a small house model on a desk, Spanish office light, no readable digits.","Calculadora, reloj de arena y casita sobre un escritorio"),
}
ids=json.load(open(f'{REPO}/blog/ids.json'))
S=[]
for f in sorted(glob.glob(f'{REPO}/blog/blog_[0-9].json')): S+=json.load(open(f))
missing=[s['slug'] for s in S if s['slug'] not in POST2]
if missing: print('SIN ESCENA:',missing)
for s in S:
    if s['slug'] not in POST2: continue
    sc,alt=POST2[s['slug']]; kw=s['focus_kw']; kwc=kw[0].upper()+kw[1:]
    add(s['slug']+'-2', s['kind'], ids[s['slug']], s['slug'][:50]+'-2.webp', sc, f"{kwc}: {alt[0].lower()+alt[1:]}", s['title_corto'], 'fig2')

json.dump(items,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'manifest2.json'),'w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(items),'imágenes en manifest2.json',Counter(i['slot'] for i in items))
