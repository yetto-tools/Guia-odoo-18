# Día 6 — Cambios

## Archivos nuevos
- `gestion_inmobiliaria/security/security.xml` — categoría, 2 grupos, 2 record rules.
- `gestion_inmobiliaria/security/ir.model.access.csv` — ACL para `inmueble.property`, `inmueble.property.type`, `inmueble.property.tag` y `inmueble.property.offer`.

## Archivos modificados
- `gestion_inmobiliaria/__manifest__.py` — agrega seguridad a `data`, **antes** de las vistas.

## Nota
El día 6 del material solo muestra el ACL de `inmueble.property` como ejemplo. Este snapshot lo amplía a los otros 3 modelos del módulo (tipo, etiqueta, oferta) porque sin esas filas esos modelos quedarían completamente inaccesibles — necesario para que el módulo funcione de punta a punta, no solo como ejemplo aislado.

## Probar
Creá dos usuarios de prueba, asignales `group_inmueble_agent` y `group_inmueble_manager` respectivamente desde Ajustes → Usuarios, y confirmá el filtrado.
