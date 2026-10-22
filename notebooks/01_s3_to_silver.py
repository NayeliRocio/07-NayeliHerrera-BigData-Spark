# Databricks notebook source
# MAGIC %md
# MAGIC # S11 AP5-AP6: IPD, de S3 a Silver
# MAGIC Lee deportistas.csv (id, nombre, disciplina, region), valida registros, guarda Delta en S3 y registra la tabla Unity Catalog.

# COMMAND ----------
from pyspark.sql import functions as F

RAW_PATH = "s3://ipd-noestructurados-nayeli-20260928-7314/raw/deportistas.csv"
SILVER_PATH = "s3://ipd-noestructurados-nayeli-20260928-7314/silver/deportistas"
TABLE_NAME = "ipd_catalog.silver.deportistas"

# COMMAND ----------
# La External Location debe permitir leer raw/ y escribir silver/. No guardes claves AWS aquí.
raw = (spark.read.option("header", True).option("inferSchema", True).csv(RAW_PATH))
clean = (raw.select(
    F.col("id").cast("int").alias("id"),
    F.trim(F.col("nombre").cast("string")).alias("nombre"),
    F.trim(F.col("disciplina").cast("string")).alias("disciplina"),
    F.trim(F.col("region").cast("string")).alias("region"))
    .filter(F.col("id").isNotNull())
    .filter(F.col("nombre").isNotNull() & (F.col("nombre") != ""))
    .filter(F.col("disciplina").isNotNull() & (F.col("disciplina") != ""))
    .filter(F.col("region").isNotNull() & (F.col("region") != ""))
    .dropDuplicates(["id"]))

# COMMAND ----------
print(f"Filas Silver: {clean.count()}")
display(clean.orderBy("id"))

# COMMAND ----------
(clean.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(SILVER_PATH))
spark.sql(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} USING DELTA LOCATION '{SILVER_PATH}'")
display(spark.table(TABLE_NAME).orderBy("id"))
