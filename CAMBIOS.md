# Día 18 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/static/src/js/state_badge.js` — componente OWL, widget de campo `state_badge`.
- `gestion_inmobiliaria/static/src/js/state_badge.xml` — template del componente.

## Archivos modificados
- `gestion_inmobiliaria/__manifest__.py` — agrega la clave `assets` (`web.assets_backend`).
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — el campo `state` de la lista usa `widget="state_badge"`.

## Probar
Recordá `--dev=all` para evitar caché de assets al actualizar.
