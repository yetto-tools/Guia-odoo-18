# Día 14 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `action_cancel()`.
- `gestion_inmobiliaria/models/inmueble_property_offer.py` — agrega `create()` override (transición automática `new → offer_received`), `action_accept()` (marca la oferta aceptada, rechaza las demás, actualiza la propiedad, postea mensaje y crea actividad) y `action_refuse()`.
- `gestion_inmobiliaria/views/inmueble_property_views.xml`:
  - `<header>` con botón "Cancelar" (bloqueado si `state == 'sold'`) y `widget="statusbar"`.
  - `expected_price` ahora `readonly` fuera de `state == 'new'`.
  - La lista embebida de ofertas gana botones "Aceptar"/"Rechazar" y decoraciones de color.

## Flujo completo ya funcional
`new` → (crear oferta) → `offer_received` → (Aceptar en la lista de ofertas) → `offer_accepted` → (botón "Confirmar venta", día 12) → `sold`. "Cancelar" disponible en cualquier estado salvo `sold`.
