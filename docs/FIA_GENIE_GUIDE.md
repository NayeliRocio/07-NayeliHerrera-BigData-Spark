# FIA | Databricks, S3 y Genie — guía de entrega IPD

## Proyecto y repositorio

Repositorio: [07-NayeliHerrera-BigData-Spark](https://github.com/NayeliRocio/07-NayeliHerrera-BigData-Spark)  
Consultas SQL para GitHub: [sql/02_genie_queries.sql](../sql/02_genie_queries.sql)  
Workspace Databricks documentado por el proyecto: `dbc-2aa79bb9-b5b2`.

## Tablas del pipeline del proyecto

El pipeline de este repositorio define estas tablas externas de Unity Catalog:

- Silver: `ipd_catalog.silver.eventos_internacionales`, ubicación `s3://ipd-nayeli-s3/silver/eventos_internacionales`.
- Gold: `ipd_catalog.gold.participaciones_por_federacion_pais`, ubicación Delta `s3://ipd-nayeli-s3/gold/delta/participaciones_por_federacion_pais`.
- CSV Gold: `s3://ipd-nayeli-s3/gold/participaciones_por_federacion_pais.csv`.

Silver conserva el detalle por participación (`item_id`, federación, evento, país, deportista, puesto y fechas). Gold agrega participaciones por federación y país anfitrión (`federacion`, `pais_evento`, `total_participaciones`). Una participación no equivale a una persona única, una medalla ni una victoria.

## Configuración sugerida de Genie

1. En Databricks, comprobar que el Job S3 → Silver → Gold terminó correctamente y que las tablas se pueden consultar.
2. Crear un espacio Genie nuevo con nombre `IPD — Inteligencia Deportiva FIA`.
3. Agregar como fuente principal `ipd_catalog.gold.participaciones_por_federacion_pais`. Agregar `ipd_catalog.silver.eventos_internacionales` solo si se necesita detalle por evento, deportista, puesto o fecha.
4. Asegurar permisos `USE CATALOG`, `USE SCHEMA` y `SELECT` para el usuario que ejecutará las preguntas.
5. Pegar en las instrucciones del espacio:

> El dataset contiene participaciones de deportistas peruanos en eventos internacionales. Cada `item_id` identifica una participación y no necesariamente una persona única, una medalla o una victoria. Gold contiene el total de participaciones por federación y país del evento. Para detalle usa Silver. No inventes resultados, no interpretes puesto como medalla sin validar sus valores y menciona las limitaciones de cobertura temporal. Si una petición solicita una predicción, explica el método, el periodo usado y la incertidumbre; si los datos no permiten validar una tendencia, dilo claramente.

6. Abrir `sql/02_genie_queries.sql` y ejecutar las cinco consultas. Se diseñaron para las tablas reales del pipeline: ranking por federación, ranking por país, comparación por federación/país, top 3 países por federación y detalle Silver filtrable.
7. Capturar la tabla/fuente conectada y las respuestas de Genie con su SQL visible. Las consultas del repositorio son código de referencia; las capturas deben corresponder a ejecuciones reales en Databricks.

## Tres preguntas predictivas para Genie

Estas son solicitudes exploratorias que deben responderse con el método y la evidencia visibles; no se deben presentar resultados inventados. Antes, comprobar que `fecha_inicio` tiene suficientes años distintos y que sus valores se pueden interpretar como fechas.

1. **Tendencia de participaciones:** “Usando Silver, calcula las participaciones por federación y año a partir de `fecha_inicio`. Si hay por lo menos tres años completos comparables, estima la tendencia del siguiente año con una regresión lineal sencilla y muestra los datos históricos, la estimación y sus limitaciones. Si la cobertura no alcanza, informa que no hay base suficiente.”
2. **Países anfitriones:** “Resume por año el número de participaciones y eventos por `pais_evento`. Solo si existe cobertura temporal suficiente, estima qué países podrían mantener o aumentar actividad el próximo año; separa observaciones históricas de estimaciones.”
3. **Riesgo de descenso:** “Identifica federaciones con descenso en participaciones durante al menos dos periodos consecutivos, usando fechas válidas. Muestra la serie, el tamaño de muestra y una estimación prudente del riesgo de continuar el descenso; no uses el ranking Gold transversal como pronóstico.”

La tabla Gold actual es un agregado sin dimensión temporal. No permite, por sí sola, entrenar ni validar una predicción temporal. Las predicciones requieren usar Silver, revisar calidad y cobertura de fechas, registrar periodo/método/limitaciones y capturar la respuesta real de Genie.

## Evidencia y video individual

Guardar en el documento del curso:

- Captura del espacio Genie y las tablas conectadas.
- Capturas de las cinco respuestas ejecutadas en Genie, con SQL visible.
- Captura de cada una de las tres respuestas predictivas, mostrando el análisis y sus límites.
- Enlace al repositorio y al video.

Guion breve para el video (2–4 minutos):

1. Mostrar el bucket S3 del proyecto y las capas `raw/`, `silver/` y `gold/`; explicar el flujo hasta las tablas de Unity Catalog.
2. Mostrar en Databricks la tabla Silver/Gold y el espacio Genie conectado a esas tablas.
3. Hacer una pregunta SQL de ejemplo, enseñar la respuesta y el SQL generado; mostrar dónde están las cinco consultas en el repositorio.
4. Hacer las tres preguntas predictivas y explicar que son estimaciones exploratorias, no resultados oficiales ni garantías.
5. Cerrar mostrando la URL del repositorio y las evidencias guardadas en el documento.

No mostrar credenciales, tokens, claves AWS, información privada ni valores sensibles en la grabación.
