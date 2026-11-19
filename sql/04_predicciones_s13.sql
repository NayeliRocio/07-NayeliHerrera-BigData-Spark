-- S13 AP7: tres proyecciones exploratorias desde Silver.
-- Excluye el último año observado (posiblemente incompleto), usa los 3 años
-- calendario previos y proyecta el siguiente año con una tendencia lineal.
-- El método requiere al menos 3 años previos y cobertura de fechas suficiente.

WITH parsed AS (
  SELECT item_id, federacion, pais_evento, evento,
         COALESCE(
           TRY_TO_TIMESTAMP(fecha_inicio, 'yyyyMMdd'),
           TRY_TO_TIMESTAMP(fecha_inicio, 'yyyy-MM-dd'),
           TRY_TO_TIMESTAMP(fecha_inicio, 'dd/MM/yyyy'),
           TRY_TO_TIMESTAMP(fecha_inicio, 'yyyy/MM/dd'),
           TRY_TO_TIMESTAMP(fecha_inicio, 'MM/dd/yyyy')
         ) AS fecha
  FROM ipd_catalog.silver.eventos_internacionales
),
dated AS (
  SELECT item_id, federacion, pais_evento, evento, YEAR(fecha) AS anio
  FROM parsed
  WHERE fecha IS NOT NULL AND item_id IS NOT NULL
),
bounds AS (
  SELECT MAX(anio) AS ultimo_anio_observado FROM dated
),
parameters AS (
  SELECT ultimo_anio_observado,
         LEAST(ultimo_anio_observado, YEAR(CURRENT_DATE()) - 1) AS ultimo_anio_completo,
         GREATEST(ultimo_anio_observado + 1, YEAR(CURRENT_DATE()) + 1) AS anio_proyectado
  FROM bounds
),
training AS (
  SELECT d.*,
         p.anio_proyectado
  FROM dated d CROSS JOIN parameters p
  WHERE d.anio BETWEEN p.ultimo_anio_completo - 2 AND p.ultimo_anio_completo
),
years AS (
  SELECT explode(sequence(ultimo_anio_completo - 2, ultimo_anio_completo)) AS anio
  FROM parameters
),
dimensions AS (
  SELECT 'Federación' AS prediccion, 'federacion' AS dimension,
         federacion AS categoria, anio, anio_proyectado, item_id
  FROM training WHERE federacion IS NOT NULL AND TRIM(federacion) <> ''
  UNION ALL
  SELECT 'País anfitrión', 'pais_evento', pais_evento, anio, anio_proyectado, item_id
  FROM training WHERE pais_evento IS NOT NULL AND TRIM(pais_evento) <> ''
  UNION ALL
  SELECT 'Evento', 'evento', evento, anio, anio_proyectado, item_id
  FROM training WHERE evento IS NOT NULL AND TRIM(evento) <> ''
),
categories AS (
  SELECT DISTINCT prediccion, dimension, categoria, anio_proyectado FROM dimensions
),
annual AS (
  SELECT prediccion, dimension, categoria, anio_proyectado, anio,
         COUNT(DISTINCT item_id) AS participaciones
  FROM dimensions
  GROUP BY prediccion, dimension, categoria, anio_proyectado, anio
),
grid AS (
  SELECT c.prediccion, c.dimension, c.categoria, c.anio_proyectado, y.anio,
         COALESCE(a.participaciones, 0) AS participaciones
  FROM categories c CROSS JOIN years y
  LEFT JOIN annual a
    ON a.prediccion = c.prediccion
   AND a.dimension = c.dimension
   AND a.categoria = c.categoria
   AND a.anio_proyectado = c.anio_proyectado
   AND a.anio = y.anio
),
regression AS (
  SELECT prediccion, dimension, categoria, anio_proyectado,
         COUNT_IF(participaciones > 0) AS anios_con_actividad,
         REGR_SLOPE(participaciones, anio) AS variacion_anual_estimada,
         REGR_INTERCEPT(participaciones, anio) AS intercepto
  FROM grid
  GROUP BY prediccion, dimension, categoria, anio_proyectado
),
forecast AS (
  SELECT prediccion, dimension, categoria, anio_proyectado,
         ROUND(variacion_anual_estimada, 2) AS variacion_anual_estimada,
         GREATEST(0, CAST(ROUND(intercepto + variacion_anual_estimada * anio_proyectado) AS BIGINT))
           AS participaciones_estimadas
  FROM regression
  WHERE anios_con_actividad >= 2
)
SELECT prediccion, categoria, anio_proyectado,
       variacion_anual_estimada, participaciones_estimadas
FROM forecast
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY prediccion ORDER BY participaciones_estimadas DESC, categoria
) <= 10
ORDER BY prediccion, participaciones_estimadas DESC, categoria;
