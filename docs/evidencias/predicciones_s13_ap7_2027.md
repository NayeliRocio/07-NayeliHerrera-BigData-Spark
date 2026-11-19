# Evidencia de predicciones S13 AP7

## Datos y método

- Fuente: `ipd_catalog.silver.eventos_internacionales`.
- Fecha de consulta: 18 de noviembre de 2026.
- Último año disponible en Silver: 2024.
- Años usados para ajustar la tendencia: 2022, 2023 y 2024.
- Año proyectado: 2027. El conjunto no contiene registros de 2025 ni 2026, por lo que la proyección queda a tres años del último dato observado.
- Método: regresión lineal ordinaria sobre los totales anuales por categoría; los valores negativos se limitan a cero.
- Métrica: `ITEM` distintos por año, interpretados como participaciones registradas; no equivalen a deportistas únicos ni a medallas.

## Resultados principales

### Federaciones

| Federación | Participaciones estimadas 2027 | Cambio anual estimado |
|---|---:|---:|
| ATLETISMO | 680 | +79.0 |
| TENIS | 673 | +17.0 |
| GIMNASIA | 659 | +69.0 |

### País asociado al evento

| País | Participaciones estimadas 2027 | Cambio anual estimado |
|---|---:|---:|
| PERU | 1,808 | -22.0 |
| CHILE | 1,366 | +213.5 |
| BRASIL | 1,238 | +171.0 |

Estos valores describen el país asociado a los eventos históricos de Silver; no anuncian sedes oficiales futuras.

### Eventos

| Evento | Participaciones estimadas 2027 | Cambio anual estimado |
|---|---:|---:|
| COPA INDERVALLE | 61 | +12.0 |
| J30 TRUJILLO | 50 | +9.0 |
| J100 LIMA | 40 | +8.0 |

## Interpretación y límites

1. ATLETISMO presenta la mayor proyección entre las federaciones listadas, seguido de TENIS y GIMNASIA.
2. CHILE y BRASIL tienen tendencias anuales positivas en los registros por país; PERU muestra una reducción leve.
3. Entre los eventos listados, COPA INDERVALLE tiene la mayor proyección de participaciones.

Son estimaciones exploratorias basadas en solo tres observaciones anuales por categoría. No se calcularon intervalos de predicción ni validación retrospectiva; además, faltan dos años recientes en la fuente, así que la incertidumbre es alta y los resultados no garantizan valores futuros.
