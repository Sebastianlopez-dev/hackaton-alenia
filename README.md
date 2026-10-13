# Hackathon Ironhack - Ayvens / Alenia

Base de preparacion para el Alenia AI Ticketing Challenge, 15-16 de octubre de 2026, Madrid. Stack elegido: Python, uv y LangChain; infraestructura oficial Databricks/OpenProject.

## Estado

Requisitos oficiales y plan de desarrollo documentados. Codigo, demo, tests y evaluacion aun pendientes de implementacion. Docker/OpenProject local reportados como instalados, sin verificacion desde cloud. La recuperacion de conversaciones y Markdown v2 sigue parcial.

## Antes de desarrollar

1. Leer [AGENTS.md](AGENTS.md) y [decisiones](docs/decisiones.md).
2. Consultar [contrato y arquitectura](docs/arquitectura.md), [plan y criterios de terminado](docs/plan-preparacion.md).
3. Elegir primer UC y preparar paquete uv, contratos, guard de aprobaciones y demo mock con evaluacion.
4. Verificar runtime y manual de accesos antes de conectar herramientas reales.

SQL generado, comentarios y cambios de estado requieren aprobacion humana explicita. Competicion: solo datos sinteticos del equipo, herramientas oficiales y capacidad SQL descrita; sin APIs externas ni cambios de infraestructura.

## Documentacion

- [Contexto y puntuacion](docs/contexto-proyecto.md)
- [Decisiones y aclaraciones pendientes](docs/decisiones.md)
- [Plan, calendario y cambio Mac/cloud](docs/plan-preparacion.md)
- [Arquitectura, contratos y modelo de datos](docs/arquitectura.md)
- [Fuentes y cobertura](docs/fuentes-contexto.md)
- [Referencias originales](docs/referencias/README.md)

## Dependencias iniciales

Antes de instalar, obtener la version Python del entorno del equipo siguiendo [verificacion de Databricks](docs/compatibilidad-databricks.md). Cuando este confirmada, usar esa misma version localmente:

```bash
uv venv --python <version-python-confirmada>
uv pip install -r requirements.txt
```

`requirements.txt` incluye LangChain, Pydantic, HTTPX y pytest con rangos de version principal provisionales. Python 3.11 no se ha verificado contra Databricks y no es una version acordada. No es un lockfile: fijar versiones y consolidar `pyproject.toml` y `uv.lock` tras verificar el entorno oficial. La resolucion previa de dependencias no demuestra instalacion ni compatibilidad con el workspace.

Los clientes oficiales de Databricks se incorporaran cuando se verifique el contrato tecnico. Aun no hay comandos de demo disponibles. Los secretos oficiales se gestionan en vault y no se publican en Git.

LangChain instala LangGraph y LangSmith como dependencias transitivas; esto no cambia la arquitectura elegida ni activa tracing externo. Mantener `LANGSMITH_TRACING=false` al ejecutar el proyecto.
