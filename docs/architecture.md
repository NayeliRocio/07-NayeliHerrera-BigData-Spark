# Arquitectura Java — IPD (S07)

Se adopta la estructura de cuatro módulos Maven trabajada en la referencia de clase del docente; se adapta al caso **Inteligencia Deportiva — IPD**.

```text
ipd-bigdata (pom.xml, Java 17)
├── contracts/     Contratos compartidos: Deportista, ResumenDisciplina
├── spark-worker/  Ingesta CSV, limpieza, deduplicación y agregación con Spark Java
├── backend-api/   Spring Boot WebFlux, endpoints de demostración
├── frontend/      Interfaz web de demostración, servidor Spring Boot
└── data/sample/   CSV académico de prueba; no son datos reales del IPD
```

```text
CSV de prueba ─→ spark-worker ─→ Dataset limpio ─→ Resumen por disciplina
                      │
                      └──── usa contratos compartidos
backend-api ───────────────→ contratos compartidos ─→ frontend (HTTP demo)
```

**Estado del avance:** arquitectura y ejemplo funcional básico. No hay despliegue,
integración de una base de datos ni comunicación automatizada entre worker y API;
esas integraciones corresponden a iteraciones posteriores.

**Separación de responsabilidades:** no se mezcla la lógica Spark con el controlador HTTP.
El módulo contracts evita duplicación de estructuras de datos. El frontend consume una ruta
de demostración para comprobar la organización de módulos.
