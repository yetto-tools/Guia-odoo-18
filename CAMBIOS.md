# Día 5 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/models/inmueble_property_type.py`
- `gestion_inmobiliaria/models/inmueble_property_tag.py`
- `gestion_inmobiliaria/models/inmueble_property_offer.py` ⚠️ ver nota abajo

## Archivos modificados
- `gestion_inmobiliaria/models/inmueble_property.py` — agrega `property_type_id`, `tag_ids`, `buyer_id`, `salesperson_id`, `offer_ids`.
- `gestion_inmobiliaria/models/__init__.py` — importa los 3 modelos nuevos.
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — agrega los campos de relación al form y una pestaña "Ofertas" con la lista embebida (todavía sin botones de aceptar/rechazar — eso llega el día 14).

## Nota sobre `inmueble.property.offer`
El material del día 5 (`dias/dia-05-relaciones-entre-modelos.md`) se enfoca en tipo/etiqueta como ejercicio guiado. El modelo de **ofertas** no tiene un día dedicado explícito en la guía de 30 días, pero se referencia desde el día 8 en adelante (campo `best_price`, flujo de estados del día 14, tests del día 22). Este snapshot lo introduce acá porque es, temáticamente, el mismo tipo de ejercicio (relaciones `Many2one`/`One2many`) y porque el resto del curso lo da por existente. La lógica de **aceptar/rechazar** una oferta (botones, transición de estado) se agrega recién en el snapshot del día 14, que es donde el material sí la describe paso a paso.

## Actualizar
```bash
./odoo-bin -d midb -u gestion_inmobiliaria --stop-after-init
```
