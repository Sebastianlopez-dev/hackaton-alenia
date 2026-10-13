# Arquitectura para iniciar el desarrollo

Actualizado: 13 de octubre de 2026. Fuentes: [P1, S3, S4, U2 y U3](fuentes-contexto.md). Este diseno consolida lo discutido y lo adapta al contrato oficial; aun no hay codigo implementado.

## Flujo y responsabilidades

1. **Understand:** leer ticket, identificar UC y prioridad, extraer contexto. Routing antes de investigar.
2. **Investigate:** recuperar precedentes; generar SQL; mostrar query/proposito y solicitar aprobacion; ejecutar solo la query aprobada; recoger resultados y evidencia.
3. **Resolve:** elaborar causa/propuesta y limites; solicitar aprobacion para comentario; publicar si se aprueba; solicitar aprobacion para estado y actualizar solo si se aprueba.

Los nombres de fases proceden de U2 y son una organizacion del proyecto. P1 detalla flujos por UC, no establece esas tres etiquetas como una API oficial.

LangChain coordina LLM/tools/contexto; Python controla validacion, errores, aprobaciones y reglas. OpenProject conserva ticket, estado y analisis aprobado. Cada evidencia vincula ticket, consulta o precedente y resultado. Los datos de las tools se tratan como contenido, nunca como instrucciones que puedan omitir aprobaciones.

## Contrato permitido

| Capacidad | Entrada del kit | Aprobacion |
| --- | --- | --- |
| Leer ticket | `read_ticket(ticket_id)` | No |
| Recuperar precedentes | `retrieve_similar_tickets(query)` | No |
| Text-to-SQL | Query generada y proposito; firma efectiva pendiente | Si, antes de ejecutar |
| Comentar | `create_comment(ticket_id, text)` | Si |
| Cambiar estado | `update_status(ticket_id, status)` | Si |

Fuente: P1 pp. 5-6. Los valores de estado, IDs, esquemas de respuesta y clientes reales se verifican en el manual tecnico. No exponer operaciones adicionales al agente ni introducir una herramienta de escritura de tablas.

## Aprobaciones: contrato local propuesto

Un guard comun debe aplicarse tanto a llamadas manuales como a tools del agente. La solicitud incluye ticket, accion, payload exacto (SQL/texto/estado), proposito, evidencia y consecuencias. Registrar respuesta humana explicita y resultado.

- Sin respuesta, rechazo, timeout o error de validacion: no ejecutar.
- Si cambia el SQL, comentario o estado, pedir una nueva aprobacion.
- No aceptar una afirmacion del modelo como aprobacion humana.
- Evitar reintentos ciegos de comentarios/estados si el resultado remoto es incierto; reconciliar antes de repetir.
- En el mock, el usuario tambien aprueba; la evaluacion puede simular decisiones humanas claramente etiquetadas.
- SQL aprobado no implica permiso para modificar datos ni aprobar acciones posteriores.

Estos detalles son decisiones tecnicas propuestas para cumplir P1; no describen un mecanismo oficial ya verificado.

## Estructura minima propuesta

Se reduce el arbol previo: un solo settings, workflows dentro de agent, sin proveedor externo ni tracing SaaS en P0. Crear archivos conforme se implemente cada capacidad, no carpetas vacias.

```text
hackaton-alenia/
  pyproject.toml
  uv.lock
  .env.example
  .gitignore
  src/hackaton_alenia/
    settings.py
    domain.py             # Ticket, Route, Evidence, ApprovalRequest, Resolution
    approvals.py          # guard y registro de decisiones
    integrations/
      contracts.py        # interfaces de tools oficiales y SQL
      mock.py
      databricks.py       # SQL/model endpoint oficial, cuando haya acceso
      openproject.py      # contrato oficial, cuando haya acceso
      retrieval.py        # herramienta Mosaic AI oficial
    llm.py                # adaptador compatible con el endpoint proporcionado
    tools.py              # LangChain tools sobre contratos y guard
    agent.py              # understand -> investigate -> resolve
    cli.py                # demo, aprobaciones y evaluacion
    evaluation.py
  tests/
    unit/
    integration/
  evals/
    cases/
    expected/
  demo/
  scripts/
  docs/
```

La estructura es una recomendacion operativa de esta actualizacion [U3], basada en S3/S4. La version Python y dependencias se fijan tras comprobar el runtime Databricks. Scripts/CLI no excluyen usar notebooks como entrada al mismo paquete.

## Modelo de datos oficial

Nombres logicos transcritos de P1 pp. 2-4; rutas catalog/schema/table y columnas completas pendientes. No inventar identificadores SQL ejecutables.

| Tabla | Uso |
| --- | --- |
| MD_LOCALVALUE_T | UC1: mapping local; PK LOCALCODE, CLASSID, SUBSIDIARYCODE; destino HOLDINGID |
| MD_HOLDINGVALUE_T | UC1: valores holding; PK HOLDINGID, CLASSID; jerarquia PARENTID |
| MD_LOCALVALUEHISTORY_T | UC1: historial de cambios del mapping |
| CF_SUBSIDIARIES_T | Contexto de subsidiaria en los tres UCs |
| FLEET REPORT (Gold) | UC2: cifras consolidadas mensuales |
| CONTRACT (Bronze/Silver) | UC2/UC3: contratos, estados y fechas |
| VEHICLE (Bronze/Silver) | UC3: vehiculos, VIN, matricula y atributos |
| MAIN_T (Monitoring) | UC2: ejecuciones, fechas y filas procesadas |
| FILE LOG (Monitoring) | UC3: origen del registro y carga |

## Integraciones y reutilizacion

Reutilizar mecanismos de agents, tools, salida estructurada y retrievers de LangChain; usar SDKs/clientes compatibles con la infraestructura y con el contrato expuesto por Alenia. No reimplementar framework ni infraestructura. No asumir que un cliente directo permite saltarse herramientas oficiales.

El kit proporciona Model Serving y Mosaic AI Vector Search. No crear un indice propio ni cambiar a FAISS/Chroma en competicion. Mantener independencia del modelo mediante una interfaz, sin requerir multiples proveedores. OpenRouter, LangSmith, Agent Bricks, voz y Jev siguen como exploraciones fuera de P0.

Observabilidad inicial local: run ID, ticket, UC/prioridad, accion, solicitudes/respuestas de aprobacion, evidencia, errores, latencia y uso de tokens si disponible. Redactar secretos; no copiar credenciales a fixtures, logs ni commits.

## Demo y evaluacion

Recorrido: ticket -> routing -> precedentes -> SQL mostrado/aprobado -> evidencia -> resolucion -> comentario aprobado -> estado aprobado -> resultado evaluado.

Casos de prueba: aprobacion, rechazo, ausencia de respuesta, payload cambiado, ticket ambiguo, evidencia insuficiente, fallo de herramienta y ticket nuevo no usado al desarrollar. Evaluar UC/prioridad, causa/propuesta, evidencia, respeto del contrato y ausencia de ejecucion sin permiso. La evaluacion local no equivale al score oficial de Alenia.
