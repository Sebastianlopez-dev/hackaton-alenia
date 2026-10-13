# Plan de preparacion y desarrollo

Revisado al **13 de octubre de 2026**, zona Europe/Madrid. La ventana original **7-15 de octubre** se conserva [D2, U2]; el documento diario original sigue pendiente. Este plan es nuevo y no acredita tareas realizadas en dias anteriores.

## Estado comprobado y reportado

| Elemento | Estado |
| --- | --- |
| Contexto, decisiones, arquitectura y fuentes | Documentados; actualizacion con P1 en esta tarea |
| GitHub y sincronizacion Mac/cloud | Primer commit publicado, historial local integrado y PDF recibido en main [E2] |
| Participant Kit | Original conservado y texto consultado [P1] |
| Docker Desktop Mac Intel | Instalado segun resumen U2; no verificado por ejecucion |
| OpenProject Docker Compose stable/17, HTTP localhost:8080 | Reportado en U2; salud/API pendiente |
| Token OpenProject | Creado segun U2; no consultado ni guardado en Git |
| Databricks, modelo, retrieval y proyecto oficial | Infraestructura proporcionada segun P1; acceso del equipo no verificado |
| Codigo, demo y evaluacion | Aun no implementados en este checkout |
| Markdown v2 e historial completo | Recuperacion pendiente; no frena el inicio con contrato oficial conocido |

## Orden de trabajo

| Prioridad | Entregable | Criterio para avanzar |
| --- | --- | --- |
| P0.1 | Paquete Python con uv y contratos minimos | Instalacion reproducible, version compatible, imports correctos, fixtures sin secretos |
| P0.2 | Demo de ticket con routing y aprobaciones mock | SQL/comentario/estado no se ejecutan sin permiso humano; rechazo y payload cambiado cubiertos |
| P0.3 | Agente LangChain y un UC completo | Evidencia -> causa/propuesta -> comentario/estado aprobados; demo y evaluacion del mismo flujo |
| P0.4 | Adaptadores oficiales | Accesos comprobados, contrato real probado, mock sustituible sin cambiar flujo |
| P0.5 | Regresion y ensayo con tickets nuevos | Casos no vistos, fallos y abstencion comprobados; limites documentados |
| P1 | Segundo y tercer UC | Ampliar solo cuando el primero mantiene calidad y aprobaciones |
| P2 | UI/dashboard | Estado y aprobaciones visibles; buscar bonus sin comprometer P0 |

Propuesta de primer UC: UC1 con un mapping ausente y fixture pequeno. Seleccion definitiva pendiente. No empezar multiagente complejo, voz ni proveedores externos. Preferir scripts/CLI reproducibles; notebooks pueden ejecutar el mismo paquete en Databricks.

## Calendario revisado y oficial

Los dias 13-14 son una recomendacion de preparacion actual; las horas del 15-16 vienen de P1 pp. 1, 7, zona Madrid.

- **13 octubre:** fijar primer UC, comprobar herramientas Python locales/cloud y preparar contratos, guard de aprobaciones y fixtures.
- **14 octubre:** demo vertical mock con evaluacion; preparar adaptadores sin asumir endpoints; ensayo de aprobacion/rechazo y revision del manual tecnico si llega.
- **15 octubre 09:30:** checkpoint tecnico en Teams; verificar acceso a Databricks y OpenProject antes del kick-off.
- **15 octubre 10:00:** kick-off; confirmar firmas, schemas, estados y limites SQL; conectar el primer UC a herramientas reales.
- **15 octubre 13:00 y 17:00:** sincronias Teams; resolver dudas de workflow/infraestructura.
- **16 octubre 09:30:** ultima sincronia; completar pruebas y ensayo final.
- **16 octubre 14:00:** freeze; infraestructura apagada para desarrollo y sin cambios posteriores de codigo.
- **16 octubre antes de 15:45:** llegar a Espacio Vizcaya, Calle Vizcaya 12, Madrid.
- **16 octubre desde 16:00:** infraestructura vuelve para presentaciones; 25 minutos + 5 de preguntas, con tickets nuevos en directo.

El kit describe "48 horas", pero el calendario fija el cierre de codigo el 16 a las 14:00: planificar con ese limite concreto.

## Definition of Done operativa

Una capacidad esta lista cuando tiene contrato y entradas/salidas claras, demo reproducible, pruebas relevantes, evaluacion con expectativas explicitas y evidencia del resultado. Registrar UC/prioridad, evidencia y causa/propuesta, aprobaciones y errores; un fixture no debe presentarse como dato oficial.

Para acciones protegidas, cubrir aprobacion, rechazo, ausencia de respuesta y cambio de payload. Cero ejecuciones SQL/comentario/estado sin aprobacion en estos escenarios es un criterio interno de aceptacion; los umbrales de accuracy/prioridad se fijan con el dataset local y se distinguen del score oficial.

El recorrido final debe usar herramientas del equipo, respetar aprobaciones y manejar un ticket no visto. No declarar una integracion operativa hasta ejecutar su prueba.

## Evaluacion orientada al jurado

Priorizar routing/prioridad (20), accuracy (25), coste (20), aprobacion humana (20), presentacion honesta (10) y calidad tecnica (5). Bonus: dos UCs +10 o tres +20, UI +15, maximo 135 [P1 pp. 6-7].

Comparar resultados locales con expectativas, documentar fallos y abstenciones. Alenia mide compute/tokens; nuestras metricas auxiliares no sustituyen su evaluacion. Aclarar como acceder al coste oficial para la presentacion.

## Preguntas tecnicas que desbloquean conexiones

Manual de registro; runtime Python/librerias; endpoints y mecanismo de credenciales en vault; catalogos/schemas completos; interfaces y retornos de tools; estados validos; aprobacion humana oficial; mecanismo y limites de SQL; permiso o prohibicion efectiva de tracing externo; consulta de metricas oficiales. El desarrollo mock puede avanzar mientras llegan estas respuestas.

## Cambio de entorno

En Mac: actualizar main antes de crear rama de tarea. En cloud: comprobar rama/commit y actualizar antes de continuar. Publicar commits al cerrar una etapa; en otro entorno hacer fetch y continuar esa rama o integrar su PR. No editar la misma tarea simultaneamente. GitHub sincroniza archivos versionados; chats, servicios Docker locales y secretos no se trasladan automaticamente.
