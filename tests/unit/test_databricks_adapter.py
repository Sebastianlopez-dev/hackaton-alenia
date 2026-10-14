"""Databricks SQL Statement Execution API adapter using httpx.MockTransport."""

import json

import httpx
import pytest

from hackaton_alenia.integrations.databricks import DatabricksSQLClient, DatabricksSQLError


def _client(transport: httpx.MockTransport) -> DatabricksSQLClient:
    return DatabricksSQLClient(
        client=httpx.Client(
            base_url="https://adb-123.azuredatabricks.net",
            headers={"Authorization": "Bearer token"},
            transport=transport,
        ),
        warehouse_id="warehouse-1",
        catalog="catalog_1",
        schema="schema_1",
    )


def test_query_posts_expected_body_and_auth():
    captured: dict = {}

    def handler(request: httpx.Request):
        captured["method"] = request.method
        captured["path"] = str(request.url)
        captured["auth"] = request.headers.get("Authorization")
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json={
                "statement_id": "stmt-1",
                "status": {"state": "SUCCEEDED"},
                "manifest": {
                    "schema": {
                        "column_count": 2,
                        "columns": [
                            {"name": "id", "position": 0},
                            {"name": "name", "position": 1},
                        ],
                    }
                },
                "result": {
                    "data_array": [
                        ["1", "Alice"],
                        ["2", "Bob"],
                    ]
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    rows = client.query_sql("SELECT id, name FROM users")

    assert captured["method"] == "POST"
    assert captured["path"].endswith("/api/2.0/sql/statements")
    assert captured["auth"] == "Bearer token"
    assert captured["body"]["statement"] == "SELECT id, name FROM users"
    assert captured["body"]["warehouse_id"] == "warehouse-1"
    assert captured["body"]["disposition"] == "INLINE"
    assert captured["body"]["format"] == "JSON_ARRAY"
    assert rows == [
        {"id": "1", "name": "Alice"},
        {"id": "2", "name": "Bob"},
    ]


def test_query_polls_until_succeeded():
    calls = []

    def handler(request: httpx.Request):
        calls.append((request.method, str(request.url)))
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "statement_id": "stmt-2",
                    "status": {"state": "PENDING"},
                },
            )
        # GET poll
        return httpx.Response(
            200,
            json={
                "statement_id": "stmt-2",
                "status": {"state": "SUCCEEDED"},
                "manifest": {
                    "schema": {
                        "column_count": 1,
                        "columns": [{"name": "n", "position": 0}],
                    }
                },
                "result": {"data_array": [["42"]]},
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    assert client.query_sql("SELECT 42 AS n") == [{"n": "42"}]
    assert len(calls) == 2
    assert calls[0][0] == "POST"
    assert calls[1][0] == "GET"


def test_query_raises_on_failed_state():
    def handler(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "statement_id": "stmt-3",
                "status": {
                    "state": "FAILED",
                    "error": {
                        "error_code": "BAD_REQUEST",
                        "message": "Syntax error",
                    },
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    with pytest.raises(DatabricksSQLError, match="FAILED"):
        client.query_sql("SELECT bad")


def test_query_raises_on_canceled_state():
    def handler(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "statement_id": "stmt-4",
                "status": {"state": "CANCELED"},
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    with pytest.raises(DatabricksSQLError, match="CANCELED"):
        client.query_sql("SELECT 1")


def test_query_raises_on_closed_state():
    def handler(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "statement_id": "stmt-5",
                "status": {"state": "CLOSED"},
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    with pytest.raises(DatabricksSQLError, match="CLOSED"):
        client.query_sql("SELECT 1")
