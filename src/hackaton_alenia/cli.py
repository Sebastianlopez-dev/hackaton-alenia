"""Run the local simulation with explicit terminal approvals."""

import argparse
import json

from hackaton_alenia.agent import run_ticket
from hackaton_alenia.approvals import Approval, ApprovalDenied, ApprovalGate
from hackaton_alenia.evaluation import evaluate
from hackaton_alenia.integrations.services_s import SimulatedServices
from hackaton_alenia.llm_s import simulated_model
from hackaton_alenia.settings import CASE_PATH, EXPECTED_PATH


def human_decision(request):
    print(f"\nAction: {request.action}\nTicket: {request.ticket_id}\nPayload: {request.payload}\nPurpose: {request.purpose}")
    try:
        approved = input("Type approve to execute this simulated action: ").strip() == "approve"
    except (EOFError, KeyboardInterrupt):
        approved = False
    return Approval(request, approved)


def main() -> int:
    parser = argparse.ArgumentParser(description="Local scripted ticket simulation; no external services.")
    parser.add_argument("--evaluate", action="store_true", help="Compare the approved demo result with local expectations.")
    args = parser.parse_args()
    print("SIMULATION: scripted model and in-memory services; approvals are human.")
    case = json.loads(CASE_PATH.read_text())
    services = SimulatedServices(case)
    try:
        result = run_ticket(case["ticket"]["id"], services, simulated_model(case), ApprovalGate(human_decision))
    except ApprovalDenied as error:
        print(str(error))
        return 1
    result["simulation"] = True
    if args.evaluate:
        result["evaluation"] = evaluate(result, json.loads(EXPECTED_PATH.read_text()))
    print(json.dumps(result, indent=2))
    return 0 if result.get("evaluation", {}).get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
