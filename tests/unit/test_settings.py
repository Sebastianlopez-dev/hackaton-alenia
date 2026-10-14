"""Typed environment settings and secret redaction."""

import pytest

from hackaton_alenia.settings import Settings, load_settings


class TestModeValidation:
    def test_simulation_is_default(self):
        settings = load_settings()
        assert settings.alenia_mode == "simulation"

    def test_live_mode_is_accepted(self):
        settings = load_settings({"ALENIA_MODE": "live"})
        assert settings.alenia_mode == "live"

    def test_blank_values_from_env_example_count_as_unset(self):
        settings = load_settings({"ALENIA_MODE": "", "DATABRICKS_HOST": "  ", "DATABRICKS_TOKEN": ""})
        assert settings.alenia_mode == "simulation"
        assert settings.databricks_host is None
        assert settings.databricks_token is None

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError) as exc_info:
            load_settings({"ALENIA_MODE": "production"})
        message = str(exc_info.value)
        assert "ALENIA_MODE" in message
        assert "'simulation' or 'live'" in message


class TestSecretRedaction:
    def _live_settings(self):
        return load_settings(
            {
                "ALENIA_MODE": "live",
                "DATABRICKS_HOST": "https://adb-123.azuredatabricks.net",
                "DATABRICKS_TOKEN": "super-secret-token",
                "DATABRICKS_WAREHOUSE_ID": "abc123",
                "DATABRICKS_CATALOG": "catalog",
                "DATABRICKS_SCHEMA": "schema",
                "DATABRICKS_VECTOR_SEARCH_INDEX_NAME": "index",
                "OPENPROJECT_BASE_URL": "https://openproject.example.com",
                "OPENPROJECT_API_KEY": "super-secret-key",
                "OPENPROJECT_PROJECT_IDENTIFIER": "proj",
            }
        )

    def test_repr_hides_token(self):
        text = repr(self._live_settings())
        assert "super-secret-token" not in text
        assert "super-secret-key" not in text
        assert "***" in text

    def test_str_hides_token(self):
        text = str(self._live_settings())
        assert "super-secret-token" not in text
        assert "super-secret-key" not in text

    def test_structured_dumps_hide_secrets(self):
        settings = self._live_settings()
        for text in (str(settings.model_dump()), settings.model_dump_json()):
            assert "super-secret-token" not in text
            assert "super-secret-key" not in text

    def test_the_secret_value_is_still_available_to_adapters(self):
        settings = self._live_settings()
        assert settings.databricks_token is not None
        assert settings.openproject_api_key is not None
        assert settings.databricks_token.get_secret_value() == "super-secret-token"
        assert settings.openproject_api_key.get_secret_value() == "super-secret-key"

    def test_mode_validation_error_does_not_leak_secrets_present_in_env(self):
        with pytest.raises(ValueError) as exc_info:
            load_settings(
                {
                    "ALENIA_MODE": "invalid",
                    "DATABRICKS_TOKEN": "super-secret-token",
                }
            )
        assert "ALENIA_MODE" in str(exc_info.value)
        assert "super-secret-token" not in str(exc_info.value)


class TestVectorSearchColumns:
    def test_empty_by_default(self):
        settings = load_settings()
        assert settings.vector_search_columns == []

    def test_comma_separated_env_var_is_split(self):
        settings = load_settings({"ALENIA_VECTOR_SEARCH_COLUMNS": "id, title , description"})
        assert settings.vector_search_columns == ["id", "title", "description"]

    def test_explicit_list_is_accepted(self):
        settings = Settings(vector_search_columns=["id", "text"])
        assert settings.vector_search_columns == ["id", "text"]


class TestPathConstants:
    def test_path_constants_still_exist(self):
        from hackaton_alenia import settings

        assert settings.CASES_DIR.name == "cases"
        assert settings.EXPECTED_DIR.name == "expected"
        assert settings.CASE_PATH.name == "uc1_missing_mapping_s.json"
