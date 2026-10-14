#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tool_root="$project_root/.codegraph/cli"
cli="$tool_root/node_modules/.bin/codegraph"

if [[ ! -x "$cli" ]]; then
    npm install --prefix "$tool_root" \
        --cache "$project_root/.codegraph/npm-cache" \
        --no-audit --no-fund '@colbymchenry/codegraph@1.6.2' >&2
fi

cd "$project_root"
export CODEGRAPH_TELEMETRY=0
export CODEGRAPH_NO_DAEMON=1
export CODEGRAPH_INSTALL_DIR="$tool_root/bundles"
exec "$cli" "$@"
