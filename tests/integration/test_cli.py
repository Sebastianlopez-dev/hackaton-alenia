import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize("answers,exit_code", [("approve\napprove\napprove\n", 0), ("reject\n", 1), ("", 1)])
def test_cli_shows_payload_and_requires_human_input(answers, exit_code):
    result = subprocess.run([sys.executable, "-m", "hackaton_alenia.cli", "--evaluate"],
        input=answers, text=True, capture_output=True, env={**os.environ, "PYTHONPATH": "src"})
    assert result.returncode == exit_code
    assert "SIMULATION" in result.stdout
    assert "Payload: SELECT" in result.stdout
    assert "Purpose:" in result.stdout
    if exit_code == 0:
        assert '"passed": true' in result.stdout
    else:
        assert "Blocked sql" in result.stdout
        assert "Action: comment" not in result.stdout
