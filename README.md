# API Tasa

Una API estática, rápida y eficiente para consultar tasas de cambio (USD/EUR) históricas desde el año 2023 y actuales. Este proyecto está diseñado para ofrecer una respuesta de latencia casi nula mediante archivos JSON alojados en GitHub Pages.

## Estructura de la API

La API no utiliza una base de datos dinámica, sino que sirve archivos JSON estáticos organizados por moneda, año y fecha.

### Endpoint Base
`https://ronaldmedrano.github.io/api-tasa/`

### Formato de Consulta
La ruta para acceder a un dato específico es:
`https://ronaldmedrano.github.io/api-tasa/tasa/{MONEDA}/{AÑO}/{FECHA}.json`

**Ejemplos:**
- **USD:** `https://ronaldmedrano.github.io/api-tasa/tasa/USD/2026/2026-04-24.json`
- **EUR:** `https://ronaldmedrano.github.io/api-tasa/tasa/EUR/2026/2026-04-24.json`

## Estructura de Datos (JSON)
Cada archivo devuelve un array con el siguiente formato:

```json
[
  {
    "fuente": "BCV",
    "moneda": "USD",
    "tasa": 480.25,
    "fecha": "2026-04-24"
  }
]