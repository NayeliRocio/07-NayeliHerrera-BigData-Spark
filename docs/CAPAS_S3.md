# Dataset real de eventos internacionales en Databricks y S3

El Job trabaja con el archivo `deportistas_eventos_internacionales.csv` aportado por la estudiante. El CSV tiene 55,027 registros y 17 columnas; `ITEM` identifica cada registro y el archivo se mantiene fuera del repositorio GitHub.

| Capa | Ruta S3 | Contenido | Tabla Databricks |
| --- | --- | --- | --- |
| Raw | `raw/deportistas_eventos_internacionales.csv` | CSV fuente de eventos internacionales | Lectura con Spark |
| Silver | `silver/eventos_internacionales/` | Registros validados y deduplicados por `ITEM`, conservando los campos del archivo | `ipd_catalog.silver.eventos_internacionales` |
| Gold | `gold/participaciones_por_federacion_pais.csv` | Conteo de participaciones por federación y país del evento | Lectura del CSV desde S3 |
| Gold | `gold/delta/participaciones_por_federacion_pais/` | Delta del reporte Gold leído desde S3 | `ipd_catalog.gold.participaciones_por_federacion_pais` |

S3 presenta `raw/`, `silver/` y `gold/` como prefijos, equivalentes a carpetas.

## Flujo automatizado

`databricks/ipd_workflow.json` define el Job programado y ejecuta estas tareas:

1. Sincroniza el Git Folder con la rama `main`.
2. Copia el CSV desde `/Volumes/ipd_catalog/default/source_uploads/` al prefijo Raw del bucket privado `ipd-nayeli-s3`.
3. Lee el CSV con Spark, estandariza nombres de columnas, valida `ITEM`, federación, evento, país y deportista, deduplica por `ITEM`, y guarda Silver en Delta.
4. Agrupa Silver por federación y país del evento, escribe un CSV Gold en S3, lo lee de nuevo desde S3 y crea la tabla externa Delta Gold.

El Job corre diariamente a las 07:00, hora de Lima; también se puede iniciar manualmente desde [Jobs & Pipelines](https://dbc-6d9a3ebe-2368.cloud.databricks.com/jobs/1010035654278929?o=7474649658925615). GitHub Actions sincroniza el Git Folder con cada push a `main`.

El indicador Gold se llama `total_participaciones`: cuenta los registros con `ITEM` único en cada combinación de federación y país. No pretende contar personas únicas. `DEPARTAMENTO` del dataset solo tiene Lima, por eso el reporte utiliza `PAIS_EVENTO`.

## Consultas

```sql
SELECT * FROM ipd_catalog.gold.participaciones_por_federacion_pais
ORDER BY federacion, pais_evento;
```

Para comprobar el CSV fuente directamente desde S3:

```sql
SELECT count(*) AS filas
FROM read_files(
  's3://ipd-nayeli-s3/raw/deportistas_eventos_internacionales.csv',
  format => 'csv', header => true
);
```
