"""Local demo paths, resolved independently of the terminal directory."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = ROOT / "evals/cases/ticket_demo_s.json"
EXPECTED_PATH = ROOT / "evals/expected/ticket_demo_s.json"
