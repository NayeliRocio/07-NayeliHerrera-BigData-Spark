-- S11 | FIA | Consultas Genie para Inteligencia Deportiva (IPD)
-- Fuente verificada en el pipeline del repositorio:
-- Silver: ipd_catalog.silver.eventos_internacionales
-- Columnas Silver: item_id, federacion, evento, pais_evento, ciudad_evento,
-- deportista, puesto, especialidad, colectivo, departamento, provincia,
-- distrito, ubigeo, fecha_inicio, fecha_fin, fecha_publicacion, fecha_corte.
-- Gold: ipd_catalog.gold.participaciones_por_federacion_pais
-- Columnas Gold: federacion, pais_evento, total_participaciones.
-- Ejecutar después del Job S3 → Silver → Gold y validar permisos del catálogo.
-- Cada pregunta también puede escribirse en lenguaje natural en Genie.

-- 1. Ranking de federaciones por número de participaciones.
SELECT federacion,
       SUM(total_participaciones) AS participaciones
FROM ipd_catalog.gold.participaciones_por_federacion_pais
GROUP BY federacion
ORDER BY participaciones DESC;

-- 2. Ranking de países anfitriones por participaciones registradas.
SELECT pais_evento,
       SUM(total_participaciones) AS participaciones
FROM ipd_catalog.gold.participaciones_por_federacion_pais
GROUP BY pais_evento
ORDER BY participaciones DESC
LIMIT 10;

-- 3. Comparativa de participaciones por federación y país.
SELECT federacion, pais_evento, total_participaciones
FROM ipd_catalog.gold.participaciones_por_federacion_pais
ORDER BY federacion, total_participaciones DESC;

-- 4. Top 3 países por federación (ranking dentro de cada federación).
WITH ranking AS (
  SELECT federacion, pais_evento, total_participaciones,
         ROW_NUMBER() OVER (
           PARTITION BY federacion
           ORDER BY total_participaciones DESC, pais_evento
         ) AS posicion
  FROM ipd_catalog.gold.participaciones_por_federacion_pais
)
SELECT federacion, pais_evento, total_participaciones, posicion
FROM ranking
WHERE posicion <= 3
ORDER BY federacion, posicion;

-- 5. Filtro dinámico: detalle Silver de la federación con más participaciones.
-- El valor se obtiene de Gold, así no depende de adivinar nombres o categorías.
SELECT item_id, federacion, evento, pais_evento, ciudad_evento,
       deportista, puesto, especialidad, fecha_inicio
FROM ipd_catalog.silver.eventos_internacionales
WHERE federacion = (
  SELECT federacion
  FROM ipd_catalog.gold.participaciones_por_federacion_pais
  GROUP BY federacion
  ORDER BY SUM(total_participaciones) DESC
  LIMIT 1
)
ORDER BY fecha_inicio DESC, evento, deportista
LIMIT 100;

-- Nota de análisis predictivo:
-- La tabla Gold actual es un agregado transversal sin serie temporal ni
-- variables de resultado suficientes para entrenar o validar predicciones.
-- Para proponer tendencias futuras en Genie, usar Silver y comprobar primero
-- que fecha_inicio tenga cobertura temporal; no presentar como pronóstico
-- cuantitativo un ranking histórico. Las predicciones de tendencias,
-- participaciones por evento y riesgos de cobertura requieren evidencia,
-- periodo de entrenamiento y validación temporal.
