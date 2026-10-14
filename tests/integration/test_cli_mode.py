"""CLI mode selection and live-mode refusal."""

import subprocess
import sys


def test_cli_invalid_mode_fails_cleanly_without_leaking_secrets():
    result = subprocess.run(
        [sys.executable, "-m", "hackaton_alenia.cli", "--evaluate"],
        input="",
        text=True,
        capture_output=True,
        env={"PYTHONPATH": "src", "ALENIA_MODE": "prod", "DATABRICKS_TOKEN": "super-secret-token"},
    )
    output = result.stdout + result.stderr
    assert result.returncode == 2
    assert "Traceback" not in output
    assert "ALENIA_MODE must be 'simulation' or 'live'" in output
    assert "super-secret-token" not in output


def test_cli_simulation_first_line_shows_mode():
    result = subprocess.run(
        [sys.executable, "-m", "hackaton_alenia.cli", "--evaluate"],
        input="approve\n" * 12,
        text=True,
        capture_output=True,
        env={"PYTHONPATH": "src"},
    )
    first_line = result.stdout.splitlines()[0]
    assert "simulation" in first_line.lower()
    assert result.returncode == 0


def _live(args):
    return subprocess.run(
        [sys.executable, "-m", "hackaton_alenia.cli", *args],
        input="",
        text=True,
        capture_output=True,
        env={"PYTHONPATH": "src", "ALENIA_MODE": "live", "DATABRICKS_TOKEN": "super-secret-token"},
        timeout=60,
    )


def test_cli_live_requires_a_ticket_id():
    result = _live([])

    assert result.returncode == 2
    assert result.stdout.splitlines()[0].startswith("LIVE")
    assert "--ticket" in result.stdout


def test_cli_live_names_every_missing_setting_without_touching_the_network():
    result = _live(["--ticket", "1"])
    output = result.stdout + result.stderr

    assert result.returncode == 2
    assert "Traceback" not in output
    for name in ("MODEL_SERVING_ENDPOINT", "DATABRICKS_HOST", "OPENPROJECT_BASE_URL", "ALENIA_STATUS_PROPOSAL"):
        assert name in output
    assert "super-secret-token" not in output
