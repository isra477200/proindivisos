# Keyword Planner España — volumen nacional y por provincia (23/10/2026)

Fuente: Google Ads API v24, KeywordPlanIdeaService (generateKeywordIdeas + generateKeywordHistoricalMetrics), idioma español, red Búsqueda, vía endpoint n8n `gaql-historico-lectura` (activado solo para esta extracción y desactivado después). Ideas: 3 tandas de semillas (proindiviso / vender parte piso-herencia / condominio) = 550 keywords únicas, 36.300 búsquedas/mes agregadas. Histórico: 30 keywords semilla × 70 geos (España, 19 CCAA, 50 provincias).

Datos completos: `docs/datos/keyword-planner-ideas-es-2026-10-23.csv` y `docs/datos/keyword-planner-geo-2026-10-23.csv`.

## 1. Lo que cambia respecto a lo observado en campañas

- El mercado transaccional "proindiviso" es **pequeño**: vender proindiviso 390/mes, compra proindiviso 390, empresas que compran 320, sin avisar 320, mejores empresas 260, cuánto pagan 210. Unas 2.500 búsquedas/mes en total con intención de venta.
- **"extinción de condominio" tiene 8.100/mes** (+ 880 entre hermanos, 880 extincion condominio, 720 disolución, 590 qué es, 390 hipoteca, 390 impuestos…). Es la vía legal alternativa a vender la parte: el usuario quiere quedarse o comprar la parte del otro. Es la mayor fuente de tráfico del nicho y el 80 % de esas personas acaban sin acuerdo. Hub informativo obligatorio con CTA "si no hay acuerdo, vende tu parte".
- **"proindiviso" (3.600) + "proindiviso que es" (2.400)**: informativo puro, pero es la puerta de entrada. Página "qué es" con CTA suave.
- Cluster herencia con búsquedas reales: "puedo vender mi parte de una casa heredada" 320, "se puede vender una propiedad si un heredero no quiere" 210, "empresas que compran herencias" 210, "vender mi parte de la herencia a otro heredero" 140.
- CPC: lo transaccional cuesta 4-8 € (compra de proindiviso 7,70 €, venta de proindivisos 5,71 €); lo informativo 0,3-2 €. En orgánico, cada lead transaccional ahorra ese CPC.
- Long tail que **no** tiene volumen (0-10): proindiviso divorcio, vender mi parte de la casa de mis padres, cuánto vale mi parte de un piso, vender parte de piso heredado. No merecen página propia: se cubren dentro de otra.

## 2. Geo: dónde está la demanda (suma de las 30 semillas, búsquedas/mes)

| Provincia | Vol. | | CCAA | Vol. |
|---|---|---|---|---|
| Madrid | 3990 | | Community of Madrid | 3990 |
| Barcelona | 1450 | | Andalusia | 2770 |
| Valencia | 950 | | Valencian Community | 1760 |
| Seville | 830 | | Catalonia | 1670 |
| Province of Malaga | 760 | | Galicia | 840 |
| Alicante | 670 | | Castile and Leon | 840 |
| Biscay | 550 | | Basque Country | 740 |
| Cadiz | 520 | | Castile-La Mancha | 680 |
| Las Palmas | 500 | | Canary Islands | 670 |
| Murcia | 460 | | Region of Murcia | 460 |
| Pontevedra | 460 | | Aragon | 440 |
| A Coruna | 430 | | Balearic Islands | 430 |
| Province of Castellon | 430 | | Asturias | 380 |
| Balearic Islands | 430 | | Extremadura | 370 |
| Granada | 380 | | Cantabria | 320 |
| Zaragoza | 380 | | Navarre | 290 |
| Asturias | 380 | | La Rioja | 230 |
| Valladolid | 370 | | Ceuta | 120 |
| Toledo | 350 | | Melilla | 120 |
| Cordoba | 340 | |  |  |
| Santa Cruz de Tenerife | 330 | |  |  |
| Cantabria | 320 | |  |  |
| Gipuzkoa | 300 | |  |  |
| Navarre | 290 | |  |  |
| Badajoz | 290 | |  |  |
| Province of Almeria | 290 | |  |  |
| Province of Jaen | 280 | |  |  |
| Tarragona | 280 | |  |  |
| Girona | 270 | |  |  |
| Alava | 270 | |  |  |
| Albacete | 270 | |  |  |
| Huelva | 270 | |  |  |
| Province of Leon | 260 | |  |  |
| Ciudad Real | 260 | |  |  |
| Guadalajara | 260 | |  |  |
| Burgos | 250 | |  |  |
| Salamanca | 250 | |  |  |
| Caceres | 250 | |  |  |
| La Rioja | 230 | |  |  |
| Lugo | 230 | |  |  |
| Segovia | 210 | |  |  |
| Lleida | 200 | |  |  |
| Province of Ourense | 200 | |  |  |
| Palencia | 190 | |  |  |
| Soria | 180 | |  |  |
| Cuenca | 180 | |  |  |
| Zamora | 170 | |  |  |
| Avila | 160 | |  |  |
| Teruel | 150 | |  |  |
| Huesca | 140 | |  |  |

Lectura: Madrid concentra el 25-30 % de la demanda; Madrid + Barcelona + Valencia + Sevilla + Málaga + Alicante suman más de la mitad. Las provincias pequeñas (Huesca, Teruel, Ávila, Soria…) tienen 140-180 búsquedas/mes **sumando las 30 keywords**, casi todo "extinción de condominio" y "proindiviso". Una página por ciudad mediana no tiene búsqueda que justificarla.

**Consecuencia para la arquitectura:** 50 páginas de provincia + 19 de CCAA (con contenido real), y páginas de ciudad solo para las capitales y ciudades grandes de las 10-12 primeras provincias (unas 25 ciudades), no 150. El resto de municipios se cubre desde la provincia.

## 3. Hoja keyword → URL (propuesta de fase 2)

| URL | Keyword principal | Vol. cluster/mes | Keywords del cluster (vol.) |
|---|---|---|---|
| `/ (home)` | vender proindiviso | 1420 | vender proindiviso (390), proindivisos compra (390), venta proindiviso (320), venta de proindivisos (170), compra de proindiviso (110), vender mi proindiviso (40) |
| `/empresas-que-compran-proindivisos` | empresas que compran proindivisos | 1230 | compradores proindivisos (390), empresas que compran proindivisos (320), empresas que compran herencias (210), opiniones sobre empresas que compran proindivisos (170), vender proindiviso opiniones (140) |
| `/cuanto-pagan-por-un-proindiviso` | cuánto pagan por un proindiviso | 140 | valor vivienda extinción de condominio (140), cuanto pagan las empresas que compran proindivisos (0) |
| `/vender-proindiviso-sin-avisar` | vender proindiviso sin avisar | 530 | vender proindiviso sin avisar (320), se puede vender una propiedad si un heredero no quiere (210) |
| `/vender-parte-casa-heredada` | vender mi parte de una casa heredada | 1530 | puedo vender mi parte de una casa heredada (320), condominio herencia (320), proindiviso herencia (170), proindivisos y herencias (170), vender mi parte de la herencia a otro heredero (140), vender parte de una vivienda heredada (110), vender un piso heredado (110), se puede vender una casa heredada sin escrituras (90), venta proindiviso herencia (70), vender proindiviso herencia (30) |
| `/extincion-de-condominio (hub)` | extinción de condominio | 10890 | extinción de condominio (8100), extincion condominio (880), disolucion de condominio (720), extincion de condominio que es (590), escision de condominio (170), exención de condominio (140), extincion de proindiviso (110), cesion de condominio (90), escritura de extincion de condominio (90) |
| `/extincion-de-condominio/entre-hermanos` | extinción de condominio entre hermanos | 2250 | extinción de condominio entre hermanos (880), extincion de condominio hermanos (880), extinción de condominio entre hermanos con compensación económica (170), extinción de condominio entre hermanos sin compensación económica (140), disolucion de condominio entre hermanos (90), disolución de comunidad de bienes entre hermanos (90) |
| `/extincion-de-condominio/hipoteca` | extinción de condominio con hipoteca | 400 | extinción de condominio hipoteca (390), proindiviso con hipoteca (10) |
| `/extincion-de-condominio/impuestos-y-notario` | impuestos extinción de condominio | 740 | extincion de condominio impuestos (390), precio notario extinción de condominio (170), extincion condominio impuestos (90), extinción de condominio con compensación económica (90) |
| `/que-es-un-proindiviso` | qué es un proindiviso | 7800 | proindiviso (3600), proindiviso que es (2400), pro indivisa (720), proindiviso que significa (480), proindiviso ventajas y desventajas (170), pro indiviso que significa (140), propiedad en proindiviso (110), mitad indivisa que significa (90), terreno proindiviso (90) |
| `/division-de-cosa-comun` | división de cosa común | 420 | división de cosa común (170), division cosa comun (110), minuta abogado división cosa común (70), division cosa comun procedimiento (70) |
| `/vender-parte-de-un-piso` | vender parte de un piso | 60 | vender parte de un piso (40), vender mi parte de un piso (10), vender parte de una vivienda (10) |

Más: 50 provincias (`/vender-proindiviso-en/{provincia}`), 19 CCAA, ~25 ciudades, FAQ por página, páginas legales. Las keywords geo observadas en campañas ("proindivisos madrid" 77 clics, "empresas que compran proindivisos madrid" 42) van a la página de Madrid.

## 4. Limitaciones
- Los volúmenes del Planner son redondeados por Google y agrupan variantes cercanas.
- El histórico por provincia se calculó sobre 30 semillas, no sobre las 550 ideas; sirve para ordenar provincias, no como volumen total del nicho.
- Lo observado en campañas (docs/investigacion-cuentas-proindivisos.md) sigue siendo la mejor señal de qué convierte; el Planner dice dónde está el volumen.
