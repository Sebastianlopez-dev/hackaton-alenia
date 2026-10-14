"""Decision ledger: every approval request and its outcome are recorded."""

from dataclasses import replace

import pytest

from hackaton_alenia.approvals import (
    Approval,
    ApprovalDenied,
    ApprovalRequest,
    AuditApprovalGate,
)


def test_audit_gate_records_an_approved_request():
    request = ApprovalRequest("sql", 101, "SELECT 1", "Check")
    gate = AuditApprovalGate(lambda shown: Approval(shown, True), run_id="run-1")

    gate.require(request)

    assert len(gate.ledger) == 1
    entry = gate.ledger[0]
    assert entry.run_id == "run-1"
    assert entry.sequence == 1
    assert entry.ticket_id == 101
    assert entry.action == "sql"
    assert entry.payload == "SELECT 1"
    assert entry.purpose == "Check"
    assert entry.outcome == "approved"
    assert entry.executed is False


def test_audit_gate_records_a_rejected_request():
    request = ApprovalRequest("sql", 101, "SELECT 1", "Check")
    gate = AuditApprovalGate(lambda shown: Approval(shown, False))

    with pytest.raises(ApprovalDenied):
        gate.require(request)

    assert len(gate.ledger) == 1
    assert gate.ledger[0].outcome == "rejected"


def test_audit_gate_records_an_absent_request():
    request = ApprovalRequest("sql", 101, "SELECT 1", "Check")
    gate = AuditApprovalGate(lambda shown: None)

    with pytest.raises(ApprovalDenied):
        gate.require(request)

    assert len(gate.ledger) == 1
    assert gate.ledger[0].outcome == "absent"


def test_audit_gate_records_a_changed_payload():
    request = ApprovalRequest("sql", 101, "SELECT 1", "Check")
    gate = AuditApprovalGate(
        lambda shown: Approval(replace(shown, payload="SELECT 2"), True)
    )

    with pytest.raises(ApprovalDenied):
        gate.require(request)

    assert len(gate.ledger) == 1
    assert gate.ledger[0].outcome == "changed_payload"


def test_audit_gate_marks_an_approved_action_as_executed():
    request = ApprovalRequest("sql", 101, "SELECT 1", "Check")
    gate = AuditApprovalGate(lambda shown: Approval(shown, True))

    gate.require(request)
    gate.mark_executed(request.token)

    assert gate.ledger[0].executed is True


def test_audit_gate_stores_routing_context():
    gate = AuditApprovalGate(lambda shown: None)

    gate.set_context(ticket_id=101, use_case="UC1", priority="high")

    assert gate.context == {"ticket_id": 101, "use_case": "UC1", "priority": "high"}


def test_audit_gate_increments_sequence_for_each_request():
    gate = AuditApprovalGate(lambda shown: Approval(shown, True))

    gate.require(ApprovalRequest("sql", 1, "a", "a"))
    gate.require(ApprovalRequest("sql", 1, "b", "b"))

    assert [entry.sequence for entry in gate.ledger] == [1, 2]
