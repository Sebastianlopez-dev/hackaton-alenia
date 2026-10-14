"""Mosaic AI Vector Search query adapter using httpx.MockTransport."""

import json

import httpx

from hackaton_alenia.integrations.vector_search import VectorSearchClient


def _client(transport: httpx.MockTransport) -> VectorSearchClient:
    return VectorSearchClient(
        client=httpx.Client(base_url="https://adb-123.azuredatabricks.net", transport=transport),
        index_name="tickets_index",
        columns=["id", "title", "description"],
    )


def test_query_posts_expected_body_and_maps_response():
    captured: dict = {}

    def handler(request: httpx.Request):
        captured["method"] = request.method
        captured["path"] = str(request.url)
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json={
                "manifest": {
                    "column_count": 3,
                    "columns": [
                        {"name": "id"},
                        {"name": "title"},
                        {"name": "description"},
                    ],
                },
                "result": {
                    "data_array": [
                        ["1", "Old ticket", "Similar issue"],
                    ]
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    rows = client.retrieve_similar_tickets("missing mapping")

    assert captured["method"] == "POST"
    assert captured["path"].endswith("/api/2.0/vector-search/indexes/tickets_index/query")
    assert captured["body"]["query_text"] == "missing mapping"
    assert captured["body"]["columns"] == ["id", "title", "description"]
    assert captured["body"]["num_results"] == 10
    assert rows == [{"id": "1", "title": "Old ticket", "description": "Similar issue"}]


def test_empty_columns_setting_is_allowed():
    def handler(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "manifest": {"column_count": 1, "columns": [{"name": "id"}]},
                "result": {"data_array": []},
            },
        )

    transport = httpx.MockTransport(handler)
    client = VectorSearchClient(
        client=httpx.Client(base_url="https://adb-123.azuredatabricks.net", transport=transport),
        index_name="idx",
        columns=[],
    )
    assert client.retrieve_similar_tickets("x") == []
