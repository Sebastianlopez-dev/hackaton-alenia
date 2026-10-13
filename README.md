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

No hay comandos de instalacion/demo disponibles hasta implementar el paquete. Los secretos oficiales se gestionan en vault y no se publican en Git.
