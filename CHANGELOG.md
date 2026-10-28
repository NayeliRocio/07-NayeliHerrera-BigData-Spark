# Changelog

Todos los cambios relevantes del proyecto se documentan en este archivo.

## [1.0.0] - 2026-09-21

### Agregado
- Estructura inicial del proyecto Big Data con Spark.
- Separación en capas `domain`, `application` e `infrastructure`.
- Adaptador `CsvInputAdapter` para lectura de fuentes CSV.
- Pipeline inicial `SparkPipeline` para limpieza y deduplicación.
- `QualityGate` para validaciones básicas de calidad.
- Dataset deportivo de ejemplo.
- Prueba unitaria del control de calidad.
- Documentación de arquitectura y evidencias.
- README de la versión 1.0.0.

### Pendiente
- Integración de fuentes reales priorizadas del IPD.
- Capas RAW/Bronze, Silver y Gold.
- Indicadores y visualizaciones deportivas.
- Despliegue cloud.
