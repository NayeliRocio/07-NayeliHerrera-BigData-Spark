# Databricks notebook source
# MAGIC %md
# MAGIC # IPD: archivo Gold en S3 y tabla de indicadores
# MAGIC Genera un CSV de indicadores desde Silver, lo carga al bucket y vuelve a leerlo desde S3 para crear la tabla Gold.
# MAGIC Los datos de origen son demostrativos y no representan estadísticas oficiales.

# COMMAND ----------
import csv
import io
import json
from pyspark.sql import functions as F

SILVER_TABLE = "ipd_catalog.silver.deportistas"
GOLD_TABLE = "ipd_catalog.gold.deportistas_por_disciplina_region"
GOLD_CSV = "s3://ipd-nayeli-s3/gold/deportistas_por_disciplina_region.csv"
GOLD_DELTA = "s3://ipd-nayeli-s3/gold/delta/deportistas_por_disciplina_region"

silver = spark.table(SILVER_TABLE)
summary = (silver.groupBy("disciplina", "region")
           .agg(F.countDistinct("id").alias("total_deportistas")))
# La exportación de este reporte académico está limitada para proteger el driver.
rows = summary.orderBy("disciplina", "region").limit(10001).collect()
if not rows or len(rows) > 10000:
    raise ValueError("El reporte debe contener entre 1 y 10000 grupos para exportar un único CSV")
silver_count = silver.count()
if sum(row.total_deportistas for row in rows) != silver_count:
    raise ValueError("El total Gold no coincide con el número de deportistas en Silver")

# COMMAND ----------
csv_buffer = io.StringIO(newline="")
writer = csv.writer(csv_buffer, lineterminator="\n")
writer.writerow(["disciplina", "region", "total_deportistas"])
writer.writerows((row.disciplina, row.region, row.total_deportistas) for row in rows)
dbutils.fs.put(GOLD_CSV, csv_buffer.getvalue(), overwrite=True)
print(f"Archivo Gold cargado en {GOLD_CSV}")

# COMMAND ----------
# Esta lectura consume el archivo de S3, no el DataFrame que originó el CSV.
from_s3 = (spark.read.schema("disciplina STRING, region STRING, total_deportistas LONG")
           .option("header", True).option("mode", "FAILFAST").csv(GOLD_CSV))
loaded = from_s3.collect()
if len(loaded) != len(rows) or sum(row.total_deportistas for row in loaded) != silver_count:
    raise RuntimeError("El archivo Gold leído desde S3 no coincide con el reporte generado")
spark.sql("CREATE SCHEMA IF NOT EXISTS ipd_catalog.gold")
if spark.catalog.tableExists(GOLD_TABLE):
    detail = spark.sql(f"DESCRIBE DETAIL {GOLD_TABLE}").first()
    if detail.location.rstrip("/") != GOLD_DELTA:
        raise ValueError("La tabla Gold existente apunta a otra ubicación; no se modifica")
from_s3.write.format("delta").mode("overwrite").save(GOLD_DELTA)
spark.sql(f"CREATE TABLE IF NOT EXISTS {GOLD_TABLE} USING DELTA LOCATION '{GOLD_DELTA}'")
if spark.table(GOLD_TABLE).count() != len(rows):
    raise RuntimeError("La tabla Gold no contiene todos los grupos del archivo CSV")
display(spark.table(GOLD_TABLE).orderBy("disciplina", "region"))
metrics = {"gold_csv": GOLD_CSV, "gold_delta": GOLD_DELTA, "gold_table": GOLD_TABLE,
           "groups": len(rows), "total_deportistas": silver_count,
           "loaded_from_s3": True}
print(json.dumps(metrics))
dbutils.notebook.exit(json.dumps(metrics))
