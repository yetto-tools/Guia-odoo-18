# Día 19 — Cambios

## Archivos nuevos
- `scripts/create_property_xmlrpc.py` — script externo (fuera del módulo) que crea una propiedad vía XML-RPC y llama a `get_available_properties`.

## Archivos modificados
- `gestion_inmobiliaria/controllers/main.py` — agrega el endpoint `/api/propiedades` (`type="json"`, reto del día 19).

## Probar
```bash
python scripts/create_property_xmlrpc.py
```
