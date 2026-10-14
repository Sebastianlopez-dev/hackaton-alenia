"""OpenProject API v3 adapter for work packages.

Written against public documentation:
- Work packages endpoint: https://www.openproject.org/docs/api/endpoints/work-packages
- Statuses endpoint: https://www.openproject.org/docs/api/endpoints/statuses

This adapter is **untested against Alenia's infrastructure**. It maps the
work package ``subject`` to ``Ticket.title`` and the raw description to
``Ticket.description``. Status changes resolve the human-readable status name
against ``GET /api/v3/statuses`` and include the current ``lockVersion`` for
optimistic locking, as required by the PATCH endpoint.

Ambiguities not resolved by the public docs:
- The exact authentication scheme preferred by Alenia's OpenProject instance;
  this adapter uses HTTP Basic with user ``apikey`` and the configured API key
  as password, which is the documented API-key pattern.
- Whether Alenia exposes ``lockVersion`` at the top level of the work package
  payload; this implementation expects it there.
- How OpenProject handles concurrent updates if the ``lockVersion`` changes
  between the GET and PATCH; the API returns 409, which this adapter surfaces
  as an ``httpx.HTTPStatusError``.
"""

from __future__ import annotations

from typing import Any

import httpx

from hackaton_alenia.ticket import Ticket


class OpenProjectError(Exception):
    """An OpenProject API request could not be satisfied."""


class OpenProjectClient:
    """Read and update OpenProject work packages."""

    def __init__(self, client: httpx.Client, project_identifier: str):
        self.client = client
        self.project_identifier = project_identifier

    def read_ticket(self, ticket_id: int) -> Ticket:
        """Fetch a work package by id and map it to the local ``Ticket``."""
        response = self.client.get(f"/api/v3/work_packages/{ticket_id}")
        response.raise_for_status()
        data = response.json()
        description = data.get("description") or {}
        return Ticket(
            id=data["id"],
            title=data["subject"],
            description=description.get("raw", ""),
        )

    def create_comment(self, ticket_id: int, text: str) -> dict[str, Any]:
        """Add a comment activity to the work package."""
        response = self.client.post(
            f"/api/v3/work_packages/{ticket_id}/activities",
            json={"comment": {"format": "markdown", "raw": text}},
        )
        response.raise_for_status()
        return response.json()

    def update_status(self, ticket_id: int, status: str) -> dict[str, Any]:
        """Resolve ``status`` by name and PATCH the work package."""
        status_id = self._resolve_status_id(status)
        work_package = self._fetch_work_package(ticket_id)
        lock_version = work_package.get("lockVersion")
        if lock_version is None:
            raise OpenProjectError("work package response missing lockVersion")

        response = self.client.patch(
            f"/api/v3/work_packages/{ticket_id}",
            json={
                "lockVersion": lock_version,
                "_links": {
                    "status": {"href": f"/api/v3/statuses/{status_id}"},
                },
            },
        )
        response.raise_for_status()
        return response.json()

    def _resolve_status_id(self, status: str) -> int:
        response = self.client.get("/api/v3/statuses")
        response.raise_for_status()
        data = response.json()
        for element in data.get("_embedded", {}).get("elements", []):
            if element.get("name") == status:
                return element["id"]
        raise OpenProjectError(f"Unknown status name: {status!r}")

    def _fetch_work_package(self, ticket_id: int) -> dict[str, Any]:
        response = self.client.get(f"/api/v3/work_packages/{ticket_id}")
        response.raise_for_status()
        return response.json()
