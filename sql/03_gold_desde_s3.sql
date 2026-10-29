-- Ejecutar después del notebook 02_silver_to_gold.py.
-- Comprueba que Databricks consume el archivo Gold cargado en el bucket.
SELECT * FROM read_files(
  's3://ipd-nayeli-s3/gold/deportistas_por_disciplina_region.csv',
  format => 'csv',
  header => true,
  schema => 'disciplina STRING, region STRING, total_deportistas BIGINT'
) ORDER BY disciplina, region;

-- El notebook guarda la tabla Gold como Delta externa en S3.
SELECT * FROM ipd_catalog.gold.deportistas_por_disciplina_region
ORDER BY disciplina, region;

SELECT SUM(total_deportistas) AS total_deportistas
FROM ipd_catalog.gold.deportistas_por_disciplina_region;
