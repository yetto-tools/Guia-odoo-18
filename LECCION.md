# Día 11 — Herencia de modelos y vistas

**Semana:** 2 — Lógica de negocio y ORM avanzado
**Duración estimada:** 3–4 h

## Objetivo del día
Extender `res.partner` para mostrar las propiedades compradas por ese contacto, y entender las tres formas de herencia de Odoo.

---

## Conceptos de Odoo

### Herencia clásica (`_inherit` solo): la misma tabla, más campos
```python
class ResPartner(models.Model):
    _inherit = "res.partner"
    property_ids = fields.One2many(...)
```
No creás un modelo nuevo — estás **agregando** campos y métodos a `res.partner` mismo. No hay tabla nueva, no hay id propio: es literalmente el mismo `res.partner` de siempre, con más columnas/comportamiento. Es lo que usás cuando querés que **cualquier módulo que ya use `res.partner`** vea automáticamente tus campos nuevos.

### Herencia por extensión (`_name` + `_inherit`): modelo nuevo que reutiliza código
```python
class InmueblePropertyPremium(models.Model):
    _name = "inmueble.property.premium"
    _inherit = "inmueble.property"
```
Esto crea una **tabla nueva** (`inmueble_property_premium`), copiando todos los campos y métodos de `inmueble.property` como punto de partida, pero como una entidad completamente separada — los registros de una no aparecen en la otra. Es poco común y no la vas a necesitar en este proyecto, pero es importante distinguirla de la clásica: la diferencia entre "agregar `_name` nuevo" o no cambia todo.

### Herencia por delegación (`_inherits`): composición con proxy automático
Así funciona `res.users` en el código real de Odoo:
```python
class ResUsers(models.Model):
    _inherits = {"res.partner": "partner_id"}
```
`res.users` tiene su **propia tabla**, con una columna `partner_id` (`Many2one` obligatorio a `res.partner`). Pero además, Odoo genera automáticamente campos "proxy" para cada campo de `res.partner`: cuando accedés a `some_user.email`, en realidad Odoo está yendo a buscar `some_user.partner_id.email` sin que tengas que escribirlo — es composición, no copia.

### XPath: apuntar con precisión a un nodo dentro de una vista existente
Al heredar una vista con `<field name="inherit_id" ref="modulo.vista_original"/>`, usás `<xpath expr="..." position="...">` para localizar un nodo del XML original:
- `expr` es una expresión XPath estándar (`//div[hasclass('oe_button_box')]`, `//field[@name='email']`, etc.).
- `position="inside"` mete tu contenido **dentro** del nodo encontrado, al final.
- `position="after"` / `"before"` lo ponen como hermano, después/antes.
- `position="replace"` reemplaza el nodo completo.
- `position="attributes"` te deja modificar solo atributos del nodo existente (por ejemplo, agregar `invisible="..."` a un campo que ya estaba ahí), usando `<attribute name="...">valor</attribute>` adentro.

### Por qué esto importa: no rompés el módulo original
Todo esto existe porque en Odoo **nunca editás el código fuente de otro módulo** para agregarle algo — ni siquiera el tuyo propio en producción, si podés evitarlo. Heredás. Así, cuando `base` (el módulo que define `res.partner`) se actualiza en una nueva versión de Odoo, tu extensión sigue funcionando sin conflictos de merge.

---

## Ejercicios prácticos

### Ejercicio 1 — Extender `res.partner` (guiado)

`models/res_partner.py`:
```python
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many("inmueble.property", "buyer_id", string="Propiedades compradas")

    def action_view_properties(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Propiedades",
            "res_model": "inmueble.property",
            "view_mode": "list,form",
            "domain": [("buyer_id", "=", self.id)],
        }
```

`views/res_partner_views.xml`:
```xml
<odoo>
    <record id="view_partner_form_inmueble" model="ir.ui.view">
        <field name="name">res.partner.form.inmueble</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <xpath expr="//div[hasclass('oe_button_box')]" position="inside">
                <button type="object" name="action_view_properties" class="oe_stat_button" icon="fa-building">
                    <field name="property_ids" widget="statinfo" string="Propiedades"/>
                </button>
            </xpath>
        </field>
    </record>
</odoo>
```
Actualizá el módulo y confirmá el smart button en el formulario de contacto.

### Ejercicio 2 — Confirmar que no hay tabla nueva
1. Antes y después de agregar `property_ids`, ejecutá `\d res_partner` en PostgreSQL.
2. Confirmá que **no aparece ninguna columna nueva** para `property_ids` (porque es un `One2many`, virtual) y que la tabla sigue siendo la misma `res_partner` de siempre — no se creó `inmueble_res_partner` ni nada similar.

### Ejercicio 3 — Explorar `_inherits` en el código real de Odoo
1. Sin modificar nada, desde `odoo shell`, ejecutá:
   ```python
   env["res.users"].browse(2)._fields.get("email")
   ```
2. Investigá (leyendo el código fuente de `res.users` en tu instalación de Odoo, carpeta `addons/base/models/res_users.py`) dónde está declarado `_inherits = {"res.partner": "partner_id"}`.
3. Confirmá, accediendo a `env["res.users"].browse(2).email`, que el valor viene realmente de `res.partner` por delegación.

### Ejercicio 4 — Practicar los 4 valores de `position`
Usando una vista de prueba descartable (no la de partner, para no romper nada):
1. Heredá la vista formulario de `inmueble.property.type` (la que creaste el día 5, si le agregaste una) o cualquier vista simple propia.
2. Probá agregar un campo con `position="after"`, después con `position="before"`, después con `position="replace"` sobre un `<group>` completo, y finalmente con `position="attributes"` agregando `invisible="1"` a un campo existente.
3. Confirmá visualmente el efecto de cada uno.

### Ejercicio 5 — Reto: contador eficiente
- Agregá `property_count = fields.Integer(compute="_compute_property_count")` en `res.partner`.
- Usalo en el `widget="statinfo"` en vez de contar directo sobre `property_ids`.
- Pista de por qué importa: contar sobre `property_ids` directamente en la vista obliga a cargar el recordset completo solo para saber su longitud; un campo computado puede usar `search_count` internamente, más liviano.

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia hay entre `_inherit` solo y `_name` + `_inherit` juntos?
2. ¿Cómo funciona `_inherits` — es una copia de campos o una composición con proxy automático?
3. Nombrá los 4 valores posibles de `position` en un XPath y qué hace cada uno.
4. ¿Por qué en Odoo se prefiere heredar un módulo en vez de editar directamente su código fuente?
5. Al agregar `property_ids` (`One2many`) a `res.partner`, ¿se crea alguna columna nueva en la tabla `res_partner`?

<details>
<summary>Ver respuestas</summary>

1. `_inherit` solo extiende el modelo existente in-place, agregando campos/métodos a la misma tabla sin crear nada nuevo. `_name` + `_inherit` juntos crean un modelo (y tabla) completamente nuevo, usando el otro como punto de partida de campos y métodos, pero como entidad separada.
2. Es composición: el modelo que usa `_inherits` tiene su propia tabla con un `Many2one` obligatorio al modelo delegado, y Odoo genera campos proxy automáticos que, por debajo, navegan esa relación — no copia los datos.
3. `inside` (mete el contenido dentro del nodo encontrado, al final), `after`/`before` (lo agrega como hermano, después/antes del nodo), `replace` (reemplaza el nodo completo), `attributes` (permite modificar solo atributos del nodo existente).
4. Porque heredar no genera conflictos cuando el módulo original se actualiza en una nueva versión — editar el código fuente directamente se pierde en la próxima actualización y además rompe la separación entre módulos.
5. No — al ser `One2many`, es un campo virtual/calculado; no agrega ninguna columna física a la tabla `res_partner`.

</details>

## Checklist de cierre
- [ ] Puedo explicar cuándo usar `_inherit` solo y cuándo `_inherits`.
- [ ] Sé qué hace cada valor de `position` en un XPath.
- [ ] Confirmé en PostgreSQL que extender `res.partner` no crea una tabla nueva.
- [ ] Encontré `_inherits` en el código fuente real de `res.users`.
