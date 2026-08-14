# Día 13 — Cambios

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `_inherit = ["mail.thread", "mail.activity.mixin"]`.
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — agrega `<chatter/>` como hermano de `<sheet>`.

## Probar
```python
prop = env["inmueble.property"].search([], limit=1)
prop.message_post(body="Mensaje de prueba desde shell")
```
La notificación automática al aceptar una oferta (`message_post` + `activity_schedule`) se implementa en el snapshot del día 14, dentro de `inmueble.property.offer.action_accept()`.
