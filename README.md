# Hackathon Ironhack - Ayvens / Alenia

Preparación para el Alenia AI Ticketing Challenge, 15–16 de octubre de 2026, Madrid.

**Stack:** Python 3.12, uv y LangChain. **Infraestructura oficial:** Databricks y OpenProject.

## Estado

Demo local LangChain con modelo y servicios simulados. Accesos e integraciones oficiales aún sin verificar.

## 1. Preparar y comprobar el entorno

En macOS o Linux:

1. Instalar uv si falta:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Abrir una terminal nueva y entrar en la carpeta del repositorio.

3. Instalar Python 3.12:

   ```bash
   uv python install 3.12
   ```

4. Crear `.venv` e instalar las dependencias del lock:

   ```bash
   uv sync --locked
   ```

5. Activar el entorno y comprobarlo:

   ```bash
   source .venv/bin/activate
   uv --version
   python --version
   which python
   ```

   Esperado: Python `3.12.x` y una ruta terminada en `.venv/bin/python`.

   Para salir del entorno: `deactivate`.

Repetir en cada equipo; no copiar `.venv`. Versionar `pyproject.toml`, `uv.lock` y `.python-version`.

`requirements.txt` es una exportación; no editarlo a mano. Para regenerarlo:

```bash
uv export --locked --format requirements-txt --output-file requirements.txt
```

## 2. Desarrollo

Desde la raíz, ejecutar la demo:

```bash
PYTHONPATH=src uv run --locked python -m hackaton_alenia.cli --evaluate
```

Muestra payload y propósito; escribir `approve` para cada acción. Rechazo o falta de respuesta bloquean la ejecución. Modelo y resultados están guionados: no prueba razonamiento de IA ni integraciones reales.

Ejecutar las pruebas:

```bash
PYTHONPATH=src uv run --locked pytest -q
```

1. Leer [AGENTS.md](AGENTS.md), [decisiones](docs/decisiones.md) y [arquitectura](docs/arquitectura.md).
2. Revisar los archivos de la demo. El ejemplo UC1 no fija la elección del primer UC.
3. Verificar [compatibilidad con Databricks](docs/compatibilidad-databricks.md) y contratos oficiales antes de conectar servicios reales.

| Archivo en `src/hackaton_alenia/` | Responsabilidad |
| --- | --- |
| `ticket.py` | Información del ticket |
| `settings.py` | Rutas locales |
| `integrations/contracts.py` | Interfaces locales de servicios |
| `integrations/services_s.py` | Servicios simulados en memoria |
| `approvals.py` | Decisión humana ligada al payload exacto |
| `llm.py` | Clasificación de UC y prioridad |
| `llm_s.py` | Respuestas simuladas del modelo |
| `tools.py` | Tools permitidas con guard de aprobación |
| `agent.py` | Coordinación LangChain |
| `cli.py` | Demo y aprobaciones por terminal |
| `evaluation.py` | Comparación con expectativas locales |

`_s.py` identifica simulaciones; casos y expectativas están en `evals/` como `_s.json`. Los mocks pueden conservarse para pruebas cuando se incorporen adaptadores reales.

## Reglas clave

- Aprobación humana explícita antes de ejecutar SQL generado, publicar comentarios o cambiar estados.
- En competición: datos sintéticos del equipo y herramientas oficiales; sin APIs externas ni cambios de infraestructura.
- Secretos oficiales en vault, nunca en Git. Mantener `LANGSMITH_TRACING=false`.

## Documentación

- [Contexto y puntuación](docs/contexto-proyecto.md)
- [Decisiones](docs/decisiones.md)
- [Plan y calendario](docs/plan-preparacion.md)
- [Arquitectura y contratos](docs/arquitectura.md)
- [Fuentes y pendientes de recuperación](docs/fuentes-contexto.md)
- [Referencias originales](docs/referencias/README.md)
- [CodeGraph: skill de proyecto y CLI local/cloud](docs/codegraph.md)
