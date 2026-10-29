-- S11 AP5-AP6 | Inteligencia Deportiva
-- Usa un catálogo asignado por el docente si no tienes permiso para crear uno.
CREATE CATALOG IF NOT EXISTS ipd_catalog;
CREATE SCHEMA IF NOT EXISTS ipd_catalog.silver;

-- Ejecutar después del notebook 01_s3_to_silver.py.
CREATE TABLE IF NOT EXISTS ipd_catalog.silver.deportistas
USING DELTA
LOCATION 's3://ipd-nayeli-s3/silver/deportistas';

SELECT * FROM ipd_catalog.silver.deportistas LIMIT 10;
