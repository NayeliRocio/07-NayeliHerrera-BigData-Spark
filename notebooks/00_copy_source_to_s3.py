# Databricks notebook source
# MAGIC %md
# MAGIC # Copiar la fuente real al bucket S3
# MAGIC La fuente se carga de forma privada en un volumen Unity Catalog y este paso la copia sin alterar sus 17 columnas al prefijo raw del bucket del proyecto.

# COMMAND ----------
import json

dbutils.widgets.text(
    "source_path",
    "/Volumes/ipd_catalog/default/source_uploads/deportistas_eventos_internacionales.csv",
)
dbutils.widgets.text(
    "target_path",
    "s3://ipd-nayeli-s3/raw/deportistas_eventos_internacionales.csv",
)
SOURCE_PATH = dbutils.widgets.get("source_path")
TARGET_PATH = dbutils.widgets.get("target_path")

if not SOURCE_PATH.startswith("/Volumes/ipd_catalog/default/source_uploads/"):
    raise ValueError("La entrada debe estar en el volumen privado de cargas del proyecto")
if TARGET_PATH != "s3://ipd-nayeli-s3/raw/deportistas_eventos_internacionales.csv":
    raise ValueError("La salida debe ser el CSV de eventos en raw/ del bucket IPD autorizado")

source_items = dbutils.fs.ls(SOURCE_PATH)
if len(source_items) != 1 or source_items[0].isDir():
    raise ValueError("La ruta fuente debe apuntar a un único archivo CSV")
source_size = source_items[0].size
if source_size <= 0:
    raise ValueError("El CSV fuente está vacío")

if not dbutils.fs.cp(SOURCE_PATH, TARGET_PATH, True):
    raise RuntimeError("No se pudo copiar el CSV fuente a S3")

target_parent = TARGET_PATH.rsplit("/", 1)[0]
target_name = TARGET_PATH.rsplit("/", 1)[1]
target_items = [item for item in dbutils.fs.ls(target_parent) if item.name == target_name]
if len(target_items) != 1 or target_items[0].size != source_size:
    raise RuntimeError("El objeto S3 no coincide en tamaño con el archivo fuente")

metrics = {"source_path": SOURCE_PATH, "raw_s3_path": TARGET_PATH,
           "bytes": source_size, "copied_and_verified": True}
print(json.dumps(metrics))
dbutils.notebook.exit(json.dumps(metrics))
