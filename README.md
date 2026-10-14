# Hackathon Ironhack - Ayvens / Alenia

Preparación para el Alenia AI Ticketing Challenge, 15–16 de octubre de 2026, Madrid.

**Stack:** Python 3.12, uv y LangChain. **Infraestructura oficial:** Databricks y OpenProject.

## Estado

Documentación y dependencias preparadas. Código, demo, tests y evaluación pendientes. Accesos e integraciones oficiales aún sin verificar.

## Instalación

En macOS o Linux:

1. Instalar uv si falta:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Abrir una terminal nueva y entrar en la carpeta del repositorio.

3. Instalar Python 3.12:

   ```bash
   uv python install 3.12
   ```

4. Crear `.venv` e instalar las dependencias del lock:

   ```bash
   uv sync --locked
   ```

Repetir en cada equipo; no copiar `.venv`. Versionar `pyproject.toml`, `uv.lock` y `.python-version`.

`requirements.txt` es una exportación; no editarlo a mano. Para regenerarlo:

```bash
uv export --locked --format requirements-txt --output-file requirements.txt
```

## Desarrollo

1. Leer [AGENTS.md](AGENTS.md), [decisiones](docs/decisiones.md) y [arquitectura](docs/arquitectura.md).
2. Elegir el primer UC y construir una demo mock con pruebas y evaluación.
3. Verificar [compatibilidad con Databricks](docs/compatibilidad-databricks.md) y contratos oficiales antes de conectar servicios reales.

## Reglas clave

- Aprobación humana explícita antes de ejecutar SQL generado, publicar comentarios o cambiar estados.
- En competición: datos sintéticos del equipo y herramientas oficiales; sin APIs externas ni cambios de infraestructura.
- Secretos oficiales en vault, nunca en Git. Mantener `LANGSMITH_TRACING=false`.

## Documentación

- [Contexto y puntuación](docs/contexto-proyecto.md)
- [Decisiones](docs/decisiones.md)
- [Plan y calendario](docs/plan-preparacion.md)
- [Arquitectura y contratos](docs/arquitectura.md)
- [Fuentes y pendientes de recuperación](docs/fuentes-contexto.md)
- [Referencias originales](docs/referencias/README.md)
