"""OpenProject API v3 adapter using httpx.MockTransport."""

import json

import httpx
import pytest

from hackaton_alenia.integrations.openproject import OpenProjectClient, OpenProjectError


def _client(transport: httpx.MockTransport) -> OpenProjectClient:
    return OpenProjectClient(
        client=httpx.Client(base_url="https://op.example.com", transport=transport),
        project_identifier="proj",
    )


def test_read_ticket_maps_work_package_to_ticket():
    def handler(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "id": 42,
                "lockVersion": 3,
                "subject": "Missing mapping",
                "description": {
                    "format": "markdown",
                    "raw": "The local code is not mapped.",
                    "html": "<p>The local code is not mapped.</p>",
                },
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    ticket = client.read_ticket(42)
    assert ticket.id == 42
    assert ticket.title == "Missing mapping"
    assert ticket.description == "The local code is not mapped."


def test_create_comment_posts_to_activities():
    captured: dict = {}

    def handler(request: httpx.Request):
        captured["method"] = request.method
        captured["path"] = str(request.url)
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json={
                "_type": "Activity",
                "id": 7,
                "comment": {"format": "markdown", "raw": "Proposed resolution."},
            },
        )

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    result = client.create_comment(42, "Proposed resolution.")
    assert captured["method"] == "POST"
    assert captured["path"].endswith("/api/v3/work_packages/42/activities")
    assert captured["body"] == {"comment": {"raw": "Proposed resolution."}}
    assert result["id"] == 7


def test_update_status_resolves_name_and_sends_lock_version():
    captured: dict = {}

    def handler(request: httpx.Request):
        captured[(request.method, str(request.url))] = json.loads(request.content) if request.content else None
        if request.method == "GET" and "/statuses" in str(request.url):
            return httpx.Response(
                200,
                json={
                    "_embedded": {
                        "elements": [
                            {"id": 1, "name": "New"},
                            {"id": 5, "name": "Resolved"},
                        ]
                    }
                },
            )
        if request.method == "GET":
            return httpx.Response(
                200,
                json={"id": 42, "lockVersion": 3, "subject": "T"},
            )
        if request.method == "PATCH":
            return httpx.Response(
                200,
                json={"id": 42, "lockVersion": 4, "subject": "T"},
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    result = client.update_status(42, "Resolved")
    assert result["lockVersion"] == 4
    patch = captured[("PATCH", "https://op.example.com/api/v3/work_packages/42")]
    assert patch["lockVersion"] == 3
    assert patch["_links"]["status"]["href"] == "/api/v3/statuses/5"


def test_update_status_raises_for_unknown_status():
    def handler(request: httpx.Request):
        if request.method == "GET" and "/statuses" in str(request.url):
            return httpx.Response(
                200,
                json={"_embedded": {"elements": [{"id": 1, "name": "New"}]}},
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    with pytest.raises(OpenProjectError, match="Unknown status"):
        client.update_status(42, "NotAStatus")


def test_update_status_raises_when_work_package_missing_lock_version():
    def handler(request: httpx.Request):
        if request.method == "GET" and "/statuses" in str(request.url):
            return httpx.Response(
                200,
                json={"_embedded": {"elements": [{"id": 1, "name": "New"}]}},
            )
        if request.method == "GET":
            return httpx.Response(200, json={"id": 42, "subject": "T"})
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = _client(transport)
    with pytest.raises(OpenProjectError):
        client.update_status(42, "New")
