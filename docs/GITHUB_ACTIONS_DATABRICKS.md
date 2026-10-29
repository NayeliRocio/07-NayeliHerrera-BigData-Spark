# GitHub Actions, Databricks y S3

## Referencia revisada

Se revisó [paulpoma15/github-databricks, commit 435c08d](https://github.com/paulpoma15/github-databricks/tree/435c08d250f58f4a28361b22ea9b05b752368620).
Su archivo `.github/workflows/pipeline.yml` ejecuta `databricks repos update` al recibir un push a `main`. La autenticación depende de secretos del environment `development`. El código publicado no permite comprobar sus secretos ni acreditar que una ejecución haya terminado correctamente.

El notebook de la referencia lee CSV con Spark mediante Unity Catalog y registra una tabla. Sus rutas, tabla y separador `;` corresponden a sus propios datos. El proyecto IPD de Nayeli utiliza su bucket `ipd-nayeli-s3`, su tabla `ipd_catalog.silver.deportistas` y CSV separado por comas.

## Adaptación aplicada

| Componente | Implementación IPD |
| --- | --- |
| Evento de sincronización | Push a `main` y ejecución manual desde Actions |
| Pull requests | Pruebas, sin acceso a Databricks |
| Autenticación | Token de Databricks almacenado como secreto cifrado de GitHub Actions |
| Actualización del Git Folder | API Repos, equivalente al comando `databricks repos update` |
| Verificación | Se comprueban repositorio, rama y SHA completo después de actualizar |
| Evidencia | Artefacto `databricks-sync-<SHA>` en la ejecución de Actions |
| Procesamiento S3 | Job Databricks diario a las 07:00, America/Lima: copia fuente → Silver → Gold |
| Fuente | CSV real de 55,027 registros, cargado fuera del repositorio en un volumen privado y copiado a `raw/` de S3 |
| Tabla Silver | `ipd_catalog.silver.eventos_internacionales` |
| Archivo Gold consumido desde S3 | `gold/participaciones_por_federacion_pais.csv` → `ipd_catalog.gold.participaciones_por_federacion_pais` |

Los pasos de Actions están fijados a commits de sus repositorios oficiales. La sincronización falla si faltan credenciales, si el Git Folder pertenece a otro repositorio o si el commit final no coincide con el push. No descarta cambios locales por la fuerza.

## Configuración del repositorio

- Variable `DATABRICKS_HOST`: `https://dbc-6d9a3ebe-2368.cloud.databricks.com`.
- Variable `DATABRICKS_REPO_ID`: `152918773774445`.
- Secreto `DATABRICKS_TOKEN`: almacenado cifrado en GitHub; su valor no está en este repositorio.
- El token configurado vence el **26 de enero de 2027 a las 20:54, America/Lima**. Se debe renovar el secreto antes de esa fecha para mantener la sincronización desde Actions. La autenticación nativa del job diario es independiente de ese secreto.

La cuenta Free Edition no tiene acceso a las API de cuenta necesarias para configurar la federación OIDC de un service principal. Se utiliza un token con vigencia limitada para este pipeline.

## Comprobación de la entrega

En [Actions](https://github.com/NayeliRocio/07-NayeliHerrera-BigData-Spark/actions/workflows/databricks-sync.yml), abrir la ejecución de `main` y verificar que **Validar proyecto** y **Sincronizar y verificar Git Folder** estén en verde. Descargar el artefacto y comprobar `status: verified`, `branch: main` y `head_commit_id`.

La ejecución con el dataset real terminó correctamente: se copiaron 10,422,598 bytes a S3, se conservaron 55,027 filas Silver y se generaron 1,084 grupos Gold (55,027 participaciones). La evidencia está en `docs/evidencias/dataset_real_s3_2026-10-28.json`; la evidencia previa de cinco filas de muestra permanece separada en `docs/evidencias/integracion_databricks_s3_2026-10-28.json`.

Documentación oficial: [GitHub Actions con Databricks](https://docs.databricks.com/aws/en/dev-tools/ci-cd/github), [secretos de Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) y [límites de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
