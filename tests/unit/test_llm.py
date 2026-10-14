"""The routing read tolerates how a chat endpoint wraps its answer."""

import json

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from hackaton_alenia.llm import Routing, classify_ticket
from hackaton_alenia.ticket import Ticket

TICKET = Ticket(id=101, title="Missing local mapping", description="Local code ABC has no holding mapping.")
ROUTING = Routing(use_case="UC1", priority="high")
ANSWER = json.dumps(ROUTING.model_dump())


def reading(content) -> FakeMessagesListChatModel:
    return FakeMessagesListChatModel(responses=[AIMessage(content=content)])


def test_plain_json_is_read():
    assert classify_ticket(reading(ANSWER), TICKET) == ROUTING


def test_fenced_json_is_read():
    assert classify_ticket(reading(f"```json\n{ANSWER}\n```"), TICKET) == ROUTING


def test_content_blocks_are_read():
    assert classify_ticket(reading([{"type": "text", "text": ANSWER}]), TICKET) == ROUTING
