import json
from dataclasses import replace
from pathlib import Path

import pytest

from hackaton_alenia.agent import run_ticket
from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import simulated_model


CASE = Path("evals/cases/ticket_demo_s.json")
EXPECTED = Path("evals/expected/ticket_demo_s.json")


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
