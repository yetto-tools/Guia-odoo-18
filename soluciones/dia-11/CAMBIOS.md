# Día 11 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/models/res_partner.py` — extiende `res.partner` con `property_ids` y `action_view_properties`.
- `gestion_inmobiliaria/views/res_partner_views.xml` — smart button en el formulario de contacto.

## Archivos modificados
- `gestion_inmobiliaria/models/__init__.py` — importa `res_partner`.
- `gestion_inmobiliaria/__manifest__.py` — agrega la vista nueva a `data`.

## Probar
Abrir un contacto: debería verse el smart button "Propiedades" (en 0 hasta que haya una venta cerrada con `buyer_id` asignado).
