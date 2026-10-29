# Databricks notebook source
# MAGIC %md
# MAGIC # IPD: participaciones por federación y país del evento
# MAGIC Genera el CSV Gold desde el dataset de eventos internacionales, lo escribe en S3 y lo vuelve a leer desde S3 para crear la tabla Delta Gold.

# COMMAND ----------
import csv
import io
import json
from pyspark.sql import functions as F

SILVER_TABLE = "ipd_catalog.silver.eventos_internacionales"
GOLD_TABLE = "ipd_catalog.gold.participaciones_por_federacion_pais"
GOLD_CSV = "s3://ipd-nayeli-s3/gold/participaciones_por_federacion_pais.csv"
GOLD_DELTA = "s3://ipd-nayeli-s3/gold/delta/participaciones_por_federacion_pais"

silver = spark.table(SILVER_TABLE)
summary = (silver.groupBy("federacion", "pais_evento")
           .agg(F.countDistinct("item_id").alias("total_participaciones")))
rows = summary.orderBy("federacion", "pais_evento").limit(10001).collect()
if not rows or len(rows) > 10000:
    raise ValueError("El reporte debe contener entre 1 y 10000 grupos para exportar un CSV")
silver_count = silver.select("item_id").distinct().count()
if sum(row.total_participaciones for row in rows) != silver_count:
    raise ValueError("El total Gold no coincide con las participaciones Silver")

# COMMAND ----------
csv_buffer = io.StringIO(newline="")
writer = csv.writer(csv_buffer, lineterminator="\n")
writer.writerow(["federacion", "pais_evento", "total_participaciones"])
writer.writerows((row.federacion, row.pais_evento, row.total_participaciones)
                 for row in rows)
dbutils.fs.put(GOLD_CSV, csv_buffer.getvalue(), overwrite=True)
print(f"Archivo Gold cargado en {GOLD_CSV}")

# COMMAND ----------
# Se valida una lectura nueva del CSV guardado en S3.
from_s3 = (spark.read.schema(
    "federacion STRING, pais_evento STRING, total_participaciones LONG")
    .option("header", True).option("mode", "FAILFAST").csv(GOLD_CSV))
loaded = from_s3.collect()
if (len(loaded) != len(rows)
        or sum(row.total_participaciones for row in loaded) != silver_count):
    raise RuntimeError("El archivo Gold leído desde S3 no coincide con Silver")

spark.sql("CREATE SCHEMA IF NOT EXISTS ipd_catalog.gold")
if spark.catalog.tableExists(GOLD_TABLE):
    detail = spark.sql(f"DESCRIBE DETAIL {GOLD_TABLE}").first()
    if detail.location.rstrip("/") != GOLD_DELTA:
        raise ValueError("La tabla Gold existente apunta a otra ubicación; no se modifica")
(from_s3.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
 .save(GOLD_DELTA))
spark.sql(f"CREATE TABLE IF NOT EXISTS {GOLD_TABLE} USING DELTA LOCATION '{GOLD_DELTA}'")
gold = spark.table(GOLD_TABLE)
if gold.count() != len(rows):
    raise RuntimeError("La tabla Gold no contiene todos los grupos del CSV")

metrics = {"gold_csv": GOLD_CSV, "gold_delta": GOLD_DELTA,
           "gold_table": GOLD_TABLE, "groups": len(rows),
           "total_participations": silver_count, "loaded_from_s3": True}
print(json.dumps(metrics))
display(gold.orderBy("federacion", "pais_evento").limit(50))
dbutils.notebook.exit(json.dumps(metrics))
