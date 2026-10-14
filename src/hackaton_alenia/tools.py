"""Allowed capabilities; protected calls share a host-owned approval gate.

Every capability follows the same order: the active ticket is checked, the
host-owned approval gate is asked for this exact request, and only then the
service runs. A capability failure comes back to the model as data so the
investigation can continue; a human refusal always stops the run.

A SQL statement that is not recognised as a single read is refused before
the human is asked: no data-write permission is documented, so it could
never be executed, and the model gets the reason to rewrite it as a read.
"""

from langchain_core.tools import tool

from hackaton_alenia.approvals import ApprovalDenied, ApprovalGate, ApprovalRequest
from hackaton_alenia.integrations.contracts import Services
from hackaton_alenia.sql_guard import read_only_reason


def ticket_tools(services: Services, gate: ApprovalGate, active_ticket_id: int, origin: str = "agent"):
    """Build the five capabilities; ``origin`` labels who produces the payloads."""
    def protect(action, payload, purpose):
        request = ApprovalRequest(action, active_ticket_id, payload, purpose, origin=origin)
        gate.require(request)
        return request

    def mark_executed(token: str):
        record = getattr(gate, "mark_executed", None)
        if record is not None:
            record(token)

    def this_ticket(ticket_id):
        if ticket_id != active_ticket_id:
            raise ValueError("Action targets another ticket")

    def guarded(call):
        """Hand a capability failure to the model; never swallow a human refusal."""
        try:
            return call()
        except ApprovalDenied:
            raise
        except Exception as error:
            return {"error": f"{type(error).__name__}: {error}"}

    @tool
    def read_ticket(ticket_id: int) -> dict:
        """Read the active ticket. A failure returns an error object."""
        def call() -> dict:
            this_ticket(ticket_id)
            return services.read_ticket(ticket_id).model_dump()
        return guarded(call)

    @tool
    def retrieve_similar_tickets(query: str) -> list[dict] | dict:
        """Retrieve historical tickets for reference. A failure returns an error object."""
        return guarded(lambda: services.retrieve_similar_tickets(query))

    @tool
    def query_sql(sql: str, purpose: str) -> list[dict] | dict:
        """Request human approval before querying the ticket's data. A failure returns an error object."""
        def call() -> list[dict]:
            reason = read_only_reason(sql)
            if reason:
                raise ValueError(f"Statement refused: not a single read ({reason}). Rewrite it as one SELECT.")
            request = protect("sql", sql, purpose)
            result = services.query_sql(sql)
            mark_executed(request.token)
            return result
        return guarded(call)

    @tool
    def create_comment(ticket_id: int, text: str) -> dict:
        """Request human approval before publishing a resolution comment. A failure returns an error object."""
        def call() -> dict:
            this_ticket(ticket_id)
            request = protect("comment", text, "Publish the analysis and proposed resolution")
            result = services.create_comment(ticket_id, text)
            mark_executed(request.token)
            return result
        return guarded(call)

    @tool
    def update_status(ticket_id: int, status: str) -> dict:
        """Request human approval before changing the ticket status. A failure returns an error object."""
        def call() -> dict:
            this_ticket(ticket_id)
            request = protect("status", status, "Update the ticket after reviewing the proposal")
            result = services.update_status(ticket_id, status)
            mark_executed(request.token)
            return result
        return guarded(call)

    return [read_ticket, retrieve_similar_tickets, query_sql, create_comment, update_status]
