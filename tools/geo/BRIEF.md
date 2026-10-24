# Brief: contenido local para páginas geo de zonaproindiviso.com

Empresa: Zona Proindiviso. COMPRAMOS proindivisos (cuotas indivisas de pisos, casas, locales, garajes, terrenos) con fondos propios en toda España. NO somos intermediarios ni captadores. Promesa: oferta por escrito en 48 h, firma en notaría en 2-4 semanas, pago al contado en notaría, gastos de notaría y gestión a nuestro cargo, sin exclusividad, sin compromiso. Pagamos entre el 40 % y el 70 % del valor proporcional de la cuota.

Estilo: español de España, directo, frases cortas, segunda persona (tú). Sin emojis, sin guiones largos (—), sin paréntesis excesivos. Nada de relleno. Cada texto debe ser ÚNICO y específico del lugar: hechos locales reales (comarcas, barrios, municipios, tipo de parque de viviendas, perfil de herencias, costa/turismo, emigración, segunda residencia, pisos de los años 60-70, cascos antiguos, etc.). Prohibido texto genérico que valdría para cualquier ciudad. No inventes cifras precisas: población y €/m² orientativos en redondeo ("unos 1.900 €/m²", "cerca de 700.000 habitantes") y marcados como orientativos. No cites números de Registros de la Propiedad ni nombres de notarías concretas. Sí puedes citar el nombre de la Hacienda autonómica (ATRIGA, ATC, Agencia Tributaria de Andalucía, ATIB, Hacienda Foral de Bizkaia/Gipuzkoa/Álava, Hacienda Foral de Navarra, Dirección General de Tributos de Madrid, ATV (Agència Tributària Valenciana)...), el tipo de AJD vigente orientativo de la CCAA y que la plusvalía municipal la fija cada ayuntamiento.

Jerarquía de URL: /vender-proindiviso/{ccaa}/{provincia}/{ciudad}/. CCAA uniprovinciales (madrid, murcia, asturias, cantabria, navarra, la-rioja, baleares): una sola página hace de CCAA + provincia + capital; sus ciudades cuelgan directamente de ella. Cuando la capital se llama como la provincia (sevilla, valencia, zaragoza...), la página de provincia es también la de la capital: su texto debe cubrir ciudad capital Y provincia.

Entrega: un único fichero JSON (lista de objetos) con EXACTAMENTE este esquema por lugar:
{
 "slug": "sevilla",
 "nombre": "Sevilla",
 "tipo": "ccaa" | "provincia" | "ciudad",
 "padre": "andalucia"  (slug del padre; para ccaa: null; para ciudad de CCAA uniprovincial: el slug de la CCAA),
 "en": "en Sevilla"  (forma con preposición: "en la provincia de Cádiz", "en Madrid", "en la Comunidad Valenciana", "en Las Palmas de Gran Canaria"),
 "poblacion": "cerca de 1,9 millones de habitantes en la provincia y unos 680.000 en la capital" (texto orientativo),
 "precio_m2": "unos 2.300 €/m² en la capital (orientativo, 2026)",
 "zonas": ["Triana", "Nervión", "Los Remedios", "Macarena", "Sevilla Este", "Dos Hermanas", "Alcalá de Guadaíra", "Utrera", "Écija", "Carmona"]  (8-14 barrios/comarcas/municipios reales y relevantes),
 "municipios": ["Dos Hermanas", "Alcalá de Guadaíra", ...]  (para ccaa/provincia: 14-25 municipios reales de la provincia ordenados por población; para ciudad: 8-14 barrios o distritos reales),
 "mercado": "2-3 frases únicas sobre el parque de viviendas y el tipo de proindiviso habitual aquí, con el €/m² orientativo integrado.",
 "angulo": "3-5 frases únicas: por qué surgen proindivisos en este lugar (herencias de pueblos de la provincia, pisos de los 70 en barrios obreros, segundas residencias en la costa, emigración, divorcios, viviendas de protección, parcelas rústicas...), con nombres de lugares reales.",
 "tramites": "2-3 frases: Registro de la Propiedad de la ciudad o ciudades (sin números), Hacienda autonómica a la que se liquida el AJD/ITP y tipo orientativo, plusvalía municipal del ayuntamiento, cualquier particularidad (derecho foral, valor de referencia, etc.).",
 "faq": [["Pregunta local 1", "Respuesta 2-4 frases, específica del lugar"], ["Pregunta 2", "..."], ["Pregunta 3", "..."]]  (3 preguntas que un vecino de ese lugar haría de verdad; al menos una sobre precio local, una sobre herencias o un caso típico local, una sobre trámites o cobertura de municipios),
 "kw": ["proindivisos sevilla", "vender proindiviso sevilla", "empresas que compran proindivisos en sevilla"]
}

Reglas: los textos de "mercado", "angulo", "tramites" y "faq" NO pueden repetirse ni parafrasearse entre lugares. Entre 250 y 350 palabras de texto propio por lugar sumando esos campos. Escribe siempre desde la posición de comprador ("compramos", "te damos precio", "firmamos contigo"). Hechos verificables y prudentes; si no estás seguro de un dato, omítelo.
