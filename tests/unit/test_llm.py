"""The routing read tolerates how a chat endpoint wraps its answer."""

import json

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from hackaton_alenia.llm import Routing, classify_ticket
from hackaton_alenia.ticket import Ticket

TICKET = Ticket(id=101, title="Missing local mapping", description="Local code ABC has no holding mapping.")
ROUTING = Routing(use_case="UC1", priority="high")
ANSWER = json.dumps(ROUTING.model_dump())
UC1_CONTEXT_ANSWER = json.dumps({
    "use_case": "UC1",
    "priority": "high",
    "subsidiary": "ES",
    "class": "CHANNEL",
    "affected_local_code": "CH_NEW",
})


def reading(content) -> FakeMessagesListChatModel:
    return FakeMessagesListChatModel(responses=[AIMessage(content=content)])


def test_plain_json_is_read():
    assert classify_ticket(reading(ANSWER), TICKET) == ROUTING


def test_fenced_json_is_read():
    assert classify_ticket(reading(f"```json\n{ANSWER}\n```"), TICKET) == ROUTING


def test_content_blocks_are_read():
    assert classify_ticket(reading([{"type": "text", "text": ANSWER}]), TICKET) == ROUTING


def test_uc1_context_is_extracted_in_the_routing_call():
    routing = classify_ticket(reading(UC1_CONTEXT_ANSWER), TICKET)
    data = routing.model_dump()

    assert data["use_case"] == "UC1"
    assert data["priority"] == "high"
    assert data["subsidiary"] == "ES"
    assert data["class_id"] == "CHANNEL"
    assert data["affected_local_code"] == "CH_NEW"


def test_uc1_context_stays_optional_for_unrelated_tickets():
    answer = json.dumps({"use_case": "UC2", "priority": "normal"})

    routing = classify_ticket(reading(answer), TICKET)
    data = routing.model_dump()

    assert data["use_case"] == "UC2"
    assert data["priority"] == "normal"
    assert data["subsidiary"] is None
    assert data["class_id"] is None
    assert data["affected_local_code"] is None
