# S11 AP5-AP6 — IPD: Databricks, S3 y Genie

## Proyecto y rutas
Se reutiliza `NayeliRocio/07-NayeliHerrera-BigData-Spark`, proyecto IPD. El CSV real del repositorio tiene las columnas `id`, `nombre`, `disciplina`, `region`.

- Bucket: `s3://ipd-nayeli-s3`
- Raw CSV: `s3://ipd-nayeli-s3/raw/deportistas.csv`
- Silver Delta: `s3://ipd-nayeli-s3/silver/deportistas`
- Tabla: `ipd_catalog.silver.deportistas`

La captura del bucket muestra la carpeta `raw/`. Sube allí el archivo `data/sample/deportistas.csv` con el nombre `deportistas.csv`. El notebook crea el prefijo Silver al escribir Delta.

## Ejecución en Databricks
1. El workflow sincroniza la rama `main` de este repositorio con el Git Folder antes de procesar datos. También puedes ejecutar el job manualmente.
2. En Unity Catalog, necesitas una External Location para el bucket con permisos de lectura sobre `raw/` y escritura sobre `silver/`. El bucket ARN por sí solo no concede acceso. No guardes claves AWS en GitHub.
3. Ejecuta `sql/01_catalog_schema.sql`. Si no puedes crear `ipd_catalog`, usa el catálogo que te asignó el docente y ajusta el nombre en los archivos.
4. Ejecuta `notebooks/01_s3_to_silver.py`. Comprueba el conteo y las filas que muestra.
5. Ejecuta de nuevo el SQL para registrar/consultar `ipd_catalog.silver.deportistas`.
6. Crea un espacio Genie usando esa tabla. Descripción sugerida: “Cada fila representa un deportista único; id es el identificador y disciplina y region describen su práctica. Silver elimina filas con datos obligatorios vacíos y conserva un registro por id.”
7. Prueba las cinco consultas/preguntas de `sql/02_genie_queries.sql` en Genie.

El CSV del repositorio es pequeño y de prueba, así que sus resultados son demostrativos, no estadísticas oficiales. La actividad se termina cuando el notebook ejecuta en Databricks y las cinco preguntas responden en Genie.
