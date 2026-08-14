# Día 24 — Multi-compañía y multi-moneda

**Semana:** 4 — Calidad, performance y profesionalización
**Duración estimada:** 3–4 h

## Objetivo del día
Aislar las propiedades por compañía, y entender cómo Odoo modela múltiples empresas en una sola base de datos.

---

## Conceptos de Odoo

### Una base de datos, múltiples compañías
Odoo permite que **una sola instalación** (una base de datos) gestione varias empresas legalmente separadas (`res.company`), cada una con su propia contabilidad, configuración y, opcionalmente, datos aislados. Esto no es multi-tenancy en el sentido de "bases de datos separadas" — es aislamiento **dentro** de la misma base, a nivel de fila, similar en mecánica a lo que ya viste con record rules el día 6, pero con reglas que Odoo genera automáticamente para modelos marcados como multi-company.

### Qué gatilla el aislamiento automático
Cuando un modelo tiene un campo `company_id` (`Many2one` a `res.company`), Odoo **genera automáticamente** una record rule que filtra los registros según las compañías activas del usuario actual (las que tiene habilitadas en su selector de compañías). No necesitás escribir esa `ir.rule` vos mismo — simplemente declarar el campo con el nombre correcto (`company_id`) activa el comportamiento estándar. Esto es distinto de las record rules manuales del día 6: acá es una convención que el propio framework reconoce y actúa en consecuencia.

### `default=lambda self: self.env.company` vs `self.env.companies`
- `self.env.company` es la compañía **activa actualmente** (la que el usuario tiene seleccionada en ese momento, si trabaja con varias).
- `self.env.companies` es el conjunto de **todas** las compañías que el usuario tiene habilitadas (puede ver/alternar entre varias sin cerrar sesión).

Para un `default` de un nuevo registro, `self.env.company` (singular) es lo correcto — un registro nuevo pertenece a una compañía específica al momento de crearse, no a "todas las habilitadas".

### Por qué `Monetary` necesita `currency_id`, y `Float` no
Un campo `Monetary` no solo guarda un número — Odoo necesita saber en qué moneda interpretarlo para mostrarlo correctamente formateado (símbolo, posición, cantidad de decimales según la moneda) y, más importante, para poder hacer conversiones si comparás montos en distintas monedas. Por eso todo campo `Monetary` requiere un campo `currency_id` (`Many2one` a `res.currency`) en el mismo modelo, típicamente vinculado por `related` a la moneda de la compañía.

### La relación entre compañía y moneda
Cada `res.company` tiene su propia `currency_id` configurada (la moneda en la que opera esa empresa). Un patrón común es `currency_id = fields.Many2one(related="company_id.currency_id")` — así, el campo monetario de tu modelo automáticamente usa la moneda de la compañía a la que pertenece ese registro, sin que el usuario tenga que elegirla manualmente cada vez.

---

## Ejercicios prácticos

### Ejercicio 1 — Agregar `company_id` (guiado)

```python
company_id = fields.Many2one(
    "res.company", required=True, default=lambda self: self.env.company
)
```
Agregalo a `inmueble.property`, actualizá el módulo, creá una segunda compañía (`Ajustes → Usuarios y Compañías → Compañías`), cambiá de compañía activa (selector arriba a la derecha), y verificá que las propiedades de la otra compañía no aparecen.

### Ejercicio 2 — Confirmar la record rule automática
1. Con modo desarrollador activo, andá a `Ajustes → Técnico → Seguridad → Reglas de registro` y buscá reglas relacionadas a `inmueble.property`.
2. Confirmá que aparece una regla generada automáticamente por Odoo (no una que vos hayas escrito), relacionada al campo `company_id`.
3. Compará su dominio con las reglas manuales que escribiste el día 6 — ¿qué diferencia notás en cómo está armada?

### Ejercicio 3 — Habilitar varias compañías para un mismo usuario
1. Desde `Ajustes → Usuarios`, editá tu usuario y habilitale **ambas** compañías (no solo activá una, sino que aparezcan las dos como accesibles en el selector).
2. Con ambas habilitadas, activá "ver todas las compañías" si la opción está disponible en el selector — confirmá si ahora ves las propiedades de ambas juntas o seguís viendo solo una a la vez según cuál esté activa.

### Ejercicio 4 — Probar el aislamiento desde `odoo shell`
1. Desde `odoo shell`, ejecutá `env["inmueble.property"].search([])` con el usuario admin en el contexto de una sola compañía (la que sea default) — anotá cuántos resultados trae.
2. Repetí forzando el contexto a la otra compañía: `env["inmueble.property"].with_company(OTRA_COMPANY_ID).search([])`.
3. Compará los resultados y confirmá el aislamiento también desde código, no solo desde la UI.

### Ejercicio 5 — Reto: convertir a `Monetary`
Convertí `expected_price` y `selling_price` a `fields.Monetary`, con:
```python
currency_id = fields.Many2one(related="company_id.currency_id")
```
- Actualizá el módulo y confirmá que el campo ahora se muestra con el símbolo de moneda correspondiente.
- Cambiá la moneda de una de las dos compañías de prueba (`Ajustes → Empresas`) y confirmá que las propiedades de esa compañía reflejan el nuevo símbolo.

---

## Preguntas de repaso conceptual

1. ¿Qué gatilla que Odoo genere automáticamente una record rule de aislamiento multi-compañía para un modelo?
2. ¿Cuál es la diferencia entre `self.env.company` y `self.env.companies`?
3. ¿Por qué un campo `Monetary` necesita un `currency_id` asociado, a diferencia de un `Float` normal?
4. ¿Qué patrón se usa comúnmente para que un campo monetario use automáticamente la moneda de la compañía del registro?
5. Si un usuario tiene habilitadas dos compañías pero solo una activa a la vez, ¿ve los registros de ambas simultáneamente o solo los de la activa?

<details>
<summary>Ver respuestas</summary>

1. La sola presencia de un campo llamado `company_id` (`Many2one` a `res.company`) en el modelo — Odoo reconoce esa convención de nombre y genera automáticamente la record rule correspondiente, sin necesidad de escribirla manualmente.
2. `self.env.company` es la compañía activa actualmente (una sola, la que el usuario tiene seleccionada en ese momento); `self.env.companies` es el conjunto completo de compañías que el usuario tiene habilitadas para alternar.
3. Porque un número solo no alcanza para mostrarlo correctamente formateado (símbolo, decimales según la moneda) ni para permitir comparaciones/conversiones entre montos en distintas monedas — el `currency_id` le da ese contexto necesario al valor numérico.
4. `currency_id = fields.Many2one(related="company_id.currency_id")` — así el campo monetario hereda automáticamente la moneda configurada en la compañía del registro, sin que el usuario deba elegirla manualmente.
5. Depende de la configuración del selector: por defecto ve solo los de la compañía activa en ese momento, aunque Odoo permite en ciertas vistas habilitar ver varias compañías a la vez si el usuario las tiene todas habilitadas.

</details>

## Checklist de cierre
- [ ] Entiendo qué reglas genera Odoo automáticamente al agregar `company_id`, y las ubiqué en la configuración técnica.
- [ ] Sé por qué un campo `Monetary` necesita un `currency_id` asociado.
- [ ] Probé el aislamiento tanto desde la UI como desde `odoo shell` con `with_company`.
- [ ] Convertí los campos de precio a `Monetary` con moneda ligada a la compañía.
