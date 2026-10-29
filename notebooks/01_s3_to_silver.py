# Databricks notebook source
# MAGIC %md
# MAGIC # IPD: CSV de eventos internacionales → Delta Silver
# MAGIC Conserva las columnas del dataset real, estandariza nombres y tipos, y elimina filas sin datos clave y duplicados por ITEM.

# COMMAND ----------
import json
from pyspark.sql import functions as F
from pyspark.sql.window import Window

dbutils.widgets.text(
    "raw_path",
    "s3://ipd-nayeli-s3/raw/deportistas_eventos_internacionales.csv",
)
dbutils.widgets.text(
    "silver_path",
    "s3://ipd-nayeli-s3/silver/eventos_internacionales",
)
RAW_PATH = dbutils.widgets.get("raw_path")
SILVER_PATH = dbutils.widgets.get("silver_path")
TABLE_NAME = "ipd_catalog.silver.eventos_internacionales"

if not RAW_PATH.startswith("s3://ipd-nayeli-s3/raw/"):
    raise ValueError("La entrada debe pertenecer a raw/ del bucket IPD autorizado")
if SILVER_PATH != "s3://ipd-nayeli-s3/silver/eventos_internacionales":
    raise ValueError("La salida debe ser silver/eventos_internacionales")

# COMMAND ----------
raw = (spark.read.option("header", True).option("inferSchema", False)
       .option("encoding", "UTF-8").option("mode", "FAILFAST").csv(RAW_PATH))
source_columns = (
    "FECHA_CORTE", "ITEM", "FEDERACION", "EVENTO", "PAIS_EVENTO",
    "CIUDAD_EVENTO", "FECHA_INICIO", "FECHA_FIN", "DEPORTISTA", "PUESTO",
    "ESPECIALIDAD", "COLECTIVO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO",
    "UBIGEO", "FECHA_PUBLICACION",
)
missing = set(source_columns) - set(raw.columns)
if missing:
    raise ValueError(f"Columnas ausentes en el dataset de eventos: {sorted(missing)}")

silver_columns = (
    ("FECHA_CORTE", "fecha_corte"), ("FEDERACION", "federacion"),
    ("EVENTO", "evento"), ("PAIS_EVENTO", "pais_evento"),
    ("CIUDAD_EVENTO", "ciudad_evento"), ("DEPORTISTA", "deportista"),
    ("PUESTO", "puesto"), ("ESPECIALIDAD", "especialidad"),
    ("COLECTIVO", "colectivo"), ("DEPARTAMENTO", "departamento"),
    ("PROVINCIA", "provincia"), ("DISTRITO", "distrito"),
    ("UBIGEO", "ubigeo"), ("FECHA_INICIO", "fecha_inicio"),
    ("FECHA_FIN", "fecha_fin"), ("FECHA_PUBLICACION", "fecha_publicacion"),
)
normalized = raw.select(
    F.expr("try_cast(trim(ITEM) AS BIGINT)").alias("item_id"),
    *[F.trim(F.col(source).cast("string")).alias(target)
      for source, target in silver_columns],
)
raw_count = raw.count()
valid = normalized.filter(F.col("item_id").isNotNull() & (F.col("item_id") > 0))
for name in ("federacion", "evento", "pais_evento", "deportista"):
    valid = valid.filter(F.col(name).isNotNull() & (F.col(name) != ""))
valid_count = valid.count()

order = Window.partitionBy("item_id").orderBy(
    F.col("fecha_inicio"), F.col("evento"), F.col("pais_evento"), F.col("deportista")
)
clean = (valid.withColumn("_row", F.row_number().over(order))
         .filter(F.col("_row") == 1).drop("_row"))
clean_count = clean.count()
if clean_count == 0:
    raise ValueError("No hay filas válidas; se conserva la salida existente")

# COMMAND ----------
spark.sql("CREATE SCHEMA IF NOT EXISTS ipd_catalog.silver")
if spark.catalog.tableExists(TABLE_NAME):
    detail = spark.sql(f"DESCRIBE DETAIL {TABLE_NAME}").first()
    if detail.location.rstrip("/") != SILVER_PATH:
        raise ValueError("La tabla Silver existente apunta a otra ubicación; no se modifica")
(clean.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
 .save(SILVER_PATH))
spark.sql(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} USING DELTA LOCATION '{SILVER_PATH}'")
persisted = spark.table(TABLE_NAME)
if persisted.count() != clean_count:
    raise RuntimeError("El conteo de la tabla Silver no coincide con los datos persistidos")

metrics = {"raw_path": RAW_PATH, "silver_path": SILVER_PATH, "table": TABLE_NAME,
           "input_rows": raw_count, "invalid_rows": raw_count - valid_count,
           "duplicate_rows": valid_count - clean_count, "silver_rows": clean_count,
           "source_fields_preserved": len(silver_columns) + 1}
print(json.dumps(metrics))
display(persisted.select("item_id", "federacion", "pais_evento", "evento", "puesto")
        .orderBy("item_id").limit(20))
dbutils.notebook.exit(json.dumps(metrics))
