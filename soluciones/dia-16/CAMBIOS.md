# Día 16 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/views/inmueble_property_kanban_views.xml` — vista Kanban agrupada por estado + vista Graph (tipo × precio).

## Archivos modificados
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — `view_mode` de la acción pasa a `list,kanban,graph,form`; decoraciones de color en la lista.
- `gestion_inmobiliaria/__manifest__.py` — agrega la vista Kanban/Graph a `data`.
