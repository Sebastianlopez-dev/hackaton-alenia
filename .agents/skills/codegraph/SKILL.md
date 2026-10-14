---
name: codegraph
description: Explore Python symbols, call relationships and change impact in hackaton-alenia using the local CodeGraph CLI. Use before structural code changes or questions about execution flows.
---

# CodeGraph for this project

Project adaptation, not an upstream official skill. Based on colbymchenry/codegraph 1.6.2 README and MCP server instructions, inspected at commit 5da4a41d92671d31a4759df5ca935d25a3e5a1de. Source: https://github.com/colbymchenry/codegraph.

## Availability

The managed cloud session may not expose a CodeGraph MCP tool. Use the CLI through `bash scripts/codegraph.sh` from the repository root. The wrapper installs pinned CodeGraph under ignored `.codegraph/`, disables telemetry, and does not start a persistent daemon. Requires Node/npm and network access for the first installation. No Python dependencies are added.

## Workflow

1. Check `bash scripts/codegraph.sh status --json`. If this checkout has no index, initialize only when setup/indexing is authorized: `bash scripts/codegraph.sh init --yes`. The user authorized indexing this project during the original setup; a different project requires its own context.
2. Without an MCP watcher, run `bash scripts/codegraph.sh sync` after code changes or pulling commits, before relying on structural results.
3. Query exact symbols or file names: `bash scripts/codegraph.sh explore 'ApprovalGate ticket_tools run_ticket' --max-files 4`. Natural-language queries use lexical matching; retry with precise names if empty.
4. Use returned source and call relationships to identify modules and affected tests. Read docs/configs with normal tools because CodeGraph does not cover everything.
5. If freshness warnings appear, sync again or read the flagged files. Treat cross-file resolution as best effort; the graph does not validate correctness. Run relevant tests after changes.

If the CLI fails or the index is absent, use normal repository tools and report the limitation. Do not claim an MCP connection just because the CLI works. Do not copy indexes between machines or commit `.codegraph/` data. Do not change business logic, agent approvals or hackathon integrations as part of graph setup.

## Optional MCP

The upstream supported integration is `codegraph install --target codex --location local --yes`, followed by loading/trusting the project configuration in a compatible Codex host. It writes `.codex/config.toml` and an instructions block in AGENTS.md. Do not run it automatically in a managed cloud session: modifying config does not make new tools appear in an already running host. This project skill and CLI work without that connection.
