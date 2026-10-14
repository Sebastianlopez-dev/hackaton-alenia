"""Local exact-match checks, independent of the official Alenia score."""


def evaluate(result: dict, expected: dict) -> dict:
    checks = {key: result.get(key) == value for key, value in expected.items()}
    return {"passed": all(checks.values()), "checks": checks}
