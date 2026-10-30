# Arquitectura de URLs — zonaproindiviso.com (fase 2, 23/10/2026)

Base: términos observados en las 8 cuentas de proindivisos del MCC (`investigacion-cuentas-proindivisos.md`) y volumen nacional del Keyword Planner (`investigacion-keyword-planner.md`). Objetivo de cada URL: captar el lead (formulario, WhatsApp o llamada). Ninguna página es "solo informativa".

## 1. Principios

1. **Una intención, una URL.** Cada página ataca un cluster de keywords; no se crean dos páginas para el mismo cluster.
2. **Transaccional primero.** Las keywords que convierten en campañas (empresas que compran proindivisos, vender proindiviso, sin avisar, herencia, cuánto pagan) son las páginas de nivel 1 y van enlazadas desde todas las demás.
3. **El hub de condominio capta, no enseña.** Cada página de extinción de condominio responde a la duda en 300-500 palabras y a continuación plantea la alternativa: "si no hay acuerdo o no quieres pagar, vende tu parte".
4. **Geo por jerarquía de páginas WordPress:** `/vender-proindiviso/{ccaa}/{provincia}/{ciudad}/`. Cuando CCAA = provincia (Madrid, Murcia, Asturias, Cantabria, Navarra, La Rioja, Baleares) hay **una sola página**. Cuando la capital se llama como la provincia, la página de provincia es también la de la capital (no se duplica).
5. **Nada se publica vacío.** Una página geo sin su bloque de datos locales se queda en borrador.

## 2. Nivel 1 — Transaccional (prioridad máxima)

| URL | Keyword principal (vol./mes ES) | Cluster | Title (≤60) | H1 | Meta description |
|---|---|---|---|---|---|
| `/` | vender proindiviso (390) | venta proindiviso 320, venta de proindiviso 170, compra proindiviso 390, vender mi proindiviso 40 | Vender proindiviso: ofertas de empresas compradoras · Zona Proindiviso | Vende tu proindiviso sin esperar al acuerdo de los demás | ¿Tienes una parte de un piso o casa y quieres venderla? Te ponemos en contacto con empresas que compran proindivisos en toda España. Oferta en 48 h, sin compromiso. |
| `/empresas-que-compran-proindivisos/` | empresas que compran proindivisos (320) | mejores empresas que compran proindivisos 260, compradores proindivisos 390, empresas proindiviso 50, qué hacen las empresas que compran proindivisos | Empresas que compran proindivisos en España: cómo elegir · Zona Proindiviso | Empresas que compran proindivisos: recibe varias ofertas y elige | Comparamos por ti las empresas que compran proindivisos. Recibe ofertas de varias compradoras, sin exclusividad y sin coste. Cuéntanos tu caso. |
| `/cuanto-pagan-por-un-proindiviso/` | cuánto pagan las empresas que compran proindivisos (210) | valor vivienda extinción de condominio 140, cuánto vale mi parte | ¿Cuánto pagan por un proindiviso? Precio real en 2026 · Zona Proindiviso | Cuánto pagan las empresas por un proindiviso | Las empresas pagan entre el 40 % y el 70 % del valor de tu parte, según el caso. Calcula cuánto puedes recibir y pide ofertas reales sin compromiso. |
| `/vender-proindiviso-sin-avisar/` | vender proindiviso sin avisar (320) | se puede vender una propiedad si un heredero no quiere 210, vender mi parte sin consentimiento | Vender tu proindiviso sin avisar: qué dice la ley · Zona Proindiviso | ¿Puedes vender tu proindiviso sin avisar a los demás? | Puedes vender tu parte sin el permiso de los otros propietarios, pero tienen derecho de retracto. Te explicamos cómo hacerlo bien y te buscamos comprador. |
| `/vender-parte-casa-heredada/` | puedo vender mi parte de una casa heredada (320) | proindiviso herencia 170, empresas que compran herencias 210, vender mi parte de la herencia a otro heredero 140, venta proindiviso herencia 70, vender un piso heredado 110 | Vender tu parte de una casa heredada sin acuerdo · Zona Proindiviso | Vende tu parte de la herencia aunque los demás no quieran | Si has heredado una parte de un piso y tus hermanos no quieren vender, puedes vender tu parte a una empresa compradora. Oferta en 48 h. |
| `/opiniones-empresas-que-compran-proindivisos/` | opiniones sobre empresas que compran proindivisos (170) | vender proindiviso opiniones 140, experiencias venta proindiviso | Opiniones sobre empresas que compran proindivisos: qué mirar · Zona Proindiviso | Opiniones sobre empresas que compran proindivisos: lo que nadie te cuenta | Antes de vender tu proindiviso, mira esto: cómo trabajan estas empresas, qué descuentos aplican y qué señales de alarma evitar. Luego pide varias ofertas. |
| `/vender-parte-de-un-piso/` | vender parte de un piso (40) | vender mi parte de un piso, vender parte de una vivienda, vender la mitad de un piso 20, vender mi parte de una propiedad 40 | Vender tu parte de un piso: guía y compradores · Zona Proindiviso | Vende tu parte de un piso aunque el otro propietario no quiera | Tienes el 50 % o menos de un piso y quieres salir. Te explicamos las tres vías y te conseguimos ofertas de compra por tu parte. |

## 3. Nivel 2 — Situaciones (captan por contexto)

| URL | Keyword principal | Notas |
|---|---|---|
| `/vender-proindiviso-con-hipoteca/` | proindiviso con hipoteca (10) + se puede vender la mitad de una casa hipotecada (20) | Poco volumen, pero objeción nº 1 en la llamada. Enlaza con `/extincion-de-condominio/hipoteca/`. |
| `/vender-proindiviso-divorcio/` | condominio divorcio (50), extinción de condominio divorcio (30) | Segunda situación más frecuente tras la herencia. |
| `/vender-proindiviso-entre-hermanos/` | vender piso heredado hermanos (30), puedo vender mi parte de la herencia a mi hermano (40) | Puente entre herencia y hub de condominio. |
| `/vender-proindiviso-con-inquilino-u-okupa/` | sin volumen medible | Se crea solo por conversión (es un caso real que llega a las compradoras). Prioridad baja. |

## 4. Nivel 3 — Hub "extinción de condominio" y qué es (captación por volumen)

| URL | Keyword principal (vol.) | Cluster | Ángulo de captación |
|---|---|---|---|
| `/extincion-de-condominio/` | extinción de condominio (8.100) | extincion condominio 880, disolución de condominio 720, qué es 590, extincion de proindiviso 110 | Explica el procedimiento en 5 pasos y el coste real. Bloque "¿Y si no hay acuerdo o no puedes pagar la parte del otro? Vende la tuya". |
| `/extincion-de-condominio/entre-hermanos/` | extinción de condominio entre hermanos (880 + 880) | con/sin compensación 170 + 140, disolución entre hermanos 90 | Caso herencia. CTA a `/vender-parte-casa-heredada/`. |
| `/extincion-de-condominio/hipoteca/` | extinción de condominio hipoteca (390) | hipoteca para extinción 50, subrogación | El banco no siempre acepta: alternativa, vender la parte. |
| `/extincion-de-condominio/impuestos-y-notario/` | extincion de condominio impuestos (390) | precio notario 170, gastos 70, AJD/ITP | Coste total realista vs vender la parte sin gastos. |
| `/que-es-un-proindiviso/` | proindiviso (3.600) | proindiviso que es 2.400, que significa 480, pro indivisa 720, ventajas y desventajas 170 | Definición clara + "las 3 salidas de un proindiviso" con CTA. |
| `/division-de-cosa-comun/` | división de cosa común (170) | procedimiento 70, minuta abogado 70, subasta | Vía judicial: lenta, cara, subasta a la baja. Alternativa: vender la parte ahora. |

## 5. Nivel 4 — Geo

Patrón: `/vender-proindiviso/{ccaa}/{provincia}/{ciudad}/`. Keyword de cada página: "vender proindiviso en {lugar}" + "empresas que compran proindivisos en {lugar}" (observadas en campañas: "proindivisos madrid" 77 clics, "empresas que compran proindivisos madrid" 42, "compra de proindivisos madrid" 40).

**Orden de publicación por demanda (Planner, suma de 30 semillas/mes):** Madrid 3.990 · Barcelona 1.450 · Valencia 950 · Sevilla 830 · Málaga 760 · Alicante 670 · Bizkaia 550 · Cádiz 520 · Las Palmas 500 · Murcia 460 · Pontevedra 460 · A Coruña 430 · Castellón 430 · Baleares 430 · resto.

### 5.1 Comunidades (17 + Ceuta y Melilla)
andalucia · aragon · asturias* · baleares* · canarias · cantabria* · castilla-la-mancha · castilla-y-leon · cataluna · comunidad-valenciana · extremadura · galicia · madrid* · murcia* · navarra* · pais-vasco · la-rioja* · ceuta · melilla
(* uniprovincial: una sola página que hace de CCAA + provincia + capital.)

### 5.2 Provincias (50) — slug y CCAA
| CCAA | Provincias (slug) |
|---|---|
| andalucia | almeria, cadiz, cordoba, granada, huelva, jaen, malaga, sevilla |
| aragon | huesca, teruel, zaragoza |
| canarias | las-palmas, santa-cruz-de-tenerife |
| castilla-la-mancha | albacete, ciudad-real, cuenca, guadalajara, toledo |
| castilla-y-leon | avila, burgos, leon, palencia, salamanca, segovia, soria, valladolid, zamora |
| cataluna | barcelona, girona, lleida, tarragona |
| comunidad-valenciana | alicante, castellon, valencia |
| extremadura | badajoz, caceres |
| galicia | a-coruna, lugo, ourense, pontevedra |
| pais-vasco | alava, bizkaia, gipuzkoa |
| uniprovinciales | madrid, murcia, asturias, cantabria, navarra, la-rioja, baleares |

### 5.3 Ciudades (ampliado el 23/10 a 56, solo si su nombre no coincide con la provincia)
bilbao, barakaldo, getxo (bizkaia) · palma (baleares) · telde (las-palmas) · san-cristobal-de-la-laguna (santa-cruz-de-tenerife) · mijas, fuengirola, torremolinos, velez-malaga (malaga) · san-fernando, el-puerto-de-santa-maria, chiclana-de-la-frontera (cadiz) · merida (badajoz) · lorca (murcia) · mataro, santa-coloma-de-gramenet, cornella-de-llobregat (barcelona) · reus (tarragona) · orihuela, benidorm (alicante) · torrent, gandia (valencia) · leganes, alcorcon, torrejon-de-ardoz, parla, alcobendas (madrid) · talavera-de-la-reina (toledo) · santiago-de-compostela, ferrol (a-coruna) · aviles (asturias) · · las-palmas-de-gran-canaria (las-palmas) · jerez-de-la-frontera (cadiz) · algeciras (cadiz) · vigo (pontevedra) · elche (alicante) · torrevieja (alicante) · gijon (asturias) · oviedo (asturias) · marbella (malaga) · dos-hermanas (sevilla) · sabadell, terrassa, badalona, hospitalet-de-llobregat (barcelona) · mostoles, alcala-de-henares, fuenlabrada, getafe (madrid) · cartagena (murcia) · santander (cantabria) · pamplona (navarra) · logrono (la-rioja) · donostia-san-sebastian (gipuzkoa) · vitoria-gasteiz (alava)

### 5.4 Contenido obligatorio de cada página geo (mínimo 350 palabras propias)
1. H1 "Vender proindiviso en {lugar}" + subtítulo con la cobertura (comarcas/barrios).
2. Formulario corto arriba.
3. Bloque local: Registros de la Propiedad de la provincia, tipo de inmueble más habitual (herencias rurales vs pisos), precio medio €/m² de referencia (fuente pública, con fecha), plusvalía municipal orientativa en la capital, tiempos de notaría habituales.
4. "Cómo funciona" (común) + 3 FAQ locales (schema FAQPage).
5. Enlaces: padre (CCAA/provincia), hermanas (provincias de la misma CCAA), 2 páginas transaccionales.

## 6. Páginas de soporte (noindex salvo legales)
`/gracias/` (noindex) · `/aviso-legal/` · `/politica-de-privacidad/` (sin cesión a terceros: compramos nosotros) · `/politica-de-cookies/` · `/contacto/` (index, keyword "contacto zona proindiviso").

## 7. Enlazado interno (regla fija)
- Cabecera: Home · Empresas que compran · Cuánto pagan · Herencia · Sin avisar · Dónde (geo) · Contacto.
- Cada página transaccional enlaza a 3 situaciones + 2 del hub.
- Cada página del hub enlaza a 2 transaccionales (siempre `/empresas-que-compran-proindivisos/` y la más afín).
- Cada página geo enlaza a padre + hermanas + `/empresas-que-compran-proindivisos/` + `/cuanto-pagan-por-un-proindiviso/`.
- Pie: CCAA (19 enlaces) y legales.

## 8. Lotes de publicación
1. Lote 0 (lanzamiento): nivel 1 + nivel 3 + legales + Madrid, Barcelona, Valencia, Sevilla, Málaga, Alicante.
2. Lote 1 (+2 semanas): resto de provincias top 15 + nivel 2.
3. Lote 2 (+4 semanas): resto de provincias y CCAA.
4. Lote 3 (+6 semanas): ciudades.
Cada lote entra en el sitemap solo cuando sus páginas pasan el checklist SEO de §10 del encargo.
