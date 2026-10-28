# S5 — Estado de evidencias revisadas

Revisión de los materiales proporcionados el 27 de octubre de 2026, hora de Lima. Los estados describen la evidencia disponible; no son una calificación ni certifican recursos externos que no se ejecutaron.

## Admisibilidad

| Requisito | Estado de la evidencia |
|---|---|
| Plan de acción hasta sprint 3 | No se adjuntó el plan para revisar. |
| Actas de reuniones | No se adjuntaron actas. No deben inventarse reuniones ni acuerdos. |
| Carpetas organizadas por sprint | Pendiente de revisar la organización compartida del equipo. |
| GitHub actualizado | Cambios publicados en `feature/s5-evaluacion-integraciones`, PR #4 hacia `develop`. Actions aprobó la validación; el job de sincronización cloud quedó omitido por configuración pendiente. El PR está en borrador y no se ha integrado. |

## Criterios por curso

| Curso | Criterio | Puntos | Evidencia y pendiente |
|---|---|---:|---|
| Administración | Objetivo y alcance | 1 | README contiene alcance inicial del proyecto IPD. Debe contrastarse con el informe y sprint 3 del equipo. |
| Administración | Stakeholders | 1 | No se aportó una matriz o descripción para verificar. |
| Administración | Planificación fundamentada | 1 | Falta revisar plan de acción, responsables y fechas reales. |
| Administración | Historias completadas | 1 | Existen notas de validación parcial de US2 en este repositorio. Faltan las historias del equipo, criterios de aceptación y evidencia vinculada. |
| IA | GitHub → Git Folder mediante pipeline | 2 | Workflow y script publicados con validación del SHA. El Git Folder real fue visible en `feature/s11-s3-genie`, pero Databricks bloqueó el control automatizado de su consola. Falta configurar y ejecutar la sincronización mediante una conexión autorizada. |
| IA | Databricks → S3, lectura CSV/Excel | 2 | Notebook independiente de lectura CSV preparado. Falta confirmar bucket/objeto, permisos y ejecución en Databricks. |
| FCS | Gitflow y Conventional Commits en GitLab | 1 | Los repositorios GitLab requieren acceso. No se verificaron sus ramas, commits, tags ni releases. El historial de GitHub no sustituye esta evidencia. |
| FCS | 5 atributos ISO 25010:2011 | 1 | Pendiente documento vinculado al producto y evidencia verificable del job Spark. Las métricas de calidad de datos deben distinguirse de los atributos de calidad del software. |
| FCS | 7 fases Medallion y nomenclatura en S3 | 1 | El notebook adjunto muestra RAW, SILVER, GOLD y LOGS. Eso no verifica las siete fases pedidas. Falta confirmar la nomenclatura exacta del curso e inspeccionar S3. |
| FCS | 5 pruebas del job con JUnit + Mockito | 1 | La rama `feature/s07-java-architecture` contiene 2 métodos JUnit y no declara Mockito. Falta revisar el job de Nayeli en GitLab e implementar allí las 5 pruebas requeridas. Las pruebas Python de sincronización no sustituyen este criterio. |
| Big Data | Explicar Medallion | 1 | El notebook compartido documenta Bronze/RAW, Silver y Gold. Debe relacionarse con el diagrama del proyecto. |
| Big Data | Ingesta y limpieza | 1 | La copia adjunta muestra ingesta y limpieza de seis fuentes IPD con salidas guardadas. No se reejecutó ni se modificó el notebook. |
| Big Data | Transformación para análisis | 1 | La copia adjunta muestra un CSV Gold unificado de 29 columnas y siete tipos de registro. Falta verificar su consumo actual por la aplicación. |
| Big Data | Prototipo de dashboard | 1 | El repositorio web requiere acceso. No se verificaron pantallas ni conexión al CSV Gold. |
| Distribuidos | Prototipo Figma | 1 | No se proporcionó el enlace del prototipo. |
| Distribuidos | Carpetas features | 1 | Falta inspeccionar `vg-web-inteligenciadeportiva`. |
| Distribuidos | Dashboard | 1 | Falta verificar la ejecución del frontend. |
| Distribuidos | Gráficos con datos en memoria | 1 | Falta verificar el frontend. Debe indicarse de forma visible qué gráficos usan datos de muestra/en memoria y cuáles provienen de una fuente real. |

## Orden de cierre

1. Acceder a `vg-jobs-inteligenciadeportiva`, identificar la rama y el job de Nayeli, revisar los tags existentes e implementar las pruebas del job. Después preparar y publicar la primera versión que corresponda al historial real; no crear un tag desde un commit supuesto.
2. Confirmar cuenta AWS y bucket/objeto a utilizar. Mantener privado el bucket y conceder únicamente el acceso necesario.
3. Configurar y ejecutar la sincronización y la lectura S3 descritas en `S5_INTEGRACION_DATABRICKS.md`.
4. Revisar frontend y referencia de Valery. El repositorio de referencia devolvió 404 con el acceso disponible; no se derivó una paleta ni una estructura de archivos inventadas.
5. Reunir Figma, plan, actas e historias de usuario del equipo para completar las evidencias documentales.

El pipeline unificado compartido queda reservado a Freddy. Los totales de sus salidas son registros de distintos tipos; no deben presentarse como una cantidad de deportistas únicos.

## Validación de esta entrega

- 11 pruebas Python aprobadas localmente.
- GitHub Actions, ejecución `40631710870`: validación correcta; sincronización cloud omitida. Esta ejecución no acredita conexión a Databricks.
- Sesión Databricks verificada y Git Folder identificado; ninguna ejecución del job ni lectura S3 verificada.
- La consola AWS resultó inaccesible desde el navegador disponible. No se creó ni modificó un bucket.
- GitLab rechazó el inicio de sesión con `Invalid login or password`; no se crearon tags, releases ni cambios del job.
