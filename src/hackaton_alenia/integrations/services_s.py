"""In-memory simulated services: no database, HTTP or persisted writes."""

from hackaton_alenia.ticket import Ticket


class SimulatedServices:
    """Replay a fixture.

    A fixture declares a set of approved SQL statements with their result
    rows in ``approved_queries``. Any statement not listed raises, which the
    tool guard converts into an ``{"error": ...}`` message for the model.
    """

    def __init__(self, case: dict):
        self.case = case
        self.actions: list[dict] = []
        self._approved: dict[str, list[dict]] = dict(case.get("approved_queries", {}))

    def read_ticket(self, ticket_id: int) -> Ticket:
        ticket = Ticket(**self.case["ticket"])
        if ticket.id != ticket_id:
            raise ValueError("Ticket is outside this simulated case")
        return ticket

    def retrieve_similar_tickets(self, query: str) -> list[dict]:
        return self.case["precedents"]

    def query_sql(self, sql: str) -> list[dict]:
        if sql not in self._approved:
            raise ValueError("SQL is outside this simulated case")
        self.actions.append({"action": "sql", "payload": sql})
        return self._approved[sql]

    def create_comment(self, ticket_id: int, text: str) -> dict:
        self.read_ticket(ticket_id)
        self.actions.append({"action": "comment", "payload": text})
        return {"simulation": True, "created": True}

    def update_status(self, ticket_id: int, status: str) -> dict:
        self.read_ticket(ticket_id)
        self.actions.append({"action": "status", "payload": status})
        return {"simulation": True, "status": status}
