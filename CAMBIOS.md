# Día 23 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `get_total_expected_price()` (versión corregida, sin `search()` dentro de un loop).

## Probar
```python
env["inmueble.property"].get_total_expected_price(TYPE_ID)
```
Comparar contra la versión ineficiente descrita en el material del día 23 (no incluida en este snapshot, es el "antes" que se corrige).
