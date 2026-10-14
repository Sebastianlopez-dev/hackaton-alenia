"""End-to-end checks for the three official UC1 triggers."""

import json
from pathlib import Path

import pytest

from hackaton_alenia.agent import run_ticket
from hackaton_alenia.approvals import Approval, ApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import simulated_model
from hackaton_alenia.tools import ticket_tools

CASES = Path("evals/cases")
EXPECTED = Path("evals/expected")


def approve_all(request):
    return Approval(request, True)


@pytest.mark.parametrize(
    "case_name",
    [
        "uc1_missing_mapping_s",
        "uc1_holding_changed_s",
        "uc1_reporting_mismatch_s",
    ],
)
def test_uc1_fixture_runs_to_expected_result(case_name):
    case = json.loads((CASES / f"{case_name}.json").read_text())
    services = SimulatedServices(case)

    result = run_ticket(
        case["ticket"]["id"],
        services,
        simulated_model(case),
        ApprovalGate(approve_all),
    )

    expected = json.loads((EXPECTED / f"{case_name}.json").read_text())
    assert evaluate(result, expected)["passed"] is True
    assert services.actions == case["expected_actions"]


def test_unlisted_sql_returns_an_error_and_does_not_run():
    case = json.loads((CASES / "uc1_missing_mapping_s.json").read_text())
    services = SimulatedServices(case)
    tools = {tool.name: tool for tool in ticket_tools(services, ApprovalGate(approve_all), case["ticket"]["id"])}

    result = tools["query_sql"].invoke({"sql": "SELECT * FROM invented_table", "purpose": "Probe"})

    assert "error" in result
    assert services.actions == []


def test_approved_queries_run_independently():
    case = json.loads((CASES / "uc1_missing_mapping_s.json").read_text())
    services = SimulatedServices(case)

    for sql, rows in case["approved_queries"].items():
        assert services.query_sql(sql) == rows

    assert len(services.actions) == len(case["approved_queries"])
