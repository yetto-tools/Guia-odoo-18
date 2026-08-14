# Día 5 — Relaciones entre modelos

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 3–4 h

## Objetivo del día
Agregar tipo, etiquetas, comprador y agente a la propiedad.

---

## Conceptos de Odoo

### Cómo se guarda cada tipo de relación, en serio
- **`Many2one`**: agrega una columna FK en tu propia tabla (`inmueble_property.property_type_id` apuntando a `inmueble_property_type.id`). Es la única relación que "cuesta" espacio en tu tabla.
- **`One2many`**: **no existe como columna**. Es una vista calculada: Odoo busca en el modelo relacionado todos los registros cuyo `Many2one` inverso apunte a este registro. Por eso un `One2many` siempre necesita que exista un `Many2one` real del otro lado — no es opcional, es un requisito técnico.
- **`Many2many`**: crea una **tabla intermedia** automática (por convención `inmueble_property_inmueble_property_tag_rel`, con dos columnas FK) para poder relacionar N a N sin duplicar datos.

### Por qué esto importa para performance
Un `Many2one` es barato de leer (un JOIN simple, o ni eso si accedés al id). Un `One2many` implica una consulta adicional buscando coincidencias. Un `Many2many` implica un JOIN contra la tabla intermedia. Ninguno es "malo", pero elegir mal el tipo de relación para lo que necesitás (por ejemplo, usar `Many2many` cuando en realidad cada propiedad tiene un solo tipo) genera modelos de datos confusos y consultas más caras de lo necesario.

### `related`: leer sin duplicar
Un campo `related="property_type_id.name"` no duplica el dato — lo **reexpone** en tiempo real desde el modelo relacionado. Es azúcar sintáctico sobre "andá a buscar este campo a través de esta cadena de relaciones". Si le agregás `store=True`, Odoo sí lo graba físicamente en tu tabla (para poder indexarlo/buscarlo rápido), pero se recalcula automáticamente si el original cambia.

### `ondelete`: qué pasa si borran el registro relacionado
En un `Many2one`, `ondelete` define el comportamiento si el registro apuntado se borra:
- `"set null"` (default en muchos casos): el campo queda vacío.
- `"cascade"`: se borra también el registro que apuntaba (¡peligroso, usalo con cuidado!).
- `"restrict"`: Odoo impide borrar el registro apuntado mientras haya referencias.

Elegir mal esto es una fuente común de bugs de "por qué se borró esto en cascada" o "por qué no me deja borrar este tipo de propiedad".

### `default=lambda self: ...` con acceso al entorno
`salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)` no es solo sintaxis: `self.env.user` es el usuario que está ejecutando la operación en ese momento (quien está logueado y creando el registro). Es el patrón estándar para "asigname automáticamente a quien está creando esto".

---

## Ejercicios prácticos

### Ejercicio 1 — Modelos y campos de relación (guiado)

`models/inmueble_property_type.py`:
```python
from odoo import fields, models


class InmueblePropertyType(models.Model):
    _name = "inmueble.property.type"
    _description = "Tipo de propiedad"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
```

`models/inmueble_property_tag.py`:
```python
from odoo import fields, models


class InmueblePropertyTag(models.Model):
    _name = "inmueble.property.tag"
    _description = "Etiqueta de propiedad"

    name = fields.Char(required=True)
    color = fields.Integer()
```

Agregar a `inmueble_property.py`:
```python
property_type_id = fields.Many2one("inmueble.property.type", string="Tipo")
tag_ids = fields.Many2many("inmueble.property.tag", string="Etiquetas")
buyer_id = fields.Many2one("res.partner", string="Comprador", copy=False)
salesperson_id = fields.Many2one(
    "res.users", string="Agente", default=lambda self: self.env.user
)
```
Y en la vista formulario:
```xml
<field name="property_type_id"/>
<field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
<field name="buyer_id"/>
<field name="salesperson_id"/>
```
Importá los nuevos modelos, actualizá el módulo, creá 2-3 tipos y etiquetas, asignalos a una propiedad.

### Ejercicio 2 — Ver la tabla intermedia del Many2many
1. Conectate a PostgreSQL y ejecutá `\dt` filtrando por `inmueble` — identificá el nombre de la tabla intermedia que Odoo generó para `tag_ids`.
2. Hacé `SELECT * FROM esa_tabla;` después de asignar etiquetas a una propiedad desde la UI, y confirmá que ves las dos columnas FK.

### Ejercicio 3 — Probar `ondelete`
1. Agregá explícitamente `ondelete="restrict"` a `property_type_id`.
2. Actualizá el módulo, asigná un tipo a una propiedad, e intentá borrar ese tipo desde la UI — confirmá que Odoo lo impide.
3. Cambiá a `ondelete="set null"`, repetí el borrado, y confirmá que ahora sí se borra el tipo (y la propiedad queda con `property_type_id` vacío).

### Ejercicio 4 — `related` con y sin `store`
1. Agregá a `inmueble.property`: `type_sequence = fields.Integer(related="property_type_id.sequence")` (sin `store`).
2. Desde `odoo shell`, intentá `env["inmueble.property"].search([("type_sequence", ">", 5)])` — confirmá que falla o no filtra como esperás (un campo no-stored no es buscable de forma eficiente).
3. Agregá `store=True` al campo, actualizá, y repetí el `search` — confirmá que ahora sí funciona.

### Ejercicio 5 — Reto: One2many inverso
- Agregá `property_ids = fields.One2many("inmueble.property", "property_type_id")` en `inmueble.property.type`.
- Mostrala como una lista embebida en el formulario del tipo (`<field name="property_ids"/>` dentro de una vista formulario para `inmueble.property.type` que también vas a tener que crear).

---

## Preguntas de repaso conceptual

1. ¿Cuál de los tres tipos de relación (`Many2one`, `One2many`, `Many2many`) no genera ninguna columna nueva en ninguna tabla, y por qué necesita igual que exista un `Many2one` en otro modelo?
2. ¿Qué tabla adicional genera un `Many2many`, y qué guarda?
3. ¿Qué diferencia hay entre un campo `related` con `store=False` y uno con `store=True`, en términos de qué podés hacer con `search()`?
4. Nombrá las tres opciones más comunes de `ondelete` en un `Many2one` y qué hace cada una.
5. ¿Qué te da acceso `self.env.user` dentro de un `default=lambda self: ...`?

<details>
<summary>Ver respuestas</summary>

1. `One2many` no crea columna propia: es una consulta calculada que busca, en el modelo relacionado, los registros cuyo `Many2one` inverso apunte al registro actual. Por eso necesita que ese `Many2one` exista del otro lado — sin él, Odoo no sabe qué buscar.
2. Una tabla intermedia con dos columnas FK, una por cada modelo relacionado (por ejemplo, id de propiedad + id de etiqueta), permitiendo relacionar muchos a muchos sin duplicar filas.
3. Con `store=False` el campo se calcula al vuelo y no se puede usar de forma eficiente en un dominio de `search()`; con `store=True` se graba físicamente en la tabla (recalculándose cuando cambia el original), lo que sí permite filtrar/ordenar por él con normalidad.
4. `"set null"` deja el campo vacío si se borra el registro apuntado; `"cascade"` borra también el registro que apuntaba (riesgoso); `"restrict"` impide borrar el registro apuntado mientras haya referencias activas.
5. Te da el usuario que está ejecutando la operación actual (quien está logueado creando el registro) — es el patrón estándar para autoasignar "creado/gestionado por quien lo creó".

</details>

## Checklist de cierre
- [ ] Entiendo por qué `One2many` no crea columna propia.
- [ ] Vi la tabla intermedia real de un `Many2many` en PostgreSQL.
- [ ] Sé cuándo usar `related` con `store=True` vs `store=False`.
- [ ] Probé al menos dos valores distintos de `ondelete` y vi la diferencia de comportamiento.
