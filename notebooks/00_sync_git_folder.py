# Databricks notebook source
# MAGIC %md
# MAGIC # Sincronización GitHub → Git Folder
# MAGIC Primera tarea del workflow IPD. Usa la identidad de ejecución de Databricks; no guarda tokens.

# COMMAND ----------
import json
from databricks.sdk import WorkspaceClient

dbutils.widgets.text("repo_id", "152918773774445")
dbutils.widgets.text("git_branch", "main")
repo_id = int(dbutils.widgets.get("repo_id"))
branch = dbutils.widgets.get("git_branch")
expected_url = "https://github.com/NayeliRocio/07-NayeliHerrera-BigData-Spark"
client = WorkspaceClient()
before = client.repos.get(repo_id)
if before.url.removesuffix(".git") != expected_url:
    raise ValueError("El Git Folder no corresponde al repositorio IPD esperado")

# No se descartan cambios locales: la API debe fallar si hay conflictos.
client.repos.update(repo_id, branch=branch)
after = client.repos.get(repo_id)
if after.branch != branch or not after.head_commit_id:
    raise RuntimeError("No se pudo verificar la rama y el commit sincronizados")
result = {"repo_id": repo_id, "branch": after.branch,
          "previous_commit": before.head_commit_id, "commit": after.head_commit_id}
print(json.dumps(result))
dbutils.notebook.exit(json.dumps(result))
