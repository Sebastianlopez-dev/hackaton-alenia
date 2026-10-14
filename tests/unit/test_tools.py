"""Capability failures reach the model as data; a human refusal never does."""

import json
from pathlib import Path

import pytest

from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.tools import ticket_tools

CASE = json.loads(Path("evals/cases/ticket_demo_s.json").read_text())


def tools_for(decision):
    services = SimulatedServices(dict(CASE))
    gate = ApprovalGate(lambda request: Approval(request, decision))
    tools = ticket_tools(services, gate, CASE["ticket"]["id"])
    return {tool.name: tool for tool in tools}, services


def test_a_capability_failure_reaches_the_model_as_data():
    tools, services = tools_for(True)

    assert "error" in tools["query_sql"].invoke({"sql": "SELECT unknown", "purpose": "Probe"})
    assert services.actions == []


def test_reading_outside_the_active_ticket_reaches_the_model_as_data():
    tools, services = tools_for(True)

    assert "error" in tools["read_ticket"].invoke({"ticket_id": 999})
    assert services.actions == []


def test_a_human_refusal_is_never_swallowed():
    tools, services = tools_for(False)

    with pytest.raises(ApprovalDenied):
        tools["query_sql"].invoke({"sql": CASE["sql"], "purpose": "Probe"})

    assert services.actions == []
