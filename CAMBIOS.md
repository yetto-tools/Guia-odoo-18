# Día 26 — Cambios

## Archivos nuevos (fuera del módulo, a nivel de infraestructura)
- `odoo.conf`
- `nginx.conf`
- `docker-compose.prod.yml`

El módulo `gestion_inmobiliaria/` no cambia este día.

## Probar
```bash
docker compose -f docker-compose.prod.yml up -d
```
Acceder vía `http://localhost` (puerto 80, a través de Nginx) en vez de `:8069` directo.
