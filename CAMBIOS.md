# Día 4 — Cambios

## Archivos nuevos/modificados
- `gestion_inmobiliaria/views/inmueble_property_views.xml` (nuevo) — form, list, search, acción y menú.
- `gestion_inmobiliaria/__manifest__.py` (modificado) — agrega la vista a `data`.

## Actualizar
```bash
./odoo-bin -d midb -u gestion_inmobiliaria --stop-after-init
```
CRUD completo desde la UI: menú Inmobiliaria → Propiedades.
