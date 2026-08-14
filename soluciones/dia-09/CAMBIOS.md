# Día 9 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `_check_expected_price` (`@api.constrains`) y `_onchange_garden` (`@api.onchange`).

## Probar
- Onchange: tildar/destildar "garden" en el formulario, sin guardar.
- Constraint: `env["inmueble.property"].create({"name": "x", "expected_price": -1})` desde shell debe fallar.
