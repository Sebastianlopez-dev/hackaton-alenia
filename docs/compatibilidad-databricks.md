# Verificacion de compatibilidad con Databricks

Estado al 13 de octubre de 2026: **pendiente de acceso al entorno del equipo**. No hay una version Python o de LangChain verificada contra ese workspace.

## Evidencia disponible

El Participant Kit P1, paginas 4-5, proporciona Databricks Serverless, Unity Catalog, Model Serving y Mosaic AI Vector Search. No identifica version del entorno serverless, Python ni paquetes. No asumir un Databricks Runtime numerado de cluster clasico para este entorno.

Este checkout no contiene manual de registro ni configuracion de acceso a Databricks. No hay variables DATABRICKS configuradas en la sesion cloud. La consulta a docs.databricks.com fallo con `Tunnel connection failed: 403 Forbidden`; no se pudo contrastar documentacion publica. Esto no es una respuesta del workspace ni demuestra incompatibilidad.

La resolucion anterior de requirements uso objetivo Python 3.11, con aviso de que solo Python 3.12 estaba disponible para construir dependencias. Fue una comprobacion del resolver, no instalacion ni prueba en Databricks. La referencia provisional Python 3.11 se retira hasta verificar el entorno.

## Datos necesarios

En el notebook del equipo, confirmar el tipo de compute y la version seleccionada del entorno en el panel Environment. Si el manual establece otro mecanismo de ejecucion, usarlo como fuente antes de elegir dependencias. Obtener version Python y paquetes existentes con este codigo de inspeccion, que no muestra credenciales ni consulta datos:

```python
import sys
from importlib.metadata import PackageNotFoundError, version

print("Python:", sys.version)
for package in (
    "langchain", "langchain-core", "pydantic", "httpx", "pytest",
    "databricks-sdk", "databricks-sql-connector", "databricks-langchain",
):
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "no instalado")
```

Compartir solo esa salida, la version del entorno y las instrucciones de dependencias del manual. No adjuntar tokens, claves, variables de entorno completas ni configuracion de secretos. Un paquete no instalado no implica que no se pueda agregar.

## Como fijar versiones

1. Confirmar donde ejecuta el agente: notebook/job serverless o proceso local que llama a herramientas oficiales; no confundir la version de Python del servidor con la de un cliente remoto.
2. Usar la misma version Python local que el destino de ejecucion cuando el paquete vaya a ejecutarse alli. Confirmar restricciones del manual, versiones exigidas y cliente oficial antes de agregar integraciones.
3. Resolver e instalar dependencias en un entorno limpio con uv; guardar versiones exactas y dependencias transitivas en un lockfile. No convertir versiones preinstaladas automaticamente en requisitos sin comprobar compatibilidad.
4. Probar imports y construccion de tools/agente LangChain, schemas y aprobaciones mock. Probar el mismo conjunto en el entorno del equipo, sin activar servicios externos.
5. Incorporar cliente oficial y hacer smoke tests de conexion con aprobaciones cuando corresponda. Documentar versiones y resultados; actualizar el lockfile solo de forma deliberada.

No hay garantia de estabilidad por usar rangos amplios: el lockfile evita cambios accidentales, pero solo debe presentarse como compatible con Databricks despues de estas comprobaciones.
