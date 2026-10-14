"""Allowed capabilities; protected calls share a host-owned approval gate."""

from langchain_core.tools import tool

from hackaton_alenia.approvals import ApprovalGate, ApprovalRequest
from hackaton_alenia.integrations.contracts import Services


def ticket_tools(services: Services, gate: ApprovalGate, active_ticket_id: int):
    def protect(action, payload, purpose):
        gate.require(ApprovalRequest(action, active_ticket_id, payload, purpose))

    def check_ticket(ticket_id):
        if ticket_id != active_ticket_id:
            raise ValueError("Action targets another ticket")

    @tool
    def read_ticket(ticket_id: int) -> dict:
        """Read the active ticket."""
        check_ticket(ticket_id)
        return services.read_ticket(ticket_id).model_dump()

    @tool
    def retrieve_similar_tickets(query: str) -> list[dict]:
        """Retrieve historical tickets for reference."""
        return services.retrieve_similar_tickets(query)

    @tool
    def query_sql(sql: str, purpose: str) -> list[dict]:
        """Request human approval before querying the ticket's data."""
        protect("sql", sql, purpose)
        return services.query_sql(sql)

    @tool
    def create_comment(ticket_id: int, text: str) -> dict:
        """Request human approval before publishing a resolution comment."""
        check_ticket(ticket_id)
        protect("comment", text, "Publish the analysis and proposed resolution")
        return services.create_comment(ticket_id, text)

    @tool
    def update_status(ticket_id: int, status: str) -> dict:
        """Request human approval before changing the ticket status."""
        check_ticket(ticket_id)
        protect("status", status, "Update the ticket after reviewing the proposal")
        return services.update_status(ticket_id, status)

    return [read_ticket, retrieve_similar_tickets, query_sql, create_comment, update_status]
