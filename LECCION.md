# Día 8 — Campos computados y related

**Semana:** 2 — Lógica de negocio y ORM avanzado
**Duración estimada:** 3–4 h

## Objetivo del día
Agregar un campo calculado: superficie total, y entender a fondo el costo/beneficio de `store`.

---

## Conceptos de Odoo

### Qué dispara realmente un recálculo
Un método `@api.depends("living_area", "garden_area")` no se ejecuta "cuando el usuario cambia la vista" — se ejecuta cuando el **valor efectivo** de cualquiera de esos campos cambia, sin importar si fue desde la UI, desde otro método Python, desde un import CSV, o desde un script externo. El decorador es una declaración de dependencia, no un evento de UI.

### `store=False` (default): rápido de escribir, limitado para buscar
Un campo computado no-stored se recalcula **cada vez que se lee**, en memoria, sin tocar la base de datos. Ventaja: nunca queda desactualizado, no ocupa espacio. Desventaja: no podés hacer `search([('total_area', '>', 100)])` de forma eficiente — Odoo tendría que calcular el valor para cada fila de la tabla antes de poder filtrar, lo cual generalmente ni siquiera está permitido sin una implementación de `search=` adicional.

### `store=True`: buscable, pero con costo de escritura
Cuando marcás `store=True`, Odoo graba el resultado como una columna real. Cada vez que cambia una dependencia, Odoo **vuelve a calcular y grabar** — eso significa una escritura extra en la base de datos en cada `write()` relevante. Para un campo que se lee mucho y cambia poco (como `total_area`), vale la pena. Para un campo que cambia constantemente y rara vez se busca, puede ser un desperdicio.

### `related` no es "una copia": es una ventana
`fields.Char(related="buyer_id.email")` no duplica el email del comprador — cada vez que accedés al campo, Odoo sigue la cadena de relaciones (`buyer_id` → `email`) y te trae el valor actual. Es, en esencia, un `compute` automático que Odoo genera por vos, siguiendo el path que le diste. Por eso tiene el mismo trade-off de `store` que cualquier otro computado.

### La trampa de los `@api.depends` sobre relaciones (`offer_ids.price`)
`@api.depends("offer_ids.price")` no solo dispara cuando cambia el `price` de una oferta existente — también dispara cuando se **agrega o quita** una oferta del `One2many`. Es una de las razones por las que Odoo puede seguir dependencias a través de relaciones: sabe que agregar/quitar/editar cualquier oferta relacionada puede afectar el resultado.

---

## Ejercicios prácticos

### Ejercicio 1 — Superficie total (guiado)

```python
from odoo import api, fields, models


class InmuebleProperty(models.Model):
    _name = "inmueble.property"
    # ... resto de los campos existentes ...

    total_area = fields.Integer(compute="_compute_total_area", string="Superficie total (m²)")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
```
Agregalo a la clase existente en `models/inmueble_property.py`, mostralo en la vista formulario, actualizá el módulo, y confirmá que cambia en vivo al editar superficie construida o de jardín.

### Ejercicio 2 — Ver el costo real de `store=True`
1. Con `total_area` como `store=True` (default cuando no especificás `store`), abrí la consola de PostgreSQL y hacé `\d inmueble_property` — confirmá que `total_area` **sí** existe como columna.
2. Cambiá el campo a `store=False` explícito, actualizá el módulo, y repetí `\d inmueble_property` — confirmá que la columna **desaparece**.
3. Con `store=False`, intentá `env["inmueble.property"].search([("total_area", ">", 50)])` desde `odoo shell` y observá qué pasa (puede fallar o comportarse de forma inesperada, porque no es una columna real).
4. Volvé a dejarlo en `store=True` (o simplemente sin especificar `store`, que ya es `True` por default en un campo `compute`).

### Ejercicio 3 — Un campo `related` con y sin `store`
1. Agregá a `inmueble.property`: `salesperson_email = fields.Char(related="salesperson_id.email")`.
2. Mostralo en la vista, actualizá, y confirmá que muestra el email del agente asignado.
3. Cambiá el email del usuario agente desde `Ajustes → Usuarios` y confirmá que el campo `related` en la propiedad se actualiza solo, sin tocar la propiedad.

### Ejercicio 4 — Depender de un campo a través de una relación
1. Si ya tenés `inmueble.property.offer` (o creala ahora con al menos `price` y `property_id`), agregá el campo de abajo.
2. Confirmá que agregar una nueva oferta recalcula `best_price` automáticamente, sin que edites ningún campo de la propiedad directamente.

```python
best_price = fields.Float(compute="_compute_best_price")

@api.depends("offer_ids.price")
def _compute_best_price(self):
    for record in self:
        record.best_price = max(record.mapped("offer_ids.price"), default=0)
```

### Ejercicio 5 — Reto: computado con múltiples dependencias encadenadas
- Creá un campo `price_gap` (`Float`, compute) que muestre la diferencia entre `best_price` y `expected_price`.
- Su `@api.depends` tiene que incluir tanto `best_price` como `expected_price` — confirmá que cambia si modificás cualquiera de los dos.

---

## Preguntas de repaso conceptual

1. ¿Qué dispara realmente la ejecución de un método `@api.depends(...)` — un evento de UI o un cambio de valor?
2. ¿Qué ventaja tiene `store=False` y qué pierdo a cambio?
3. ¿Qué ventaja tiene `store=True` y qué cuesta a cambio?
4. ¿Un campo `related` "copia" el valor original, o lo consulta cada vez?
5. Si tenés `@api.depends("offer_ids.price")`, ¿se recalcula solo cuando cambia el precio de una oferta existente, o también cuando agregás/quitás una oferta?

<details>
<summary>Ver respuestas</summary>

1. Un cambio real en el valor efectivo de cualquier campo listado en el `@api.depends`, sin importar si vino de la UI, de otro método, de un import, o de un script externo.
2. Ventaja: nunca queda desactualizado y no ocupa espacio en la tabla. Pierdo: no se puede filtrar/ordenar de forma eficiente con `search()`.
3. Ventaja: se puede usar en dominios de búsqueda como cualquier campo normal. Cuesta: una escritura adicional en la base de datos cada vez que cambia alguna de sus dependencias.
4. Lo consulta cada vez (sigue la cadena de relaciones en el momento de la lectura) — no es una copia estática, aunque con `store=True` sí queda grabado físicamente y se resincroniza cuando el original cambia.
5. También se recalcula al agregar o quitar una oferta del `One2many`, no solo al editar el precio de una existente — Odoo entiende que ambos casos pueden afectar el resultado.

</details>

## Checklist de cierre
- [ ] Entiendo qué dispara el recálculo de un campo `compute`.
- [ ] Vi con mis propios ojos la diferencia de columna en PostgreSQL entre `store=True` y `store=False`.
- [ ] Sé la diferencia entre `related` y un `compute` que lee un campo relacionado.
- [ ] Implementé un computado que depende de un `One2many`.
