# Día 24 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `company_id` (dispara la record rule automática de multi-compañía).
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — muestra `company_id` (solo visible con multi-compañía activado).

## Probar
Creá una segunda compañía y confirmá el aislamiento al cambiar la compañía activa.
