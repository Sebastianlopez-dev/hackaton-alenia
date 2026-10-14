"""Run the local simulation with explicit terminal approvals."""

import argparse
import json
from pathlib import Path

from hackaton_alenia.agent import run_ticket
from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import simulated_model
from hackaton_alenia.settings import CASE_PATH, CASES_DIR, EXPECTED_DIR, EXPECTED_PATH


def human_decision(request):
    print(f"\nAction: {request.action}\nTicket: {request.ticket_id}\nPayload: {request.payload}\nPurpose: {request.purpose}")
    try:
        approved = input("Type approve to execute this simulated action: ").strip() == "approve"
    except (EOFError, KeyboardInterrupt):
        approved = False
    return Approval(request, approved)


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
    print("SIMULATION: scripted model and in-memory services; approvals are human.")
    case_path, expected_path = resolve_case_paths(args.case)
    try:
        case = json.loads(case_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Cannot load case {case_path}: {error}")
        return 2
    services = SimulatedServices(case)
    try:
        result = run_ticket(case["ticket"]["id"], services, simulated_model(case), ApprovalGate(human_decision))
    except ApprovalDenied as error:
        print(str(error))
        return 1
    result["simulation"] = True
    if args.evaluate:
        try:
            expected = json.loads(expected_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(f"Cannot load expected result {expected_path}: {error}")
            return 2
        result["evaluation"] = evaluate(result, expected)
    print(json.dumps(result, indent=2))
    return 0 if result.get("evaluation", {}).get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
