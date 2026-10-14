# Contratos y aprobaciones locales

- `ticket.py`: captura `id`, `title` y `description`, todos obligatorios.
- `integrations/contracts.py`: define interfaces locales; las firmas oficiales siguen pendientes.
- `approvals.py`: vincula cada decision humana al ticket, accion, payload, proposito y token de una solicitud inmutable.

Sin aprobacion explicita para esa solicitud, la accion se bloquea. Una respuesta vieja o alterada no autoriza una solicitud nueva. El guard recibe la decision desde el host; no se expone como tool del modelo.

Pruebas desde la raiz:

```bash
PYTHONPATH=src uv run --locked pytest tests/unit -q
```

Las simulaciones posteriores usan `_s.py`. Estos contratos no conectan servicios ni ejecutan SQL.
