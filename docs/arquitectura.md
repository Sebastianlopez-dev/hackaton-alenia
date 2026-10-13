# Arquitectura discutida

Fuentes: S3 y correccion de S4 en [inventario](fuentes-contexto.md). Estado: propuesta documental, sin codigo implementado. LangChain, uv, demo/evaluacion y reutilizacion son requisitos confirmados; el resto del arbol requiere revision.

## Principios

LangChain coordina LLM, tools, prompts y contexto. Python contiene reglas, validacion, clientes de APIs, errores y revision humana. Se propone intercambiar proveedores de modelos sin cambiar logica de negocio. Flujo conceptual: ticket -> investigacion con evidencia -> propuesta de resolucion -> revision humana -> accion. No implica una implementacion con LangGraph.

## Arbol propuesto recuperado

Adaptado de S3 al nombre del repositorio; no son archivos existentes. Los directorios `use_cases` y el contrato retrieval proceden tambien de S4 y S3, respectivamente.

```text
hackaton-alenia/
  pyproject.toml
  README.md
  .env.example
  .gitignore
  src/
    core/                 # config.py, settings.py, exceptions.py, logging.py
    llm/                  # base.py, factory.py, openrouter.py, databricks_model.py
    integrations/
      databricks/         # client.py, sql.py, vector_search.py
      openproject/        # client.py, tickets.py, comments.py
      langsmith/          # tracing.py
    tools/                # databricks, openproject, retrieval, validation
    agent/                # prompts.py, tools.py, agent.py, runner.py
    domain/               # schemas.py, ticket.py, evidence.py, resolution.py
    evaluation/           # dataset.py, evaluators.py, run_eval.py
    workflows/            # investigate.py, resolve.py, human_review.py
    use_cases/            # alternativas discutidas: normalization, fleet_discrepancy, data_error
  tests/
    unit/
    integration/
    fixtures/
  evals/
    cases/
    expected/
  demo/                   # sample_ticket.json, run_demo.py
  scripts/                # pruebas de conectores y smoke_test.py
```

`use_cases` y `workflows` pueden solaparse; `config.py` y `settings.py` tambien. La poda modulo por modulo sigue pendiente [S3]. No crear toda esta estructura sin decidir su utilidad. Los tres casos de uso proceden de recomendaciones del asistente y requieren contrastarse con la especificacion original.

## Conectores y contratos discutidos

| Pieza | Operaciones propuestas | Estado |
| --- | --- | --- |
| LLM | `invoke(messages)`, `get_llm(provider, model)` | Contrato generico y factory; OpenRouter y Databricks como adaptadores candidatos |
| Databricks | `execute_sql`, `get_table`, `query_table`, `vector_search`, `get_job_status` | Interfaces genericas propuestas; queries, schemas y acceso reales pendientes |
| OpenProject | `read_ticket`, `create_comment`, `update_ticket_status`, `get_ticket_history` | Adaptador de tickets propuesto; API y permisos pendientes |
| Retrieval | `retrieve_similar_documents`, `retrieve_similar_tickets`, `retrieve_context` | Contrato propuesto; backend sin seleccionar |
| Tools | Envolver funciones Python con tools de LangChain | Reutilizar mecanismos existentes; definir contratos, errores y validaciones locales |
| LangSmith | Trazas, datasets, experimentos, evaluacion | Integracion recomendada desde el primer agente; acceso y obligatoriedad sin confirmar |

Las funciones anteriores son nombres y pseudocontratos de la conversacion, no APIs verificadas de una version instalada.

## Codigo reutilizable y trabajo propio

Reutilizar chat models, agents, tool calling, salida estructurada, retrievers, callbacks e integraciones de LangChain; SDK y conector SQL de Databricks; API de OpenProject; APIs de proveedores; trazas/evaluacion de LangSmith [S3, S4]. No se recuperaron archivos fuente, versiones, ejemplos ejecutados ni enlaces a implementaciones concretas.

El trabajo propio propuesto es configurar y envolver esas piezas: contratos, schemas, cliente/adaptador, mocks, tests, prompts base, logica de investigacion y resolucion, revision humana, demo y evaluadores. S4 menciona Pydantic como opcion para schemas, sin seleccion confirmada.

La demostracion con mocks permite preparar la base antes de disponer de datos reales. Evaluacion propuesta: calidad de respuesta, evidencia, uso de herramientas, errores, latencia, tokens y coste [S3]. Criterios y umbrales siguen abiertos.

## Exploraciones

Databricks Vector Search, FAISS y Chroma son alternativas mencionadas, no tres dependencias requeridas [S3]. Voz es una posibilidad cuya discusion detallada no llego en los turnos disponibles [U1, S2]. S2 explora un orquestador con agentes especializados y Jev para routing, comparado con prompts y salida estructurada; nombres transcritos como Sol/Jeff/JEV no fijan un modelo de produccion. Las afirmaciones del asistente sobre productos y disponibilidad necesitan verificacion tecnica actual.
