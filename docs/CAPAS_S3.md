# Archivo Gold en S3 consumido desde el Git Folder

La actividad requiere un archivo de datos del proyecto en S3 y código Python o SQL en Databricks que lo lea y cree una tabla. Se implementa con el bucket privado `ipd-nayeli-s3` y la External Location existente de Unity Catalog.

| Capa | Ruta en S3 | Contenido | Tabla de Databricks |
| --- | --- | --- | --- |
| Raw | `raw/deportistas.csv` | Archivo original, 5 filas de muestra | Se lee con Spark |
| Silver | `silver/deportistas/` | Delta, 3 deportistas válidos sin duplicados | `ipd_catalog.silver.deportistas` |
| Gold | `gold/deportistas_por_disciplina_region.csv` | CSV con indicadores del proyecto | Se consume desde el notebook Gold |
| Gold | `gold/delta/deportistas_por_disciplina_region/` | Delta del archivo Gold consumido | `ipd_catalog.gold.deportistas_por_disciplina_region` |

S3 utiliza prefijos; `raw/`, `silver/` y `gold/` se muestran como carpetas en la consola.

## Qué hace el archivo Python

`notebooks/02_silver_to_gold.py`, ubicado en el Git Folder:

1. Agrupa los deportistas de Silver por disciplina y región.
2. Carga un único archivo CSV con encabezado a `s3://ipd-nayeli-s3/gold/deportistas_por_disciplina_region.csv`.
3. Lee ese archivo desde S3 usando `spark.read.csv`.
4. Verifica los conteos y guarda la tabla externa Delta Gold, registrada en Unity Catalog.

El archivo contiene las columnas `disciplina`, `region`, `total_deportistas`. Para los datos de muestra, el reporte tiene 3 grupos y suma 3 deportistas.

El workflow ejecuta `sync_git_folder → s3_to_silver → silver_to_gold` cada día a las 07:00 de Lima. Se puede ejecutar manualmente en [Jobs & Pipelines](https://dbc-6d9a3ebe-2368.cloud.databricks.com/jobs/1010035654278929?o=7474649658925615). GitHub Actions actualiza el Git Folder en cada push a `main`.

## Consultar el archivo y la tabla

El archivo `sql/03_gold_desde_s3.sql` contiene las consultas completas. Para revisar la tabla:

```sql
SELECT * FROM ipd_catalog.gold.deportistas_por_disciplina_region;
```

Para comprobar el CSV directamente en el bucket:

```sql
SELECT * FROM read_files(
  's3://ipd-nayeli-s3/gold/deportistas_por_disciplina_region.csv',
  format => 'csv', header => true,
  schema => 'disciplina STRING, region STRING, total_deportistas BIGINT'
);
```

Estas rutas pertenecen a la cuenta AWS cuyo acceso ya se verificó desde Databricks. El nombre de una capa describe el estado de los datos; la carga a S3 y la creación de una tabla son operaciones distintas y ambas están implementadas en el notebook. Los resultados son demostrativos.
