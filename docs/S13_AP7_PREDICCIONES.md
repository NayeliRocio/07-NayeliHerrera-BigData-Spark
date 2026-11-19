# S13 AP7 — Tres predicciones con Silver

## Objetivo

Estimar para el siguiente año posterior al último año disponible:

1. las participaciones registradas por federación;
2. las participaciones asociadas al país anfitrión;
3. las participaciones por nombre de evento.

El indicador cuenta registros `ITEM` distintos. No significa deportistas únicos, medallas ni probabilidad de ganar una competencia.

## Método y lectura

El notebook `notebooks/03_predicciones_s13.py` y la consulta `sql/04_predicciones_s13.sql` usan `ipd_catalog.silver.eventos_internacionales`. Interpretan `fecha_inicio` en formatos ISO (`yyyy-MM-dd`), día/mes/año, año/mes/día y mes/día/año. El último año que aparezca en los datos se trata como incompleto y se excluye. Sobre los tres años calendario anteriores se ajusta una tendencia lineal por categoría; los años sin registros de una categoría se completan con cero. Solo se muestran categorías presentes en al menos dos años de entrenamiento y las proyecciones negativas se limitan a cero.

El notebook presenta el año objetivo, los años usados, la cantidad de fechas no interpretadas y las 10 categorías con mayor valor estimado para cada una de las tres predicciones. Ejecutarlo en Databricks después de que Silver esté actualizado. Si faltan fechas o no hay tres años de cobertura suficientes, no presentar los resultados como pronóstico: explicar que la base no permite sostener una estimación temporal.

## Limitaciones

- Es una tendencia exploratoria de tres puntos, sin intervalos de confianza ni validación retrospectiva.
- El conteo futuro presupone que la tendencia reciente continúa y la cobertura del dataset es comparable entre años.
- Los nombres de eventos pueden cambiar entre ediciones; una categoría no recurrente queda fuera.
- El país es el país del evento registrado, no necesariamente una predicción oficial de la sede futura.
- No se predicen ganadores deportivos: `puesto` requiere normalización y resultados comparables para modelar ese objetivo.

## Cómo presentar

1. En Databricks, abrir y ejecutar `notebooks/03_predicciones_s13.py` con acceso a la tabla Silver.
2. Mostrar los tres grupos de resultados y explicar años de entrenamiento, año objetivo y limitaciones.
3. Abrir `sql/04_predicciones_s13.sql` para mostrar la consulta equivalente en SQL.

Las cifras finales dependen de la versión actual de Silver y deben leerse de la salida de Databricks, no de un ranking histórico guardado.
