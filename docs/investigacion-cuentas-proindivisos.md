# Barrido MCC Google Ads — cuentas de proindivisos (23/10/2026)

Fuente: Google Ads API v24 vía gateway n8n (`panel-gaql` para cuentas activas del panel, `gaql-historico-lectura` con flag archivo para las archivadas). Jerarquía completa del MCC 880-539-6896: 168 cuentas (79 ENABLED cliente, 6 MCC, 80 CANCELED, 3 CLOSED). Se consultaron las 79 ENABLED: nombre de cuenta, campañas, keywords y términos de búsqueda (23/10/2025 → 23/10/2026) con regex `pro[ -]?indivis`. 0 errores.

## Cuentas con señal de proindiviso (8)

| CID | Cuenta | En Notion | Keywords | Términos 12m | Clics 12m | Coste 12m |
|---|---|---|---|---|---|---|
| 463-061-4423 | Compramos Proindivisos | NO | 50 | 11 | 11 | 46.91 € |
| 120-143-7650 | Expertos en Proindivisos | sí | 20 | 73 | 451 | 3570.57 € |
| 746-018-9091 | Fin del Proindiviso | NO | 29 | 24 | 18 | 24.37 € |
| 707-824-2970 | SOLUCIONES PROINDIVISO, SL | sí | 5 | 45 | 100 | 829.22 € |
| 930-792-9427 | Sal del Proindiviso | sí | 7 | 72 | 474 | 2950.99 € |
| 615-393-8152 | Valora tu proindiviso | sí | 33 | 48 | 475 | 2583.13 € |
| 431-279-2125 | Vender mi Proindiviso | sí | 6 | 83 | 1164 | 2358.08 € |
| 851-660-5362 | proindivisosgestionpropiedades.com | sí | 20 | 73 | 644 | 2661.07 € |

Notas:
- **Compramos Proindivisos (463-061-4423)** y **Fin del Proindiviso (746-018-9091)** no están en la BD Clientes de Notion. Ambas con campaña de búsqueda activa (Canarias la primera).
- **Proindiviso Directo (408-846-3488)** figura en Notion pero NO está en la jerarquía de este MCC (la ficha dice "CUIDADO MILCLIENTES"): queda fuera del barrido.
- Las 80 cuentas CANCELED no se pueden consultar por API; por nombre ninguna contiene "proindiviso".
- Los términos de búsqueda vienen filtrados por Google (oculta los de poco volumen) y sesgados por la geo de cada campaña (Madrid sobre todo).

## Términos de búsqueda agregados (top 30 por clics, 8 cuentas)

| Clics | Coste | Cuentas | Término |
|---|---|---|---|
| 469 | 1697.40 € | 7 | mejores empresas que compran proindivisos |
| 386 | 1689.25 € | 7 | empresas que compran proindivisos |
| 184 | 289.75 € | 5 | vender proindiviso sin avisar |
| 182 | 489.18 € | 6 | vender proindiviso |
| 180 | 1116.37 € | 7 | compra de proindivisos |
| 126 | 618.26 € | 7 | compra proindiviso |
| 120 | 636.62 € | 6 | empresas que compran proindivisos en toda españa |
| 117 | 796.83 € | 5 | compra proindivisos |
| 112 | 266.71 € | 3 | venta proindiviso |
| 90 | 616.11 € | 6 | empresas proindiviso |
| 88 | 197.54 € | 4 | venta de proindiviso |
| 77 | 668.27 € | 7 | proindivisos madrid |
| 70 | 409.57 € | 6 | compra de proindiviso |
| 65 | 375.93 € | 7 | compramos tu proindiviso |
| 52 | 96.29 € | 5 | venta proindiviso herencia |
| 49 | 344.83 € | 6 | compramos proindivisos |
| 49 | 310.24 € | 6 | empresas de proindiviso |
| 48 | 249.79 € | 6 | empresa proindiviso |
| 47 | 115.25 € | 5 | proindiviso venta |
| 44 | 156.57 € | 5 | vender proindiviso herencia |
| 42 | 257.66 € | 6 | empresas que compran proindivisos madrid |
| 42 | 177.46 € | 4 | vender herencia proindiviso |
| 40 | 324.37 € | 5 | compra de proindivisos madrid |
| 39 | 195.67 € | 6 | compra proindivisos herencias |
| 38 | 143.62 € | 6 | venta de proindivisos |
| 32 | 51.90 € | 6 | qué hacen las empresas que compran proindivisos |
| 31 | 58.31 € | 3 | vender un proindiviso |
| 31 | 127.33 € | 4 | venta de proindiviso herencia |
| 29 | 84.50 € | 3 | vender mi proindiviso |
| 28 | 206.72 € | 6 | proindiviso compra |

## Lectura rápida para la web
- Intención dominante: **"empresas que compran proindivisos"** y su variante "mejores empresas que compran proindivisos" (aparecen en 7-8 cuentas). Valida el posicionamiento de comparador/red de compradores.
- **"vender proindiviso sin avisar"** es el término nº 1 de la cuenta con más clics (180): página propia obligatoria ("vender mi parte sin avisar al otro propietario").
- **"cuánto pagan las empresas que compran proindivisos"** → página de precio/valoración (lead magnet).
- Geo: "proindivisos madrid", "en toda españa", Canarias → confirma la necesidad de páginas por provincia con Madrid como prioridad 1.
- Pendiente: volumen nacional por provincia con Keyword Planner (modo `ideas`/`hist` del endpoint `gaql-historico-lectura`) para separar observado de volumen general.
