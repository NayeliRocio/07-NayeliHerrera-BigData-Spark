-- Consultas de validación y preguntas sugeridas para Genie.
-- Tabla: ipd_catalog.silver.deportistas (id, nombre, disciplina, region).

-- 1. ¿Cuántos deportistas únicos hay?
SELECT COUNT(DISTINCT id) AS deportistas_unicos FROM ipd_catalog.silver.deportistas;

-- 2. ¿Cuántos deportistas hay por disciplina?
SELECT disciplina, COUNT(DISTINCT id) AS total FROM ipd_catalog.silver.deportistas GROUP BY disciplina ORDER BY total DESC;

-- 3. ¿Cuántos deportistas hay por región?
SELECT region, COUNT(DISTINCT id) AS total FROM ipd_catalog.silver.deportistas GROUP BY region ORDER BY total DESC;

-- 4. ¿Qué disciplinas se practican en cada región?
SELECT region, disciplina, COUNT(DISTINCT id) AS total FROM ipd_catalog.silver.deportistas GROUP BY region, disciplina ORDER BY region, total DESC;

-- 5. ¿Quiénes practican voleibol en Cusco?
SELECT id, nombre, disciplina, region FROM ipd_catalog.silver.deportistas WHERE disciplina = 'Voleibol' AND region = 'Cusco' ORDER BY nombre;
