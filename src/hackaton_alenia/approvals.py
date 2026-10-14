"""Human decisions bound to one immutable action request."""

from dataclasses import dataclass, field
from typing import Callable, Literal
from uuid import uuid4


@dataclass(frozen=True)
class ApprovalRequest:
    action: Literal["sql", "comment", "status"]
    ticket_id: int
    payload: str
    purpose: str
    token: str = field(default_factory=lambda: uuid4().hex)


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
        if not isinstance(response, Approval) or response.request != request or response.approved is not True:
            raise ApprovalDenied(f"Blocked {request.action}: explicit approval required")
