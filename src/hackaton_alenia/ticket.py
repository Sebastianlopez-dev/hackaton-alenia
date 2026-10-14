"""Local representation of the information captured from a ticket."""

from pydantic import BaseModel


class Ticket(BaseModel):
    """Required ticket information, independent of the source service."""

    id: int
    title: str
    description: str
