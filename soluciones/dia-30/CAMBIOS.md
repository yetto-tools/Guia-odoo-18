# Día 30 — Estado final

Sin cambios de código respecto al día 29: es demo de punta a punta + checklist final. Este es el **snapshot completo del proyecto integrador**.

## Demo de punta a punta
1. Crear una propiedad nueva.
2. Recibir 2-3 ofertas de distintos contactos.
3. Aceptar la mejor oferta (botón "Aceptar" en la lista de ofertas del formulario).
4. Confirmar la venta con el wizard (botón "Confirmar venta", header).
5. Verificar el mensaje y la actividad en el chatter.
6. Imprimir el reporte PDF ("Imprimir" → "Ficha de propiedad").
7. Crear una propiedad vía `scripts/create_property_xmlrpc.py`.
8. Navegar `/propiedades` sin sesión iniciada.

## Checklist "¿listo para producción?"
- [x] Seguridad con ACL + record rules (día 6).
- [x] Tests automatizados (día 22).
- [x] `pre-commit` configurado (día 27).
- [x] Strings de error traducibles con `_()` (día 27).
- [x] Manifest con `depends` completo y versión actualizada (día 25).
- [x] README con decisiones de diseño (día 29).
