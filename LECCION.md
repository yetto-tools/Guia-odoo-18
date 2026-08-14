# Día 21 — Repaso e integración de la semana 3

**Semana:** 3 — Frontend, reportes e integraciones
**Duración estimada:** 2–3 h (sin contenido nuevo)

## Objetivo del día
Consolidar reporte PDF, Kanban, portal público y endpoint externo funcionando juntos, y confirmar que entendés el "por qué" de cada pieza.

---

## Tareas de consolidación

1. Confirmar que el reporte PDF (día 15) sigue generando bien tras los cambios de los días 16-20.
2. Confirmar que la vista Kanban (día 16) muestra los tipos y etiquetas cargados el día 20.
3. Confirmar que `/propiedades` (día 17) lista correctamente incluyendo datos cargados por XML.
4. Revisar que la clave `assets` del manifest esté bien declarada (JS + XML del widget OWL del día 18).
5. Volver a correr el script XML-RPC del día 19 contra el estado actual del módulo, incluyendo la prueba con API Key.

---

## Ejercicio de integración: flujo público completo

Sin mirar el código de los días anteriores, intentá recrear de memoria el flujo completo, desde cero, en un módulo de prueba descartable:

1. Un controlador público (`auth="public"`) que liste registros de un modelo simple.
2. Una plantilla QWeb con `website.layout` para mostrarlos.
3. Un reporte PDF de un registro individual, con `web.external_layout`.
4. Un endpoint `type="json"` que devuelva los mismos datos en formato JSON.

Si te trabás en algún punto, es la señal de qué repasar antes de la semana 4.

---

## Autoevaluación

1. ¿Diferencia entre `auth="public"`, `"user"` y `"none"` en un controlador?
2. ¿Por qué los reportes y las páginas de website comparten el motor QWeb pero no exactamente los mismos helpers? (`web.external_layout` vs `website.layout`)
3. ¿Qué pasa si olvidás `binding_model_id` en un `ir.actions.report`?
4. ¿Por qué un `noupdate="1"` no es lo mismo que "datos de solo lectura"?
5. ¿Qué diferencia hay entre `search()` y `browse()` respecto a cuándo se dispara la consulta SQL?
6. ¿Qué te garantiza extender tus props con `...standardFieldProps` en un widget OWL?

<details>
<summary>Ver respuestas</summary>

1. `auth="public"` no requiere sesión; `auth="user"` requiere sesión iniciada (redirige a login si no la hay); `auth="none"` no aplica ningún chequeo de autenticación ni de sesión.
2. Porque cada contexto (reporte vs. página de sitio) heredó de una plantilla base distinta (`web.html_container`/`web.external_layout` vs `website.layout`) pensada para ese propósito específico, aunque ambas usen la misma sintaxis de directivas `t-*` de QWeb por debajo.
3. El reporte sigue existiendo y se puede invocar programáticamente, pero no aparece automáticamente en el menú "Imprimir" del formulario de ese modelo — habría que abrirlo manualmente por otra vía.
4. Porque `noupdate="1"` solo evita que una actualización del módulo resincronice el registro con el XML original; el usuario puede seguir editándolo libremente desde la UI en cualquier momento.
5. `search()` dispara la consulta SQL de inmediato (necesita preguntarle a la base qué ids matchean); `browse()` es lazy, arma el recordset a partir de ids ya conocidos sin consultar hasta que efectivamente accedés a un campo.
6. Que tu componente reciba las props mínimas que el sistema de vistas necesita para invocar cualquier widget de campo de forma consistente (`record`, `name`, y el resto del contrato estándar).

</details>

---

## Estado esperado del módulo al cierre de la semana 3
- [ ] Reporte PDF de ficha de propiedad.
- [ ] Vista Kanban agrupada por estado.
- [ ] Página pública `/propiedades`.
- [ ] Widget OWL de badge de estado.
- [ ] Datos iniciales de tipos de propiedad vía XML.
- [ ] Integración externa probada por XML-RPC, incluyendo autenticación con API Key.
