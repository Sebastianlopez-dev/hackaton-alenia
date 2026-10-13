# Fuentes y cobertura

Recuperacion y actualizacion realizadas el 13 de octubre de 2026. **Migracion parcial, no completa.** Los documentos consolidan lo accesible, el resumen aportado posteriormente por el usuario y el Participant Kit oficial; no son un archivo integral de conversaciones.

## Metodo y limites

Se reviso primero `/workspace/hackaton-alenia`: solo existia `.git`, sin commits ni AGENTS.md. No se encontro AGENTS.md en `/workspace`. La ruta Mac solicitada no existe en el entorno cloud, aunque `list_projects` reconoce el proyecto local `hackaton-alenia` en `/Users/adm/Documents/work/hackaton-alenia`. Su contenido no se inspecciono y los cambios de esta tarea no se han escrito alli [E1].

`list_projects` identifico el proyecto ChatGPT `hackaton-ayvens-alenia`, ID `g-p-6ac755aec2ec8191804e4e0fae203b1e`. `list_threads(limit=50)` devolvio las siete conversaciones siguientes asociadas a ese ID y ninguna otra del proyecto dentro de la ventana visible. La herramienta no ofrece paginacion para ese listado; no demuestra que no existan conversaciones mas antiguas.

Se consultaron las siete con `read_thread`, incluyendo outputs y hasta 20000 caracteres por mensaje. Todas devolvieron `hasMore=false` y `nextCursor=null`; eso agota lo expuesto por la herramienta, no certifica un historial completo. Algunos mensajes son solo marcadores `chatgpt-content-reference`, hay imagenes omitidas y al menos una respuesta corta de S7 acaba incompleta. La documentacion de la herramienta indica lectura de estado y resumenes recientes, no exportacion integral.

La consulta de conversaciones archivadas devolvio: `Archived ChatGPT conversations are only available from local desktop tasks.` No se pudo comprobar ese inventario. No hay herramienta disponible para descargar los adjuntos historicos de ChatGPT. La busqueda de Markdown en `/workspace` y `/tmp` no encontro originales; una zona de `/tmp` estaba restringida. `/mnt/data` no existe en esta sesion.

No se modificaron, archivaron, renombraron ni borraron conversaciones originales. No se crearon enlaces publicos de comparticion.

## Inventario de conversaciones

Las fechas de turnos siguientes son las originales entregadas por la herramienta en UTC. En Madrid eran dos horas mas; los turnos de S5 corresponden ya al 8 de octubre local. La fecha de actualizacion del listado no se trata como fecha de una decision.

| ID | Conversacion y referencia | Turnos expuestos | Cobertura |
| --- | --- | --- | --- |
| S1 | [HACKATON IRONHACK](https://chatgpt.com/c/6ac68661-7f00-83ed-9cd3-53e894ba8323) | 6, 2026-10-07 18:57-19:00 UTC | Parcial: prioridad P0, aceptacion y anuncio de documentos v2. Documentos y contexto anterior ausentes |
| S2 | [Instalación y cuentas Hackathon](https://chatgpt.com/c/6ac6973e-a75c-83ed-b9fc-05049056057a) | 5, 2026-10-07 20:37-20:41 UTC | Parcial: Jev, routing y experimento. No se recupero instalacion/cuentas anterior ni contenido detallado de voz |
| S3 | [Árbol y código del hackathon](https://chatgpt.com/c/6ac6b57e-26b4-83eb-80b4-b5eca72ec41d) | 1, 2026-10-07 21:13 UTC | Turno textual recuperado con peticion, arbol y respuesta extensa; sin adjuntos ni codigo ejecutado. Cobertura global no certificada |
| S4 | [Friendly greeting exchange](https://chatgpt.com/c/6ac6aed8-23b8-83eb-8b07-2e98f2a6b1c1) | 5, 2026-10-07 21:06-21:10 UTC | Parcial: modulos, codigo reutilizable, arbol antiguo y correccion explicita a LangChain |
| S5 | [Instalación para hackathon](https://chatgpt.com/c/6ac6c9c5-9794-83eb-a01d-de24ad22526a) | 2, 2026-10-07 22:38 UTC | Parcial: pregunta sobre Conda y confirmacion de uv; respuestas del asistente son referencias sin texto |
| S6 | [Resumen del proyecto](https://chatgpt.com/c/6acd175f-3488-83eb-9f83-446ee94652b2) | 1, 2026-10-12 17:22 UTC | Contenido sustantivo no recuperado: pregunta visible, respuesta solo como referencia |
| S7 | [Configurar repositorio Git](https://chatgpt.com/c/6ace69b7-0c9c-83eb-816e-37873ff09569) | 5, 2026-10-13 17:42-17:55 UTC | Parcial: distincion entre proyectos y prompt de migracion. Capturas omitidas; configuracion Git/GitHub anterior no recuperada |

## Documentos y otras fuentes

| ID | Fuente | Estado |
| --- | --- | --- |
| D1 | `Hackathon_Ayvens_Alenia_Contexto_y_Estrategia_v2.md` | No consultado ni conservado: solo anuncio y enlace historico en S1 |
| D2 | `Hackathon_Ayvens_Alenia_Plan_Preparacion_7-15_Octubre_v2.md` | No consultado ni conservado: solo anuncio y enlace historico en S1 |
| U1 | Peticion actual del usuario, 13 de octubre de 2026, en esta tarea | Consultada: confirma LangChain, uv, demo/eval, reutilizacion, limites y destinos |
| E1 | Inspeccion del checkout y herramientas de inventario, 13 de octubre de 2026 | `git status --short --branch`: `No commits yet on work`; `git ls-remote origin`: sin refs. Ruta Mac no accesible; proyecto local reconocido por la aplicacion |
| P1 | [Alenia AI Ticketing Challenge_Participant Kit.pdf](referencias/Alenia%20AI%20Ticketing%20Challenge_Participant%20Kit.pdf), octubre 2026 | Original conservado; texto de las 7 paginas consultado con pdftotext. Fuente oficial de reglas, calendario, casos, datos y puntuacion |
| U2 | Resumen pegado por el usuario en esta conversacion, 13 de octubre de 2026 | Contenido consultado; aporta instalaciones locales, Docker, scripts, fases y orientacion de simplicidad. Es un resumen secundario, no exportacion completa de S6 ni prueba de ejecucion |
| U3 | Peticion del usuario de actualizar todo para empezar a desarrollar, 13 de octubre de 2026 | Autoriza consolidar requisitos y preparar plan operativo; estructura minima y criterios locales son recomendaciones de implementacion |
| E2 | Publicacion y sincronizacion posteriores, 13 de octubre de 2026 | Commit inicial 93b8ce4 publicado en main; usuario reporta merge local; main recibido en cloud en f59d19f incluye PDF. Autenticacion local reportada reparada con gh; no se verifico el shell Mac |

Los originales deben conservarse en [referencias](referencias/README.md) cuando esten disponibles. No se ha usado un resumen de S1 como si fuera el contenido de D1/D2.

## Participant Kit: referencias oficiales

| Pagina PDF | Secciones y hechos utilizados |
| --- | --- |
| 1 | Evento 15-16 octubre 2026, Madrid; calendario/checkpoint/freeze; elegir uno, dos o tres UCs |
| 2 | UC1 Normalization Management y comienzo de UC2 Monthly Report Reconciliation |
| 3 | Flujo UC2 y UC3 Data Verification & Correction |
| 4 | Modelo medallon y tablas; Unity Catalog y comienzo de infraestructura Databricks Serverless |
| 5 | OpenProject, Model Serving, Mosaic AI Vector Search, vault; cuatro funciones y SQL; aprobacion de SQL/comentarios/estados; datos sinteticos y sin APIs externas |
| 6 | Aislamiento; librerias compatibles; criterios base 100 puntos y routing antes de investigar |
| 7 | Bonus hasta 35; tres UCs sustituye bonus de dos; presentacion 25+5, tickets nuevos, freeze y lugar |

El PDF permite SQL ademas de cuatro funciones y luego dice "solo las cuatro funciones". Registrar esta ambiguedad para preguntar por el mecanismo de SQL, sin ignorar su requisito de aprobacion. Tambien afirma que Alenia mide el coste sin necesidad de presentarlo y sugiere metricas de coste en la demo: aclarar acceso a esas metricas.

Las fases Understand/Investigate/Resolve y OpenProject como source of truth se recogen de U2, no como etiquetas literales oficiales de P1. Agent Bricks no figura como requisito del PDF. LangSmith/OpenRouter no son infraestructura oficial enumerada y requieren aclaracion frente a la prohibicion de APIs externas.

## Contexto aportado por el resumen U2

U2 reporta Docker Desktop en Mac Intel, OpenProject mediante Docker Compose del repositorio oficial en rama stable/17, HTTP localhost:8080 y token creado. Prueba de API y conectores pendiente. No se recibieron comandos, logs ni secretos; el estado se documenta como reportado, no verificado.

U2 tambien recuerda scripts modulares, GitHub compartido, trazabilidad, tres fases, demo/evaluacion/evidencia y arquitectura sencilla. La frase "hoy es 12 de octubre" pertenece al resumen; esta actualizacion usa 13 de octubre. Los documentos sin sufijo v2 citados en U2 no sustituyen los originales v2 solicitados. Su procedencia exacta de S6 no esta certificada y su cobertura no pasa a completa.

## Evidencia clave y trazabilidad

Estos extractos son citas breves recuperadas, no transcripciones completas. No contienen credenciales.

- **S4 / D01**, usuario, turno `12abefdd-e0a1-41ce-acd6-83ae9e001349`, 7 de octubre 21:10:24 UTC: "Creo que te equivocas y mandaste el landgraph de nuevo y las especificaciones de hackathon es que trabajamos con LangChain."
- **S5 / D02**, usuario, turno `4f3e857a-2966-4a4c-84e3-4566341bdcdd`, 7 de octubre 22:38:34 UTC: "uv es sufi. agracias". U1 ratifica uv y la ausencia de necesidad de Conda.
- **S1 / D03, D05, D06**, asistente, turno `e4fecfc4-0524-42ec-bec2-150bf50343e2`, 7 de octubre 18:57:44 UTC: "Yo dejaria como P0, solo lo que refuerza el nucleo: demo y evaluacion desde el inicio, ser agnosticos al modelo, humano en el loop, y \"evidence first\"." Cita normalizada a ASCII. En esa respuesta propone interfaz propia y multi-modelo como P2, Definition of Done y tickets variados. Usuario, turno `34c42af9-db49-4da9-b475-1551e5b94221`, 18:58:38 UTC: "Estoy de acuerdo contigo. Gracias".
- **S1 / D1, D2**, respuesta `3e4077fd-0a24-4505-9348-b8fbeca6f9c9` al turno `dc78753b-1ae0-49e2-aa29-6670b3db62f7`: anuncia los v2 en `sandbox:/mnt/data/Hackathon_Ayvens_Alenia_Contexto_y_Estrategia_v2.md` y `sandbox:/mnt/data/Hackathon_Ayvens_Alenia_Plan_Preparacion_7-15_Octubre_v2.md`. El anuncio no acredita sus bytes.
- **S3 / D04 y arquitectura**, usuario, turno `8401acb2-40d7-4048-97ff-2bf2dfedd9c9`: pide volver a crear el arbol y listar codigo existente que pueda preparar en pequenos scripts antes del hackathon. Respuesta `bfc5aaab-3856-46be-a3de-aee302ad1449`: propone kit modular, adaptadores, demo/eval y revision modulo por modulo. No acredita implementacion.
- **S2 / D08**, turno `4e2628a6-760e-4f72-91db-d9c2cb0076fa`: usuario pregunta si es necesario o bastaria buen prompting. Turno posterior `5faf13cc-9dc9-4c45-a8c0-5f4ced9b9a10`: pide ejemplo para decidir si usar Jeff; el asistente propone comparar Jev con una referencia, midiendo precision, latencia y coste. No hay adopcion confirmada.
- **S7 / nombres y preservacion**, turno `dc99dcd9-9132-47be-8647-983ee96d9c53`: imagenes no incluidas; el texto del asistente corrige Ayvens frente a Eventos y distingue los proyectos. Turno `3ea0ed4b-ddde-4bfe-80a4-0f775edf6606`: propone llevar contexto al repo y conservar conversaciones originales. U1 confirma nombres y alcance.

Los IDs D01-D13 se desarrollan en [decisiones](decisiones.md). La arquitectura historica procede de S3/S4; las exploraciones de S2; el contrato y calendario actuales de P1; el estado local reportado de U2. La estructura minima, orden de trabajo y pruebas de aprobacion son propuestas operativas de esta actualizacion U3, no texto original de D1/D2 ni resultados ejecutados.

## Contenido necesario para completar

1. Adjuntar los dos Markdown v2 originales, con sus nombres indicados en D1/D2. No basta un resumen para conservarlos fielmente.
2. Exportar las conversaciones del proyecto completo, incluyendo turnos anteriores, adjuntos y respuestas que aparecen solo como referencias. Prioridad: S6 completo; S7 con configuracion local/GitHub y conexion ChatGPT-Codex; S1 con contexto inicial/bases; S2 con instalaciones, cuentas y exploracion de voz; respuestas completas de S5.
3. Incluir un listado o exportacion que cubra conversaciones mas antiguas y archivadas del proyecto. Las siete localizadas no certifican el total. Si hay conversaciones adicionales, incluir sus titulos y contenido.
4. El Participant Kit ya esta recibido y consultado. Falta el manual tecnico de registro/accesos y confirmar cuentas, endpoints y funcionamiento de instalaciones, sin compartir secretos. Actualizar el checkout Mac tras publicar cambios.

Actualizar este inventario y las decisiones al recuperar fuentes. Resolver contradicciones con correcciones explicitas y decisiones posteriores del usuario, manteniendo referencia de la correccion.
