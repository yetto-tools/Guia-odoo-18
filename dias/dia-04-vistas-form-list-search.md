# Día 4 — Vistas: Form, List, Search, acciones y menús

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 3–4 h

## Objetivo del día
Tener un CRUD completo de `inmueble.property` funcionando desde la interfaz web.

---

## Conceptos de Odoo

### Tres piezas separadas que trabajan juntas
Es clave no confundirlas:
- **Vista** (`ir.ui.view`): define el `arch` XML — el layout visual. Una vista sola no es navegable.
- **Acción de ventana** (`ir.actions.act_window`): le dice a Odoo "abrí el modelo X, con las vistas en este orden (`view_mode`), con este dominio/contexto". Es lo que realmente "abre" algo.
- **Menú** (`ir.ui.menu`): es un link en la barra de navegación que dispara una acción. Sin menú, la acción existe pero nadie la ve (aunque igual se puede abrir por URL o desde un botón).

### Cómo Odoo elige qué vista mostrar
El atributo `view_mode="list,form"` de la acción define **el orden de prioridad**. Al abrir la acción, Odoo muestra la primera (`list`); al hacer clic en un registro, pasa a la siguiente (`form`). Si no especificás una vista concreta con `id`, Odoo toma la vista **por defecto** de ese modelo y ese tipo (la que tenga menor `priority`, o la última creada si no hay prioridad explícita) — por eso, si tenés una sola vista `form` para un modelo, no hace falta referenciarla por id en la acción.

### `<list>`, no `<tree>` — sintaxis de Odoo 18
Versiones anteriores de Odoo llamaban "tree" a la vista de lista tabular (arrastra el nombre de cuando internamente se armaba como un árbol colapsable). Odoo 18 formalizó el cambio de nombre a `<list>`, que es semánticamente lo que siempre fue: una tabla. Si ves `<tree>` en documentación o módulos viejos, es el equivalente exacto de `<list>` en versiones anteriores a la 18.

### La vista Search no es solo un cuadro de texto
`<search>` define tres cosas a la vez:
- Sobre qué campos busca el cuadro de texto libre (`<field name="..."/>`).
- Qué **filtros predefinidos** aparecen en el menú desplegable (`<filter domain="...">`).
- Por qué campos se puede **agrupar** (`<filter context="{'group_by': '...'}">`).

Sin una vista search propia, Odoo genera una automática (busca solo por `name`), pero cualquier filtro o agrupamiento útil tenés que declararlo vos.

### Jerarquía de menús
`menuitem` usa `parent_id` para anidarse. Un menú sin `parent_id` es de nivel raíz (aparece en la barra superior de apps). El `sequence` controla el orden entre hermanos.

---

## Ejercicios prácticos

### Ejercicio 1 — Vistas y menú completos (guiado)

```xml
<odoo>
    <record id="view_inmueble_property_form" model="ir.ui.view">
        <field name="name">inmueble.property.form</field>
        <field name="model">inmueble.property</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="expected_price"/>
                        <field name="selling_price"/>
                        <field name="date_availability"/>
                    </group>
                    <group>
                        <field name="bedrooms"/>
                        <field name="living_area"/>
                        <field name="garden"/>
                        <field name="garden_area"/>
                        <field name="garden_orientation"/>
                    </group>
                    <field name="description"/>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_inmueble_property_list" model="ir.ui.view">
        <field name="name">inmueble.property.list</field>
        <field name="model">inmueble.property</field>
        <field name="arch" type="xml">
            <list>
                <field name="name"/>
                <field name="expected_price"/>
                <field name="state"/>
            </list>
        </field>
    </record>

    <record id="view_inmueble_property_search" model="ir.ui.view">
        <field name="name">inmueble.property.search</field>
        <field name="model">inmueble.property</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <filter name="new" string="Nuevas" domain="[('state', '=', 'new')]"/>
                <group expand="0" string="Agrupar por">
                    <filter name="group_state" string="Estado" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_inmueble_property" model="ir.actions.act_window">
        <field name="name">Propiedades</field>
        <field name="res_model">inmueble.property</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_inmueble_root" name="Inmobiliaria"/>
    <menuitem id="menu_inmueble_property" name="Propiedades"
              parent="menu_inmueble_root" action="action_inmueble_property"/>
</odoo>
```
Agregalo a `data` en el manifest, actualizá el módulo, y probá crear/editar/eliminar desde la UI.

### Ejercicio 2 — Romper y arreglar el orden de vistas
1. Quitá momentáneamente la vista `list` del `data` (dejala fuera del manifest) y actualizá.
2. Observá qué vista de lista usa Odoo igual (la genérica autogenerada) — notá qué columnas trae por defecto.
3. Volvé a agregarla al manifest y actualizá.

### Ejercicio 3 — Ampliar la vista Search
1. Agregá un segundo filtro `vendidas` con dominio `[('state', '=', 'sold')]`.
2. Agregá un tercer campo de búsqueda de texto libre: `expected_price` (para poder buscar por precio exacto).
3. Probá ambos desde la UI.

### Ejercicio 4 — Jugar con `view_mode` y prioridad de vistas
1. Cambiá `view_mode` de la acción a `form,list` (invertido).
2. Observá qué cambia al hacer clic en el menú (¿abre directo un formulario vacío o la lista?).
3. Volvé a dejarlo como `list,form`.

### Ejercicio 5 — Reto: filtro + groupby combinados
- Agregá al `search` un filtro `disponibles` con dominio `[('state', 'in', ('new', 'offer_received'))]`.
- Agregá un `groupby` adicional por `garden_orientation`.
- Probá activar ambos a la vez desde la UI y confirmá que se combinan con AND.

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia hay entre una vista, una acción de ventana y un menú?
2. ¿Qué pasa si abrís una acción sin haber definido ninguna vista `form` propia para ese modelo?
3. ¿Por qué en Odoo 18 se usa `<list>` en vez de `<tree>`?
4. ¿Qué tres cosas define, a la vez, una vista `<search>`?
5. Si un `menuitem` no tiene `parent_id`, ¿dónde aparece?

<details>
<summary>Ver respuestas</summary>

1. La vista define el layout XML; la acción de ventana decide qué modelo abrir y con qué vistas/dominio; el menú es el link visible que dispara la acción. Podés tener una vista sin acción, o una acción sin menú (accesible solo por URL o botón).
2. Odoo genera una vista formulario automática mostrando todos los campos en un orden genérico — funcional pero poco prolija.
3. Es un cambio de nomenclatura de la versión 18: lo que antes se llamaba vista "tree" (por cómo se armaba internamente) pasó a llamarse "list", que refleja mejor que es una tabla.
4. Sobre qué campos busca el texto libre, qué filtros predefinidos aparecen en el desplegable, y por qué campos se puede agrupar.
5. Aparece como un menú de nivel raíz, en la barra superior de aplicaciones.

</details>

## Checklist de cierre
- [ ] Sé la diferencia entre vista, acción y menú.
- [ ] Recuerdo usar `<list>` en vez de `<tree>` (sintaxis Odoo 18).
- [ ] Puedo navegar al módulo desde el menú principal.
- [ ] Agregué al menos un filtro y un groupby propios en la vista search.
