# Día 20 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/data/inmueble_property_type_data.xml` — 3 tipos de propiedad (`noupdate="1"`).

## Archivos modificados
- `gestion_inmobiliaria/__manifest__.py` — agrega el data file.

## Probar
Tras actualizar, deberían existir 3 tipos de propiedad precargados, editables desde la UI sin que una futura actualización los pise.
