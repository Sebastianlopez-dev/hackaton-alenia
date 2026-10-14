import pytest
from pydantic import ValidationError

from hackaton_alenia.ticket import Ticket


def test_ticket_preserves_captured_information():
    data = {
        "id": 101,
        "title": "Missing local mapping",
        "description": "Local code ABC has no holding mapping.",
    }

    ticket = Ticket(**data)

    assert ticket.model_dump() == data


@pytest.mark.parametrize("missing_field", ["id", "title", "description"])
def test_ticket_requires_each_field(missing_field):
    data = {"id": 101, "title": "Example ticket", "description": "Example details"}
    del data[missing_field]

    with pytest.raises(ValidationError) as error:
        Ticket(**data)

    assert error.value.errors()[0]["loc"] == (missing_field,)
    assert error.value.errors()[0]["type"] == "missing"
