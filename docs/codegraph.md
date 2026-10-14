# CodeGraph en local y cloud

CodeGraph 1.6.2 probado el 14 de octubre de 2026. Upstream: https://github.com/colbymchenry/codegraph, commit inspeccionado 5da4a41d92671d31a4759df5ca935d25a3e5a1de.

El upstream proporciona CLI y servidor MCP para Codex, no un SKILL.md independiente. Este repositorio incorpora una [skill de proyecto adaptada](../.agents/skills/codegraph/SKILL.md) y un wrapper CLI. No es una skill oficial del autor.

## Preparar cada checkout

Requiere Node/npm para instalar el paquete de lanzamiento; CodeGraph distribuye su propio runtime. Desde la raiz:

```bash
bash scripts/codegraph.sh init --yes
bash scripts/codegraph.sh status --json
bash scripts/codegraph.sh explore 'ApprovalGate ticket_tools run_ticket' --max-files 4
```

El wrapper instala version 1.6.2 en `.codegraph/cli` en la primera llamada. Todo el indice, cache y herramientas quedan ignorados por `.codegraph/.gitignore`. No se agregan dependencias Python ni se cambian configuraciones globales. Telemetria desactivada; daemon persistente desactivado.

Despues de editar codigo o descargar commits, ejecutar `bash scripts/codegraph.sh sync` antes de explorar. La CLI no mantiene un watcher en segundo plano.

## MCP y skills

El instalador oficial de CodeGraph soporta `codegraph install --target codex --location local --yes`; escribe configuracion MCP de proyecto e instrucciones en AGENTS.md. Se necesita un host Codex que cargue y confie esa configuracion. No se ha ejecutado ese instalador aqui ni conectado un MCP a esta sesion cloud.

La skill vive en `.agents/skills/codegraph/SKILL.md`, una ubicacion de skills de proyecto. Nuevas sesiones compatibles pueden descubrirla; si una sesion gestionada no la lista, leer ese archivo explicitamente y usar la CLI. Versionar una skill no garantiza que el host recargue su catalogo durante una sesion abierta.

## Verificacion y alcance

El CLI upstream instalo y ejecuto correctamente en Linux cloud: 15 archivos Python, 119 nodos y 234 relaciones. `status` informo indice completo sin cambios pendientes. Una consulta de aprobaciones devolvio source, callers y tests relacionados. Esto comprueba el analisis local, no razonamiento del agente ni integraciones Databricks.

Cada maquina construye su propio indice. No copiar la base de datos del Mac a cloud. La herramienta ayuda al desarrollo del repositorio; no forma parte de las tools del agente de competicion y no altera sus reglas de acceso o aprobacion.
