# Live demo path

Branch: `codex/uc1-hardening` (continues `odd/tasks/uc1-hardening.md`); delivery: work-unit commits, push authorized by the user.
Runner: `PYTHONPATH=src uv run --locked pytest -q`. No official access exists yet; nothing here is verified against Alenia.

## Specs

- S1: "1 quiero hacer - databricks-langchain (ChatDatabricks): es la integración oficial de LangChain con Databricks. Es la que yo elegiría." Add the dependency deliberately and a Model Serving adapter built from typed settings, so live mode no longer refuses for lack of a model.
- S2: "y 2 tambien aplicarlo. Porque me llevara directo a demo." Deterministic UC1 orchestration: the script fixes the structure (read ticket, route, retrieve precedents, investigate, resolve, comment, status) and the model only proposes the next read-only query or `done`, and writes the resolution. No dependency on model tool calling.
- S3: "Es posible poner un label para saber de donde viene el output. por ajemplo cuando es el agente o el script?" Every step of the output states its source: script, agent (model), human (approval) or service (Databricks/OpenProject). The approval prompt states who generated the payload.
- S4: "Todo lo demas estoy de acuerdo contigo. procede. commit y push". Also: a set of never-seen synthetic tickets to measure routing with the real model; the two missing reviewer roles in the user's RDD model routing config (`/Users/adm/.pi/agent/subagents.json`); work-unit commits and push.

## Tasks

- T7 (S1): `databricks-langchain` dependency, `requirements.txt` export, model adapter and settings. Route: inline, risk item 5. Commit `feat(model): add the Databricks Model Serving adapter`.
- T8 (S2, S3): UC1 pipeline with provenance labels, default CLI flow. Route: inline, independent verifier after (risk item 2). Commit `feat(pipeline): orchestrate UC1 deterministically with labelled sources`.
- T9 (S4): never-seen routing tickets and a live-only routing evaluation. Route: inline. Commit `feat(eval): add unseen routing tickets and a live evaluation`.
- T10 (S4): add `review-refuter` and `review-validator` to the user's model routing config. Route: inline, outside the repository, no commit.

## Log

- L1: User request: "1 quiero hacer - databricks-langchain (ChatDatabricks): es la integración oficial de LangChain con Databricks. Es la que yo elegiría. y 2 tambien aplicarlo. Porque me llevara directo a demo. Es posible poner un label para saber de donde viene el output. por ajemplo cuando es el agente o el script? Todo lo demas estoy de acuerdo contigo. procede. commit y push".
- L2: Baseline `71f6c09` pushed to `origin/codex/uc1-hardening` before any change. `uv add databricks-langchain` resolved `databricks-langchain 0.21.0` without changing `langchain 1.4.5` or `langchain-core 1.6.10`; the lock grows from 46 to 165 packages (mlflow 3.17.1, databricks-connect 17.0.10, databricks-sdk 0.152.0, openai-agents among them); 118 tests still pass. `ChatDatabricks` constructs without credentials, exposes `bind_tools`, `with_structured_output(method=function_calling|json_mode|json_schema)` and accepts `workspace_client`. Importing it prints an mlflow agent hint unless `MLFLOW_DISABLE_AGENT_HINT=1`. The fixtures use 2, 5 and 6 queries, so the pipeline asks the model for the next query or `done` instead of a fixed step count.
- L3: User: "recuerda que aun no hay conectores reles. solo estamos creando la infra para que databricks se conecte, no necesita test ahora". The model adapter is infrastructure only and gets no new tests; runnable simulation behaviour (the pipeline) keeps test-first.
- L4: T7 complete. `build_model(settings)` in `integrations/factory.py` returns `ChatDatabricks(endpoint, temperature=0, timeout=60, max_retries=1)` and names any missing `MODEL_SERVING_ENDPOINT`, `DATABRICKS_HOST` or `DATABRICKS_TOKEN`. Measured: `WorkspaceClient(host, token)` performs network I/O in its constructor and did not return within 45 s against an unreachable host (`timeout` exit 124), so it is not used; `ChatDatabricks` reads the same environment variables, constructs in 0.0 s, and its `repr` and `model_dump` do not contain the token. The import is local to `build_model` so simulation never loads mlflow (about 7 s import). `MLFLOW_DISABLE_AGENT_HINT=1` is set by default. `requirements.txt` re-exported from the lock (164 pinned packages). Smoke run without network: `build_model` returns `ChatDatabricks`; a blank endpoint reports `Live model missing required settings: MODEL_SERVING_ENDPOINT`. Suite: 118 passed. Untested against Alenia's endpoint. Risk: item 5 (dependencies).
