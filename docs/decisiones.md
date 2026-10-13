# Decisiones

Fecha de consolidacion: 13 de octubre de 2026. Fuentes: [inventario](fuentes-contexto.md). La confirmacion del usuario tiene prioridad sobre recomendaciones del asistente; una propuesta no equivale a trabajo completado.

## Confirmadas

| ID | Decision | Evidencia |
| --- | --- | --- |
| D01 | Usar LangChain como capa del agente | S4, turno `12abefdd-e0a1-41ce-acd6-83ae9e001349`: el usuario corrige expresamente LangGraph; U1 lo ratifica |
| D02 | Usar uv; no preparar Conda | S5, turno `4f3e857a-2966-4a4c-84e3-4566341bdcdd`: usuario confirma que uv basta; U1 |
| D03 | Demo y evaluacion desde el inicio, P0 | S1: propuesta en `e4fecfc4-0524-42ec-bec2-150bf50343e2`, aceptada en `34c42af9-db49-4da9-b475-1551e5b94221`; U1 |
| D04 | Preparar modulos y conectores reutilizables | S3, peticion del usuario en `8401acb2-40d7-4048-97ff-2bf2dfedd9c9`; U1 |
| D05 | Priorizar evidencia, modelo intercambiable, revision humana y auditabilidad | Propuesta y aceptacion de S1 citadas en D03 |
| D06 | Interfaz propia y multi-modelo en P2 | Propuesta aceptada de S1; no implica prohibir una interfaz minima de demo |
| D07 | Conservar conversaciones y documentos originales; excluir secretos | U1; S7 confirma conservar el proyecto original |
| D08 | Voz y modelos especializados siguen siendo posibilidades | U1; S2 explora Jev y comparacion experimental |

## Contradicciones resueltas

LangGraph aparece en respuestas antiguas de S4 y en la exploracion S2. La correccion posterior del usuario en S4 exige LangChain; S3 ya presenta un arbol basado en LangChain. No adoptar `StateGraph`, nodos ni edges como arquitectura del proyecto por esas respuestas antiguas. Esto no exige prohibir dependencias transitivas que use una version de LangChain.

El arbol corregido de S4 contiene `requirements.txt` y ejemplos antiguos usan pip. La confirmacion posterior de S5 y U1 establece uv como herramienta elegida. No existe aun un manifiesto ni una version de Python verificada.

S7 corrige errores de reconocimiento de voz: el nombre es Ayvens y el proyecto original es `hackaton-ayvens-alenia`; `hackaton-alenia` es el proyecto conectado al repositorio. Las variantes Ivans, I-vents o Eventos no identifican otros proyectos confirmados.

## Propuestas pendientes

| Propuesta | Estado y aclaracion necesaria | Fuente |
| --- | --- | --- |
| Databricks: SDK, SQL, modelos y Vector Search | Preparar interfaces; confirmar servicio disponible, endpoints, datos y necesidad de cada capacidad | S3, S4 |
| LangSmith desde el primer agente | Recomendado para trazas, evaluacion, coste y latencia; no hay cuenta ni obligatoriedad verificadas. D03 no depende de que este servicio este disponible | S3, S4 |
| OpenRouter como proveedor intercambiable | Adaptador propuesto; no hay modelo final, presupuesto, cuenta o prueba de acceso confirmados | S3 |
| OpenProject para tickets | Lectura, comentarios, historial y cambios de estado propuestos; confirmar si es plataforma del reto | S3, S4 |
| RAG / retrieval | Contrato generico propuesto; Databricks Vector Search, FAISS y Chroma son alternativas, ninguna seleccionada | S3 |
| Arbol de carpetas y contratos | Revisar y podar modulos antes de implementarlos; no hay aprobacion completa del arbol | S3 |
| Jev y agentes especializados | Experimento sugerido: comparar routing con una referencia basada en prompts y salida estructurada; adopcion condicionada a resultados | S2 |

## Descartadas o aplazadas

- Sustituir LangChain por LangGraph: descartado por D01.
- Instalar Conda para esta preparacion: innecesario por D02.
- Convertir voz o Jev en requisitos: incompatible con D08; siguen abiertos como experimentos.
- Construir la solucion final antes de conocer el reto: S3 recomienda aplazar logica especifica, prompts finales y schemas reales. No consta una decision oficial sobre el alcance del reto.

## Abiertas

Faltan las bases oficiales, los dos documentos v2, el historial anterior de configuracion Git y de cuentas, el estado real de instalaciones y la seleccion del alcance minimo. No se puede resolver con evidencia si los tres casos de uso son obligatorios o ejemplos, ni si Databricks/OpenProject son servicios proporcionados por la organizacion. Ver [faltantes](fuentes-contexto.md#contenido-necesario-para-completar).
