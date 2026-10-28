# S5 — GitHub, Git Folder y lectura desde S3

Este cambio prepara la automatización y su verificación. **No acredita todavía una ejecución en Databricks ni una conexión activa con S3.** No modifica el notebook compartido `pipeline_unificado_completo.ipynb`, reservado a Freddy.

## 1. Pipeline de sincronización

Archivo: `.github/workflows/databricks-sync.yml`.

El flujo ejecuta las pruebas en los pushes y PR indicados. La sincronización cloud se habilita únicamente cuando la variable `DATABRICKS_SYNC_ENABLED` vale `true` y la rama del evento coincide con `DATABRICKS_SYNC_BRANCH`. Un resultado verde de las pruebas, con el job `sync` omitido, **no demuestra sincronización**.

Configurar en GitHub → Settings → Secrets and variables → Actions:

| Tipo | Nombre | Valor |
|---|---|---|
| Variable | `DATABRICKS_HOST` | Origen HTTPS del workspace; el observado en la captura es `https://dbc-6d9a3ebe-2368.cloud.databricks.com`. |
| Variable | `DATABRICKS_REPO_ID` | ID numérico del Git Folder exacto de este repositorio, obtenido de Databricks. No es el ID del workspace. |
| Variable | `DATABRICKS_SYNC_BRANCH` | Rama que debe seguir ese Git Folder; para probar esta entrega: `feature/s5-evaluacion-integraciones`. |
| Variable | `DATABRICKS_SYNC_ENABLED` | `true`, después de comprobar el destino y los accesos. |
| Secret | `DATABRICKS_TOKEN` | Token existente del workspace autorizado para gestionar ese Git Folder, si el workspace permite PAT. Nunca escribirlo en el repositorio. |

Se necesita una credencial Git configurada dentro de Databricks y permiso para gestionar el Git Folder. La credencial de Databricks y la credencial de Git son distintas. Si PAT no está disponible, se debe adaptar la autenticación a OAuth admitido por el workspace; no se debe habilitar este flujo con credenciales improvisadas. Databricks recomienda OAuth para nuevas integraciones.

El script consulta primero el Git Folder por ID, comprueba que su URL corresponde a este repositorio y solicita actualizar la rama. Después vuelve a consultar y exige igualdad tanto de rama como de SHA respecto al evento de GitHub. Solo entonces produce el artefacto `databricks-sync-<sha>` con `status: verified`.

La API de actualización puede rechazar cambios locales pendientes dentro del Git Folder. Deben revisarse antes de activar la automatización; este flujo no borra ni fuerza esos cambios. La versión actual no gestiona Git Folders habilitados exclusivamente mediante Git CLI si no admiten la API Repos.

### Evidencia para el criterio de IA (2 puntos)

1. Ejecución de Actions con el job **Sincronizar y verificar commit en Databricks** finalizado correctamente.
2. Artefacto JSON de esa ejecución, con rama y commit.
3. Git Folder en Databricks mostrando la misma rama y commit.

Para reejecutar desde Actions mediante `workflow_dispatch`, el archivo del workflow también debe existir en la rama predeterminada. Antes de integrarlo en `main`, el evento `push` de esta rama permite probarlo.

## 2. Lectura real desde Amazon S3

Archivo independiente: `notebooks/02_validar_lectura_s3.py`.

Se debe confirmar la cuenta AWS, el bucket accesible y la **clave exacta del CSV**. Después, una External Location de Unity Catalog debe autorizar esa ruta. La captura de una carpeta `raw/` no confirma qué archivos contiene ni concede permisos a Databricks.

El notebook recibe la URI exacta, separador, codificación, columnas requeridas y clasificación de la fuente. Lee con Apache Spark y ejecuta una agregación para comprobar que se procesó el archivo. Rechaza archivos vacíos y esquemas que no cumplen las columnas solicitadas; no escribe ni transforma el pipeline compartido. La salida JSON contiene URI, conteo, columnas, clasificación y fecha, sin imprimir filas personales.

Para una fuente oficial, la clasificación `fuente_oficial` debe apoyarse en su origen verificable; es un parámetro declarado por quien ejecuta, no una certificación automática. El archivo `data/sample/deportistas.csv` sigue siendo una muestra y debe clasificarse como `muestra` si se usa para probar conectividad.

### Rutas encontradas en los materiales

| Nombre | Dónde aparece | Qué está comprobado |
|---|---|---|
| `inteligenciaa04-deportiva-ipd` | Notebook compartido de Colab | La copia adjunta contiene salidas de una ejecución con RAW, SILVER y GOLD. No se verificó el estado actual en AWS. |
| `ipd-nayeli-s3` | Captura de la consola AWS | La captura muestra `raw/`. No se verificaron objetos, permisos ni acceso actual. |
| `ipd-noestructurados-nayeli-20260928-7314` | Archivos S11 de este repositorio | Es una ruta codificada anterior; no hay evidencia adjunta de su disponibilidad actual. |

No se creó otro bucket: primero debe verificarse cuál se utilizará y desde qué cuenta. Tampoco se sustituyen rutas del notebook S11 por un nombre supuesto.

### Evidencia para el criterio de IA (2 puntos)

1. URI exacta del CSV existente en S3 y su fuente identificada.
2. Permisos y External Location autorizados, sin exponer claves.
3. Ejecución real del notebook en Databricks con JSON `status: verified` y `row_count > 0`.

Databricks Free Edition solo dispone de cómputo serverless y limita el acceso saliente; la compatibilidad efectiva debe comprobarse en el workspace. Crear carpetas o mostrar un CSV local no acredita la lectura desde Amazon S3.

## Referencias oficiales

- [CI/CD con Git Folders](https://docs.databricks.com/aws/en/repos/ci-cd).
- [Repositorio: consultar y actualizar](https://docs.databricks.com/api/repos/v1/update-repo).
- [Conectar S3 con Unity Catalog](https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/s3).
- [Limitaciones de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
- [Autenticación PAT y recomendación de OAuth](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
