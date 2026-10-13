# Instrucciones del proyecto

Lee primero [contexto](docs/contexto-proyecto.md), [decisiones](docs/decisiones.md), [plan](docs/plan-preparacion.md), [arquitectura](docs/arquitectura.md) y [fuentes y cobertura](docs/fuentes-contexto.md).

- Usa LangChain como capa del agente. No sustituyas este requisito por una arquitectura LangGraph.
- Usa uv para la preparacion Python. No introduzcas Conda para el alcance previsto.
- Incluye demo y evaluacion desde la primera capacidad. Prioriza evidencia, auditabilidad y revision humana segun las decisiones documentadas.
- Prepara conectores y modulos pequenos reutilizables. Reutiliza SDKs y APIs existentes; verifica versiones y contratos antes de implementar ejemplos del historial.
- El arbol es propuesto y requiere poda. No inventes schemas, datos reales, prompts finales ni requisitos del hackathon.
- Databricks, LangSmith, OpenRouter y OpenProject estan discutidos; confirma necesidad y acceso. Voz y modelos especializados son exploraciones.
- Distingue decisiones del usuario, recomendaciones, trabajo ejecutado y pendientes. Cita fuente y turno para decisiones importantes; registra correcciones posteriores.
- La migracion es parcial. No reconstruyas ni etiquetes resumenes como documentos originales. Guarda los originales v2 en `docs/referencias/` solo al recuperarlos.
- No modifiques ni borres conversaciones originales. No guardes credenciales, tokens o secretos en archivos o historial Git.
- No afirmes que cuentas, instalaciones, integraciones, demo o tests funcionan sin evidencia de ejecucion.
- Esta tarea escribe en `/workspace/hackaton-alenia`; el destino Mac solicitado es `/Users/adm/Documents/work/hackaton-alenia`, no accesible desde el shell cloud. Verifica el checkout local antes de transferir cambios.
