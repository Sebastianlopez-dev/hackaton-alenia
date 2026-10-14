"""Human decisions bound to one immutable action request, plus an audit ledger."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4


@dataclass(frozen=True)
class ApprovalRequest:
    action: Literal["sql", "comment", "status"]
    ticket_id: int
    payload: str
    purpose: str
    token: str = field(default_factory=lambda: uuid4().hex)
    # Who produced the payload: the model ("agent") or deterministic code
    # ("script"). Part of the bound request, so it cannot change after display.
    origin: Literal["agent", "script"] = "agent"


@dataclass(frozen=True)
class Approval:
    request: ApprovalRequest
    approved: bool


class ApprovalDenied(RuntimeError):
    """The action has no explicit approval for this exact request."""


class ApprovalGate:
    def __init__(self, respond: Callable[[ApprovalRequest], Approval | None]):
        self.respond = respond

    def require(self, request: ApprovalRequest) -> None:
        response = self.respond(request)
        if not self._valid(response, request):
            raise ApprovalDenied(
                f"Blocked {request.action}: explicit approval required"
            )

    @staticmethod
    def _valid(response, request: ApprovalRequest) -> bool:
        return (
            isinstance(response, Approval)
            and response.request == request
            and response.approved is True
        )


Outcome = Literal["approved", "rejected", "absent", "changed_payload"]


@dataclass
class AuditEntry:
    """One approval request and its outcome. Never stores credentials."""

    run_id: str
    sequence: int
    timestamp: str
    ticket_id: int
    action: str
    payload: str
    purpose: str
    token: str
    outcome: Outcome
    origin: str = "agent"
    executed: bool = False

    def as_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "ticket_id": self.ticket_id,
            "action": self.action,
            "payload": self.payload,
            "purpose": self.purpose,
            "token": self.token,
            "outcome": self.outcome,
            "origin": self.origin,
            "executed": self.executed,
        }


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _outcome(response, request: ApprovalRequest) -> Outcome:
    if response is None:
        return "absent"
    if not isinstance(response, Approval):
        return "absent"
    if response.request != request:
        return "changed_payload"
    if response.approved is True:
        return "approved"
    return "rejected"


class AuditApprovalGate(ApprovalGate):
    """Approval gate that records every request, outcome and execution status."""

    def __init__(self, respond, run_id: str | None = None):
        super().__init__(respond)
        self.run_id = run_id or uuid4().hex
        self._ledger: list[AuditEntry] = []
        self._sequence = 0
        self._context: dict = {}

    def set_context(
        self,
        *,
        ticket_id: int | None = None,
        use_case: str | None = None,
        priority: str | None = None,
    ) -> None:
        if ticket_id is not None:
            self._context["ticket_id"] = ticket_id
        if use_case is not None:
            self._context["use_case"] = use_case
        if priority is not None:
            self._context["priority"] = priority

    @property
    def context(self) -> dict:
        return dict(self._context)

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def ledger(self) -> list[AuditEntry]:
        return list(self._ledger)

    def mark_executed(self, token: str) -> None:
        for entry in self._ledger:
            if entry.token == token:
                entry.executed = True
                return

    def require(self, request: ApprovalRequest) -> None:
        self._sequence += 1
        timestamp = _now()
        response = self.respond(request)
        outcome = _outcome(response, request)
        self._ledger.append(
            AuditEntry(
                run_id=self.run_id,
                sequence=self._sequence,
                timestamp=timestamp,
                ticket_id=request.ticket_id,
                action=request.action,
                payload=request.payload,
                purpose=request.purpose,
                token=request.token,
                outcome=outcome,
                origin=request.origin,
                executed=False,
            )
        )
        if not self._valid(response, request):
            raise ApprovalDenied(
                f"Blocked {request.action}: explicit approval required"
            )
