# Día 8 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `total_area` (compute) y `_compute_total_area`.
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — muestra `total_area` en el form.

## Probar
Editar `living_area` o `garden_area` en el formulario y confirmar que `total_area` cambia en vivo.
