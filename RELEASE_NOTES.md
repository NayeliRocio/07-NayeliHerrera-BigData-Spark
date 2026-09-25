# Borrador de release — v2.0.0

**Proyecto:** IPD — Inteligencia Deportiva  
**Estudiante:** Nayeli Rocío Herrera Albino  
**Estado:** PREPARACIÓN; no publicar sin integración y comprobación en Valle Grande.

## Cambio principal

Migración de la estructura inicial Python/PySpark a la arquitectura Java del curso.

## Componentes

- Multi-módulo Maven: contracts, spark-worker, backend-api y frontend.
- Worker Apache Spark en Java con datos deportivos sintéticos de prueba.
- Contratos Java compartidos.
- API HTTP y frontend de demostración.
- Pruebas unitarias de calidad y documentación.

## Validación pendiente

- Compilar con `mvn clean verify` en un equipo con JDK/Maven y dependencias.
- Confirmar acceso al repositorio institucional.
- Integrar allí la rama de desarrollo y publicar tag/release `v2.0.0`.
