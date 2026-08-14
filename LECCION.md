# Día 7 — Integración y repaso de la semana 1

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 2–3 h (sin contenido nuevo)

## Objetivo del día
Consolidar lo construido en los días 1 a 6, sin agregar temas nuevos, y confirmar que realmente entendiste — no solo que copiaste el código.

---

## Tareas de pulido

1. Revisar breadcrumbs del módulo (¿el nombre del registro se ve bien en la parte superior al entrar a un formulario?).
2. Agregar un ícono propio al `menuitem` raíz (`web_icon`).
3. Confirmar que `depends` en el manifest sea exactamente `["base", "mail"]`.
4. Revisar que no queden campos sin `string` legible en casos poco obvios (Odoo genera uno automático del nombre técnico, pero no siempre queda bien).
5. Repasar el orden de `data` en el manifest: seguridad → vistas → (más adelante: datos, reportes).

---

## Ejercicio de integración: armar el módulo desde cero, sin mirar código previo

Este es el ejercicio central del día. Sin copiar y pegar de los días anteriores, y **solo con tus notas o memoria**, intentá recrear de punta a punta:

1. Un modelo con al menos 5 campos de tipos distintos.
2. Una relación `Many2one` y una `Many2many` hacia otros dos modelos nuevos.
3. Vista formulario, lista y búsqueda.
4. Un menú de dos niveles.
5. Seguridad con 2 grupos y al menos una record rule.

Si te trabás en algún punto, es una señal de qué repasar antes de seguir a la semana 2 — no lo resuelvas mirando el código de los días anteriores hasta después de haberlo intentado solo.

---

## Autoevaluación de la semana 1

1. ¿Cuál es la diferencia entre ACL y record rule?
2. ¿Qué pasa si actualizás un módulo sin haber cambiado una vista? ¿Se reprocesa igual?
3. ¿Por qué importa el orden de los archivos dentro de `data` en el manifest?
4. ¿Qué campos trae "gratis" todo modelo, sin declararlos?
5. ¿Cuál es la diferencia entre `Many2one`, `One2many` y `Many2many` en términos de qué tabla guarda la relación?
6. ¿Qué diferencia hay entre `required=True` y `default=...`?
7. ¿Por qué en Odoo 18 se usa `<list>` en vez de `<tree>`?
8. ¿Qué evalúa exactamente el dominio de una `ir.rule`, y con qué variables cuenta?

<details>
<summary>Ver respuestas</summary>

1. El ACL decide si un grupo puede operar sobre un modelo (todo o nada por operación); la record rule filtra, dentro de eso, qué filas concretas ve/toca el usuario.
2. Sí — Odoo vuelve a procesar todos los archivos declarados en `data`, no solo los que cambiaron; por eso `-u` reprocesa vistas aunque no las hayas tocado en esa sesión particular.
3. Porque los archivos se cargan secuencialmente; si algo referencia (por `ref`) un registro definido en un archivo posterior en la lista, la carga falla.
4. `id`, `create_date`, `create_uid`, `write_date`, `write_uid`.
5. `Many2one` guarda una columna FK en la tabla propia; `One2many` no guarda nada (es una consulta calculada sobre el `Many2one` inverso); `Many2many` crea una tabla intermedia con dos FK.
6. `required=True` bloquea el guardado si falta el valor; `default=...` solo se usa si no se especificó nada al crear, y no impide que después quede vacío.
7. Es un cambio de nomenclatura de esa versión: la vista de tabla, antes llamada "tree", pasó a llamarse "list", nombre que refleja mejor qué es.
8. Evalúa una condición sobre los campos del registro, con `user` (usuario actual) y `time` disponibles como variables de contexto.

</details>

---

## Estado esperado del módulo al cierre de la semana 1
- [ ] Modelo `inmueble.property` con campos básicos.
- [ ] Modelos `inmueble.property.type` y `inmueble.property.tag` relacionados.
- [ ] Vistas form, list y search funcionando.
- [ ] Menú de dos niveles (Inmobiliaria → Propiedades).
- [ ] Seguridad con 2 grupos y record rules probada con usuarios reales.
- [ ] Pude recrear una versión mínima del módulo sin mirar el código de los días anteriores.

## Recursos de repaso
- Documentación oficial de Odoo 18: sección "Tutorials: Getting started" en `odoo.com/documentation/18.0`.
