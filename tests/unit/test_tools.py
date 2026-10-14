"""Capability failures reach the model as data; a human refusal never does."""

import json
from pathlib import Path

import pytest

from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.tools import ticket_tools

CASE = json.loads(Path("evals/cases/uc1_missing_mapping_s.json").read_text())


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
    approved_sql = next(iter(CASE["approved_queries"]))

    with pytest.raises(ApprovalDenied):
        tools["query_sql"].invoke({"sql": approved_sql, "purpose": "Probe"})

    assert services.actions == []


def test_a_statement_that_can_write_is_refused_before_the_human_is_asked():
    services = SimulatedServices(dict(CASE))
    asked = []
    gate = ApprovalGate(lambda request: asked.append(request) or Approval(request, True))
    query_sql = {tool.name: tool for tool in ticket_tools(services, gate, CASE["ticket"]["id"])}["query_sql"]

    result = query_sql.invoke({"sql": "DELETE FROM MD_LOCALVALUE_T", "purpose": "Clean up"})

    assert "not a single read" in result["error"]
    assert asked == []
    assert services.actions == []
