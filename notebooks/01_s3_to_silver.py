# Databricks notebook source
# MAGIC %md
# MAGIC # IPD: Amazon S3 → Delta Silver → Unity Catalog
# MAGIC Lee el CSV privado con la credencial IAM de Unity Catalog. Los datos son demostrativos.

# COMMAND ----------
import json
from pyspark.sql import functions as F
from pyspark.sql.window import Window

dbutils.widgets.text("raw_path", "s3://ipd-nayeli-s3/raw/deportistas.csv")
dbutils.widgets.text("silver_path", "s3://ipd-nayeli-s3/silver/deportistas")
RAW_PATH = dbutils.widgets.get("raw_path")
SILVER_PATH = dbutils.widgets.get("silver_path")
TABLE_NAME = "ipd_catalog.silver.deportistas"
if not RAW_PATH.startswith("s3://ipd-nayeli-s3/raw/"):
    raise ValueError("La entrada debe pertenecer a raw/ del bucket IPD autorizado")
if SILVER_PATH != "s3://ipd-nayeli-s3/silver/deportistas":
    raise ValueError("La salida debe ser silver/deportistas del bucket IPD autorizado")

# COMMAND ----------
raw = (spark.read.option("header", True).option("inferSchema", True)
       .option("mode", "FAILFAST").csv(RAW_PATH))
required = ("id", "nombre", "disciplina", "region")
missing = set(required) - set(raw.columns)
if missing:
    raise ValueError(f"Columnas ausentes: {sorted(missing)}")
normalized = raw.select(
    F.expr("try_cast(id AS INT)").alias("id"),
    *[F.trim(F.col(name).cast("string")).alias(name) for name in required[1:]])
valid = normalized.filter(F.col("id").isNotNull())
for name in required[1:]:
    valid = valid.filter(F.col(name).isNotNull() & (F.col(name) != ""))
order = Window.partitionBy("id").orderBy("nombre", "disciplina", "region")
clean = (valid.withColumn("_row", F.row_number().over(order))
         .filter(F.col("_row") == 1).drop("_row"))
raw_count, valid_count, clean_count = raw.count(), valid.count(), clean.count()
if clean_count == 0:
    raise ValueError("No hay filas válidas; se conserva la salida existente")

# COMMAND ----------
spark.sql("CREATE SCHEMA IF NOT EXISTS ipd_catalog.silver")
if spark.catalog.tableExists(TABLE_NAME):
    detail = spark.sql(f"DESCRIBE DETAIL {TABLE_NAME}").first()
    if detail.location.rstrip("/") != SILVER_PATH.rstrip("/"):
        raise ValueError("La tabla existente apunta a otra ruta; no se modifica")
(clean.write.format("delta").mode("overwrite").save(SILVER_PATH))
spark.sql(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} USING DELTA LOCATION '{SILVER_PATH}'")
persisted = spark.table(TABLE_NAME)
if persisted.count() != clean_count:
    raise RuntimeError("El conteo de la tabla no coincide con Silver")
display(persisted.orderBy("id"))
metrics = {"raw_path": RAW_PATH, "silver_path": SILVER_PATH, "table": TABLE_NAME,
           "input_rows": raw_count, "invalid_rows": raw_count - valid_count,
           "duplicate_rows": valid_count - clean_count, "silver_rows": clean_count}
print(json.dumps(metrics))
dbutils.notebook.exit(json.dumps(metrics))
