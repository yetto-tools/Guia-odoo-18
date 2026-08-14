# Día 13 — Automatización, mail y actividades

**Semana:** 2 — Lógica de negocio y ORM avanzado
**Duración estimada:** 3–4 h

## Objetivo del día
Agregar chatter a la propiedad, notificar automáticamente al aceptar una oferta, y programar una tarea recurrente.

---

## Conceptos de Odoo

### Qué te da `mail.thread`, exactamente
Heredar `mail.thread` no es solo "agregar un cuadro de comentarios". Le da a tu modelo:
- `message_ids`: histórico de mensajes/notas asociados al registro (el chatter).
- `message_follower_ids`: quién sigue este registro (recibe notificaciones de cambios).
- El método `message_post()`, para postear mensajes desde código.
- Integración automática con el sistema de correo saliente de Odoo (si un mensaje se postea "por email", puede enviarse de verdad).

`mail.activity.mixin` es un mixin **aparte**, que agrega `activity_ids` y el método `activity_schedule()` — actividades son tareas con fecha límite asignadas a un usuario ("Preparar contrato", "Llamar al comprador"), distintas de un simple mensaje en el chatter. Podés usar uno sin el otro, pero en la práctica casi siempre van juntos.

### El elemento `<chatter/>`
Es sintaxis de vista, no de modelo — le dice al cliente web "renderizá acá el widget de chatter completo" (mensajes + seguidores + actividades, con su propia UI para postear). Va como **hermano** de `<sheet>`, no adentro. Si tu modelo no heredó `mail.thread`, agregar `<chatter/>` a la vista no rompe nada pero tampoco muestra nada útil.

### `message_post()` vs `activity_schedule()`: dos cosas distintas
- `message_post(body="...")` deja un mensaje permanente en el historial — es informativo, de solo lectura una vez posteado (más allá de poder eliminarlo con permisos).
- `activity_schedule("mail.mail_activity_data_todo", summary="...", user_id=...)` crea una **tarea pendiente**, con fecha límite, asignada a alguien específico, que aparece en su panel de actividades hasta que la marque como hecha. Es accionable, no solo informativo.

Usar el correcto según el caso importa: un simple registro de "esto pasó" es un mensaje; algo que alguien tiene que **hacer** es una actividad.

### `ir.cron`: cómo Odoo ejecuta código sin que nadie lo dispare
Un `ir.cron` es un registro que le dice al servidor "cada tantos `interval_number` `interval_type`, ejecutá este código o este método". Internamente, Odoo tiene un proceso (o worker dedicado, en producción con `workers > 0`) que revisa periódicamente qué crons están vencidos y los corre. El campo `code` (cuando `state="code"`) es Python que se ejecuta con `model` disponible como el recordset vacío del modelo indicado — típicamente vas a llamar ahí a un método tuyo, no a escribir lógica inline.

---

## Ejercicios prácticos

### Ejercicio 1 — Activar chatter (guiado)

```python
class InmuebleProperty(models.Model):
    _name = "inmueble.property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Propiedad en venta"
    # ... resto de los campos ...
```

```xml
<form>
    <sheet>
        <!-- ... contenido existente ... -->
    </sheet>
    <chatter/>
</form>
```
Actualizá el módulo y probá `message_post` manualmente desde `odoo shell`:
```python
prop = env["inmueble.property"].search([], limit=1)
prop.message_post(body="Mensaje de prueba desde shell")
```
Confirmá que aparece en el chatter al abrir esa propiedad en la UI.

### Ejercicio 2 — Diferencia entre mensaje y actividad
1. Sobre la misma propiedad, ejecutá:
   ```python
   prop.activity_schedule(
       "mail.mail_activity_data_todo",
       summary="Llamar al comprador",
       user_id=env.user.id,
   )
   ```
2. Abrí la propiedad en la UI y confirmá que ahora aparece, además del mensaje, una **actividad pendiente** con fecha límite, distinta visualmente de un mensaje simple.
3. Marcá la actividad como hecha desde la UI y confirmá que desaparece de "pendientes" pero queda registrada en el historial.

### Ejercicio 3 — Notificar automáticamente al aceptar una oferta
1. En el método que acepta una oferta (`inmueble.property.offer`, ya sea que lo tengas del día 11-14 o lo escribas ahora), agregá:
   ```python
   self.property_id.message_post(body=f"Oferta de {self.partner_id.name} aceptada por {self.price}.")
   self.property_id.activity_schedule(
       "mail.mail_activity_data_todo",
       summary="Preparar contrato de venta",
       user_id=self.property_id.salesperson_id.id,
   )
   ```
2. Aceptá una oferta desde la UI y confirmá que el mensaje y la actividad aparecen automáticamente, sin intervención manual.

### Ejercicio 4 — Seguidores automáticos
1. Desde la UI, en el chatter de una propiedad, agregate a vos mismo como seguidor (ícono de seguidores).
2. Postéale un mensaje a esa propiedad desde otro usuario (o desde shell simulando otro usuario).
3. Confirmá que te llega una notificación (campana de notificaciones en Odoo) por ser seguidor — esto demuestra que `message_follower_ids` no es solo una lista pasiva.

### Ejercicio 5 — Reto: cron de propiedades sin movimiento
Creá un `ir.cron` que, una vez al día, busque propiedades en estado `new` con `date_availability` vencida hace más de 90 días y les postee un mensaje de recordatorio:
```xml
<record id="cron_inmueble_stale_properties" model="ir.cron">
    <field name="name">Recordatorio de propiedades sin movimiento</field>
    <field name="model_id" ref="model_inmueble_property"/>
    <field name="state">code</field>
    <field name="code">model._cron_notify_stale_properties()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
</record>
```
Escribí el método `_cron_notify_stale_properties` en `inmueble.property`. No hace falta cambiar el estado, solo postear el mensaje. Para probarlo sin esperar un día real, ejecutalo manualmente desde `odoo shell`: `env["inmueble.property"]._cron_notify_stale_properties()`.

---

## Preguntas de repaso conceptual

1. ¿Qué te da `mail.thread` que no te da `mail.activity.mixin`, y viceversa?
2. ¿Dónde va `<chatter/>` en la vista formulario: dentro de `<sheet>` o como hermano?
3. ¿Cuál es la diferencia práctica entre `message_post()` y `activity_schedule()`?
4. En un `ir.cron` con `state="code"`, ¿qué representa la variable `model` disponible dentro del campo `code`?
5. Si querés probar la lógica de un cron sin esperar a que se cumpla su intervalo real, ¿cómo lo hacés?

<details>
<summary>Ver respuestas</summary>

1. `mail.thread` da el historial de mensajes (`message_ids`) y seguidores (`message_follower_ids`) junto con `message_post()`; `mail.activity.mixin` da las actividades programadas (`activity_ids`) junto con `activity_schedule()` — son mixins independientes que suelen combinarse pero no son lo mismo.
2. Como hermano de `<sheet>`, dentro de `<form>` pero fuera del `<sheet>`.
3. `message_post()` deja un registro informativo permanente en el historial; `activity_schedule()` crea una tarea pendiente con fecha límite, asignada a un usuario específico, que permanece "accionable" hasta que se marca como hecha.
4. Es el recordset vacío del modelo indicado en `model_id` — típicamente se usa para llamar a un método propio de ese modelo (`model._mi_metodo()`), en vez de escribir lógica inline ahí.
5. Llamando manualmente al método correspondiente desde `odoo shell` (por ejemplo `env["inmueble.property"]._cron_notify_stale_properties()`), sin necesidad de esperar a que el cron se dispare solo.

</details>

## Checklist de cierre
- [ ] Sé qué gana un modelo al heredar `mail.thread` frente a `mail.activity.mixin`.
- [ ] Entiendo la diferencia entre un mensaje y una actividad, y cuándo usar cada uno.
- [ ] Implementé la notificación automática al aceptar una oferta.
- [ ] Escribí y probé manualmente el cron de propiedades sin movimiento.
