"""Composition point: choose simulation or live services from settings."""

import pytest

from hackaton_alenia.integrations.databricks import DatabricksSQLClient
from hackaton_alenia.integrations.factory import ConfigurationError, LiveServices, build_services
from hackaton_alenia.integrations.openproject import OpenProjectClient
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.settings import Settings, load_settings


def _live_settings() -> Settings:
    return load_settings(
        {
            "ALENIA_MODE": "live",
            "DATABRICKS_HOST": "https://adb-123.azuredatabricks.net",
            "DATABRICKS_TOKEN": "token",
            "DATABRICKS_WAREHOUSE_ID": "warehouse",
            "DATABRICKS_CATALOG": "catalog",
            "DATABRICKS_SCHEMA": "schema",
            "DATABRICKS_VECTOR_SEARCH_INDEX_NAME": "index",
            "OPENPROJECT_BASE_URL": "https://op.example.com",
            "OPENPROJECT_API_KEY": "key",
            "OPENPROJECT_PROJECT_IDENTIFIER": "proj",
            "ALENIA_VECTOR_SEARCH_COLUMNS": "id,title",
        }
    )


def test_simulation_uses_simulated_services():
    case = {"ticket": {"id": 1, "title": "T", "description": "D"}}
    services = build_services(load_settings({"ALENIA_MODE": "simulation"}), simulated_case=case)
    assert isinstance(services, SimulatedServices)


def test_simulation_requires_fixture_case():
    with pytest.raises(ConfigurationError, match="fixture"):
        build_services(load_settings({"ALENIA_MODE": "simulation"}))


def test_live_with_missing_settings_names_the_variables():
    with pytest.raises(ConfigurationError) as exc_info:
        build_services(load_settings({"ALENIA_MODE": "live", "DATABRICKS_TOKEN": "super-secret-token"}))
    text = str(exc_info.value)
    assert "DATABRICKS_HOST" in text
    assert "OPENPROJECT_API_KEY" in text
    assert "super-secret-token" not in text


def test_live_refuses_simulated_fixture():
    case = {"ticket": {"id": 1, "title": "T", "description": "D"}}
    with pytest.raises(ConfigurationError, match="fixture"):
        build_services(_live_settings(), simulated_case=case)


def test_live_does_not_fall_back_to_simulation():
    services = build_services(_live_settings())
    assert not isinstance(services, SimulatedServices)
    assert isinstance(services, LiveServices)
    assert isinstance(services.openproject, OpenProjectClient)
    assert isinstance(services.databricks, DatabricksSQLClient)


def test_blank_live_settings_are_reported_as_missing():
    env = dict.fromkeys((
        "DATABRICKS_HOST", "DATABRICKS_TOKEN", "DATABRICKS_WAREHOUSE_ID", "DATABRICKS_CATALOG",
        "DATABRICKS_SCHEMA", "DATABRICKS_VECTOR_SEARCH_INDEX_NAME", "OPENPROJECT_BASE_URL",
        "OPENPROJECT_API_KEY", "OPENPROJECT_PROJECT_IDENTIFIER",
    ), "")
    env["ALENIA_MODE"] = "live"

    with pytest.raises(ConfigurationError) as error:
        build_services(load_settings(env))

    assert "DATABRICKS_HOST" in str(error.value)
    assert "OPENPROJECT_API_KEY" in str(error.value)
