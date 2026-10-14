"""Scripted model for one fixture; it performs no inference or network calls."""

import json

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage


class SimulatedModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


def simulated_model(case: dict) -> SimulatedModel:
    responses = [AIMessage(content=json.dumps(case["routing"]))]
    for index, call in enumerate(case["tool_calls"]):
        responses.append(AIMessage(content="", tool_calls=[{**call, "id": f"demo_{index}", "type": "tool_call"}]))
    responses.append(AIMessage(content=json.dumps(case["resolution"])))
    return SimulatedModel(responses=responses)
