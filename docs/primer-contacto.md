# Primer contacto con el entorno oficial

Runbook para el 15 de octubre. Objetivo: pasar de la simulación al entorno de Alenia sin confundir datos sintéticos propios con datos oficiales, y sin ejecutar nada que no esté verificado.

Regla de oro: **si el dato real contradice un fixture, el fixture está mal.** Nunca se adapta el código o la consulta para que encaje con un fixture `_s`.

Estado de partida: [estado de verificación](estado-verificacion.md).

## 0. Antes del checkpoint (09:30)

```bash
git status --short && git log --oneline -1
uv sync --locked
PYTHONPATH=src uv run --locked pytest -q
printf 'approve\n%.0s' $(seq 1 12) | PYTHONPATH=src uv run --locked python -m hackaton_alenia.cli --evaluate
```

Esperado: árbol limpio, todos los tests en verde y la demo con `"passed": true`. Si algo falla, se arregla antes de tocar el entorno real.

## 1. Preguntas para el checkpoint y Teams

Anotar cada respuesta con su fuente (persona, canal, hora). Sin respuesta, el valor sigue siendo local y no oficial.

| # | Pregunta | Dónde impacta |
| --- | --- | --- |
| 1 | Catálogo y schema del Unity Catalog del equipo | `DATABRICKS_CATALOG`, `DATABRICKS_SCHEMA` |
| 2 | Columnas reales de `MD_LOCALVALUE_T`, `MD_HOLDINGVALUE_T`, `MD_LOCALVALUEHISTORY_T`, `CF_SUBSIDIARIES_T` | fixtures UC1 y prompts de SQL |
| 3 | Mecanismo y límites del SQL: ¿warehouse? ¿solo lectura? ¿cómo se aprueba oficialmente? | `DATABRICKS_WAREHOUSE_ID`, gate de aprobación |
| 4 | Estados válidos de ticket en OpenProject y prioridades oficiales | `update_status`, `Routing.priority` |
| 5 | Formato de la salida de referencia con la que se mide el accuracy | `Resolution` |
| 6 | Endpoint de Model Serving y cómo se autentica | `MODEL_SERVING_ENDPOINT` |
| 7 | Nombre del índice de Vector Search y sus columnas | `DATABRICKS_VECTOR_SEARCH_INDEX_NAME`, `ALENIA_VECTOR_SEARCH_COLUMNS` |
| 8 | ¿Está permitido el tracing externo? ¿Dónde se ve el coste oficial por ticket? | `LANGSMITH_TRACING`, presentación |

## 2. Credenciales

- Salen del vault de Alenia. Nunca se pegan en código, tests, fixtures, docs, logs ni commits.
- Copiar `.env.example` a `.env` (está en `.gitignore`) y completar sólo lo verificado.
- **Pedir una credencial o un warehouse de solo lectura.** `sql_guard` es un guard rail; la frontera real es el permiso.
- `load_settings` lee variables de entorno, **no** carga `.env` por sí solo. Exportarlas en la shell:

```bash
set -a; source .env; set +a
```

Una variable vacía cuenta como no definida: el modo live lista por nombre todo lo que falta, sin mostrar valores.

## 3. Inventario antes de cualquier SQL del agente

Desde el SQL editor o un notebook de Databricks, escrito y ejecutado por una persona (no generado por el agente):

```sql
SHOW TABLES IN <catalog>.<schema>;
DESCRIBE TABLE <catalog>.<schema>.MD_LOCALVALUE_T;
DESCRIBE TABLE <catalog>.<schema>.MD_HOLDINGVALUE_T;
DESCRIBE TABLE <catalog>.<schema>.MD_LOCALVALUEHISTORY_T;
DESCRIBE TABLE <catalog>.<schema>.CF_SUBSIDIARIES_T;
```

Comparar con los fixtures. Columnas que hoy son **locales e inventadas**: `CHANGED_AT`, `NAME`, `COUNTRY`; el uso de `PARENTID` tampoco está verificado. Corregir los fixtures para que reflejen la realidad.

## 4. Un solo contacto por servicio

Prueba de humo escrita por una persona, en modo live, una llamada por servicio. Registrar la respuesta cruda (sin credenciales) en el log de la tarea.

```bash
ALENIA_MODE=live PYTHONPATH=src uv run --locked python -c "
from hackaton_alenia.settings import load_settings
from hackaton_alenia.integrations.factory import build_services
services = build_services(load_settings())
print(services.query_sql('SELECT 1 AS probe'))
print(services.read_ticket(<ticket_id_real>))
print(services.retrieve_similar_tickets('missing holding mapping'))
"
```

Esperado: una fila, un ticket mapeado a `id/title/description` y precedentes con las columnas configuradas. Cualquier error se registra tal cual; no se reintenta a ciegas.

## 5. Escrituras al final

- `create_comment` sólo sobre un ticket descartable acordado con el equipo, y sólo a través de la CLI con aprobación humana.
- `update_status` sólo con un nombre de estado leído de `GET /api/v3/statuses`; el adaptador rechaza un nombre desconocido.
- No existe ninguna capacidad para escribir datos de tablas, y no se agrega.

## 6. Lo que todavía bloquea la demo en vivo

- **El modelo real nunca respondió.** El pipeline necesita JSON válido en tres pasos (routing, siguiente query, resolución); si el modelo no lo da, el pipeline se abstiene y lo marca `[SCRIPT]`. Probarlo con un ticket descartable antes de la demo:

  ```bash
  ALENIA_MODE=live PYTHONPATH=src uv run --locked python -m hackaton_alenia.cli --ticket <id_descartable>
  ```
- El text-to-SQL contra el schema real no está probado: falta el primer ticket **nunca visto** con el schema real.

## 7. Cierre de cada paso

Después de cada paso: `pytest -q` en verde, actualizar [estado de verificación](estado-verificacion.md) y commitear con lo que se verificó y cómo. Nada se marca como verificado sin haberlo ejecutado.
