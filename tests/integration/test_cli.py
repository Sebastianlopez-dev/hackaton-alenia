import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize("answers,exit_code", [
    ("approve\napprove\napprove\napprove\n", 0),
    ("reject\n", 1),
    ("", 1),
])
def test_cli_shows_payload_and_requires_human_input(answers, exit_code):
    result = subprocess.run([sys.executable, "-m", "hackaton_alenia.cli", "--evaluate"],
        input=answers, text=True, capture_output=True, check=False, env={**os.environ, "PYTHONPATH": "src"})
    assert result.returncode == exit_code
    assert "SIMULATION" in result.stdout
    assert "Payload: SELECT" in result.stdout
    assert "Purpose:" in result.stdout
    if exit_code == 0:
        assert '"passed": true' in result.stdout
    else:
        assert "Blocked sql" in result.stdout
        assert "Action: comment" not in result.stdout


def test_cli_can_run_an_alternate_fixture():
    result = subprocess.run(
        [sys.executable, "-m", "hackaton_alenia.cli", "--case", "uc1_holding_changed_s", "--evaluate"],
        input="approve\napprove\napprove\napprove\napprove\napprove\napprove\n",
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    assert result.returncode == 0
    assert '"passed": true' in result.stdout


def _run_cli(args, input_text):
    return subprocess.run(
        [sys.executable, "-m", "hackaton_alenia.cli", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "src"},
    )


def test_cli_prompt_shows_routing_context_and_consequences():
    result = _run_cli(["--evaluate"], "approve\n" * 6)
    assert result.returncode == 0
    assert "Use case:" in result.stdout
    assert "Priority:" in result.stdout
    assert "Approval request #" in result.stdout
    assert 'If you type "approve"' in result.stdout
    assert "the run stops here and NOTHING is executed" in result.stdout


def test_cli_includes_audit_ledger_after_success():
    result = _run_cli(["--evaluate"], "approve\n" * 6)
    assert result.returncode == 0
    assert '"audit"' in result.stdout
    assert '"outcome": "approved"' in result.stdout
    assert '"run_id"' in result.stdout


def test_cli_audit_records_a_denied_decision():
    result = _run_cli(["--evaluate"], "reject\n")
    assert result.returncode == 1
    assert '"outcome": "rejected"' in result.stdout


def test_cli_audit_records_an_absent_decision():
    result = _run_cli(["--evaluate"], "")
    assert result.returncode == 1
    assert '"outcome": "absent"' in result.stdout


def test_cli_default_flow_is_the_pipeline_and_labels_every_source():
    result = _run_cli(["--evaluate"], "approve\n" * 6)

    assert result.returncode == 0
    assert '"flow": "pipeline"' in result.stdout
    for label in ("[SERVICE]", "[AGENT]", "[SCRIPT]", "[HUMAN]"):
        assert label in result.stdout
    assert '"passed": true' in result.stdout


def test_cli_agent_flow_is_still_available():
    result = _run_cli(["--flow", "agent", "--evaluate"], "approve\n" * 6)

    assert result.returncode == 0
    assert '"passed": true' in result.stdout
