# Día 12 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/wizard/__init__.py`
- `gestion_inmobiliaria/wizard/property_sale_wizard.py`
- `gestion_inmobiliaria/wizard/property_sale_wizard_views.xml`

## Archivos modificados
- `gestion_inmobiliaria/__init__.py` — importa `wizard`.
- `gestion_inmobiliaria/views/inmueble_property_views.xml` — agrega `<header>` con el botón "Confirmar venta" (visible solo en `state == 'offer_accepted'`).
- `gestion_inmobiliaria/__manifest__.py` — agrega la vista del wizard a `data`.

## Nota
Para probar este flujo hace falta una propiedad en `state = 'offer_accepted'`. Esa transición (aceptar una oferta) todavía no existe como botón — se agrega en el snapshot del día 14. Mientras tanto podés forzarla manualmente desde `odoo shell`: `prop.write({"state": "offer_accepted"})`.

## Bug real encontrado al probar el entorno (corregido en este snapshot y en todos los siguientes)
Al instalar el módulo en una instancia Odoo 18 real, la instalación fallaba con:
```
ValueError: External ID not found in the system: gestion_inmobiliaria.action_property_sale_wizard
```
Causa: `views/inmueble_property_views.xml` (que referencia `%(action_property_sale_wizard)d` en el botón del header) estaba en `data` **antes** que `wizard/property_sale_wizard_views.xml` (que define esa acción). Odoo carga los archivos de `data` en el orden declarado, así que al llegar a la vista de propiedad, la acción del wizard todavía no existía.

**Fix**: en el manifest, `wizard/property_sale_wizard_views.xml` debe ir **antes** que `views/inmueble_property_views.xml`. Además, faltaba una fila de ACL para el modelo `inmueble.property.sale.wizard` en `security/ir.model.access.csv` (Odoo lo tolera con un warning, no un error, pero sin eso el wizard no es accesible para nadie). Ambos fixes ya están aplicados en este snapshot.
