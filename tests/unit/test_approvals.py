from dataclasses import replace

import pytest

from hackaton_alenia.approvals import Approval, ApprovalGate, ApprovalRequest, ApprovalDenied


@pytest.mark.parametrize("action", ["sql", "comment", "status"])
@pytest.mark.parametrize("decision", ["approve", "reject", "absent", "changed"])
def test_only_an_explicit_decision_for_the_exact_request_allows_execution(action, decision):
    request = ApprovalRequest(action, 101, "exact payload", "Explain the action")
    def respond(shown):
        assert shown == request
        if decision == "absent":
            return None
        target = replace(shown, payload="changed") if decision == "changed" else shown
        return Approval(target, decision in {"approve", "changed"})
    gate = ApprovalGate(respond)
    if decision == "approve":
        gate.require(request)
    else:
        with pytest.raises(ApprovalDenied):
            gate.require(request)


def test_a_decision_cannot_be_reused_for_another_request():
    first = ApprovalRequest("sql", 101, "SELECT example", "Check example")
    gate = ApprovalGate(lambda request: Approval(first, True))
    gate.require(first)
    with pytest.raises(ApprovalDenied):
        gate.require(ApprovalRequest("sql", 101, "SELECT example", "Check example"))


def test_an_untyped_approval_cannot_authorize_execution():
    request = ApprovalRequest("sql", 101, "SELECT example", "Check example")
    with pytest.raises(ApprovalDenied):
        ApprovalGate(lambda shown: {"approved": True}).require(request)
