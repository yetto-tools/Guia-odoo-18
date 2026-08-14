# Día 12 — Wizards y acciones de servidor

**Semana:** 2 — Lógica de negocio y ORM avanzado
**Duración estimada:** 3–4 h

## Objetivo del día
Crear un wizard para confirmar la venta de una propiedad con un precio final, y entender qué lo hace distinto de un modelo normal.

---

## Conceptos de Odoo

### `TransientModel`: mismo ORM, ciclo de vida distinto
Un `TransientModel` hereda del mismo motor que `Model` — tiene campos, vistas, métodos, puede tener `@api.constrains`. La diferencia real es el ciclo de vida: sus filas se purgan automáticamente por un `ir.cron` interno de Odoo después de un tiempo (típicamente unas horas). Esto tiene una consecuencia práctica importante: **nunca uses un `TransientModel` para guardar algo que necesites consultar después** — es para capturar input temporal de una interacción de un solo uso, no para historial.

### Por qué el wizard "no persiste nada" a menos que vos lo hagas explícito
Cuando el usuario completa el wizard y hace clic en "Confirmar", el registro del wizard mismo sí se graba (temporalmente, en su propia tabla transiente). Pero eso no tiene ningún efecto sobre `inmueble.property` a menos que tu método (`action_confirm_sale`) explícitamente haga un `write()` sobre el modelo real. El wizard es solo el vehículo para capturar el input del usuario — la lógica de negocio (qué hacer con ese input) la escribís vos.

### `target="new"`: cómo se abre como modal
Una acción de ventana con `target="new"` le dice al cliente web que renderice el formulario como un diálogo modal flotante, en vez de navegar a una pantalla completa nueva. Sin `target="new"`, el wizard se abriría reemplazando toda la pantalla — funcionalmente similar, pero peor UX para una interacción corta.

### `type="object"` vs `type="action"` en un botón
- `type="object"` llama a un **método Python** del modelo actual, pasándole el registro (o recordset) actual como `self`. El método puede devolver una acción (para abrir algo) o `None`/nada (si solo hace un cambio en el mismo registro).
- `type="action"` llama directamente a una **acción de ventana** ya definida (`ir.actions.act_window`), identificada con `name="%(external_id)d"`. No ejecuta ningún método Python propio — simplemente abre esa acción, pasando el `context` que le indiques.

Para el botón "Confirmar venta" que abre el wizard, usás `type="action"` porque no hay lógica previa que ejecutar — solo abrir el wizard con el contexto correcto (`default_property_id`).

### Pasar valores por defecto a un wizard vía `context`
`context="{'default_property_id': id}"` en el botón hace que, al abrirse el formulario del wizard, el campo `property_id` venga precompletado con el id de la propiedad actual. Es el patrón estándar de Odoo para "abrir un wizard ya sabiendo desde dónde se abrió" — cualquier campo del wizard puede precompletarse así con `default_<nombre_del_campo>`.

---

## Ejercicios prácticos

### Ejercicio 1 — Wizard de confirmación de venta (guiado)

`wizard/property_sale_wizard.py`:
```python
from odoo import fields, models


class PropertySaleWizard(models.TransientModel):
    _name = "inmueble.property.sale.wizard"
    _description = "Confirmar venta de propiedad"

    property_id = fields.Many2one("inmueble.property", required=True)
    final_price = fields.Float(required=True)

    def action_confirm_sale(self):
        self.ensure_one()
        self.property_id.write({"selling_price": self.final_price, "state": "sold"})
        return {"type": "ir.actions.act_window_close"}
```

`wizard/property_sale_wizard_views.xml`:
```xml
<odoo>
    <record id="view_property_sale_wizard_form" model="ir.ui.view">
        <field name="name">inmueble.property.sale.wizard.form</field>
        <field name="model">inmueble.property.sale.wizard</field>
        <field name="arch" type="xml">
            <form>
                <group>
                    <field name="property_id" invisible="1"/>
                    <field name="final_price"/>
                </group>
                <footer>
                    <button string="Confirmar" type="object" name="action_confirm_sale" class="btn-primary"/>
                    <button string="Cancelar" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="action_property_sale_wizard" model="ir.actions.act_window">
        <field name="name">Confirmar venta</field>
        <field name="res_model">inmueble.property.sale.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>
</odoo>
```

Botón en el formulario de `inmueble.property`:
```xml
<button string="Confirmar venta" type="action" name="%(action_property_sale_wizard)d"
        invisible="state != 'offer_accepted'"
        context="{'default_property_id': id}"/>
```
Implementá todo, importalo (`wizard/__init__.py` + `__init__.py` raíz), y probá el flujo desde una propiedad en estado `offer_accepted`.

### Ejercicio 2 — Confirmar que el wizard se purga
1. Confirmá una venta a través del wizard.
2. Con modo desarrollador activo, andá a `Ajustes → Técnico → Acciones de servidor` o consultá directamente desde `odoo shell`:
   ```python
   env["inmueble.property.sale.wizard"].search([])
   ```
3. Anotá cuántos registros hay. Esperá un rato (o investigá el cron `Transient Models Vacuum` en `Ajustes → Técnico → Automatización → Acciones programadas`) y volvé a consultar — confirmá que eventualmente se limpian solos.

### Ejercicio 3 — `type="object"` vs `type="action"` en la práctica
1. Cambiá el botón "Confirmar venta" para que en cambio sea `type="object"`, con un método intermedio en `inmueble.property` que arme y devuelva la acción del wizard:
   ```python
   def action_open_sale_wizard(self):
       self.ensure_one()
       return {
           "type": "ir.actions.act_window",
           "res_model": "inmueble.property.sale.wizard",
           "view_mode": "form",
           "target": "new",
           "context": {"default_property_id": self.id},
       }
   ```
2. Confirmá que el comportamiento visible es idéntico al del `type="action"` original.
3. Reflexioná: ¿en qué caso necesitarías la versión `type="object"` en vez de `type="action"` directo? (pista: cuando necesitás lógica condicional antes de decidir qué acción devolver).

### Ejercicio 4 — Precompletar más de un campo por contexto
1. Agregá al wizard un campo `suggested_price = fields.Float(default=0)` de solo lectura informativo.
2. Modificá el `context` del botón para pasar también `default_suggested_price` calculado a partir de `expected_price` de la propiedad (por ejemplo, `expected_price * 0.95`).
3. Confirmá que el wizard abre con ambos valores precompletados.

### Ejercicio 5 — Reto: validación dentro del wizard
Agregá una validación en el wizard mismo: `final_price` no puede ser menor al 90% de `expected_price` de la propiedad relacionada, usando `@api.constrains` dentro del wizard.
- Pista: dentro del constraint podés navegar `self.property_id.expected_price` sin problema, aunque estés en un `TransientModel`.

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia real de comportamiento (no solo de nombre) tiene un `TransientModel` frente a un `Model` normal?
2. Si el método del wizard no hace ningún `write()` explícito sobre `inmueble.property`, ¿queda registrado en algún lado que el usuario "confirmó una venta"?
3. ¿Qué logra `target="new"` en una acción de ventana?
4. ¿Cuál es la diferencia funcional entre un botón `type="object"` y uno `type="action"`?
5. ¿Cómo le pasás un valor por defecto a un campo específico de un wizard, desde el botón que lo abre?

<details>
<summary>Ver respuestas</summary>

1. Sus filas se purgan automáticamente después de un tiempo mediante un cron interno de Odoo — no está pensado para guardar historial, solo para capturar input temporal de una interacción puntual.
2. No — si el método no escribe explícitamente sobre `inmueble.property` (u otro modelo persistente), no queda ningún rastro real más allá del registro transiente del wizard, que además se va a purgar solo.
3. Que el formulario se abra como un diálogo modal flotante sobre la pantalla actual, en vez de navegar a una pantalla completa nueva.
4. `type="object"` ejecuta un método Python del modelo actual (que puede decidir qué acción devolver, con lógica condicional); `type="action"` abre directamente una acción de ventana ya definida, sin pasar por ningún método propio.
5. Con `context="{'default_<nombre_del_campo>': valor}"` en el botón (o en cualquier lugar que abra esa acción con ese contexto).

</details>

## Checklist de cierre
- [ ] Entiendo por qué un `TransientModel` no es para guardar historia.
- [ ] Sé cómo pasar un valor por defecto al wizard vía `context`.
- [ ] Puedo explicar la diferencia entre `type="object"` y `type="action"` en un botón, con un caso de uso para cada uno.
- [ ] Agregué la validación del reto dentro del wizard.
