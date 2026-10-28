# Evidencia parcial de US2 — validación mínima de datos de muestra

- Fecha de ejecución: 2026-09-27T20:06:26Z (UTC).
- Fuente: `data/sample/deportistas.csv` del repositorio, rama `main`.
- Regla ejecutada: `QualityGate.evaluate` de `src/domain/quality_gate.py`, con Python y biblioteca estándar (`csv.DictReader`).
- Procedimiento: leer las filas del CSV como diccionarios y evaluar los campos obligatorios `id`, `nombre` y `disciplina`.
- Salida observada:

```text
archivo=deportistas.csv
filas=5; validas=4; invalidas=1; is_valid=False
verificacion=APROBADA (reglas minimas de campos obligatorios)
ids_duplicados=1 (conteo descriptivo del CSV, no resultado Spark)
```

La fila con nombre vacío se clasifica inválida. El duplicado por `id` se contó directamente en el CSV; no se ejecutó el pipeline Spark. Esta evidencia verifica solo la regla mínima de campos obligatorios y la existencia del caso de prueba. No demuestra integración de varias fuentes, estandarización completa, persistencia Gold, trazabilidad ni ejecución de `pytest` o Spark.

Para repetir:

```python
import csv
from src.domain.quality_gate import QualityGate
with open("data/sample/deportistas.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
result = QualityGate().evaluate(rows)
assert (result.total_rows, result.valid_rows, result.invalid_rows, result.is_valid) == (5, 4, 1, False)
```
