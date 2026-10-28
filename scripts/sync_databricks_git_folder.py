"""Sincroniza un Git Folder existente y comprueba su rama y commit.

Usa DATABRICKS_TOKEN desde el entorno. No crea credenciales, carpetas ni jobs.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


@dataclass(frozen=True)
class SyncConfig:
    host: str
    token: str = field(repr=False)
    repo_id: str
    repository: str
    branch: str
    expected_commit: str

    @classmethod
    def from_env(cls, env):
        names = {
            "host": "DATABRICKS_HOST",
            "token": "DATABRICKS_TOKEN",
            "repo_id": "DATABRICKS_REPO_ID",
            "repository": "GITHUB_REPOSITORY",
            "branch": "DATABRICKS_BRANCH",
            "expected_commit": "EXPECTED_COMMIT",
        }
        values = {key: env.get(name, "").strip() for key, name in names.items()}
        missing = [name for key, name in names.items() if not values[key]]
        if missing:
            raise ValueError("Falta configurar: " + ", ".join(missing))
        host = urlsplit(values["host"])
        if (
            host.scheme != "https"
            or not (host.hostname or "").endswith(".cloud.databricks.com")
            or host.netloc != host.hostname
            or host.path not in ("", "/")
            or host.query
            or host.fragment
        ):
            raise ValueError("DATABRICKS_HOST debe ser el origen HTTPS del workspace AWS.")
        if not re.fullmatch(r"[1-9][0-9]*", values["repo_id"]):
            raise ValueError("DATABRICKS_REPO_ID debe ser el ID numérico del Git Folder.")
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", values["repository"]):
            raise ValueError("GITHUB_REPOSITORY debe tener el formato propietario/repositorio.")
        if not re.fullmatch(r"[0-9a-f]{40}", values["expected_commit"]):
            raise ValueError("EXPECTED_COMMIT debe ser un SHA completo de Git.")
        values["host"] = values["host"].rstrip("/")
        return cls(**values)


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # El encabezado de autenticación permanece en el workspace configurado.
        return None


class ReposClient:
    def __init__(self, config):
        self.config = config
        self.opener = build_opener(NoRedirects())

    def request(self, method, payload=None):
        request = Request(
            f"{self.config.host}/api/2.0/repos/{self.config.repo_id}",
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={
                "Authorization": "Bearer " + self.config.token,
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            with self.opener.open(request, timeout=60) as response:
                body = response.read()
                return json.loads(body) if body else {}
        except HTTPError as exc:
            raise RuntimeError(
                f"Databricks devolvió HTTP {exc.code}. Revisa acceso y configuración."
            ) from None
        except URLError:
            raise RuntimeError("No se pudo conectar al workspace de Databricks.") from None

    def get(self):
        return self.request("GET")

    def update(self, branch):
        return self.request("PATCH", {"branch": branch})


def assert_repository(info, repository):
    remote = urlsplit(info.get("url", ""))
    path = remote.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if (
        remote.scheme != "https"
        or remote.netloc != "github.com"
        or path.casefold() != repository.casefold()
        or remote.query
        or remote.fragment
    ):
        raise ValueError("El Git Folder pertenece a otro repositorio. No se actualizará.")


def synchronize(client, config):
    before = client.get()
    assert_repository(before, config.repository)
    client.update(config.branch)
    after = client.get()
    assert_repository(after, config.repository)
    if after.get("branch") != config.branch:
        raise RuntimeError("La rama del Git Folder no coincide con la rama solicitada.")
    if after.get("head_commit_id") != config.expected_commit:
        raise RuntimeError(
            "El commit del Git Folder no coincide con GitHub. "
            "Comprueba si la rama avanzó y ejecuta el flujo más reciente."
        )
    return {
        "status": "verified",
        "repository": config.repository,
        "repo_id": config.repo_id,
        "branch": config.branch,
        "head_commit_id": after["head_commit_id"],
    }


def main():
    try:
        config = SyncConfig.from_env(os.environ)
        evidence = synchronize(ReposClient(config), config)
        output = Path("artifacts/databricks-sync.json")
        output.parent.mkdir(exist_ok=True)
        output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(evidence))
        return 0
    except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Sincronización no verificada: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
