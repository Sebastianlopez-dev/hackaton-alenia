"""Run the local simulation with explicit terminal approvals.

The active mode is read from ``ALENIA_MODE`` (default ``simulation``). In live
mode the CLI refuses to start because the model adapter for the official Model
Serving endpoint is not implemented yet.
"""

import argparse
import json
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from hackaton_alenia.agent import run_ticket
from hackaton_alenia.approvals import Approval, ApprovalDenied, AuditApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.factory import build_services
from hackaton_alenia.llm_s import simulated_model
from hackaton_alenia.settings import CASE_PATH, CASES_DIR, EXPECTED_DIR, EXPECTED_PATH, load_settings
from hackaton_alenia.sql_guard import is_read_only, read_only_reason

_ACTION_INFO = {
    "sql": (
        "Run a read-only SQL query",
        "read-only",
        "This action only reads data; it will not modify any table.",
        "query",
    ),
    "comment": (
        "Publish a comment on the ticket",
        "ticket state change",
        "This action changes the ticket state; it does not modify data tables.",
        "comment text",
    ),
    "status": (
        "Update the ticket status",
        "ticket state change",
        "This action changes the ticket status; it does not modify data tables.",
        "status value",
    ),
}


def _action_info(request):
    """Never reassure the human about a statement the local check cannot clear."""
    if request.action == "sql" and not is_read_only(request.payload):
        return (
            "Run a SQL statement NOT recognised as read-only",
            "NOT VERIFIED AS READ-ONLY",
            f"WARNING: this statement was not recognised as a single read-only query "
            f"({read_only_reason(request.payload)}). It may modify data or storage. "
            f"The local check is a guard rail, not a security boundary: it can be wrong "
            f"in both directions, so verify the statement yourself before approving.",
            "statement",
        )
    return _ACTION_INFO[request.action]


def _approval_prompt(request, context, sequence):
    kind, scope, scope_note, thing = _action_info(request)
    return (
        f"\n--- Approval request #{sequence} ---\n"
        f"Use case: {context.get('use_case', 'unknown')} | "
        f"Priority: {context.get('priority', 'unknown')}\n"
        f"Ticket: {request.ticket_id}\n"
        f"Action kind: {kind} ({scope})\n"
        f"{scope_note}\n"
        f"\n"
        f"Payload: {request.payload}\n"
        f"Purpose: {request.purpose}\n"
        f"\n"
        f'If you type "approve", the agent will execute the exact {thing} shown above.\n'
        f"If you type anything else or press Ctrl-D, the run stops here and NOTHING is executed.\n"
        f"\n"
        f"Type approve to execute this simulated action: "
    )


def human_decision(request, gate):
    print(_approval_prompt(request, gate.context, gate.sequence))
    try:
        answer = input().strip()
    except (EOFError, KeyboardInterrupt):
        return None
    return Approval(request, answer == "approve")


def resolve_case_paths(case_arg: str | None) -> tuple[Path, Path]:
    if case_arg is None:
        return CASE_PATH, EXPECTED_PATH
    case_path = Path(case_arg)
    if not case_path.is_absolute():
        case_path = CASES_DIR / case_path
    if case_path.suffix != ".json":
        case_path = case_path.with_suffix(".json")
    expected_path = EXPECTED_DIR / f"{case_path.stem}.json"
    return case_path, expected_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Local scripted ticket simulation; no external services.")
    parser.add_argument("--case", help="Fixture name in evals/cases or an absolute path (default: uc1_missing_mapping_s).")
    parser.add_argument("--evaluate", action="store_true", help="Compare the approved demo result with local expectations.")
    args = parser.parse_args()

    try:
        settings = load_settings()
    except ValidationError as error:
        # Print only the validation messages, never the rejected input values.
        for problem in error.errors():
            print(f"Configuration error: {problem['msg'].removeprefix('Value error, ')}")
        return 2
    if settings.alenia_mode == "live":
        print("LIVE: official adapters requested.")
        print("The live model adapter is not available yet. Refusing to start.")
        return 1

    print("SIMULATION: scripted model and in-memory services; approvals are human.")
    case_path, expected_path = resolve_case_paths(args.case)
    try:
        case = json.loads(case_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Cannot load case {case_path}: {error}")
        return 2
    services = build_services(settings, simulated_case=case)
    run_id = uuid4().hex
    gate = AuditApprovalGate(
        lambda request: human_decision(request, gate),
        run_id=run_id,
    )
    try:
        result = run_ticket(case["ticket"]["id"], services, simulated_model(case), gate)
    except ApprovalDenied as error:
        result = {
            "run_id": run_id,
            "audit": [entry.as_dict() for entry in gate.ledger],
        }
        print(str(error))
        print(json.dumps(result, indent=2))
        return 1
    result["simulation"] = True
    if args.evaluate:
        try:
            expected = json.loads(expected_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(f"Cannot load expected result {expected_path}: {error}")
            return 2
        result["evaluation"] = evaluate(result, expected)
    result["run_id"] = run_id
    result["audit"] = [entry.as_dict() for entry in gate.ledger]
    print(json.dumps(result, indent=2))
    return 0 if result.get("evaluation", {}).get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
