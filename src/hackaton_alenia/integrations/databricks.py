"""Databricks SQL Statement Execution API adapter.

Written against public documentation:
- Execute statement: https://docs.databricks.com/api/statement-execution/v1/execute-statement.md
- Get statement result / poll: https://docs.databricks.com/api/statement-execution/v1/get-statement-result.md

This adapter is **untested against Alenia's infrastructure**. It uses the
 documented v1 endpoints and the INLINE / JSON_ARRAY disposition, which keeps
 small result sets inside the response body. The result manifest maps rows to
 dictionaries using the column names reported by the warehouse.

Ambiguities not resolved by the public docs:
- The exact SQL error code taxonomy and which transient errors are safe to retry.
- Whether Alenia's warehouse returns chunked results for the small result sets
  expected by UC1; this implementation reads only the first inline chunk.
- The interaction between ``catalog``/``schema`` and parameterised queries; here
  the statement text is sent verbatim and the caller is expected to qualify or
  use the configured default catalog/schema.
"""

from __future__ import annotations

import time
from typing import Any

import httpx


class DatabricksSQLError(Exception):
    """A SQL statement reached a terminal non-success state."""

    def __init__(self, state: str, message: str):
        self.state = state
        self.message = message
        super().__init__(f"Databricks SQL statement {state}: {message}")


class DatabricksSQLClient:
    """Run read-only SQL through the Databricks Statement Execution API."""

    _TERMINAL_STATES = {"SUCCEEDED", "FAILED", "CANCELED", "CLOSED"}
    _POLLING_STATES = {"PENDING", "RUNNING"}

    def __init__(
        self,
        client: httpx.Client,
        warehouse_id: str,
        catalog: str,
        schema: str,
        poll_interval: float = 1.0,
        max_poll_attempts: int = 30,
    ):
        self.client = client
        self.warehouse_id = warehouse_id
        self.catalog = catalog
        self.schema = schema
        self.poll_interval = poll_interval
        self.max_poll_attempts = max_poll_attempts

    def query_sql(self, sql: str) -> list[dict[str, Any]]:
        """Submit ``sql`` and return rows as dictionaries.

        The API may return synchronously or require polling; both paths are
        handled. Terminal states other than ``SUCCEEDED`` raise.
        """
        response = self.client.post(
            "/api/2.0/sql/statements",
            json={
                "statement": sql,
                "warehouse_id": self.warehouse_id,
                "wait_timeout": "0s",
                "disposition": "INLINE",
                "format": "JSON_ARRAY",
            },
        )
        response.raise_for_status()
        data = response.json()

        data = self._await_terminal(data)
        state = data.get("status", {}).get("state")
        if state != "SUCCEEDED":
            error = data.get("status", {}).get("error", {})
            raise DatabricksSQLError(state, error.get("message", "unknown error"))

        return self._rows_from_result(data)

    def _await_terminal(self, data: dict[str, Any]) -> dict[str, Any]:
        statement_id = data.get("statement_id")
        for _ in range(self.max_poll_attempts):
            state = data.get("status", {}).get("state")
            if state in self._TERMINAL_STATES:
                return data
            if state not in self._POLLING_STATES:
                # Unknown state: treat as terminal failure rather than spin.
                return data
            if statement_id is None:
                raise DatabricksSQLError("UNKNOWN", "statement_id missing from response")
            time.sleep(self.poll_interval)
            response = self.client.get(f"/api/2.0/sql/statements/{statement_id}")
            response.raise_for_status()
            data = response.json()
        state = data.get("status", {}).get("state")
        raise DatabricksSQLError("TIMEOUT", f"statement did not reach terminal state, last state: {state}")

    def _rows_from_result(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        manifest = data.get("manifest", {})
        schema = manifest.get("schema", {})
        columns = [col["name"] for col in schema.get("columns", [])]
        result = data.get("result", {})
        data_array = result.get("data_array", [])
        return [dict(zip(columns, row, strict=True)) for row in data_array]
