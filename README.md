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

## Integración Databricks y Amazon S3

El Job **IPD - GitHub sync y S3 a Silver-Gold** procesa el dataset de eventos internacionales en cuatro tareas: sincroniza el Git Folder, copia el CSV privado desde el volumen de carga a S3 `raw/`, valida y transforma las 55,027 filas a Delta Silver, y genera y relee el CSV Gold desde S3 para crear una tabla Delta Gold.

- Entrada real: `s3://ipd-nayeli-s3/raw/deportistas_eventos_internacionales.csv`.
- Silver: `s3://ipd-nayeli-s3/silver/eventos_internacionales` → `ipd_catalog.silver.eventos_internacionales`.
- Gold: `s3://ipd-nayeli-s3/gold/participaciones_por_federacion_pais.csv` → `ipd_catalog.gold.participaciones_por_federacion_pais`.
- Gold agrupa participaciones por federación y país del evento; `ITEM` es el identificador único. El total mide registros de participación, no personas únicas.
- El CSV no se incluye en GitHub; queda en un volumen privado de Unity Catalog y el Job lo copia al bucket mediante la identidad IAM existente.

GitHub Actions valida y sincroniza el Git Folder en cada **push a `main`**. El Job de Databricks está programado diariamente a las **07:00, America/Lima**, y puede ejecutarse también manualmente desde Jobs & Pipelines.

- [Workflow en Databricks](https://dbc-6d9a3ebe-2368.cloud.databricks.com/jobs/1010035654278929?o=7474649658925615)
- Definición reproducible: `databricks/ipd_workflow.json`.
- External Location: `ipd-nayeli-s3-n`, con la credencial IAM existente del workspace.
- No se incluyen claves AWS ni tokens en el código. GitHub Actions utiliza el secreto cifrado `DATABRICKS_TOKEN` y las variables `DATABRICKS_HOST` y `DATABRICKS_REPO_ID`.
- La lectura validada es CSV; Excel no forma parte de esta ejecución.

Las capas y consultas están descritas en [docs/CAPAS_S3.md](docs/CAPAS_S3.md).

El pipeline `.github/workflows/databricks-sync.yml` valida el proyecto antes de sincronizar y guarda un artefacto que acredita el commit aplicado. En los pull requests ejecuta únicamente las pruebas. [Configuración y comparación con la referencia](docs/GITHUB_ACTIONS_DATABRICKS.md).

Para crear el workflow en este mismo workspace mediante una sesión autenticada de la CLI:

```bash
databricks jobs create --json @databricks/ipd_workflow.json --profile IPD_NAYELI
```

El job ya desplegado debe actualizarse en lugar de crear duplicados. Los identificadores y rutas del JSON corresponden al workspace de esta entrega; para otro workspace se deben adaptar.

## Componentes de procesamiento

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
- ampliar los formatos de entrada, incluido Excel;
- extender el workflow a nuevas fuentes y capas.
