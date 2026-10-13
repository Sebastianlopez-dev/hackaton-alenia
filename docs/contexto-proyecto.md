# Contexto del proyecto

Actualizado: 13 de octubre de 2026. Migracion parcial; consultar [cobertura y fuentes](fuentes-contexto.md).

## Objetivo y contexto

Preparar una base modular reutilizable para el hackathon de Ironhack con Ayvens y Alenia en Espana. El usuario quiere llegar con conectores, pequenos scripts e interfaces preparados, aprovechando SDKs e integraciones existentes [S3, U1]. El proyecto de conversaciones es `hackaton-ayvens-alenia`; el repositorio de destino es `Sebastianlopez-dev/hackaton-alenia` [S7, U1].

La preparacion debe reducir trabajo de infraestructura antes de conocer el reto exacto. No hay bases oficiales ni datos reales recuperados que permitan afirmar requisitos detallados, calendario del evento, criterios del jurado o permisos de uso de servicios. Los tres ejemplos discutidos son normalizacion, discrepancias de flota y errores de datos; aparecen en propuestas del asistente, no en una especificacion oficial consultada [S4].

## Requisitos confirmados

- LangChain como capa del agente; la correccion explicita del usuario prevalece sobre propuestas anteriores de LangGraph [S4, U1].
- uv para la preparacion; Conda no es necesario para el trabajo previsto [S5, U1].
- Demo y evaluacion desde el inicio, con prioridad P0 [S1, U1].
- Preparar modulos y conectores reutilizables antes del hackathon [S3, U1].
- Conservar conversaciones originales y evitar credenciales, tokens o secretos en Git [U1].

## Estrategia recuperada

En S1, el usuario acepta una propuesta que prioriza evidencia, independencia del modelo, revision humana y auditabilidad junto a demo y evaluacion. Cada capacidad debe poder demostrarse y evaluarse. Una interfaz propia y el uso de varios modelos quedan en P2 dentro de esa propuesta aceptada.

S3 propone logica de negocio en Python normal, LangChain para coordinar modelos y herramientas, adaptadores pequenos para APIs y mocks sustituibles por conexiones reales. El arbol concreto sigue siendo una propuesta pendiente de revisar modulo por modulo.

## Alcance de preparacion

Preparar contratos de entrada/salida, adaptadores, tools, fixtures, pruebas, demo vertical y evaluacion. Ver [arquitectura](arquitectura.md) y [plan](plan-preparacion.md).

La respuesta de S3 propone posponer schemas reales, SQL especifico, prompts finales, reglas de negocio y configuracion de Vector Search contra datos inexistentes. Esta recomendacion es coherente con preparar una base, pero requiere contrastarse con las bases oficiales y los documentos originales pendientes.

Databricks, LangSmith, OpenRouter y OpenProject aparecen como integraciones propuestas. Su disponibilidad, obligatoriedad, cuentas y permisos no se han verificado. Voz y modelos especializados son exploraciones, no requisitos [S2, S3, U1].
