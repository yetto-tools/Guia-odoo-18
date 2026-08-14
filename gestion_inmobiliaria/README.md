# Gestión Inmobiliaria (Odoo 18)

Módulo de portafolio construido como proyecto integrador de la guía "De 0 a Pro: Odoo 18 Developer en 30 Días". Gestiona propiedades en venta, ofertas de compradores y el flujo completo hasta la venta cerrada.

## Funcionalidades
- Alta de propiedades con tipo, etiquetas, superficie y estado.
- Ofertas de compradores con aceptación/rechazo y vencimiento (`date_deadline`).
- Flujo de estados: Nueva → Oferta recibida → Oferta aceptada → Vendida (con Cancelada como salida alternativa).
- Wizard de confirmación de venta con precio final.
- Seguridad por grupos (Agente / Gerente) con record rules.
- Reporte PDF de ficha de propiedad.
- Vistas Kanban y Graph.
- Portal público (`/propiedades`) sin necesidad de sesión.
- Widget de campo propio (OWL) para el estado, con colores.
- Endpoint JSON y compatibilidad XML-RPC para integraciones externas.
- Tests automatizados (`--test-tags /gestion_inmobiliaria`).

## Instalación
```bash
docker compose up -d
./odoo-bin -d midb -i gestion_inmobiliaria --stop-after-init
```

## Decisiones de diseño
- `total_area` es `store=True` porque se usa en el reporte y se lee mucho más de lo que cambia.
- La seguridad usa dos grupos con `implied_ids` (el Gerente hereda al Agente) en vez de condicionales dentro de una sola regla, siguiendo el patrón estándar de Odoo.
- Confirmar la venta es un wizard (no un botón directo) porque el precio final puede diferir del precio de la oferta aceptada, y es una interacción de un solo uso que no necesita persistir estado propio.
- El controlador público usa `sudo()` de forma acotada, solo sobre la consulta de propiedades disponibles — nunca sobre el modelo completo sin filtro.

## Stack técnico
Odoo 18 Community · PostgreSQL 15 · OWL · QWeb

## Estado
Ver `CAMBIOS.md` de cada snapshot en `soluciones/dia-XX/` para el historial día a día de construcción.
