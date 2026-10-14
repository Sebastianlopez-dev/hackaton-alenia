# Local ticket demo
Branch: `codex/local-ticket-demo`; delivery: ask-on-risk, chosen chain: stacked-to-main; forecast ~380 authored lines, actual ~520 across two slices.
Runner: `PYTHONPATH=src uv run --locked pytest -q`; local services and model only.

## Specs

- S1: "bien podemos crearlo todo." Scope: the first local LangChain demo, approvals, CLI, evaluation, tests and synthetic fixtures from the proposed file list. No official connections. Keep the existing Ticket fields.
- S2: "para las cosas que son simulaciones que no iran cuando construyamos vamos a ponerles -s.py al final. Para saber que son simulaciones." The user accepted the compatible `_s.py` alternative with "Perffecto". Runtime simulation modules use `_s.py`; real contracts and controls do not. Simulation fixtures use `_s.json`.
- S3: "Yo quiero ir con la creación de cada uno de los archivos." Keep responsibilities small and document each file briefly. Approval payload and purpose must be shown; no answer, rejection or changed payload blocks SQL, comments and status. LangChain cannot approve actions.
- Checks: deterministic RED before implementation, full suite, approved/rejected/absent/changed-payload scenarios, independent approval verification. The normalization fixture is an example, not a final choice of initial UC or an official schema.

## Tasks

- T1a (S1, S3): inline, complete; Ticket, local service contracts and approval controls with unit tests/docs. First slice: `b7729e4..06e4264`, 162 lines, isolated 18 tests passed. Native risk review granted, no findings, acknowledged.
- T1b (S1–S3): inline, complete; scripted demo, tools, CLI, evaluation and integration tests/docs. Second slice: `06e4264..cbc4ef3`, 352 lines plus passive closing log; isolated 31 tests passed. Native assessment medium, `review_due=false`, `under_budget`.
- T2 (S1–S3): delegated verifier, complete; independent security verification in scratch passed, no blockers (risk item 2: approvals). Covered by `06e4264` and `cbc4ef3`; stale/untyped decision regression tests pass.

## Log

- L1: User request: "bien podemos crearlo todo. y para las cosas que son simulaciones que no iran cuando construyamos vamos a ponerles -s.py al final. Para saber que son simulaciones.\n\nS"; confirmation of `_s.py`: "Perffecto".
- L2: Baseline `b7729e4`; existing uncommitted Ticket and its tests belong to this unit. Python 3.12.15, uv 0.13.1, LangChain 1.4.5. Preserve existing dependency lock and `package=false`; run with `PYTHONPATH=src`.
- L3: RED: approvals/agent imports failed before implementation. GREEN: `PYTHONPATH=src uv run --locked pytest -q`, 29 passed; approved terminal demo and local evaluation passed. Real tracing disabled via host context; scripted values and synthetic SQL explicitly documented. Independent verification next. Authored scope exceeds the ~400-line delivery heuristic; chain strategy remains pending before any work-unit commit.
- L4: Independent verifier passed S1–S3: approval field binding, stale/forged decisions, cross-ticket actions, CLI exits, source/fixture hashes and zero network attempts inside run_ticket. Direct tool calls outside host tracing context require disabled tracing; documented. Regression tests added for stale and untyped decisions. No commits yet: delivery-strategy decision pending.
- L5: User accepts "dos entregas encadenadas hacia main: primero contratos y aprobaciones; despues demo y evaluacion" with "si". Strategy: stacked-to-main. Local commits only; no PR, push or merge authorized. Source suite: 31 passed. Independent slices will be checked before commits; RDD assessment uses committed boundaries.
- L6: User: "revisar cambio y commit and push". Push authorized to the feature branch, not merge. First review: lineage `review-99f7fddf7a755412`, exact target acknowledged, no security findings. Reviewed boundary advances to `06e4264`. Second slice retains full-demo tests and docs.
- L7: First slice `06e4264`: 162 lines, 18 unit tests. Second slice `cbc4ef3`: 352 lines, 31 total tests; native assessment medium/under_budget, no additional review due. Source unchanged after checks; remaining commit records this passive closing log. No PR or merge. Risk: item 2 (human approval controls), independently verified; official integration and model reasoning remain untested.
