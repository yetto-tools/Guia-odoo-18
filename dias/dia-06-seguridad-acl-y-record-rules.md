# Día 6 — Seguridad: grupos, ACL y record rules

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 3–4 h

## Objetivo del día
Que un agente solo vea sus propias propiedades, y un gerente las vea todas.

---

## Conceptos de Odoo

### Dos capas de seguridad que se complementan, no se reemplazan
- **ACL** (`ir.model.access.csv`): responde "¿este grupo puede tocar este *modelo* en general?" — es todo o nada por operación (leer/escribir/crear/borrar), sin mirar registros individuales.
- **Record rule** (`ir.rule`): responde "de los registros que el ACL ya permitió tocar, ¿cuáles *filas* puede ver/editar/borrar este usuario?" — filtra con un dominio.

Son capas independientes y **ambas se aplican**: si el ACL dice que no podés borrar, ninguna record rule te va a dar permiso de borrar. Y si el ACL sí permite borrar pero la record rule excluye ese registro del dominio visible, tampoco vas a poder tocarlo. El error más común de principiante es escribir una record rule perfecta y no entender por qué "igual no funciona" — casi siempre es que el ACL de esa fila en el CSV está mal.

### Cómo se evalúa `domain_force`
El dominio de una `ir.rule` se evalúa con dos variables de contexto disponibles: `user` (el usuario actual, un recordset de `res.users`) y `time` (para reglas basadas en fechas). `[('salesperson_id', '=', user.id)]` literalmente compara la columna `salesperson_id` del registro contra el id del usuario que está mirando.

### Reglas múltiples para el mismo modelo y su combinación
Cuando hay varias `ir.rule` para el mismo modelo:
- Reglas del **mismo grupo** (o reglas "globales" sin grupo) se combinan con **OR**.
- Reglas de **distintos grupos** se combinan con **AND** entre sí, dentro del conjunto de grupos al que pertenece el usuario.

Esto es sutil: por eso, en el ejemplo de este día, usamos dos reglas separadas (una por grupo) en vez de intentar meter toda la lógica en una sola regla con condicionales — es el patrón estándar en Odoo.

### Categorías de seguridad
`ir.module.category` agrupa visualmente los grupos relacionados en la pantalla de gestión de usuarios (`Ajustes → Usuarios`), donde cada categoría aparece como una fila con un selector. Sin una categoría propia, tus grupos quedarían mezclados en una categoría genérica, dificultando la administración.

### `implied_ids`: jerarquía entre grupos
`group_inmueble_manager` con `implied_ids` apuntando a `group_inmueble_agent` significa: "todo usuario en el grupo Gerente automáticamente también pertenece al grupo Agente". Es cómo Odoo modela jerarquías de permisos sin duplicar ACLs — el gerente hereda lo que puede hacer el agente, y además tiene sus propios permisos ampliados.

---

## Ejercicios prácticos

### Ejercicio 1 — Grupos, ACL y record rules (guiado)

`security/security.xml`:
```xml
<odoo>
    <record id="module_category_inmueble" model="ir.module.category">
        <field name="name">Inmobiliaria</field>
    </record>

    <record id="group_inmueble_agent" model="res.groups">
        <field name="name">Agente Inmobiliario</field>
        <field name="category_id" ref="module_category_inmueble"/>
    </record>

    <record id="group_inmueble_manager" model="res.groups">
        <field name="name">Gerente Inmobiliario</field>
        <field name="category_id" ref="module_category_inmueble"/>
        <field name="implied_ids" eval="[(4, ref('group_inmueble_agent'))]"/>
    </record>

    <record id="rule_inmueble_property_agent" model="ir.rule">
        <field name="name">Agente ve solo sus propiedades</field>
        <field name="model_id" ref="model_inmueble_property"/>
        <field name="domain_force">[('salesperson_id', '=', user.id)]</field>
        <field name="groups" eval="[(4, ref('group_inmueble_agent'))]"/>
    </record>

    <record id="rule_inmueble_property_manager" model="ir.rule">
        <field name="name">Gerente ve todas las propiedades</field>
        <field name="model_id" ref="model_inmueble_property"/>
        <field name="domain_force">[(1, '=', 1)]</field>
        <field name="groups" eval="[(4, ref('group_inmueble_manager'))]"/>
    </record>
</odoo>
```

`security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_inmueble_property_agent,inmueble.property.agent,model_inmueble_property,group_inmueble_agent,1,1,1,0
access_inmueble_property_manager,inmueble.property.manager,model_inmueble_property,group_inmueble_manager,1,1,1,1
```
Agregá ambos a `data` **antes** que las vistas. Creá dos usuarios, asignales cada grupo, y verificá el filtrado.

### Ejercicio 2 — Probar la combinación OR de reglas del mismo grupo
1. Agregá una segunda `ir.rule` para `group_inmueble_agent`, con dominio `[('state', '=', 'sold')]` y el mismo `groups`.
2. Como usuario agente, confirmá que ahora ves tus propiedades **más** cualquier propiedad vendida (aunque no sea tuya) — eso confirma que dos reglas del mismo grupo se combinan con OR, no con AND.
3. Sacá esta regla de prueba al terminar (no la queremos en el módulo final).

### Ejercicio 3 — Desarmar el ACL a propósito
1. Cambiá `perm_read` a `0` para el agente en el CSV.
2. Actualizá el módulo y logueate como agente — confirmá que el menú "Propiedades" ni siquiera aparece navegable, sin importar qué diga la record rule.
3. Volvé a poner `perm_read=1`.

### Ejercicio 4 — Confirmar la jerarquía de `implied_ids`
1. Logueate como el usuario gerente.
2. Andá a `Ajustes → Usuarios`, abrí ese usuario, y confirmá que también aparece marcado como perteneciente al grupo "Agente Inmobiliario" (por la herencia de `implied_ids`), sin que se lo hayas asignado manualmente.

### Ejercicio 5 — Reto: ¿por qué el agente podría borrar lo que no debería?
- Con el CSV original (`perm_unlink=0` para el agente), confirmá que el botón de eliminar no aparece para el agente.
- Ahora cambiá `perm_unlink` a `1` para el agente, dejando la record rule intacta — logueate como agente e intentá borrar una propiedad de **otro** agente navegando directamente a su URL (`/odoo/action-.../ID`). Confirmá si te deja o no, y explicá por qué (pista: la record rule sigue filtrando qué filas ve, incluso si el ACL ahora permite la operación).
- Volvé a dejar `perm_unlink=0` para el agente al terminar.

---

## Preguntas de repaso conceptual

1. ¿Cuál es la diferencia funcional entre un ACL y una record rule?
2. Si el ACL de un modelo dice `perm_write=0` para un grupo, ¿alguna record rule puede darle permiso de escritura a ese grupo?
3. ¿Cómo se combinan dos `ir.rule` que apuntan al mismo grupo? ¿Y dos que apuntan a grupos distintos?
4. ¿Qué significa que `group_inmueble_manager` tenga `implied_ids` apuntando a `group_inmueble_agent`?
5. ¿Qué variables tenés disponibles dentro de un `domain_force` para escribir la condición?

<details>
<summary>Ver respuestas</summary>

1. El ACL decide si un grupo puede operar sobre un modelo en general (todo o nada, por tipo de operación); la record rule filtra, dentro de lo que el ACL ya permite, qué filas concretas puede ver/tocar el usuario.
2. No. El ACL es un límite duro: si dice que no se puede escribir, ninguna record rule puede otorgar ese permiso — las rules solo restringen más, nunca amplían lo que el ACL ya negó.
3. Reglas del mismo grupo (o sin grupo/globales) se combinan con OR entre sí; reglas de grupos distintos se combinan con AND entre los conjuntos de cada grupo al que pertenece el usuario.
4. Que todo usuario en el grupo Gerente pertenece automáticamente también al grupo Agente — hereda sus permisos sin que haya que asignárselo manualmente ni duplicar ACLs.
5. `user` (el usuario actual, recordset de `res.users`) y `time` (para condiciones basadas en fecha/hora).

</details>

## Checklist de cierre
- [ ] Puedo explicar la diferencia entre ACL y record rule sin mirar el código.
- [ ] Probé la combinación OR de dos reglas del mismo grupo.
- [ ] Confirmé que un ACL restrictivo bloquea aunque la record rule sea permisiva.
- [ ] Probé la seguridad con usuarios reales, no solo leyendo el XML.
