import json
from dataclasses import replace
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage

from hackaton_alenia.agent import RECURSION_LIMIT, run_ticket
from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import SimulatedModel, simulated_model


CASE = Path("evals/cases/ticket_demo_s.json")
EXPECTED = Path("evals/expected/ticket_demo_s.json")


def approve_all(request):
    return Approval(request, True)


def test_complete_simulated_ticket():
    case = json.loads(CASE.read_text())
    services = SimulatedServices(case)
    shown = []
    def approve(request):
        shown.append(request)
        return Approval(request, True)
    result = run_ticket(case["ticket"]["id"], services, simulated_model(case), ApprovalGate(approve))
    assert [request.action for request in shown] == ["sql", "comment", "status"]
    assert evaluate(result, json.loads(EXPECTED.read_text()))["passed"] is True
    assert services.actions == case["expected_actions"]


@pytest.mark.parametrize("blocked_action", ["sql", "comment", "status"])
@pytest.mark.parametrize("decision", ["reject", "absent", "changed"])
def test_unapproved_action_never_reaches_the_service(blocked_action, decision):
    case = json.loads(CASE.read_text())
    services = SimulatedServices(case)
    def respond(request):
        if request.action != blocked_action:
            return Approval(request, True)
        if decision == "absent":
            return None
        if decision == "changed":
            return Approval(replace(request, payload="changed"), True)
        return Approval(request, False)
    gate = ApprovalGate(respond)
    with pytest.raises(ApprovalDenied):
        run_ticket(101, services, simulated_model(case), gate)
    index = ["sql", "comment", "status"].index(blocked_action)
    assert services.actions == case["expected_actions"][:index]


def test_a_model_that_never_returns_a_resolution_ends_in_an_abstention():
    case = json.loads(CASE.read_text())
    calls = []

    class Runaway(SimulatedModel):
        def invoke(self, *args, **kwargs):
            calls.append(1)
            return super().invoke(*args, **kwargs)

    model = Runaway(responses=[AIMessage(content=json.dumps(case["routing"])), AIMessage(content="I could not decide.")])
    result = run_ticket(case["ticket"]["id"], SimulatedServices(case), model, ApprovalGate(approve_all))

    assert result["resolution"]["abstention_reason"]
    assert result["resolution"]["proposed_correction"] == ""
    assert len(calls) <= RECURSION_LIMIT


def test_a_failing_capability_does_not_break_the_run():
    case = json.loads(CASE.read_text())
    case["sql"] = "SELECT causal_code FROM somewhere_else"
    case["tool_calls"] = [case["tool_calls"][1]]
    services = SimulatedServices(case)

    result = run_ticket(case["ticket"]["id"], services, simulated_model(case), ApprovalGate(approve_all))

    assert result["routing"] == case["routing"]
    assert result["resolution"]["analysis"] == case["resolution"]["analysis"]
    assert services.actions == []
