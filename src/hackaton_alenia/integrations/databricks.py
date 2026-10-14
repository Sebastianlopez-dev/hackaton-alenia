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
        max_chunks: int = 100,
    ):
        self.client = client
        self.warehouse_id = warehouse_id
        self.catalog = catalog
        self.schema = schema
        self.poll_interval = poll_interval
        self.max_poll_attempts = max_poll_attempts
        self.max_chunks = max_chunks

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
                "catalog": self.catalog,
                "schema": self.schema,
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
        """Collect every inline chunk; never return a silently partial result.

        An INLINE result can arrive as several chunks, each pointing to the
        next through ``next_chunk_internal_link``. A result the warehouse
        marked ``truncated`` is refused: for UC1 a missing row means "no
        mapping", so a partial result would be a wrong answer, not a short one.
        """
        manifest = data.get("manifest", {})
        if manifest.get("truncated"):
            raise DatabricksSQLError("TRUNCATED", "the result exceeds the inline limit; narrow the query")
        columns = [col["name"] for col in manifest.get("schema", {}).get("columns", [])]
        chunk = data.get("result", {})
        rows: list[dict[str, Any]] = []
        for _ in range(self.max_chunks):
            rows.extend(dict(zip(columns, row, strict=True)) for row in chunk.get("data_array", []))
            link = chunk.get("next_chunk_internal_link")
            if not link:
                return rows
            response = self.client.get(link)
            response.raise_for_status()
            chunk = response.json()
        raise DatabricksSQLError("TRUNCATED", f"more than {self.max_chunks} result chunks; narrow the query")
