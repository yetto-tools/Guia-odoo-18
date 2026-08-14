# Soluciones — snapshot completo por día

Cada carpeta `dia-XX/` contiene el estado **completo** del proyecto (módulo `gestion_inmobiliaria/` + archivos de infraestructura) tal como debería quedar después de completar ese día de `dias/dia-XX-*.md` — no fragmentos sueltos, todos los archivos.

Es el equivalente a poder hacer `git checkout dia-14`: copiás esa carpeta entera a tu `addons_path` y tenés exactamente ese punto del curso funcionando.

## Cómo usar
1. Intentá resolver el día vos mismo, siguiendo `dias/dia-XX-*.md`.
2. Si te trabás, mirá el `CAMBIOS.md` de ese mismo `soluciones/dia-XX/` — lista qué archivos son nuevos o se modificaron ese día específicamente, y por qué.
3. Compará tu código contra el snapshot, o copialo directo a tu `addons_path` para seguir avanzando desde ahí.

## Notas importantes
- Los **retos** (ejercicios "sin solución" de cada día) generalmente **no** están resueltos en estos snapshots — son para que los intentes vos. Cuando un snapshot sí incluye la solución de un reto (por ser una extensión menor y natural), el `CAMBIOS.md` de ese día lo aclara explícitamente.
- El modelo `inmueble.property.offer` (ofertas) no tiene un día dedicado explícito en la guía original — se introduce en el snapshot del día 5 (día de "Relaciones") y su lógica de aceptar/rechazar se completa en el día 14 (día de "Máquina de estados"). Está documentado en `dia-05/CAMBIOS.md` y `dia-14/CAMBIOS.md`.
- Días de repaso (7, 21, 28) no traen cambios de código — el snapshot es idéntico al del día anterior.
- Día 30 es el estado final completo del proyecto integrador.

## Verificado levantando el entorno real (2026-08-14)

El snapshot del día 30 se probó de punta a punta contra Odoo 18 + PostgreSQL 15 reales (Docker). Aparecieron dos bugs genuinos que ya están corregidos en **todos** los snapshots afectados (día 12 en adelante):

1. **Orden de carga en el manifest**: `views/inmueble_property_views.xml` referencia la acción del wizard (`%(action_property_sale_wizard)d`) pero se cargaba *antes* de que `wizard/property_sale_wizard_views.xml` definiera esa acción → fallaba la instalación con `ValueError: External ID not found`. Detalle completo en `dia-12/CAMBIOS.md`.
2. **ACL faltante**: el modelo del wizard (`inmueble.property.sale.wizard`) no tenía fila en `security/ir.model.access.csv`.

Tras el fix: instalación limpia (0 warnings propios del módulo, solo el aviso cosmético de licencia que también se corrigió agregando `"license": "LGPL-3"` al manifest), los 3 tests automatizados del día 22 pasan (`0 failed, 0 error(s)`), y el login `admin`/`admin` funciona contra la base de prueba.
