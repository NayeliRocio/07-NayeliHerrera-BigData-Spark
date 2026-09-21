# Arquitectura inicial

La entrega S05 utiliza una separación simple por responsabilidades:

- **domain**: reglas de calidad independientes de Spark.
- **application**: lógica del pipeline de preparación.
- **infrastructure**: adaptadores para leer fuentes externas, inicialmente CSV.
- **data/sample**: datos controlados para pruebas locales.

Flujo inicial:

CSV → CsvInputAdapter → SparkPipeline → datos limpios y deduplicados

Esta estructura evita usar nombres de estudiantes en clases, funciones, paquetes o variables y mantiene nombres relacionados con el dominio.
