# Instrucciones del proyecto

Lee [contexto](docs/contexto-proyecto.md), [decisiones](docs/decisiones.md), [plan](docs/plan-preparacion.md), [arquitectura](docs/arquitectura.md) y [fuentes](docs/fuentes-contexto.md). El [Participant Kit](docs/referencias/Alenia%20AI%20Ticketing%20Challenge_Participant%20Kit.pdf) es la fuente oficial P1.

- Usa Python 3.12, uv y LangChain. Instala con `uv sync --locked`; declara dependencias en pyproject.toml y actualiza uv.lock deliberadamente. requirements.txt es una exportacion. No sustituyas el requisito por LangGraph; no introduzcas Conda.
- Desarrolla primero un agente sencillo con contratos pequenos, mocks, demo y evaluacion. No crees el arbol completo por anticipado.
- Clasifica caso de uso y prioridad antes de investigar. Casos oficiales: UC1 normalizacion, UC2 reconciliacion mensual, UC3 verificacion/correccion. Primer UC aun pendiente de seleccion.
- Aprobacion humana explicita antes de ejecutar cualquier SQL generado, comentario o cambio de estado. Mostrar payload y proposito; bloquear si no hay respuesta o cambia el payload. El modelo no puede aprobarse a si mismo.
- Respeta las cuatro funciones oficiales y la capacidad SQL descrita en P1. No agregues tools ni permisos de escritura de datos sin evidencia del contrato.
- Usa datos sinteticos del equipo y la infraestructura proporcionada: Databricks, OpenProject, Model Serving y Mosaic AI Vector Search. No conectes APIs externas ni modifiques infraestructura en competicion.
- OpenRouter y LangSmith son exploraciones; no activarlos en competicion sin aclaracion oficial. Mantener evaluacion/trazas locales. Voz, Jev, multiagente complejo y Agent Bricks no son requisitos.
- Reutiliza SDKs y mecanismos LangChain compatibles con el runtime; verifica firmas, schemas y estados antes de implementar adaptadores reales. Scripts/CLI reproducibles; notebooks solo como entrada al mismo codigo si conviene.
- No confundir servicios locales reportados con accesos oficiales verificados. No afirmar que instalaciones, integraciones o demo funcionan sin ejecutarlas.
- No incluir secretos en archivos, fixtures, logs ni Git; credenciales oficiales en vault. Conservar originales y conversaciones.
- La migracion sigue parcial: dos Markdown v2 y parte del historial pendientes. Citar fuentes y distinguir decisiones, propuestas y trabajo ejecutado.
- Fecha limite: 16 octubre 2026, 14:00 Europe/Madrid, freeze sin cambios de codigo; presentacion desde 16:00 con tickets nuevos.
- GitHub conecta cloud y Mac. Antes de trabajar, revisar status, rama y commit; publicar una etapa antes de retomarla en otro checkout. No sobrescribir cambios del usuario.
