"""Deterministic UC1 pipeline: the script owns the structure, the model fills in SQL and the resolution."""

import json
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage

from hackaton_alenia.approvals import Approval, ApprovalDenied, AuditApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import SimulatedModel, pipeline_model
from hackaton_alenia.pipeline import SOURCES, StatusNames, run_pipeline

CASES = Path("evals/cases")
EXPECTED = Path("evals/expected")
FIXTURES = ["uc1_missing_mapping_s", "uc1_holding_changed_s", "uc1_reporting_mismatch_s"]
STATUSES = StatusNames(proposal="resolved", review="review_required")


def load(name):
    return json.loads((CASES / f"{name}.json").read_text())


def recording_gate(decide=lambda request: True):
    shown = []

    def respond(request):
        shown.append(request)
        return Approval(request, decide(request))

    return AuditApprovalGate(respond), shown


def fixture_sql(case):
    return [call["args"]["sql"] for call in case["tool_calls"] if call["name"] == "query_sql"]


def fixture_status(case):
    return next(call["args"]["status"] for call in case["tool_calls"] if call["name"] == "update_status")


@pytest.mark.parametrize("name", FIXTURES)
def test_pipeline_reaches_the_expected_result(name):
    case = load(name)
    services = SimulatedServices(case)
    gate, _ = recording_gate()

    result = run_pipeline(case["ticket"]["id"], services, pipeline_model(case), gate, statuses=STATUSES)

    assert result["flow"] == "pipeline"
    assert evaluate(result, json.loads((EXPECTED / f"{name}.json").read_text()))["passed"] is True
    executed = [action["payload"] for action in services.actions if action["action"] == "sql"]
    assert executed == fixture_sql(case)
    assert [action["action"] for action in services.actions][-2:] == ["comment", "status"]
    assert services.actions[-1]["payload"] == fixture_status(case)


def test_every_step_is_labelled_with_its_source():
    case = load("uc1_holding_changed_s")
    gate, _ = recording_gate()

    result = run_pipeline(case["ticket"]["id"], SimulatedServices(case), pipeline_model(case), gate, statuses=STATUSES)

    sources = {event["source"] for event in result["trace"]}
    assert sources == set(SOURCES) == {"script", "agent", "human", "service"}
    assert all(event["step"] and event["summary"] for event in result["trace"])


def test_sql_is_generated_by_the_agent_and_comment_and_status_by_the_script():
    case = load("uc1_holding_changed_s")
    gate, shown = recording_gate()

    run_pipeline(case["ticket"]["id"], SimulatedServices(case), pipeline_model(case), gate, statuses=STATUSES)

    assert {request.origin for request in shown if request.action == "sql"} == {"agent"}
    assert [request.origin for request in shown if request.action != "sql"] == ["script", "script"]


def test_a_rejected_query_stops_the_run_before_anything_executes():
    case = load("uc1_holding_changed_s")
    services = SimulatedServices(case)
    gate, _ = recording_gate(lambda request: False)

    with pytest.raises(ApprovalDenied):
        run_pipeline(case["ticket"]["id"], services, pipeline_model(case), gate, statuses=STATUSES)

    assert services.actions == []
    assert [entry.outcome for entry in gate.ledger] == ["rejected"]


def test_a_statement_that_can_write_is_refused_without_asking_the_human():
    case = load("uc1_missing_mapping_s")
    services = SimulatedServices(case)
    gate, shown = recording_gate()
    model = SimulatedModel(responses=[
        AIMessage(content=json.dumps(case["routing"])),
        AIMessage(content=json.dumps({"done": False, "sql": "DELETE FROM MD_LOCALVALUE_T", "purpose": "Clean up"})),
        AIMessage(content=json.dumps({"done": True})),
        AIMessage(content=json.dumps(case["resolution"])),
    ])

    result = run_pipeline(case["ticket"]["id"], services, model, gate, statuses=STATUSES)

    assert [request.action for request in shown] == ["comment", "status"]
    assert not [action for action in services.actions if action["action"] == "sql"]
    refusals = [event for event in result["trace"] if event["source"] == "script" and "not a single read" in event["summary"]]
    assert len(refusals) == 1


def test_the_investigation_is_bounded_when_the_model_never_finishes():
    case = load("uc1_missing_mapping_s")
    sql = fixture_sql(case)[0]
    gate, shown = recording_gate()
    model = SimulatedModel(responses=[
        AIMessage(content=json.dumps(case["routing"])),
        *[AIMessage(content=json.dumps({"done": False, "sql": sql, "purpose": "Again"})) for _ in range(3)],
        AIMessage(content=json.dumps(case["resolution"])),
    ])

    result = run_pipeline(case["ticket"]["id"], SimulatedServices(case), model, gate, statuses=STATUSES, max_queries=3)

    assert len([request for request in shown if request.action == "sql"]) == 3
    assert any(event["source"] == "script" and "limit" in event["summary"] for event in result["trace"])


def test_a_ticket_outside_uc1_is_not_investigated():
    case = load("uc1_missing_mapping_s")
    services = SimulatedServices(case)
    gate, shown = recording_gate()
    model = SimulatedModel(responses=[AIMessage(content=json.dumps({"use_case": "UC2", "priority": "normal"}))])

    result = run_pipeline(case["ticket"]["id"], services, model, gate, statuses=STATUSES)

    assert shown == []
    assert services.actions == []
    assert result["resolution"]["abstention_reason"]
    assert result["routing"]["use_case"] == "UC2"


def test_an_unparseable_model_answer_ends_in_an_abstention_not_a_crash():
    case = load("uc1_missing_mapping_s")
    gate, _ = recording_gate()
    model = SimulatedModel(responses=[
        AIMessage(content=json.dumps(case["routing"])),
        AIMessage(content="I think we should look at the mapping table."),
        AIMessage(content="Here is my analysis in prose."),
    ])

    result = run_pipeline(case["ticket"]["id"], SimulatedServices(case), model, gate, statuses=STATUSES)

    assert result["resolution"]["abstention_reason"]
    assert result["resolution"]["proposed_correction"] == ""
