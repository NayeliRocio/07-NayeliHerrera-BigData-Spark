from unittest.mock import Mock

import pytest

from scripts.sync_databricks_git_folder import (
    ReposClient,
    SyncConfig,
    synchronize,
)


def environment():
    return {
        "DATABRICKS_HOST": "https://dbc-example.cloud.databricks.com/",
        "DATABRICKS_TOKEN": "test-credential",
        "DATABRICKS_REPO_ID": "123",
        "GITHUB_REPOSITORY": "NayeliRocio/07-NayeliHerrera-BigData-Spark",
        "DATABRICKS_BRANCH": "feature/s5-evaluacion-integraciones",
        "EXPECTED_COMMIT": "a" * 40,
    }


def repo_info(config, **overrides):
    return {
        "url": f"https://github.com/{config.repository}.git",
        "branch": config.branch,
        "head_commit_id": config.expected_commit,
        **overrides,
    }


def test_missing_configuration_fails_before_network_access():
    env = environment()
    del env["DATABRICKS_TOKEN"]
    with pytest.raises(ValueError, match="Falta configurar: DATABRICKS_TOKEN"):
        SyncConfig.from_env(env)


@pytest.mark.parametrize("host", [
    "http://dbc-example.cloud.databricks.com",
    "https://dbc-example.cloud.databricks.com.attacker.example",
    "https://user@dbc-example.cloud.databricks.com",
    "https://dbc-example.cloud.databricks.com/?secret=value",
])
def test_rejects_hosts_that_can_leak_credentials(host):
    with pytest.raises(ValueError, match="DATABRICKS_HOST"):
        SyncConfig.from_env({**environment(), "DATABRICKS_HOST": host})


def test_does_not_update_an_unrelated_git_folder():
    config = SyncConfig.from_env(environment())
    client = Mock()
    client.get.return_value = repo_info(config, url="https://github.com/other/project.git")
    with pytest.raises(ValueError, match="otro repositorio"):
        synchronize(client, config)
    client.update.assert_not_called()


def test_reads_back_branch_and_exact_commit_after_update():
    config = SyncConfig.from_env(environment())
    client = Mock()
    client.get.side_effect = [repo_info(config, branch="main"), repo_info(config)]
    evidence = synchronize(client, config)
    client.update.assert_called_once_with(config.branch)
    assert client.get.call_count == 2
    assert evidence["status"] == "verified"
    assert evidence["head_commit_id"] == config.expected_commit
    assert "token" not in evidence
    assert config.token not in repr(config)


@pytest.mark.parametrize("overrides", [
    {"branch": "main"},
    {"head_commit_id": "b" * 40},
])
def test_mismatched_readback_is_not_reported_as_success(overrides):
    config = SyncConfig.from_env(environment())
    client = Mock()
    client.get.side_effect = [repo_info(config), repo_info(config, **overrides)]
    with pytest.raises(RuntimeError):
        synchronize(client, config)


def test_http_errors_do_not_expose_response_body_or_token():
    from urllib.error import HTTPError

    config = SyncConfig.from_env(environment())
    client = ReposClient(config)
    client.opener = Mock()
    client.opener.open.side_effect = HTTPError(config.host, 401, config.token, {}, None)
    with pytest.raises(RuntimeError, match="HTTP 401") as exc:
        client.get()
    assert config.token not in str(exc.value)
