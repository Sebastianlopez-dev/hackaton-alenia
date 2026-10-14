"""In-memory simulated services: no database, HTTP or persisted writes."""

from hackaton_alenia.ticket import Ticket


class SimulatedServices:
    def __init__(self, case: dict):
        self.case = case
        self.actions: list[dict] = []

    def read_ticket(self, ticket_id: int) -> Ticket:
        ticket = Ticket(**self.case["ticket"])
        if ticket.id != ticket_id:
            raise ValueError("Ticket is outside this simulated case")
        return ticket

    def retrieve_similar_tickets(self, query: str) -> list[dict]:
        return self.case["precedents"]

    def query_sql(self, sql: str) -> list[dict]:
        if sql != self.case["sql"]:
            raise ValueError("SQL is outside this simulated case")
        self.actions.append({"action": "sql", "payload": sql})
        return self.case["rows"]

    def create_comment(self, ticket_id: int, text: str) -> dict:
        self.read_ticket(ticket_id)
        self.actions.append({"action": "comment", "payload": text})
        return {"simulation": True, "created": True}

    def update_status(self, ticket_id: int, status: str) -> dict:
        self.read_ticket(ticket_id)
        self.actions.append({"action": "status", "payload": status})
        return {"simulation": True, "status": status}
