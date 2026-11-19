# Databricks notebook source
# MAGIC %md
# MAGIC # S13 AP7: tres predicciones con datos Silver
# MAGIC Proyecciones exploratorias para el siguiente año posterior al último año observado. Se excluye ese último año, que puede estar incompleto, y se ajusta una tendencia lineal a los tres años calendario completos anteriores. Cada dimensión se calcula por separado.

# COMMAND ----------
from pyspark.sql import functions as F

SILVER_TABLE = "ipd_catalog.silver.eventos_internacionales"
silver = spark.table(SILVER_TABLE)

# Acepta formatos de fecha habituales sin detener el notebook por valores inválidos.
parsed_date = F.expr("""coalesce(
    try_to_timestamp(fecha_inicio, 'yyyy-MM-dd'),
    try_to_timestamp(fecha_inicio, 'dd/MM/yyyy'),
    try_to_timestamp(fecha_inicio, 'yyyy/MM/dd'),
    try_to_timestamp(fecha_inicio, 'MM/dd/yyyy')
)""")
dated = (silver
    .withColumn("fecha_parseada", parsed_date)
    .withColumn("anio", F.year("fecha_parseada"))
    .filter(F.col("anio").isNotNull() & F.col("item_id").isNotNull()))

year_bounds = dated.agg(F.max("anio").alias("ultimo_anio_observado")).first()
if year_bounds["ultimo_anio_observado"] is None:
    raise ValueError("Silver no contiene fechas de inicio reconocibles; no se pueden calcular tendencias anuales")

latest_observed = int(year_bounds["ultimo_anio_observado"])
target_year = latest_observed + 1
training_years = list(range(latest_observed - 3, latest_observed))

if len(training_years) != 3 or min(training_years) < 1900:
    raise ValueError(f"Rango anual inválido para el entrenamiento: {training_years}")

# Se recogen únicamente agregados anuales, nunca las filas personales de Silver.
annual_rows = {}
for dimension in ("federacion", "pais_evento", "evento"):
    aggregated = (dated
        .filter(F.col("anio").isin(training_years))
        .groupBy("anio", dimension)
        .agg(F.countDistinct("item_id").alias("participaciones")))
    annual_rows[dimension] = [row.asDict() for row in aggregated.collect()]

# COMMAND ----------
def forecast_dimension(rows, dimension, label, min_active_years=2):
    """OLS sobre tres años; completa con cero los años sin participaciones."""
    values = {}
    for row in rows:
        category = row.get(dimension)
        if category is None or not str(category).strip():
            continue
        key = str(category).strip()
        values.setdefault(key, {})[int(row["anio"])] = int(row["participaciones"])

    output = []
    for category, by_year in values.items():
        ys = [by_year.get(year, 0) for year in training_years]
        if sum(value > 0 for value in ys) < min_active_years:
            continue
        # Años x = 1, 2, 3; la proyección es el año x = 4.
        mean_y = sum(ys) / 3.0
        slope = sum((x - 2.0) * (y - mean_y) for x, y in zip((1.0, 2.0, 3.0), ys)) / 2.0
        projected = max(0, round(mean_y + slope * 2.0))
        output.append((label, category, target_year, *ys, round(slope, 2), projected))

    return sorted(output, key=lambda item: (-item[-1], item[1]))[:10]

predictions = []
predictions += forecast_dimension(annual_rows["federacion"], "federacion", "Federación")
predictions += forecast_dimension(annual_rows["pais_evento"], "pais_evento", "País anfitrión")
predictions += forecast_dimension(annual_rows["evento"], "evento", "Evento")

if not predictions:
    raise ValueError(
        "No hay categorías con actividad en al menos dos de los tres años completos; "
        "se requiere revisar la cobertura temporal antes de presentar proyecciones."
    )

result = spark.createDataFrame(
    predictions,
    ["prediccion", "categoria", "anio_proyectado", "participaciones_t1",
     "participaciones_t2", "participaciones_t3", "variacion_anual_estimada",
     "participaciones_estimadas"]
)

print({
    "ultimo_anio_observado_excluido": latest_observed,
    "anios_de_entrenamiento": training_years,
    "anio_objetivo": target_year,
    "fechas_sin_parsear": dated.filter(F.col("fecha_parseada").isNull()).count(),
    "metodo": "tendencia lineal OLS de 3 años; estimación truncada en cero",
})
display(result.orderBy("prediccion", F.desc("participaciones_estimadas")))
