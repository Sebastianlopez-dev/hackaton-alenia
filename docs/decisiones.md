# Decisiones

Actualizado: 14 de octubre de 2026. [Fuentes](fuentes-contexto.md). El Participant Kit fija el contrato oficial; las decisiones explicitas del usuario fijan las elecciones del proyecto. El resumen U2 aporta contexto reportado, no prueba de ejecucion.

## Confirmadas y vigentes

| ID | Decision | Fuente |
| --- | --- | --- |
| D01 | LangChain como capa del agente; no sustituir por LangGraph | S4: correccion del usuario en turno `12abefdd-e0a1-41ce-acd6-83ae9e001349`; U1; P1 pp. 1, 4 |
| D02 | Python con uv; no Conda para la preparacion | S5: turno `4f3e857a-2966-4a4c-84e3-4566341bdcdd`; U1 |
| D03 | Demo y evaluacion desde la primera capacidad, P0 | S1: propuesta `e4fecfc4-0524-42ec-bec2-150bf50343e2`, aceptacion `34c42af9-db49-4da9-b475-1551e5b94221`; U1 |
| D04 | Modulos y conectores pequenos reutilizables | S3: peticion `8401acb2-40d7-4048-97ff-2bf2dfedd9c9`; U1 |
| D05 | Evidencia, modelos intercambiables, revision humana y auditabilidad | Propuesta aceptada de S1; P1 p. 5 refuerza aprobaciones |
| D06 | UI y varios modelos despues del nucleo funcional | S1; P1 p. 7 ofrece bonus UI sin hacerla obligatoria |
| D07 | Conservar originales y excluir secretos de Git | U1; P1 pp. 5-6 |
| D08 | Voz y modelos especializados siguen siendo exploraciones | U1, S2; U2 |
| D09 | Aprobacion explicita antes de ejecutar SQL, comentarios y cambios de estado | P1 p. 5 |
| D10 | Solo herramientas oficiales y SQL autorizado; datos sinteticos del equipo, sin APIs externas | P1 pp. 5-6 |
| D11 | Databricks, OpenProject, Model Serving y Mosaic AI Vector Search son infraestructura oficial proporcionada | P1 pp. 4-5 |
| D12 | Clasificar caso y prioridad antes de investigar; elegir entre UC1, UC2 y UC3 | P1 pp. 1-3, 6 |
| D13 | Sincronizar Mac/cloud mediante commits de GitHub y tareas en ramas | Conversacion actual y E2 |
| D14 | Python 3.12 para preparacion local/cloud; dependencias fijadas con uv.lock | U4: usuario elige explicitamente Python 3.12; compatibilidad del workspace oficial aun pendiente |
| D15 | Usar `ticket.py` en lugar del nombre propuesto `domain.py` para capturar la informacion del ticket; empezar con `id`, `title` y `description` | Decision explicita del usuario, 14 de octubre de 2026; modelo local, no schema oficial |
| D16 | Identificar modulos simulados con `_s.py`; construir la primera demo local completa | Usuario acepta `_s.py` y autoriza crear la lista de archivos, 14 de octubre de 2026 |

## Resolucion de contradicciones

- LangGraph aparecia en recomendaciones anteriores. La correccion de S4 y U1 prevalece. Esto no prohibe dependencias transitivas internas de LangChain.
- Python 3.12 queda elegido para preparacion con uv/pyproject.toml y uv.lock. requirements.txt es una exportacion del lock; compatibilidad con el runtime proporcionado pendiente.
- La aprobacion no se limita a modificar datos: P1 exige aprobar tambien SQL de lectura, comentarios y estados. No hay permiso documentado para ejecutar correcciones SQL sobre datos.
- Los tres casos dejan de ser solo ejemplos: P1 los confirma, con nombres y alcance concretos. UC2 es reconciliacion mensual, no cualquier discrepancia de flota.
- Los conectores genericos anteriores (`get_job_status`, historial por API, FAISS/Chroma, APIs de modelos externas) no amplian el contrato permitido. Mantenerlos como ideas historicas, no implementarlos como tools de competicion.
- OpenRouter/LangSmith fueron discutidos antes de conocer las restricciones. No activarlos en competicion sin aclaracion oficial. Evaluacion y trazas locales siguen siendo necesarias y no dependen de un servicio externo.
- Ayvens es el nombre correcto; Alenia es el nombre del kit. Variantes dictadas como Ivans/Eventos/Alenis no definen otros proveedores.
- U2 dice "hoy es 12 de octubre"; el plan actual se revisa al 13 de octubre de 2026. La ventana original 7-15 se conserva como antecedente.

## Orientacion para comenzar

Un agente LangChain sencillo, funciones Python y adaptadores reemplazables. Implementar primero lectura/routing, retrieval y SQL aprobado; despues propuesta basada en evidencias, comentario aprobado y estado aprobado. Demo y evaluacion acompanaran cada paso [S3, U2, U3]. Es una orientacion de implementacion, no una afirmacion de codigo existente.

Scripts modulares y CLI como entrada reproducible; notebooks pueden servir para ejecutar/inspeccionar en Databricks, sin duplicar logica. Docker local sirve como preparacion opcional y no como dependencia de la demo mock [U2, P1 p. 4].

## Pendientes de decision o aclaracion

| Tema | Estado |
| --- | --- |
| Primer caso de uso y ampliacion | Elegir UC inicial; recomendacion tecnica: comenzar UC1 con fixture pequeno, sin fijarlo como decision del usuario |
| Acceso tecnico | Falta manual de registro, endpoints, schemas completos, estados de tickets y firmas reales |
| SQL y contrato | El kit permite SQL ademas de cuatro funciones, pero la regla dice "solo cuatro". Confirmar via Teams el mecanismo y limites de SQL; usar la capacidad descrita, sin inventar APIs |
| LangSmith/OpenRouter | No activar en competicion hasta aclarar la prohibicion de APIs externas |
| Coste de presentacion | Organizacion mide coste; aclarar como consultar resultados oficiales |
| Aprobaciones | Verificar interfaz/mecanismo oficial; la propuesta local asocia aprobacion a payload exacto y caduca si cambia |
| Multiagente, voz, Jev, Agent Bricks | Sin necesidad demostrada; fuera de P0. Agent Bricks no figura como requisito en P1 |
| Instalaciones locales | Docker Desktop, OpenProject stable/17 y token reportados en U2; funcionamiento no verificado |
| Historia original | Dos Markdown v2 y parte de conversaciones siguen pendientes; no bloquean contratos ya fundamentados en P1 |
