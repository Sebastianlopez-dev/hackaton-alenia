"""Single composition point for simulated or live services."""

from __future__ import annotations

import base64
from typing import Any

import httpx

from hackaton_alenia.settings import Settings
from hackaton_alenia.ticket import Ticket

from .databricks import DatabricksSQLClient
from .openproject import OpenProjectClient
from .services_s import SimulatedServices
from .vector_search import VectorSearchClient


class ConfigurationError(Exception):
    """The requested mode cannot be satisfied with the supplied settings."""


class LiveServices:
    """Composite that delegates each capability to its official adapter."""

    def __init__(
        self,
        databricks: DatabricksSQLClient,
        openproject: OpenProjectClient,
        vector_search: VectorSearchClient,
    ):
        self.databricks = databricks
        self.openproject = openproject
        self.vector_search = vector_search

    def read_ticket(self, ticket_id: int) -> Ticket:
        return self.openproject.read_ticket(ticket_id)

    def retrieve_similar_tickets(self, query: str) -> list[dict[str, Any]]:
        return self.vector_search.retrieve_similar_tickets(query)

    def query_sql(self, sql: str) -> list[dict[str, Any]]:
        return self.databricks.query_sql(sql)

    def create_comment(self, ticket_id: int, text: str) -> dict[str, Any]:
        return self.openproject.create_comment(ticket_id, text)

    def update_status(self, ticket_id: int, status: str) -> dict[str, Any]:
        return self.openproject.update_status(ticket_id, status)


def build_services(settings: Settings, simulated_case: dict[str, Any] | None = None) -> Any:
    """Return a ``Services`` implementation chosen by ``settings.alenia_mode``.

    ``simulation`` requires a fixture case and returns ``SimulatedServices``.
    ``live`` requires every official setting to be present and returns a
    composite of the three official adapters. There is no fallback between modes
    and a simulated fixture is rejected in live mode.
    """
    if settings.alenia_mode == "simulation":
        if simulated_case is None:
            raise ConfigurationError("simulation mode requires a fixture case")
        return SimulatedServices(simulated_case)

    if settings.alenia_mode != "live":
        # Defensive: should be unreachable because Settings validates the mode.
        raise ConfigurationError("ALENIA_MODE must be 'simulation' or 'live'")

    if simulated_case is not None:
        raise ConfigurationError("live mode must not receive a simulated fixture")

    required: dict[str, object | None] = {
        "DATABRICKS_HOST": settings.databricks_host,
        "DATABRICKS_TOKEN": settings.databricks_token,
        "DATABRICKS_WAREHOUSE_ID": settings.databricks_warehouse_id,
        "DATABRICKS_CATALOG": settings.databricks_catalog,
        "DATABRICKS_SCHEMA": settings.databricks_schema,
        "DATABRICKS_VECTOR_SEARCH_INDEX_NAME": settings.databricks_vector_search_index_name,
        "OPENPROJECT_BASE_URL": settings.openproject_base_url,
        "OPENPROJECT_API_KEY": settings.openproject_api_key,
        "OPENPROJECT_PROJECT_IDENTIFIER": settings.openproject_project_identifier,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise ConfigurationError(
            "Live mode missing required settings: " + ", ".join(missing)
        )

    # The missing-variable check guarantees these are strings; assert to satisfy
    # static type checkers without repeating the error message.
    assert settings.databricks_host is not None
    assert settings.databricks_token is not None
    assert settings.databricks_warehouse_id is not None
    assert settings.databricks_catalog is not None
    assert settings.databricks_schema is not None
    assert settings.databricks_vector_search_index_name is not None
    assert settings.openproject_base_url is not None
    assert settings.openproject_api_key is not None
    assert settings.openproject_project_identifier is not None

    databricks_client = httpx.Client(
        base_url=settings.databricks_host,
        headers={"Authorization": f"Bearer {settings.databricks_token.get_secret_value()}"},
    )
    openproject_client = httpx.Client(
        base_url=settings.openproject_base_url,
        headers={
            "Authorization": _basic_auth("apikey", settings.openproject_api_key.get_secret_value()),
            "Content-Type": "application/json",
        },
    )
    vector_search_client = httpx.Client(
        base_url=settings.databricks_host,
        headers={"Authorization": f"Bearer {settings.databricks_token.get_secret_value()}"},
    )

    return LiveServices(
        databricks=DatabricksSQLClient(
            client=databricks_client,
            warehouse_id=settings.databricks_warehouse_id,
            catalog=settings.databricks_catalog,
            schema=settings.databricks_schema,
        ),
        openproject=OpenProjectClient(
            client=openproject_client,
            project_identifier=settings.openproject_project_identifier,
        ),
        vector_search=VectorSearchClient(
            client=vector_search_client,
            index_name=settings.databricks_vector_search_index_name,
            columns=settings.vector_search_columns,
        ),
    )


def _basic_auth(username: str, password: str | None) -> str:
    credentials = f"{username}:{password or ''}".encode()
    return "Basic " + base64.b64encode(credentials).decode()
