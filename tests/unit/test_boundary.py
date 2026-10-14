"""The line between simulation and the real environment is enforced, not only documented."""

import ast
from pathlib import Path

SRC = Path("src/hackaton_alenia")
EVALS = Path("evals")

# Only these modules may choose between simulation and live.
COMPOSITION_POINTS = {SRC / "cli.py", SRC / "integrations" / "factory.py"}


def _is_simulation(module: str) -> bool:
    return module.rsplit(".", 1)[-1].endswith("_s")


def _imported_modules(path: Path) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_only_the_composition_points_import_simulation_modules():
    offenders = {
        str(path): sorted(module for module in _imported_modules(path) if _is_simulation(module))
        for path in SRC.rglob("*.py")
        if path not in COMPOSITION_POINTS and not path.stem.endswith("_s")
    }

    assert {path: modules for path, modules in offenders.items() if modules} == {}


def test_every_fixture_is_marked_as_simulation():
    fixtures = list(EVALS.rglob("*.json"))

    assert fixtures
    assert [str(path) for path in fixtures if not path.stem.endswith("_s")] == []
