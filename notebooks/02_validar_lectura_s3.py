# Databricks notebook source
# MAGIC %md
# MAGIC # S5: comprobar lectura real desde Amazon S3
# MAGIC Esta comprobación independiente no modifica el pipeline unificado de Colab.
# MAGIC Usa una External Location de Unity Catalog ya autorizada. No escribe en S3.
# MAGIC La URI debe identificar un archivo CSV real, no una carpeta ni un dato de muestra local.

# COMMAND ----------
import json
from datetime import datetime, timezone
from urllib.parse import urlsplit
from pyspark.sql import functions as F

dbutils.widgets.text("s3_uri", "", "URI exacta de un CSV en S3")
dbutils.widgets.text("delimiter", ",", "Separador del CSV")
dbutils.widgets.text("encoding", "UTF-8", "Codificación del CSV")
dbutils.widgets.text("required_columns", "", "Columnas requeridas, separadas por comas")
dbutils.widgets.dropdown("data_kind", "sin_clasificar", ["sin_clasificar", "muestra", "fuente_oficial"], "Tipo de datos")

uri = dbutils.widgets.get("s3_uri").strip()
location = urlsplit(uri)
if (location.scheme != "s3" or not location.netloc or location.username
        or not location.path.lower().endswith(".csv") or location.query or location.fragment):
    raise ValueError("Indica la URI s3://bucket/clave.csv de un archivo existente.")

delimiter = dbutils.widgets.get("delimiter")
if len(delimiter) != 1:
    raise ValueError("El separador debe contener exactamente un carácter.")
data_kind = dbutils.widgets.get("data_kind")
if data_kind == "sin_clasificar":
    raise ValueError("Clasifica la fuente como muestra o fuente_oficial antes de ejecutar.")

# COMMAND ----------
# El archivo se lee con Spark usando permisos existentes de Unity Catalog.
# No configures spark.hadoop.fs.s3a con claves personales en serverless.
dataset = (spark.read
    .option("header", True)
    .option("inferSchema", False)
    .option("mode", "FAILFAST")
    .option("delimiter", delimiter)
    .option("encoding", dbutils.widgets.get("encoding"))
    .csv(uri))

required = [name.strip() for name in dbutils.widgets.get("required_columns").split(",") if name.strip()]
missing = sorted(set(required) - set(dataset.columns))
if missing:
    raise ValueError("Columnas requeridas ausentes: " + ", ".join(missing))

# Una acción de Spark comprueba que la lectura se ejecutó; no basta definir el DataFrame.
# La agregación referencia todas las columnas y admite Spark Connect/serverless.
stats = (dataset.select(F.to_json(F.struct(*[dataset[c] for c in dataset.columns])).alias("row_json"))
    .agg(F.count("*").alias("rows"), F.sum(F.length("row_json")).alias("parsed_characters"))
    .first())
row_count = stats["rows"]
if row_count == 0:
    raise ValueError("El CSV no contiene filas; no se registra una lectura válida.")

evidence = {
    "status": "verified",
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "s3_uri": uri,
    "data_kind": data_kind,
    "row_count": row_count,
    "columns": dataset.columns,
    "reader": "Apache Spark / Unity Catalog",
}
print(json.dumps(evidence, ensure_ascii=False, indent=2))
# No se imprimen nombres de personas ni filas completas para acreditar la conexión.
dbutils.notebook.exit(json.dumps(evidence, ensure_ascii=False))
