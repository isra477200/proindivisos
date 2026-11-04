# Keyphrase, título SEO (≤ 60 caracteres, empieza por la keyphrase) y meta description (≤ 156, con todas las palabras de la keyphrase)
# de las páginas de intención, hub geo, contacto y blog. pagebuilder.build() lee KW para el overline y el título del FAQ.
M={
23:("vender proindiviso","Vender proindiviso: oferta por escrito en 48 h, sin agencias","Vender proindiviso sin esperar a los demás: compramos tu parte de piso, casa o terreno con fondos propios. Oferta por escrito en 48 h, gastos a nuestro cargo."),
25:("empresas que compran proindivisos","Empresas que compran proindivisos: cómo elegir bien","Empresas que compran proindivisos: qué hacen, qué pagan y qué preguntar antes de vender. Así compramos nosotros: oferta en 48 h y gastos a nuestro cargo."),
27:("cuánto pagan por un proindiviso","Cuánto pagan por un proindiviso: precio real en 2026","Cuánto pagan por un proindiviso: entre el 40 % y el 70 % del valor de tu parte según zona, ocupación y cargas. Pide tu oferta por escrito en 48 h."),
29:("vender proindiviso sin avisar","Vender proindiviso sin avisar a los demás: qué dice la ley","Vender tu proindiviso sin avisar a los otros propietarios es legal: ellos tienen derecho de retracto. Te explicamos cómo hacerlo bien y te lo compramos."),
31:("vender parte de una casa heredada","Vender tu parte de una casa heredada sin acuerdo","Vender tu parte de una casa heredada aunque tus hermanos no quieran: compramos tu cuota con fondos propios. Oferta por escrito en 48 h y firma en notaría."),
33:("opiniones empresas que compran proindivisos","Opiniones sobre empresas que compran proindivisos","Opiniones sobre empresas que compran proindivisos: de qué se quejan quienes vendieron, las seis preguntas que debes hacer y cómo las respondemos nosotros."),
35:("vender parte de un piso","Vender tu parte de un piso aunque el otro no quiera","Vender tu parte de un piso cuando el otro propietario no quiere: las tres vías que existen y cómo compramos tu cuota. Precio en 48 h y firma en semanas."),
37:("vender proindiviso con hipoteca","Vender un proindiviso con hipoteca: así funciona","Vender un proindiviso con hipoteca es posible. Qué pasa con la deuda, qué hace el banco y cómo compramos tu parte cancelando tu tramo en la firma."),
39:("vender parte de la casa tras un divorcio","Vender tu parte de la casa tras un divorcio sin juicio","Vender tu parte de la casa tras un divorcio sin pasar por juicio: si no hay acuerdo, compramos tu mitad. Oferta en 48 h y con discreción."),
41:("vender piso heredado entre hermanos","Vender piso heredado entre hermanos sin acuerdo","Vender tu parte de un piso heredado entre hermanos cuando uno no quiere: tus derechos y cómo compramos tu cuota sin pelea. Precio en 48 h."),
43:("extinción de condominio","Extinción de condominio: pasos, coste y alternativas","Extinción de condominio: qué es, requisitos, pasos, impuestos y ejemplo con cifras. Y si no hay acuerdo o nadie puede pagar la parte del otro, la compramos."),
45:("extinción de condominio entre hermanos","Extinción de condominio entre hermanos: guía práctica","Cómo hacer la extinción de condominio entre hermanos con o sin compensación, con usufructo de los padres, qué cuesta y qué hacer si uno no firma."),
47:("extinción de condominio con hipoteca","Extinción de condominio con hipoteca: qué pide el banco","Extinción de condominio con hipoteca: la escritura no te saca del préstamo. Novación frente a subrogación y qué hacer si el banco deniega la operación."),
49:("impuestos extinción de condominio","Impuestos y notario de la extinción de condominio 2026","Impuestos de la extinción de condominio: AJD por comunidad, plusvalía, IRPF e ITP, notaría y registro, con un ejemplo con cifras. Y cuándo compensa vender."),
51:("qué es un proindiviso","Qué es un proindiviso: definición, derechos y salidas","Qué es un proindiviso: una propiedad compartida sin dividir. Qué puedes hacer con tu cuota sin permiso de nadie y cómo salir: extinción, venta o juicio."),
53:("división de cosa común","División de cosa común: juicio, plazos y coste","El juicio de división de cosa común acaba en subasta y tarda de uno a tres años. Fases, costes reales y la alternativa: vender tu cuota en semanas."),
55:("vender proindiviso en toda España","Vender proindiviso en toda España: por provincias","Vender proindiviso en toda España: compramos tu parte en las 50 provincias, Canarias, Baleares, Ceuta y Melilla. Oferta por escrito en 48 h."),
57:("precio por tu proindiviso","Precio por tu proindiviso en 48 h: cuéntanos tu caso","Pide precio por tu proindiviso: llámanos, escríbenos por WhatsApp o deja tu teléfono y te llamamos. Compramos en toda España, oferta por escrito en 48 h."),
680:("blog proindiviso","Blog Zona Proindiviso: guías para vender tu parte","Blog de Zona Proindiviso: herencias, extinción de condominio, división de cosa común, impuestos y copropiedad explicados con cifras. Y la salida rápida."),
}
KW={k:v[0] for k,v in M.items()}
if __name__=='__main__':
    for k,(kw,yt,yd) in M.items(): print(k,len(yt),len(yd),'OK' if len(yt)<=60 and 120<=len(yd)<=156 else 'REVISAR',kw)
