# Día 10 — Métodos ORM avanzados

**Semana:** 2 — Lógica de negocio y ORM avanzado
**Duración estimada:** 3–4 h

## Objetivo del día
Escribir métodos propios usando las herramientas del ORM en vez de loops manuales, y entender el costo real de cada una.

![get_available_properties() desde odoo shell](imagenes/dia-10-shell-metodo.jpg)

---

## Conceptos de Odoo

### Un recordset no es una lista de objetos separados
Cuando hacés `env["inmueble.property"].search([...])`, el resultado es **un solo objeto** que representa un conjunto de registros (un recordset), no una lista de instancias Python independientes. Por eso podés hacer `properties.expected_price` sobre un recordset de 50 elementos y obtener algo raro si no iterás — para trabajar con múltiples valores usás `mapped`, no un `for` con acceso directo a un campo escalar.

### `search()` vs `browse()`: cuándo vas a la base y cuándo no
- `search(domain)` **siempre** dispara una consulta SQL inmediatamente (necesita preguntarle a la base qué ids matchean el dominio).
- `browse([1, 2, 3])` arma un recordset a partir de ids que **ya conocés**, sin ir a la base todavía — es "lazy": la consulta real recién ocurre cuando accedés a un campo. Si nunca accedés a ningún campo de esos registros, `browse()` nunca gastó una consulta.

### `filtered`, `mapped`, `sorted`: la tríada funcional
- `filtered(lambda r: condición)` devuelve un **recordset** más chico (podés seguir encadenando métodos de recordset).
- `mapped('campo')` devuelve una **lista de valores** (o un recordset, si el campo es una relación) — con paths punteados navega relaciones: `mapped('offer_ids.price')` trae todos los precios de todas las ofertas de todo el recordset, aplanado en una sola lista.
- `sorted(key=lambda r: ...)` devuelve un recordset **reordenado**, no modifica el original.

Ninguno de los tres dispara una consulta SQL adicional por sí mismo si el recordset ya está prefetcheado — son operaciones en memoria sobre datos que el ORM ya trajo (o va a traer de forma optimizada la primera vez que los necesite).

### `sudo()`: eleva privilegios, no border de seguridad para vos mismo
`recordset.sudo()` devuelve el mismo recordset pero ejecutando como superusuario, saltándose ACL y record rules. Es necesario en casos legítimos (por ejemplo, un controlador público que necesita leer datos que el visitante anónimo no tiene permiso de ver directamente), pero usado sin criterio anula toda la seguridad que armaste el día 6. Regla práctica: usalo en el método específico que lo necesita, sobre el recordset específico que lo necesita — nunca "por las dudas" en todo un módulo.

### `with_context()`: pasar banderas sin persistir nada
Devuelve el mismo recordset pero con un diccionario de contexto adicional, accesible en `self.env.context` dentro de cualquier método que se ejecute a partir de ahí. Es la forma estándar de pasar "modo especial" (por ejemplo, `default_property_id` para precompletar un wizard, como vas a usar el día 12) sin tocar la base de datos.

---

## Ejercicios prácticos

### Ejercicio 1 — Método con `search` + `sorted` (guiado)

```python
def get_available_properties(self):
    return self.search([("state", "in", ("new", "offer_received"))]).sorted(
        key=lambda r: r.expected_price
    )
```
Agregalo a `inmueble.property`, llamalo desde `odoo shell`, y confirmá que el resultado viene ordenado por precio.

### Ejercicio 2 — Diferencia observable entre `search` y `browse`
1. Desde `odoo shell`, ejecutá `ids = env["inmueble.property"].search([]).ids` (esto sí dispara una consulta).
2. Ahora ejecutá `rec = env["inmueble.property"].browse(ids)` — este paso, por sí solo, no dispara ninguna consulta nueva.
3. Recién al ejecutar `rec.mapped("name")` se dispara la consulta que trae los datos. Confirmá esto revisando el log del servidor (con `--log-level=debug_sql` si querés ver el SQL real, o simplemente notando que `browse()` no tarda nada mientras que acceder a un campo sí).

### Ejercicio 3 — `filtered` + `mapped` encadenados
1. Escribí un método que devuelva los nombres de las propiedades con `bedrooms >= 3`, usando `filtered` seguido de `mapped('name')`.
2. Verificalo con al menos 3 propiedades de prueba, algunas con `bedrooms < 3` y otras con `>= 3`.

### Ejercicio 4 — Ver el efecto real de `sudo()`
1. Logueado como el usuario "agente" del día 6 (que solo ve sus propias propiedades), desde `odoo shell` con ese usuario en el contexto (o simulándolo con `with_user`), ejecutá `env["inmueble.property"].search([])` — confirmá que solo trae las suyas.
2. Repetí con `env["inmueble.property"].sudo().search([])` — confirmá que ahora trae **todas**, sin importar el dueño.
3. Reflexioná: ¿en qué situación real de tu módulo sería legítimo usar `sudo()` acá, y en cuál sería un error de seguridad?

### Ejercicio 5 — Reto: emails únicos sin duplicados
Escribí un método que, dado un recordset de propiedades, devuelva la lista de emails **únicos** de sus `salesperson_id`.
- Pista: `mapped('salesperson_id.email')` te da una lista con posibles duplicados (si dos propiedades comparten agente); vas a necesitar `set()` o una comprensión de lista que filtre duplicados manteniendo el resultado como lista.

---

## Preguntas de repaso conceptual

1. ¿Qué es, técnicamente, lo que devuelve `env["modelo"].search([...])`: una lista de objetos Python independientes, o un recordset?
2. ¿Cuál es la diferencia clave entre `search()` y `browse()` en cuanto a cuándo se dispara la consulta SQL?
3. ¿Qué tipo de dato devuelve `mapped('campo')` cuando el campo es un valor escalar (como `price`), y qué devuelve cuando el campo es una relación?
4. ¿Por qué usar `sudo()` "por las dudas" en todo un módulo es peligroso, aunque técnicamente funcione?
5. ¿Para qué sirve `with_context()` y qué NO hace (a diferencia de lo que alguien podría asumir)?

<details>
<summary>Ver respuestas</summary>

1. Un recordset: un único objeto que representa un conjunto de registros, con métodos propios (`filtered`, `mapped`, `sorted`, etc.) — no una lista plana de instancias independientes.
2. `search()` dispara la consulta SQL inmediatamente, porque necesita preguntarle a la base qué ids matchean el dominio; `browse()` es lazy — arma el recordset a partir de ids ya conocidos sin consultar nada hasta que efectivamente accedés a un campo.
3. Con un campo escalar devuelve una lista de valores (posiblemente con duplicados); con un campo relacional devuelve un recordset (o, si es un path punteado como `offer_ids.price`, una lista aplanada de los valores finales).
4. Porque anula silenciosamente toda la seguridad (ACL y record rules) para ese código, sin dejar rastro evidente de por qué — un bug de seguridad después es muy difícil de rastrear si `sudo()` está esparcido sin criterio.
5. Sirve para pasar banderas/contexto adicional (como valores por defecto o flags de comportamiento) a los métodos que se ejecuten sobre ese recordset, sin tocar la base de datos. No persiste nada ni modifica registros — es puramente información de contexto en memoria para esa cadena de llamadas.

</details>

## Checklist de cierre
- [ ] Puedo escribir un dominio de búsqueda sin mirar ejemplos.
- [ ] Entiendo la diferencia entre `search()` y `browse()`, y la comprobé observando cuándo se dispara la consulta.
- [ ] Sé por qué `sudo()` es riesgoso si se usa sin pensar, y puedo dar un ejemplo legítimo de uso.
- [ ] Resolví el reto de emails únicos sin duplicados.
