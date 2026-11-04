import json, glob, os, sys
sys.path.insert(0,'/home/claude/isra477200/proindivisos/tools/wordpress')
REPO='/home/claude/isra477200/proindivisos/tools'
STYLE=(" Editorial real-estate photograph taken in Spain, natural daylight, realistic, calm composition, muted palette with deep blue and warm terracotta accents, "
       "35mm lens, shallow depth of field. No visible faces, no text, no letters, no numbers, no signs, no logos, no watermark.")
items=[]
def add(key, kind, pid, filename, scene, alt, title):
    items.append({"key":key,"kind":kind,"post_id":pid,"filename":filename,"prompt":scene+STYLE,"alt":alt,"title":title})

# ---------- Blog posts and long-tail pages (72) ----------
BLOG={
"empresas-que-compran-herencias":("A sunlit living room of an inherited Spanish flat from the 1970s, vintage furniture under white dust sheets, light through old wooden shutters.","Salón de un piso heredado en España con muebles cubiertos, luz entrando por la persiana"),
"vender-derechos-hereditarios":("Close-up of a notary desk in Spain: a folded inheritance deed, a fountain pen and a brass key resting on dark wood.","Escritura de herencia, pluma y llave sobre la mesa de una notaría"),
"un-heredero-no-quiere-vender":("Exterior of an old Spanish family house with closed green shutters and a locked wrought-iron gate, late afternoon light.","Casa familiar española con las persianas cerradas y la verja cerrada"),
"vender-herencia-sin-escriturar":("An old handwritten property document and a faded black-and-white photo of a Spanish village house on a wooden table.","Documento antiguo de una vivienda y fotografía de una casa de pueblo sobre una mesa"),
"vender-mi-parte-de-la-herencia-a-otro-heredero":("Two sets of house keys placed side by side on a kitchen table in a Spanish flat, morning light.","Dos juegos de llaves sobre la mesa de la cocina de un piso heredado"),
"herencia-cuatro-hermanos-dos-quieren-vender":("Four empty chairs around a dining table in an inherited Spanish home, afternoon light through a balcony.","Cuatro sillas vacías alrededor de la mesa de una casa heredada"),
"como-se-reparte-una-herencia-de-una-casa-entre-hermanos":("A floor plan of an apartment, a wooden ruler and a pencil on a desk in a Spanish home, natural light.","Plano de una vivienda con regla y lápiz sobre un escritorio"),
"vender-un-piso-heredado-impuestos":("A calculator, a folder of tax forms and house keys on a desk, soft daylight, Spanish office.","Calculadora, carpeta de impuestos y llaves de un piso heredado"),
"vender-parte-herencia-desde-el-extranjero":("A passport, a boarding pass and a brass house key on a wooden table next to a window with a view of Spanish rooftops.","Pasaporte, tarjeta de embarque y llave de una casa en España"),
"no-quiero-vender-mi-parte-de-la-casa":("A classic Spanish apartment doorway with a solid wooden door, brass handle and a doormat, warm light in the hallway.","Puerta de madera de un piso español con pomo de latón"),
"extincion-de-condominio-con-compensacion-economica":("A notary table with a signed deed, a bank cheque book and a pen, deep blue folder, Spanish office interior.","Escritura firmada, talonario y pluma sobre la mesa del notario"),
"extincion-de-condominio-sin-compensacion-economica":("Two identical brass keys on a plain white surface, one slightly apart, soft shadow, minimal composition.","Dos llaves iguales sobre una superficie blanca"),
"escritura-de-extincion-de-condominio":("Close-up of a Spanish notarial deed with a wax-style seal and a fountain pen, warm desk lamp light.","Escritura notarial con sello y pluma estilográfica"),
"extincion-parcial-de-condominio":("A row of three mailboxes in a Spanish apartment building hallway, one open, terrazzo floor, daylight.","Buzones en el portal de un edificio español, uno abierto"),
"ejemplo-de-extincion-de-condominio-con-cifras":("A desk with a calculator, printed spreadsheets and a small wooden house model, natural window light.","Calculadora, hojas de cálculo y maqueta de casa sobre un escritorio"),
"hipoteca-para-extincion-de-condominio":("Interior of a modern bank office in Spain: a desk with a mortgage folder, keys and a glass of water, blurred background.","Mesa de una oficina bancaria con una carpeta de hipoteca y llaves"),
"disolucion-de-condominio-entre-hermanos":("Facade of a traditional Spanish family home with two identical balconies side by side, warm evening light.","Fachada de una casa familiar con dos balcones iguales"),
"cuanto-cobra-el-notario-extincion-de-condominio":("Entrance of a Spanish notary office: a polished brass door plate without lettering, dark wooden door, stone facade.","Entrada de una notaría con placa de latón y puerta de madera"),
"valor-de-la-vivienda-en-la-extincion-de-condominio":("A surveyor's laser measure and a clipboard on the floor of an empty Spanish apartment with parquet, daylight.","Medidor láser y carpeta en el suelo de un piso vacío"),
"extincion-de-condominio-por-divorcio":("A half-empty wardrobe in a bedroom of a Spanish flat, one side with hangers and clothes, the other empty, soft light.","Armario de un dormitorio medio vacío"),
"vender-o-hacer-extincion-de-condominio":("A fork in a quiet residential street in a Spanish town, two paths between whitewashed houses, morning light.","Bifurcación en una calle de casas blancas en un pueblo español"),
"que-significa-proindiviso-en-una-escritura":("Close-up of an old Spanish property deed with a magnifying glass resting on the text, vintage paper texture, no readable letters.","Escritura antigua con una lupa encima"),
"proindiviso-ventajas-y-desventajas":("A balance scale on a wooden desk with a small house model on one side and a stack of coins on the other, Spanish office.","Balanza con una casa en miniatura y monedas"),
"proindiviso-condominio-comunidad-de-bienes-diferencias":("Three different brass keys hanging on hooks on a white wall, minimal composition, soft shadows.","Tres llaves distintas colgadas en una pared blanca"),
"proindiviso-codigo-civil":("A leather-bound legal code book open on a desk with a fountain pen and reading glasses, warm library light, no readable text.","Libro de leyes abierto con gafas y pluma"),
"como-se-calcula-la-cuota-de-un-proindiviso":("A pie-shaped wooden house puzzle split into four pieces on a table, one piece pulled apart, daylight.","Casa de madera dividida en cuatro piezas, una separada"),
"riesgos-de-un-proindiviso":("A weathered apartment building facade in Spain with cracked plaster and one balcony full of plants, dramatic late light.","Fachada de un edificio con grietas y un balcón con plantas"),
"merece-la-pena-comprar-un-proindiviso":("An investor's desk with a laptop showing a blurred chart, a notebook and house keys, Spanish apartment with balcony behind.","Escritorio con portátil, cuaderno y llaves de un piso"),
"abogado-proindiviso-cuando-hace-falta":("A lawyer's office in Spain: leather chair, wooden desk with a legal folder and a brass desk lamp, blurred bookshelves.","Despacho de abogado con carpeta y lámpara de latón"),
"subasta-division-de-cosa-comun":("A wooden gavel resting on a desk inside a Spanish courthouse, marble floor and tall windows in the background.","Mazo de madera sobre una mesa en un juzgado"),
"se-puede-obligar-a-vender-a-un-copropietario":("Exterior of a Spanish civil courthouse with stone columns and steps, blue sky, no people.","Fachada de un juzgado con columnas de piedra"),
"derecho-de-tanteo-y-retracto-entre-copropietarios":("A wall calendar with nine days marked by small pins, next to house keys on a desk, no readable numbers.","Calendario con nueve días marcados junto a unas llaves"),
"vender-la-mitad-de-una-casa":("A detached Spanish house photographed from the street, half in sunlight and half in shade, clean sky.","Casa unifamiliar mitad al sol y mitad a la sombra"),
"vender-nuda-propiedad":("An elderly person's hands resting on a cane in a sunlit Spanish living room with a rocking chair, no face visible.","Manos de una persona mayor apoyadas en un bastón en su salón"),
"vender-terreno-proindiviso":("A rural plot of land in Spain with olive trees and a stone boundary wall under a clear sky, late afternoon.","Finca rústica con olivos y muro de piedra"),
"vender-proindiviso-con-inquilino-u-okupa":("Front door of a Spanish apartment with a rental agreement folder on the doormat and keys in the lock, hallway light.","Puerta de un piso con una carpeta de contrato y llaves en la cerradura"),
"vender-tu-parte-de-la-casa-a-tu-pareja":("A kitchen counter in a Spanish flat with two coffee cups, one full and one empty, morning light through the window.","Dos tazas de café en la encimera, una llena y otra vacía"),
"uno-quiere-vender-y-el-otro-no":("A 'for sale' style blank sign post without text in front of a Spanish apartment block, one balcony closed, one open.","Cartel sin texto frente a un bloque de pisos"),
"como-salir-de-una-propiedad-compartida":("An open front door of a Spanish flat leading to a bright staircase, keys left on the inside console table.","Puerta abierta de un piso con las llaves sobre la consola"),
"embargo-de-una-cuota-de-proindiviso":("A stack of official envelopes and a padlock on a dark wooden desk, dramatic side light, Spanish office.","Sobres oficiales y un candado sobre un escritorio"),
"donar-mi-parte-de-un-proindiviso":("A gift-wrapped small box with a house key tied to the ribbon, placed on a Spanish living room table.","Caja de regalo con una llave de casa atada al lazo"),
"soy-copropietario-y-quiero-vender":("A checklist notebook, a pen and house keys on a tidy desk, bright Spanish apartment, minimal composition.","Cuaderno con lista, bolígrafo y llaves sobre un escritorio"),
"urge-vender-por-herencia":("An hourglass next to a brass house key on a wooden table, warm window light, Spanish interior.","Reloj de arena junto a una llave de casa"),
"que-hacen-las-empresas-que-compran-proindivisos":("A modern Spanish office meeting table with a property folder, a tablet and two glasses of water, city view through the window.","Mesa de reuniones con una carpeta inmobiliaria y una tablet"),
"mi-hermano-vive-en-la-casa-de-mis-padres-y-no-quiere-vender":("The facade of parents' house in a Spanish town with one lit window at dusk, the rest dark.","Casa de los padres al atardecer con una sola ventana iluminada"),
"puedo-vender-la-casa-de-mi-madre-con-usufructo":("A cosy armchair by a window in an elderly woman's Spanish living room, knitted blanket, afternoon sun, no people.","Sillón junto a la ventana en el salón de una casa familiar"),
"piso-heredado-con-hipoteca-vender-mi-parte":("A mortgage statement folder and house keys on a kitchen table of an older Spanish flat, soft light.","Carpeta de hipoteca y llaves sobre la mesa de un piso heredado"),
"vender-casa-heredada-sin-testamento":("An empty document tray and a closed folder on a notary desk, a window with Spanish rooftops behind.","Bandeja vacía y carpeta cerrada sobre la mesa de un notario"),
"herencia-yacente-vender-antes-de-la-particion":("A closed inherited apartment with furniture under sheets and mail piled behind the door, dim light.","Piso heredado cerrado con muebles tapados y correo acumulado"),
"heredero-ilocalizable-o-en-el-extranjero":("A world map on a wall with a single pin, a brass key on the desk below, Spanish study room.","Mapamundi con una chincheta y una llave sobre el escritorio"),
"heredero-menor-o-incapacitado-venta-de-la-casa":("A child's small shoes and an adult's shoes at the doorway of a Spanish family home, warm light, no people.","Zapatos de niño y de adulto en la entrada de una casa familiar"),
"cuanto-tarda-vender-un-proindiviso":("A desk calendar with several weeks visible, a pen and house keys, bright Spanish office, no readable numbers.","Calendario de mesa con varias semanas, bolígrafo y llaves"),
"documentos-para-vender-tu-parte-de-un-piso":("A neat stack of property documents, a folder and an ID card holder on a desk, no readable text, soft daylight.","Documentos de la vivienda apilados sobre un escritorio"),
"nota-simple-como-pedirla-y-leerla":("A laptop open on a desk next to a printed property registry document and reading glasses, no readable text.","Portátil junto a un documento del Registro impreso y unas gafas"),
"valor-de-referencia-catastral-venta-de-tu-parte":("Aerial view of a Spanish neighbourhood with apartment blocks and streets forming a grid, golden hour.","Vista aérea de un barrio español con bloques de pisos"),
"vender-parte-de-un-garaje-trastero-o-local-heredado":("An underground parking space in a Spanish building with a numbered-style blank plate and a closed storage room door.","Plaza de garaje y puerta de trastero en un sótano"),
"vender-parte-de-una-vpo":("A modern social housing block in Spain with colourful balconies and a courtyard, clear sky.","Bloque de vivienda protegida con balcones de colores"),
"cuanto-me-dan-por-mi-parte-de-un-piso":("A calculator and a small wooden house model on a table in a Spanish apartment, balcony light.","Calculadora y casa de madera en miniatura sobre una mesa"),
"pacto-de-indivision-que-es-y-cuanto-dura":("A chain and padlock around the handles of a double wooden door in a Spanish building, daylight.","Cadena y candado en una puerta doble de madera"),
"comunidad-hereditaria-vs-proindiviso":("Two folders side by side on a desk, one old and worn, one new, with a brass key between them.","Dos carpetas, una antigua y otra nueva, con una llave entre ambas"),
"compensacion-por-uso-exclusivo-de-la-vivienda-comun":("A lived-in Spanish living room with a sofa, plants and a lit lamp, seen from the hallway, evening.","Salón habitado visto desde el pasillo, lámpara encendida"),
"ibi-y-gastos-en-un-proindiviso-quien-paga":("A pile of utility and tax bills with a calculator on a Spanish kitchen table, no readable text.","Facturas y recibos con una calculadora sobre la mesa"),
"alquilar-un-piso-en-proindiviso":("A bright empty Spanish flat ready to rent, parquet floor, open balcony door and a key on the windowsill.","Piso vacío listo para alquilar con la llave en el alféizar"),
"vender-proindiviso-a-un-familiar-o-a-una-empresa":("A family dining table and a modern office desk shown in a split composition, Spanish interiors, soft light.","Mesa familiar y escritorio de oficina en composición dividida"),
"vender-parte-de-un-garaje-o-trastero":("A row of closed garage doors in a Spanish residential building, one slightly open with light inside.","Puertas de garaje cerradas, una entreabierta"),
"vender-parte-de-un-terreno-rustico-heredado":("Rows of vineyard and an old stone shed on a rural Spanish plot, late afternoon light.","Viñedo y caseta de piedra en una finca rústica"),
"proindiviso-por-divorcio-sin-acuerdo":("A living room of a Spanish flat with a single sofa and a blank space where furniture used to be, afternoon light.","Salón con un sofá y un hueco donde había muebles"),
"testamento-con-usufructo-universal-puede-vender-el-viudo":("An elderly man's hands holding a wedding ring and a house key at a kitchen table, no face visible.","Manos de una persona mayor con una alianza y una llave"),
"que-es-una-cuota-hereditaria":("A pie chart drawn in chalk on a slate board next to a brass key, Spanish kitchen, no readable text.","Gráfico circular dibujado en una pizarra junto a una llave"),
"vender-casa-con-deudas-o-embargo-mi-parte":("A Spanish house facade with a padlocked gate and overgrown garden, overcast soft light.","Casa con la verja candada y el jardín descuidado"),
"multipropiedad-como-vender":("A coastal holiday apartment complex in Spain with palm trees and pool, off-season, empty balconies.","Complejo de apartamentos vacacionales en la costa, fuera de temporada"),
"preguntas-antes-de-vender-tu-parte":("A notebook full of blank question marks drawn in pencil next to a coffee cup and house keys, Spanish table.","Cuaderno con signos de interrogación, café y llaves"),
}
ids=json.load(open(f'{REPO}/blog/ids.json'))
S=[]
for f in sorted(glob.glob(f'{REPO}/blog/blog_[0-9].json')): S+=json.load(open(f))
for s in S:
    sc,alt=BLOG[s['slug']]
    add(s['slug'], s['kind'], ids[s['slug']], s['slug'][:60]+'.webp', sc, alt, s['title_corto'])

# ---------- Intention pages ----------
INT={
25:("empresas-que-compran-proindivisos","A bright modern office desk in Spain with a property folder, a brass key and a glass of water, city rooftops behind the window.","Mesa de oficina con carpeta inmobiliaria y llave, tejados de una ciudad española al fondo","Empresas que compran proindivisos"),
27:("cuanto-pagan-por-un-proindiviso","A calculator, a stack of euro coins and a small wooden house model on a wooden table, soft daylight.","Calculadora, monedas y casa en miniatura sobre una mesa","Cuánto pagan"),
29:("vender-proindiviso-sin-avisar","A closed wooden door of a Spanish flat with a key turning in the lock, warm hallway light, no people.","Llave girando en la cerradura de un piso","Vender sin avisar"),
31:("vender-parte-casa-heredada","Interior of an inherited Spanish village house with old tiles, a wooden sideboard and light through lace curtains.","Interior de una casa de pueblo heredada con baldosas antiguas","Parte de casa heredada"),
33:("opiniones-empresas-que-compran-proindivisos","Two coffee cups and a signed folder on a cafe table in Spain, out-of-focus street, no faces.","Dos cafés y una carpeta firmada en la mesa de una cafetería","Opiniones"),
35:("vender-parte-de-un-piso","A bright Spanish apartment living room with a balcony, half the room lit by sun and half in shade.","Salón de un piso con balcón, mitad al sol y mitad en sombra","Vender parte de un piso"),
37:("vender-proindiviso-con-hipoteca","A mortgage folder, a pen and house keys on a bank desk, blurred modern office in Spain.","Carpeta de hipoteca, bolígrafo y llaves sobre la mesa de un banco","Con hipoteca"),
39:("vender-proindiviso-divorcio","Two wedding rings and two house keys on a wooden table, soft side light, Spanish interior.","Dos alianzas y dos llaves sobre una mesa","Divorcio"),
41:("vender-proindiviso-entre-hermanos","Facade of an old Spanish family home with several balconies and closed shutters, golden light.","Fachada de una casa familiar con varios balcones","Entre hermanos"),
43:("extincion-de-condominio","Close-up of hands signing a deed with a fountain pen on a notary desk in Spain, no faces.","Firma de una escritura con pluma en la notaría","Extinción de condominio"),
45:("extincion-de-condominio-entre-hermanos","Two identical front doors side by side in a Spanish semi-detached house, warm evening light.","Dos puertas iguales de una casa pareada","Entre hermanos"),
47:("extincion-de-condominio-hipoteca","A bank building entrance in Spain with glass doors and stone facade, no readable signs.","Entrada de un banco con fachada de piedra","Con hipoteca"),
49:("extincion-de-condominio-impuestos-y-notario","Tax forms, a calculator and a notary stamp on a desk, warm lamp light, no readable text.","Impresos de impuestos, calculadora y sello sobre un escritorio","Impuestos y notario"),
51:("que-es-un-proindiviso","Facade of a classic Spanish apartment building with many balconies, each slightly different, blue sky.","Fachada de un edificio de pisos con balcones distintos","Qué es un proindiviso"),
53:("division-de-cosa-comun","Interior corridor of a Spanish courthouse with marble floor, wooden benches and tall windows, no people.","Pasillo de un juzgado con bancos de madera","División de cosa común"),
55:("vender-proindiviso-espana","Aerial view of a Spanish city at golden hour with terracotta rooftops, a cathedral dome and distant mountains.","Vista aérea de tejados de una ciudad española al atardecer","Dónde compramos"),
57:("contacto-zona-proindiviso","A smartphone, a notebook and a cup of coffee on a bright Spanish desk by a window, no readable screen.","Móvil, cuaderno y café sobre un escritorio luminoso","Contacto"),
680:("blog-zona-proindiviso","Reading glasses, a stack of legal guides and a cup of coffee on a wooden desk, Spanish apartment, morning light.","Gafas, guías y café sobre un escritorio de madera","Blog"),
}
for pid,(fn,sc,alt,title) in INT.items():
    add(fn,'page',pid,fn+'.webp',sc,alt,title)

# ---------- CCAA (19) ----------
CCAA={
"andalucia":("A whitewashed Andalusian village street with terracotta roofs, flower pots on the walls and a church tower, bright sun.","Calle de un pueblo blanco andaluz con macetas y tejados de teja","Andalucía"),
"aragon":("Brick Mudejar-style facades and a riverside promenade in Zaragoza with the Ebro reflecting the evening sky.","Fachadas de ladrillo mudéjar junto al Ebro en Zaragoza","Aragón"),
"asturias":("Traditional Asturian stone houses with wooden galleries and a raised granary among green hills, misty morning.","Casas de piedra asturianas con hórreo entre colinas verdes","Asturias"),
"baleares":("Mallorcan sandstone townhouses with green shutters on a narrow street, Mediterranean light.","Casas de piedra de Mallorca con persianas verdes","Baleares"),
"canarias":("Colourful colonial facades with carved wooden balconies on a Canary Islands street, volcanic hills behind.","Fachadas de colores con balcones de madera en Canarias","Canarias"),
"cantabria":("Houses with glazed white balconies overlooking the bay of Santander, soft Atlantic light.","Casas con miradores blancos frente a la bahía de Santander","Cantabria"),
"castilla-la-mancha":("A La Mancha plain with white windmills on a hill and a small village below, warm evening light.","Molinos blancos sobre la llanura manchega con un pueblo al fondo","Castilla-La Mancha"),
"castilla-y-leon":("Stone and adobe houses of a Castilian village with a Romanesque church, golden wheat fields around.","Casas de piedra y adobe en un pueblo castellano con iglesia románica","Castilla y León"),
"cataluna":("Modernist Eixample apartment facades in Barcelona with ornate balconies and chamfered corners, morning light.","Fachadas modernistas del Eixample de Barcelona","Cataluña"),
"comunidad-valenciana":("Mediterranean apartment blocks near the beach with palm trees and orange trees, Valencia coast, clear sky.","Bloques de pisos junto a la playa con palmeras en la costa valenciana","Comunidad Valenciana"),
"extremadura":("A dehesa landscape with holm oaks and a stone farmhouse in Extremadura, soft afternoon light.","Dehesa extremeña con encinas y un cortijo de piedra","Extremadura"),
"galicia":("Granite houses with white glazed galleries in a Galician coastal town, green hills and grey-blue sea.","Casas de granito con galerías blancas en un pueblo gallego","Galicia"),
"madrid":("Classic brick residential buildings with wrought-iron balconies in a Madrid neighbourhood, late afternoon.","Edificios de ladrillo con balcones de forja en un barrio de Madrid","Madrid"),
"murcia":("Apartment buildings and palm trees around a Murcian plaza with the huerta and mountains in the distance.","Bloques de pisos y palmeras en una plaza de Murcia","Murcia"),
"navarra":("Stone houses with wide wooden eaves and red shutters in a Navarrese town, Pyrenean foothills behind.","Casas de piedra con aleros de madera en un pueblo navarro","Navarra"),
"pais-vasco":("A Basque farmhouse with white walls and red timber on a green hillside, and a town with glazed balconies below.","Caserío vasco entre colinas verdes","País Vasco"),
"la-rioja":("Vineyards in autumn colours around a stone village with a church tower in La Rioja.","Viñedos en otoño alrededor de un pueblo de La Rioja","La Rioja"),
"ceuta":("White Mediterranean buildings and a seaside promenade in Ceuta with the strait and a hill in the background.","Edificios blancos y paseo marítimo de Ceuta frente al Estrecho","Ceuta"),
"melilla":("Modernist white and pastel facades on a sunny street in Melilla, palm trees and blue sky.","Fachadas modernistas de Melilla con palmeras","Melilla"),
}
gids=json.load(open(f'{REPO}/geo/ids.json'))
for slug,(sc,alt,title) in CCAA.items():
    add('ccaa-'+slug,'page',gids[slug],'vender-proindiviso-'+slug+'.webp',sc,alt+', donde compramos proindivisos',f'Vender proindiviso en {title}')

json.dump(items,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'manifest.json'),'w'),ensure_ascii=False,indent=1)
print(len(items),'imágenes en el manifiesto')
