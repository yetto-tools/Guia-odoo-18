# Día 27 — Cambios

## Archivos nuevos
- `.pre-commit-config.yaml` (raíz del repo) — `oca-checks-odoo-module` + `ruff`.

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — strings de error envueltos en `_()` para traducción.

## Probar
```bash
pre-commit install
pre-commit run --all-files
```
