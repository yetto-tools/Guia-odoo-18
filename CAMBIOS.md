# Día 3 — Cambios

## Archivos nuevos/modificados
- `gestion_inmobiliaria/models/inmueble_property.py` (nuevo) — modelo `inmueble.property` con campos básicos.
- `gestion_inmobiliaria/models/__init__.py` (modificado) — importa `inmueble_property`.

## Actualizar
```bash
./odoo-bin -d midb -u gestion_inmobiliaria --stop-after-init
```
Verificar desde `odoo shell`:
```python
env["inmueble.property"].create({"name": "Casa de prueba", "expected_price": 150000})
```
