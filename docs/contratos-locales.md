# Contratos y aprobaciones locales

- `ticket.py`: captura `id`, `title` y `description`, todos obligatorios.
- `integrations/contracts.py`: define interfaces locales; las firmas oficiales siguen pendientes.
- `approvals.py`: vincula cada decision humana al ticket, accion, payload, proposito y token de una solicitud inmutable.
- `llm.py`: `Routing` (UC, prioridad y, para UC1, contexto de normalizacion opcional: subsidiaria, clase y codigo local afectado) y `Resolution` (analisis, correccion propuesta, registros impactados, evidencia, confianza, motivo de abstencion). Es un contrato local: el formato de referencia oficial de Alenia no esta publicado.
- `tools.py`: un fallo de capacidad vuelve al modelo como `{"error": ...}` para poder continuar; una negativa humana nunca se absorbe y detiene la corrida.
- `agent.py`: la corrida esta acotada por `RECURSION_LIMIT`. Sin resolucion valida, o si el modelo no termina, el resultado es una abstencion explicita en lugar de una excepcion.

`Routing` acepta la respuesta del modelo como texto plano, con fences de Markdown o como bloques de contenido, y extrae el contexto UC1 en la misma llamada de clasificacion cuando el ticket lo indica.

Sin aprobacion explicita para esa solicitud, la accion se bloquea. Una respuesta vieja o alterada no autoriza una solicitud nueva. El guard recibe la decision desde el host; no se expone como tool del modelo.

`SimulatedServices` acepta un fixture con multiples consultas SQL aprobadas (`approved_queries`); una consulta no listada devuelve error al modelo sin ejecutarse.

Pruebas desde la raiz:

```bash
PYTHONPATH=src uv run --locked pytest tests/unit -q
PYTHONPATH=src uv run --locked pytest tests/integration -q
```

Las simulaciones posteriores usan `_s.py`. Estos contratos no conectan servicios ni ejecutan SQL.
