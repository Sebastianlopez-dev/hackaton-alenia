# Contexto del proyecto

Actualizado: 13 de octubre de 2026. Requisitos oficiales consultados; migracion del historial todavia parcial. Fuentes: [inventario](fuentes-contexto.md).

## Objetivo y evento

Construir un agente que analice y proponga resoluciones para tickets de soporte de datos de Ayvens, en el Alenia AI Ticketing Challenge del hackathon de Ironhack. Evento: **15-16 de octubre de 2026, Espacio Vizcaya, Madrid** [P1, p. 1]. Preparar una base modular reutilizable, funcional, demostrable y evaluable; aprovechar SDKs existentes y adaptar la logica al contrato oficial [S3, U1, U3].

Repositorio compartido: `Sebastianlopez-dev/hackaton-alenia`. Proyecto original de ChatGPT: `hackaton-ayvens-alenia`. GitHub conecta commits entre cloud y Mac; cada checkout requiere sincronizacion [S7, E2].

## Casos oficiales

Se puede elegir uno, dos o los tres; no es obligatorio cubrirlos todos [P1, pp. 1-3].

| Caso | Problema | Investigacion |
| --- | --- | --- |
| UC1 Normalization Management | Mappings locales a holding ausentes, incorrectos o rotos | Catalogos de normalizacion e historial |
| UC2 Monthly Report Reconciliation | Diferencias del Fleet Report frente al controlador de negocio | Report Gold, contratos Bronze/Silver y procesamiento |
| UC3 Data Verification & Correction | Datos operativos ausentes, inconsistentes o incorrectos | Contratos/vehiculos, ficheros fuente y registros afectados |

El ejemplo negro/gris y los nombres genericos anteriores eran escenarios exploratorios; no sustituyen estos casos oficiales. La seleccion del primer caso sigue pendiente.

## Requisitos y limites

- Python y LangChain como capa del agente; uv para dependencias, sin Conda [S4, S5, U1].
- Demo, evaluacion y evidencias desde la primera capacidad [S1, U1].
- Routing al caso de uso y prioridad antes de investigar [P1, p. 6].
- Aprobacion humana explicita antes de **cada SQL generado**, incluso lectura: presentar SQL y proposito antes de ejecutarlo. Tambien antes de `create_comment` y `update_status` [P1, p. 5].
- Operar con `read_ticket`, `retrieve_similar_tickets`, `create_comment`, `update_status` y la capacidad SQL descrita por el kit [P1, pp. 5-6].
- Solo datos sinteticos del entorno, aislamiento por equipo, sin APIs externas ni cambios de infraestructura. Secretos en vault, nunca en texto plano [P1, pp. 4-6].

## Infraestructura proporcionada

Databricks Serverless con Unity Catalog por equipo; OpenProject por equipo y service account; endpoint compartido Model Serving (el kit cita Llama 3 / DeepSeek / Mistral); indice Mosaic AI Vector Search con tickets sinteticos historicos; vault de Alenia [P1, pp. 4-5]. Endpoints, version de librerias, firmas efectivas y accesos deben verificarse con el manual tecnico.

OpenProject es la plataforma oficial de tickets. Usarlo como registro de estado, analisis, evidencias y cierre es la orientacion de arquitectura del resumen U2, compatible con el flujo del kit. No desplegar un reemplazo de la infraestructura oficial.

## Estrategia y puntuacion

| Criterio | Puntos |
| --- | --- |
| Routing y priorizacion | 20 |
| Accuracy frente al resultado ideal de Alenia | 25 |
| Cost of outcome | 20 |
| Human-in-the-loop | 20 |
| Presentacion y reflexion | 10 |
| Calidad tecnica | 5 |

Base 100; bonus de 10 por dos casos o 20 por tres (se sustituyen, no se suman), y 15 por UI/dashboard; maximo 135 [P1, pp. 6-7]. Primero conseguir una demo vertical fiable; ampliar cobertura y UI despues. La organizacion mide el coste oficial; nuestras metricas locales son auxiliares. El kit sugiere mostrar coste en la presentacion: aclarar disponibilidad de esos resultados.

## Alcance previo al desarrollo

Preparar contratos, aprobaciones, adaptadores mock, fixtures, pruebas y evaluacion reproducible; luego sustituir mocks por herramientas del equipo. Logica de negocio en Python y un agente LangChain sencillo, con proveedor intercambiable sin exigir varios modelos [S3, U2, U3].

Docker/OpenProject local se reportan como instalados en U2; no se han ejecutado ni verificado desde cloud. LangSmith y OpenRouter quedan fuera del recorrido de competicion mientras no haya aclaracion oficial compatible con las reglas. Agent Bricks, voz, Jev y multiagente complejo no son requisitos [U2, P1]. Ver [decisiones](decisiones.md), [arquitectura](arquitectura.md) y [plan](plan-preparacion.md).
