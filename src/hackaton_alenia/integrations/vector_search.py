"""Mosaic AI Vector Search query adapter.

Written against public documentation:
- Query vector index: https://docs.databricks.com/api/vector-search/v1/query-vector-index.md

This adapter is **untested against Alenia's infrastructure**. It queries the
configured Delta Sync index using ``query_text`` and returns the columns named
in the settings. The column list is intentionally a setting because the exact
fields exposed by the official index are unknown.

Ambiguities not resolved by the public docs:
- Whether Alenia's index is a Delta Sync index with model endpoint embedding or
  a self-managed vector index; this adapter uses ``query_text``, which is the
  documented path for Delta Sync indexes backed by a model endpoint.
- Which text column(s) the model endpoint embeds; this adapter leaves
  ``query_columns`` empty so the service searches all text columns, as
  documented.
- Whether ``num_results=10`` matches the intended recall; this is a local default
  and should be tuned once the official index is available.
"""

from __future__ import annotations

from typing import Any

import httpx


class VectorSearchClient:
    """Query a Mosaic AI Vector Search index by text."""

    def __init__(
        self,
        client: httpx.Client,
        index_name: str,
        columns: list[str],
        num_results: int = 10,
    ):
        self.client = client
        self.index_name = index_name
        self.columns = columns
        self.num_results = num_results

    def retrieve_similar_tickets(self, query: str) -> list[dict[str, Any]]:
        """Return similar tickets as a list of dictionaries."""
        response = self.client.post(
            f"/api/2.0/vector-search/indexes/{self.index_name}/query",
            json={
                "query_text": query,
                "columns": self.columns,
                "num_results": self.num_results,
            },
        )
        response.raise_for_status()
        data = response.json()
        return self._rows_from_result(data)

    def _rows_from_result(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        manifest = data.get("manifest", {})
        # Vector Search returns columns directly under ``manifest``; keep a
        # fallback to ``manifest.schema`` in case the response shape changes.
        column_list = manifest.get("columns") or manifest.get("schema", {}).get("columns", [])
        columns = [col["name"] for col in column_list]
        result = data.get("result", {})
        data_array = result.get("data_array", [])
        return [dict(zip(columns, row, strict=True)) for row in data_array]
