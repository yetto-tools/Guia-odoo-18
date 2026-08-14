# Día 22 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/tests/__init__.py`
- `gestion_inmobiliaria/tests/test_inmueble_property.py` — 3 tests (constraint de precio, transición automática de estado, onchange de jardín vía `Form`).

## Probar
```bash
./odoo-bin -d midb --test-tags /gestion_inmobiliaria --stop-after-init
```
