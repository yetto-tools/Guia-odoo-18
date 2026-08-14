# Día 17 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/controllers/__init__.py`
- `gestion_inmobiliaria/controllers/main.py` — rutas `/propiedades` y `/propiedades/<id>` (incluye el reto de detalle).
- `gestion_inmobiliaria/views/inmueble_templates.xml` — plantillas QWeb de sitio.

## Archivos modificados
- `gestion_inmobiliaria/__init__.py` — importa `controllers`.
- `gestion_inmobiliaria/__manifest__.py` — agrega dependencia `website` y las plantillas a `data`.

## Probar
Navegar `/propiedades` **sin sesión iniciada** (ventana de incógnito).
