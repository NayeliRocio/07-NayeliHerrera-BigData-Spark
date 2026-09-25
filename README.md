# IPD — Inteligencia Deportiva | Java + Apache Spark

**Estudiante:** Nayeli Rocío Herrera Albino · **N.º:** 07 · **Curso:** Big Data  
**Versión de trabajo:** 2.0.0 (preparación S07; no publicada todavía como release)

## Corrección del proyecto

Esta rama reemplaza la arquitectura anterior en **Python/PySpark** por el proyecto
en **Java, Maven y Apache Spark para Java** solicitado por el docente.
La versión 1.0.0 anterior se conserva únicamente en el historial de Git.

## Arquitectura

Proyecto multi-módulo Maven basado en la distribución vista en el repositorio de
referencia del docente, adaptado al caso académico IPD:

- `contracts`: modelos compartidos `Deportista` y `ResumenDisciplina`.
- `spark-worker`: lectura de CSV, limpieza, validación, deduplicación y resumen por disciplina.
- `backend-api`: servicio Spring Boot WebFlux con endpoints de demostración.
- `frontend`: interfaz HTML servida por Spring Boot.

El CSV de muestra es **sintético**, no una fuente oficial del IPD.

## Requisitos

JDK 17 y Maven 3.9+ disponibles en PATH. Las dependencias se descargan desde Maven Central
en la primera compilación; la versión Spark está alineada con el ejemplo de clase (4.1.2).

```bash
mvn clean verify
```

Para ejecutar la API y la interfaz (desde la raíz tras `mvn install`):

```bash
mvn -pl backend-api spring-boot:run
mvn -pl frontend spring-boot:run
```

Abrir `http://localhost:8081`; API de estado: `http://localhost:8080/api/status`.

Para ejecutar el worker Spark local (desde la raíz, después de `mvn install`):

```bash
mvn -pl spark-worker exec:java -Dexec.mainClass=pe.edu.vallegrande.ipd.worker.SparkWorkerApplication
```

El entorno local de Spark puede requerir opciones adicionales de Java y red según el sistema.

## Alcance real de esta versión

Estructura Java, Maven multi-módulo, contrato compartido, transformación simple con Spark,
API y frontend de muestra, documentación y test unitario de calidad. **No se declara**
que los componentes estén desplegados ni integrados con datos reales del IPD.

## Release

Antes de crear la tag y release `v2.0.0`, integrar esta arquitectura al repositorio
**institucional** y ejecutar su compilación/pruebas. El historial en Python no debe
publicarse como la nueva arquitectura Java.

Más detalles: `docs/architecture.md` y `RELEASE_NOTES.md`.
