"""Typed project settings read from environment variables.

Path constants used by the local simulated demo are preserved unchanged.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "evals/cases"
EXPECTED_DIR = ROOT / "evals/expected"
CASE_PATH = CASES_DIR / "uc1_missing_mapping_s.json"
EXPECTED_PATH = EXPECTED_DIR / "uc1_missing_mapping_s.json"

class Settings(BaseModel):
    """Environment-driven configuration.

    Secrets are ``SecretStr``: ``str``, ``repr``, ``model_dump`` and
    ``model_dump_json`` all show a mask, and adapters read the value only
    through ``get_secret_value()``. A blank variable counts as unset, so the
    empty entries of ``.env.example`` are reported as missing rather than
    accepted as empty credentials.
    """

    model_config = ConfigDict(populate_by_name=True)

    alenia_mode: str = Field(default="simulation", alias="ALENIA_MODE")

    databricks_host: str | None = Field(default=None, alias="DATABRICKS_HOST")
    databricks_token: SecretStr | None = Field(default=None, alias="DATABRICKS_TOKEN")
    databricks_warehouse_id: str | None = Field(default=None, alias="DATABRICKS_WAREHOUSE_ID")
    databricks_catalog: str | None = Field(default=None, alias="DATABRICKS_CATALOG")
    databricks_schema: str | None = Field(default=None, alias="DATABRICKS_SCHEMA")
    databricks_vector_search_index_name: str | None = Field(
        default=None, alias="DATABRICKS_VECTOR_SEARCH_INDEX_NAME"
    )

    openproject_base_url: str | None = Field(default=None, alias="OPENPROJECT_BASE_URL")
    openproject_api_key: SecretStr | None = Field(default=None, alias="OPENPROJECT_API_KEY")
    openproject_project_identifier: str | None = Field(
        default=None, alias="OPENPROJECT_PROJECT_IDENTIFIER"
    )

    # Which columns the Mosaic AI Vector Search index should return. The
    # official column set is unknown, so it is a setting, not a guess in code.
    vector_search_columns: list[str] = Field(default_factory=list, alias="ALENIA_VECTOR_SEARCH_COLUMNS")

    @field_validator("alenia_mode")
    @classmethod
    def _validate_mode(cls, value: str) -> str:
        if value not in {"simulation", "live"}:
            raise ValueError("ALENIA_MODE must be 'simulation' or 'live'")
        return value

    @field_validator("vector_search_columns", mode="before")
    @classmethod
    def _split_columns(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value



def load_settings(env: dict[str, str] | None = None) -> Settings:
    """Build settings from ``os.environ`` or an optional mapping.

    The mapping is useful for tests; it is merged on top of the process
    environment so callers can override individual variables.
    """
    source = dict(os.environ)
    if env is not None:
        source.update(env)
    kwargs: dict[str, Any] = {}
    for field_name, field_info in Settings.model_fields.items():
        alias = field_info.alias or field_name
        if source.get(alias, "").strip():
            kwargs[alias] = source[alias]
    return Settings.model_validate(kwargs)
