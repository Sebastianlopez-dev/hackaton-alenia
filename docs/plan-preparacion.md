# Plan de preparacion

Estado al 13 de octubre de 2026. Este archivo consolida lo recuperado; no reproduce el documento original pendiente [D2 en el inventario](fuentes-contexto.md).

## Fechas originales

El documento anunciado en S1 se llama `Hackathon_Ayvens_Alenia_Plan_Preparacion_7-15_Octubre_v2.md`: conservar la ventana original **7-15 de octubre**. S3 menciona preparacion antes del 15 de octubre. Las conversaciones recuperadas son de octubre de 2026; el ano del documento debe verificarse al obtener el original.

No se recupero el calendario diario. No asignar tareas inventadas a los dias 7-12 ni marcarlas como hechas. Revisar el plan original al 13 de octubre y recalcular lo que cabe antes del 15. La fecha y duracion oficiales del hackathon siguen sin verificar.

## Trabajo acreditado

| Trabajo | Evidencia y limite |
| --- | --- |
| Eleccion de LangChain y uv | Confirmaciones del usuario en S4, S5 y U1 |
| Priorizacion de demo, evaluacion y evidencia | Propuesta aceptada en S1 |
| Discusion de arbol y conectores | S3, S4; diseno propuesto, no implementacion |
| Anuncio de creacion de documentos v2 | S1; archivos originales no recuperados, contenido y conservacion pendientes |
| Identificacion del proyecto ChatGPT y proyecto local | S7 y herramientas de inventario; no demuestra configuracion Git local completa |
| Consolidacion documental parcial | Los seis archivos solicitados se crean en el checkout cloud en esta tarea |

La inspeccion del checkout cloud encontro solamente `.git`, sin commits ni AGENTS.md. `git ls-remote origin` no devolvio refs. No hay codigo, instalaciones, cuentas, pruebas de integracion o demo ejecutada verificables en este checkout. La carpeta del Mac no es accesible desde este shell [E1].

## Pendientes y orden propuesto

1. Recuperar documentos originales, respuestas omitidas e historial anterior; leer las bases oficiales y verificar cuentas/accesos sin guardar secretos.
2. Revisar y podar el arbol con el usuario; fijar el alcance minimo y las integraciones imprescindibles.
3. Preparar proyecto Python con uv y LangChain, contratos pequenos y fixtures de tickets/datos.
4. Construir una demo vertical con mocks y evaluacion desde la primera capacidad. Registrar entradas, evidencia, salida esperada, errores y resultados.
5. Preparar adaptadores reutilizables y pruebas por contrato; verificar SDKs, versiones y APIs antes de convertir pseudocodigo en implementacion.
6. Incorporar conexiones reales cuando existan permisos, datos y endpoints; repetir demo y evaluacion.
7. Revisar el calendario 7-15 de octubre con el trabajo acreditado y el tiempo disponible.

Este orden consolida recomendaciones de S3/S4 y prioridades de S1/U1; no es un calendario original ni una aprobacion del arbol completo.

## Criterio de terminado

S1 confirma anadir una Definition of Done y tickets variados, pero el texto exacto del documento no esta disponible. Propuesta operativa para revisar: una capacidad tiene contrato claro, demostracion ejecutable, casos con resultado esperado, pruebas relevantes, evidencia rastreable y resultados de evaluacion registrados. Los umbrales de calidad y el tamano del conjunto deben decidirse.

Interfaz propia, voz, varios modelos y routing especializado deben esperar a que la demo minima y la evaluacion funcionen. En S2, los 50 casos son un ejemplo de experimento, no una cuota acordada.
