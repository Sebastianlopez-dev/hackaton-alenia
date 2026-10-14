"""Scripted model for one fixture; it performs no inference or network calls."""

import json

from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, BaseMessage

from hackaton_alenia.llm import Resolution


class SimulatedModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


def simulated_model(case: dict) -> SimulatedModel:
    """Replay a fixture: routing, then its capability calls, then the resolution."""
    responses: list[BaseMessage] = [AIMessage(content=json.dumps(case["routing"]))]
    for index, call in enumerate(case["tool_calls"]):
        responses.append(AIMessage(content="", tool_calls=[{**call, "id": f"demo_{index}", "type": "tool_call"}]))
    responses.append(AIMessage(content="", tool_calls=[{
        "name": Resolution.__name__, "args": case["resolution"], "id": "demo_resolution", "type": "tool_call"}]))
    return SimulatedModel(responses=responses)


def pipeline_model(case: dict) -> SimulatedModel:
    """Replay a fixture for the UC1 pipeline: routing, each query as a next step, done, resolution."""
    responses: list[BaseMessage] = [AIMessage(content=json.dumps(case["routing"]))]
    for call in case["tool_calls"]:
        if call["name"] == "query_sql":
            responses.append(AIMessage(content=json.dumps({"done": False, **call["args"]})))
    responses.append(AIMessage(content=json.dumps({"done": True})))
    responses.append(AIMessage(content=json.dumps(case["resolution"])))
    return SimulatedModel(responses=responses)
