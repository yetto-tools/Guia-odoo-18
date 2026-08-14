# Día 23 — Performance y buenas prácticas ORM

**Semana:** 4 — Calidad, performance y profesionalización
**Duración estimada:** 3–4 h

## Objetivo del día
Detectar y corregir patrones de consulta ineficientes, y entender el prefetch del ORM a fondo.

![El método de performance corregido, ejecutado en shell](imagenes/dia-23-performance.jpg)

---

## Conceptos de Odoo

### Cómo funciona el prefetch, en detalle
Cuando accedés a un campo de **un** registro dentro de un recordset de 50, el ORM no trae solo ese campo de ese registro — trae ese campo para **los 50** en una única consulta SQL, anticipando que probablemente vas a necesitarlo para todos (es una heurística basada en que normalmente iterás recordsets completos). Esto solo funciona si el recordset se mantiene como una unidad coherente: si en cambio hacés `search()` **dentro** de un loop, estás rompiendo esa optimización — cada iteración dispara su propia consulta nueva, sin aprovechar el prefetch de nada.

### El antipatrón más común: `search()` dentro de un `for`
```python
# Mal: N+1 consultas (una por cada propiedad, dentro del loop)
for prop in self.env["inmueble.property"].search([]):
    offers = self.env["inmueble.property.offer"].search([("property_id", "=", prop.id)])
    ...
```
```python
# Bien: 2 consultas totales, sin importar cuántas propiedades haya
properties = self.env["inmueble.property"].search([])
all_offers = self.env["inmueble.property.offer"].search([("property_id", "in", properties.ids)])
```
La regla práctica: si estás por escribir un `search()` (o cualquier acceso a base de datos) **dentro** de un loop sobre otro recordset, primero preguntate si podés traer todo lo necesario **antes** del loop, con un solo dominio que cubra todos los casos.

### `read_group`/`_read_group`: agregación en la base, no en Python
Sumar, promediar o contar en Python después de traer todos los registros implica transferir cada fila individual del servidor de base de datos al servidor de Odoo, solo para descartar el detalle y quedarte con un número. `_read_group` (la API moderna en Odoo 18) le pide directamente a PostgreSQL que haga la agregación con `GROUP BY` + `SUM`/`AVG`/`COUNT`, devolviendo solo los resultados agregados — muchísimo menos tráfico de datos cuando hay muchos registros.

### `index=True`: ayuda al filtro, no a todo
Agregar `index=True` a un campo crea un índice B-tree en PostgreSQL para esa columna, acelerando `WHERE campo = valor` y `ORDER BY campo`. No acelera todo tipo de consulta (por ejemplo, no ayuda con `LIKE '%texto%'` de la misma forma), y tiene un costo: cada `INSERT`/`UPDATE` sobre esa columna es un poco más lento porque también hay que actualizar el índice. Se usa con criterio, en campos que efectivamente se filtran/ordenan seguido (como `state`, o un `Many2one` muy consultado).

### El costo real de un campo computado no-stored usado en dominios
Si intentás `search([('campo_computado_no_stored', '>', 10)])` sin haber implementado una función `search=` personalizada para ese campo, Odoo directamente no puede traducirlo a SQL — el error (o comportamiento inesperado) que viste en el ejercicio del día 8 no es un capricho, es una limitación estructural: un dominio SQL necesita una columna real (o una implementación explícita de cómo traducir esa búsqueda) para funcionar.

---

## Ejercicios prácticos

### Ejercicio 1 — Corregir el antipatrón (guiado)

Punto de partida, intencionalmente ineficiente:
```python
def get_total_expected_price_bad(self, property_type_id):
    total = 0
    properties = self.env["inmueble.property"].search([])
    for prop in properties:
        if prop.property_type_id.id == property_type_id:
            total += prop.expected_price
    return total
```
Reescribilo:
```python
def get_total_expected_price(self, property_type_id):
    properties = self.env["inmueble.property"].search(
        [("property_type_id", "=", property_type_id)]
    )
    return sum(properties.mapped("expected_price"))
```

### Ejercicio 2 — Medir la diferencia con datos reales
1. Desde `odoo shell`, creá 200 propiedades de prueba (usando `create()` con una lista de diccionarios, en batch, no un loop de 200 `create()` individuales).
2. Corré ambas versiones del método (la mala y la corregida) y compará mentalmente cuántas consultas dispara cada una — si tenés forma de ver el log SQL (`--log-handler=odoo.sql_db:DEBUG` al arrancar el servidor), contá las consultas reales de cada versión.
3. Borrá las 200 propiedades de prueba al terminar.

### Ejercicio 3 — Provocar el error de buscar por un campo no-stored
1. Con `total_area` del día 8 puesto temporalmente en `store=False`.
2. Desde `odoo shell`, intentá `env["inmueble.property"].search([("total_area", ">", 50)])`.
3. Observá el error o comportamiento resultante, y explicá — en tus propias palabras — por qué el ORM no puede traducir esto a SQL sin una columna real detrás.
4. Volvé a `store=True`.

### Ejercicio 4 — `_read_group` para agregaciones
```python
result = self.env["inmueble.property"]._read_group(
    [("property_type_id", "=", property_type_id)],
    aggregates=["expected_price:sum"],
)
```
1. Implementá esto como alternativa al método del ejercicio 1.
2. Con las 200 propiedades de prueba, compará: ¿cuántas filas viajan del servidor de base de datos al servidor de Odoo en cada una de las tres versiones (la mala del ejercicio 1, la corregida con `mapped`, y esta con `_read_group`)?

### Ejercicio 5 — Reto: decidir cuándo indexar
- Revisá todos los campos `Selection` y `Many2one` de `inmueble.property` que escribiste en las semanas anteriores.
- Para cada uno, decidí si tiene sentido agregarle `index=True`, justificando con un caso de uso real de tu módulo (¿se filtra seguido por ese campo? ¿se ordena por él?).
- Aplicá `index=True` a los que decidiste, y confirmá en PostgreSQL (`\d inmueble_property`) que el índice se creó.

---

## Preguntas de repaso conceptual

1. ¿Qué es exactamente lo que optimiza el prefetch del ORM, y qué patrón de código lo rompe?
2. ¿Por qué `search()` dentro de un `for` sobre otro recordset es casi siempre una señal de alerta?
3. ¿Qué ventaja tiene `_read_group` sobre traer todos los registros y sumar en Python?
4. ¿Qué acelera concretamente `index=True`, y qué costo tiene a cambio?
5. ¿Por qué no podés hacer `search()` eficientemente sobre un campo computado con `store=False`, sin configuración adicional?

<details>
<summary>Ver respuestas</summary>

1. Optimiza el acceso a un campo sobre un recordset completo, trayendo ese campo para todos los registros del recordset en una sola consulta en vez de una por registro. Se rompe cuando el flujo de código dispara consultas nuevas (como un `search()`) dentro de un loop, en vez de trabajar sobre el recordset ya cargado.
2. Porque generalmente indica que se está haciendo N consultas (una por cada elemento del loop) cuando un solo `search()` con el dominio adecuado, ejecutado antes del loop, podría traer todo lo necesario en una sola consulta.
3. Que la suma/promedio/conteo lo calcula PostgreSQL directamente con `GROUP BY`, transfiriendo solo el resultado agregado al servidor de Odoo, en vez de transferir cada fila individual solo para sumarlas en Python después.
4. Acelera consultas `WHERE campo = valor` y `ORDER BY campo` sobre esa columna (usando un índice B-tree); a cambio, cada `INSERT`/`UPDATE` sobre esa columna es levemente más lento porque también hay que mantener el índice actualizado.
5. Porque un campo no-stored no existe como columna real en la tabla — no hay nada que PostgreSQL pueda filtrar directamente con `WHERE`; el ORM necesitaría calcular el valor para cada fila antes de poder filtrar, lo cual no está soportado por defecto sin implementar una función `search=` propia para ese campo.

</details>

## Checklist de cierre
- [ ] Sé identificar un `search()` innecesario dentro de un loop.
- [ ] Entiendo qué gana el prefetch cuando trabajás sobre el recordset completo.
- [ ] Comparé las tres versiones del método (mala, corregida, con `_read_group`) y sé cuál elegir según el caso.
- [ ] Decidí con criterio qué campos indexar, no todos "por las dudas".
