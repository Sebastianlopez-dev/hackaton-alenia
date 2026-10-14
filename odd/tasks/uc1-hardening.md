# UC1 hardening

Branch: `codex/uc1-hardening`; delivery: local work-unit commits per task, push/PR/merge owned by the user.
Source of requirements: `docs/referencias/Alenia AI Ticketing Challenge_Participant Kit.pdf` (P1) plus the user's selection below.
Runner: `PYTHONPATH=src uv run --locked pytest -q`. Local model and services only; no official access exists yet.

## Specs

- S1: "Creo que quiero hacerlo todo. Asi que pongamoslo como 4 tareas y vamos en ODD una por una".
  Scope is exactly the four gaps offered and selected in this session: (1) robustness plus a typed
  resolution contract, (2) complete UC1 flow over the official normalization tables, (3) richer
  human approval prompt plus an audit record of decisions, (4) the integration seam for Databricks,
  OpenProject and Vector Search. No fifth workstream is added.
- S2: "Ten en cuenta que aún no tengo datos oficiales de alenia". Nothing may depend on official data
  being present. Adapters are written against documented public APIs and tested with an in-process
  transport; they must never be reported as verified, connected or working until executed against the
  official environment. No endpoint, catalogue path, column, status value or priority value may be
  presented as official.
- S3: "este demo debería funcionar para UC1". UC1 must stay runnable end to end after every task:
  routing, precedents, approved SQL, evidence, resolution, approved comment and approved status, with
  the local evaluation passing. The suite stays green; a task that breaks the demo is not complete.
- S4: "busca que aún no esta contemplando". Every gap in scope is traceable to the Participant Kit,
  not to preference: the UC1 flow steps of p. 2, the text-to-SQL requirement and approval rules of
  p. 5, the routing and priority rule of p. 6, and the "the agent does not break" criterion of p. 6.
  Where the kit does not define a value (ticket states, priority names, reference output format), the
  value stays local, configurable and labelled unverified.

## Tasks

- T1 (S1, S3, S4): inline, complete; `5c9cb06`. Typed `Resolution` and `Evidence` requested through `create_agent(response_format=...)`, `RECURSION_LIMIT = 25`, explicit abstention instead of an exception, capability failures returned as `{"error": ...}`, and a tolerant routing read. RED observed in two steps before GREEN; 39 tests pass and the CLI demo exits 0 with `evaluation.passed: true`. Commit `feat(agent): type the resolution and contain model and tool failures`.
- T2 (S1, S2, S3, S4): complete UC1 over MD_LOCALVALUE_T, MD_HOLDINGVALUE_T, MD_LOCALVALUEHISTORY_T and CF_SUBSIDIARIES_T, with several sequentially approved queries and structured ticket extraction. Route: inline. Commit `feat(uc1): cover the full normalization flow`.
- T3 (S1, S3, S4): richer human approval prompt and an audit record of approved and denied decisions. Route: inline, independent verifier after (risk item 2). Commit `feat(approvals): enrich the approval prompt and record decisions`.
- T4 (S1, S2, S4): integration seam for Databricks SQL, OpenProject and Vector Search, plus typed settings. Route: inline, independent verifier after (risk item 2). Commit `feat(integrations): add official-service adapters and settings`.

## Log

- L1: User request: "vez todo lo que hay en este repo. Estoy ansioso porque mañana empezará la hackaton. Que ves aquí que este perdiendo detales del @\"docs/referencias/Alenia AI Ticketing Challenge_Participant Kit.pdf\" este demo debería funcionar para UC1. busca que aún no esta contemplando. Ten en cuenta que aún no tengo datos oficiales de alenia".
- L2: Read-only audit performed. Verified: `PYTHONPATH=src uv run --locked pytest -q` = 31 passed; working tree clean; all branches merged to `main`. Kit text extracted with `pdftotext`. Gaps reported: UC1 covers 3 of the 7 official flow steps; no structured ticket extraction; no text-to-SQL layer, schema catalogue or read-only guard; approval prompt lacks the context the kit scores; no audit log or cost/latency instrumentation; `json.loads` on the final message is fragile and `resolution` is untyped; local evaluation is exact-match on a fixture; no settings or adapters for Databricks, OpenProject, Model Serving or Vector Search; `bind_tools` never exercised against a real model; ticket states and priority names are invented.
- L3: User selected all four offered workstreams: "Creo que quiero hacerlo todo. Asi que pongamoslo como 4 tareas y vamos en ODD una por una". Branch `codex/uc1-hardening` created from clean `main` at `1299b6d`.
- L4: Verified in the installed stack (LangChain 1.4.5) that `create_agent` accepts `response_format` and returns `structured_response` in the final state, and that no `max_iterations` parameter exists, so the iteration bound must be the graph `recursion_limit` passed to `invoke`.
- L5: T1 complete at `5c9cb06`, 309 insertions and 41 deletions across 12 files. RED observed before GREEN in two independent steps: `ImportError: cannot import name 'RECURSION_LIMIT'` for `tests/integration/test_agent_s.py`, and `2 failed, 1 passed` for `tests/unit/test_llm.py` executed against the `HEAD` implementation copied to a scratch tree. GREEN: 39 tests pass (31 before); the CLI demo exits 0 with `evaluation.passed: true`. Measured on the installed stack: with `response_format` set, a model that never emits the structured-output tool call loops to the default 9999-step limit and raises `GraphRecursionError`, which is why the bound is explicit. The lens reported a stale `RECURSION_LIMIT` import error and an import-sorting complaint; both were refuted with independent evidence, a fresh LSP probe over the two paths returning 0 diagnostics (clean=2) and `ruff --select I` reporting the same sorting complaint against the untouched `HEAD` files, so the repository is not ruff-clean at baseline and that is pre-existing. Risk: none of the listed items. The approval gate itself is unchanged; the enforcement order (active ticket, then approval, then service) is preserved and pinned by 18 parameterised approval tests plus the new containment tests, and every failure path is fail-closed because no error path reaches a protected service.
