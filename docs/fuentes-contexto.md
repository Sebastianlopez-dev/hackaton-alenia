# Fuentes y cobertura

Recuperacion realizada el 13 de octubre de 2026. **Migracion parcial, no completa.** Los documentos de este repositorio son una consolidacion fundamentada de lo accesible, no un archivo integral de conversaciones.

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

Los originales deben conservarse en [referencias](referencias/README.md) cuando esten disponibles. No se ha usado un resumen de S1 como si fuera el contenido de D1/D2.

## Evidencia clave y trazabilidad

Estos extractos son citas breves recuperadas, no transcripciones completas. No contienen credenciales.

- **S4 / D01**, usuario, turno `12abefdd-e0a1-41ce-acd6-83ae9e001349`, 7 de octubre 21:10:24 UTC: "Creo que te equivocas y mandaste el landgraph de nuevo y las especificaciones de hackathon es que trabajamos con LangChain."
- **S5 / D02**, usuario, turno `4f3e857a-2966-4a4c-84e3-4566341bdcdd`, 7 de octubre 22:38:34 UTC: "uv es sufi. agracias". U1 ratifica uv y la ausencia de necesidad de Conda.
- **S1 / D03, D05, D06**, asistente, turno `e4fecfc4-0524-42ec-bec2-150bf50343e2`, 7 de octubre 18:57:44 UTC: "Yo dejaria como P0, solo lo que refuerza el nucleo: demo y evaluacion desde el inicio, ser agnosticos al modelo, humano en el loop, y \"evidence first\"." Cita normalizada a ASCII. En esa respuesta propone interfaz propia y multi-modelo como P2, Definition of Done y tickets variados. Usuario, turno `34c42af9-db49-4da9-b475-1551e5b94221`, 18:58:38 UTC: "Estoy de acuerdo contigo. Gracias".
- **S1 / D1, D2**, respuesta `3e4077fd-0a24-4505-9348-b8fbeca6f9c9` al turno `dc78753b-1ae0-49e2-aa29-6670b3db62f7`: anuncia los v2 en `sandbox:/mnt/data/Hackathon_Ayvens_Alenia_Contexto_y_Estrategia_v2.md` y `sandbox:/mnt/data/Hackathon_Ayvens_Alenia_Plan_Preparacion_7-15_Octubre_v2.md`. El anuncio no acredita sus bytes.
- **S3 / D04 y arquitectura**, usuario, turno `8401acb2-40d7-4048-97ff-2bf2dfedd9c9`: pide volver a crear el arbol y listar codigo existente que pueda preparar en pequenos scripts antes del hackathon. Respuesta `bfc5aaab-3856-46be-a3de-aee302ad1449`: propone kit modular, adaptadores, demo/eval y revision modulo por modulo. No acredita implementacion.
- **S2 / D08**, turno `4e2628a6-760e-4f72-91db-d9c2cb0076fa`: usuario pregunta si es necesario o bastaria buen prompting. Turno posterior `5faf13cc-9dc9-4c45-a8c0-5f4ced9b9a10`: pide ejemplo para decidir si usar Jeff; el asistente propone comparar Jev con una referencia, midiendo precision, latencia y coste. No hay adopcion confirmada.
- **S7 / nombres y preservacion**, turno `dc99dcd9-9132-47be-8647-983ee96d9c53`: imagenes no incluidas; el texto del asistente corrige Ayvens frente a Eventos y distingue los proyectos. Turno `3ea0ed4b-ddde-4bfe-80a4-0f775edf6606`: propone llevar contexto al repo y conservar conversaciones originales. U1 confirma nombres y alcance.

Los IDs D01-D08 se desarrollan en [decisiones](decisiones.md). Las propuestas arquitectonicas proceden de S3/S4; las posibilidades de modelos de S2; las fechas del plan de los nombres anunciados en S1 y la referencia antes del 15 en S3.

## Contenido necesario para completar

1. Adjuntar los dos Markdown v2 originales, con sus nombres indicados en D1/D2. No basta un resumen para conservarlos fielmente.
2. Exportar las conversaciones del proyecto completo, incluyendo turnos anteriores, adjuntos y respuestas que aparecen solo como referencias. Prioridad: S6 completo; S7 con configuracion local/GitHub y conexion ChatGPT-Codex; S1 con contexto inicial/bases; S2 con instalaciones, cuentas y exploracion de voz; respuestas completas de S5.
3. Incluir un listado o exportacion que cubra conversaciones mas antiguas y archivadas del proyecto. Las siete localizadas no certifican el total. Si hay conversaciones adicionales, incluir sus titulos y contenido.
4. Aportar las bases oficiales y el estado real de cuentas/instalaciones si no vienen en la exportacion; excluir secretos. Verificar el repositorio del Mac y transferir alli los cambios de este checkout.

Actualizar este inventario y las decisiones al recuperar fuentes. Resolver contradicciones con correcciones explicitas y decisiones posteriores del usuario, manteniendo referencia de la correccion.
