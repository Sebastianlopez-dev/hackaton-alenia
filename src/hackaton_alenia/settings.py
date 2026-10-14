"""Local demo paths, resolved independently of the terminal directory."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = ROOT / "evals/cases"
EXPECTED_DIR = ROOT / "evals/expected"
CASE_PATH = CASES_DIR / "uc1_missing_mapping_s.json"
EXPECTED_PATH = EXPECTED_DIR / "uc1_missing_mapping_s.json"
