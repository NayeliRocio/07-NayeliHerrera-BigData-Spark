# Proyecto Big Data con Spark

- **Estudiante:** Nayeli Rocio Herrera Albino
- **Número de orden:** 07
- **Proyecto asignado:** IPD
- **Usuario GitHub:** @NayeliRocio
- **Versión actual:** 1.0.0

## Inteligencia Deportiva – IPD

Proyecto académico orientado a la integración y preparación de información deportiva mediante Apache Spark. Esta primera versión establece el entorno, la arquitectura inicial y componentes base para incorporar fuentes deportivas, aplicar controles de calidad y preparar los datos para etapas posteriores de análisis.

## Estructura

```text
.
├── data/
│   └── sample/
│       └── deportistas.csv
├── docs/
│   ├── architecture.md
│   └── evidencias/
│       └── README.md
├── src/
│   ├── application/
│   │   └── spark_pipeline.py
│   ├── domain/
│   │   └── quality_gate.py
│   ├── infrastructure/
│   │   └── csv_input_adapter.py
│   └── main.py
├── tests/
│   └── test_quality_gate.py
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── requirements.txt
└── README.md
```

## Arquitectura inicial

- **Domain:** reglas de calidad del dato.
- **Application:** procesamiento y preparación mediante Spark.
- **Infrastructure:** adaptadores de entrada de datos.
- **Data:** datos controlados para pruebas.

Flujo inicial:

```text
CSV → CsvInputAdapter → SparkPipeline → datos preparados
                     ↘ QualityGate
```

## Entorno

- Python 3.11 o superior recomendado.
- Apache Spark / PySpark 4.1.2.
- pytest para pruebas automatizadas.

## Instalación

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
python src/main.py
```

## Pruebas

```bash
pytest -q
```

La prueba incluida comprueba que `QualityGate` detecte registros deportivos con campos obligatorios incompletos.

## Git Flow aplicado

```text
main
  └── develop
       └── feature/s05-entorno-arquitectura
       └── release/1.0.0
```

Flujo de la entrega:

1. `develop` creado desde `main`.
2. `feature/s05-entorno-arquitectura` creado desde `develop`.
3. Avance desarrollado mediante commits en la rama feature.
4. Pull Request de feature hacia develop.
5. `release/1.0.0` creado desde develop.
6. Actualización de README, evidencias y CHANGELOG.
7. Pull Request de release hacia main.
8. Publicación de `v1.0.0` sobre main.

## Alcance v1.0.0

Incluye:

- estructura inicial del proyecto;
- lectura de archivos CSV con Spark;
- limpieza y deduplicación básica;
- validación inicial de calidad;
- datos de muestra;
- prueba unitaria;
- documentación de arquitectura;
- documentación de la entrega.

## Pendiente para siguientes versiones

- integración de fuentes oficiales priorizadas del IPD;
- persistencia por capas RAW/Bronze, Silver y Gold;
- reglas de calidad adicionales;
- indicadores deportivos;
- integración con almacenamiento cloud;
- automatización completa del pipeline.
