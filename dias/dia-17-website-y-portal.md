# Día 17 — Website y Portal

**Semana:** 3 — Frontend, reportes e integraciones
**Duración estimada:** 3–4 h

## Objetivo del día
Publicar una página pública que liste propiedades disponibles, y entender los niveles de autenticación de un controlador.

---

## Conceptos de Odoo

### Un controlador es solo una función mapeada a una URL
`@http.route(ruta, ...)` sobre un método de una clase que extiende `http.Controller` registra ese método para que responda cuando alguien pida esa URL. No hay magia adicional: es routing HTTP clásico, con la particularidad de que `request.env` te da acceso al ORM completo dentro del handler.

### Los tres niveles de `auth`
- `auth="public"`: no requiere sesión. Cualquiera (logueado o no) puede acceder. El usuario efectivo dentro del request es el usuario público configurado en el sistema (normalmente uno con permisos muy limitados).
- `auth="user"`: requiere sesión iniciada (cookie válida). Si no hay sesión, Odoo redirige a login antes de ejecutar tu método.
- `auth="none"`: no aplica ningún chequeo de autenticación ni de sesión — ni siquiera asigna un usuario al contexto. Se usa para endpoints muy específicos (webhooks externos, health checks) que manejan su propia autenticación por otro medio.

### Por qué `sudo()` aparece en un controlador público
Con `auth="public"`, el usuario efectivo es el usuario público, que normalmente **no tiene** permisos para leer `inmueble.property` directamente (porque no pertenece a ningún grupo del día 6). Si tu página necesita mostrar datos igual, tenés que decidir conscientemente: o le das permisos de lectura al usuario público sobre ese modelo (vía ACL), o usás `sudo()` en el controlador para esa consulta específica, confiando en que el propio controlador ya filtra correctamente qué se expone (por ejemplo, solo propiedades `disponibles`, nunca datos sensibles).

### `website=True`: heredás el layout, no solo el look
Con `website=True`, tu respuesta se integra al sitio (header de navegación, footer, menú de idiomas si aplica) automáticamente vía `t-call="website.layout"` dentro de tu plantilla. Sin esto, tu HTML se serviría "pelado", sin ningún elemento del sitio alrededor.

### `request.render` vs devolver un dict
`request.render(template, values)` renderiza una plantilla QWeb y devuelve la respuesta HTTP lista. Es el patrón estándar para páginas HTML. Para endpoints que devuelven datos (no HTML), como vas a ver el día 19 con `type="json"`, en cambio devolvés directamente una estructura de datos (dict/list) que Odoo serializa.

---

## Ejercicios prácticos

### Ejercicio 1 — Página pública de propiedades (guiado)

`controllers/main.py`:
```python
from odoo import http
from odoo.http import request


class InmueblePortal(http.Controller):
    @http.route("/propiedades", type="http", auth="public", website=True)
    def list_properties(self, **kwargs):
        properties = request.env["inmueble.property"].sudo().search(
            [("state", "in", ("new", "offer_received"))]
        )
        return request.render("gestion_inmobiliaria.properties_list", {"properties": properties})
```

`views/inmueble_templates.xml`:
```xml
<odoo>
    <template id="properties_list" name="Propiedades disponibles">
        <t t-call="website.layout">
            <div class="container">
                <h1>Propiedades disponibles</h1>
                <div t-foreach="properties" t-as="prop" class="mb-3">
                    <strong t-out="prop.name"/> — <t t-out="prop.expected_price"/>
                </div>
            </div>
        </t>
    </template>
</odoo>
```
Agregá `"website"` a `depends`, importá el controlador, y navegá `/propiedades` **sin sesión iniciada** (probalo en una ventana de incógnito).

### Ejercicio 2 — Comparar los tres niveles de `auth`
1. Cambiá temporalmente la ruta a `auth="user"` y probá acceder sin sesión — confirmá que te redirige a login.
2. Cambiá a `auth="none"` y agregá un `print` o log dentro del método imprimiendo `request.env.user` — confirmá qué usuario ves (o si falla al intentar acceder al ORM sin contexto de usuario claro).
3. Volvé a `auth="public"`.

### Ejercicio 3 — Sacar el `sudo()` y ver qué pasa
1. Quitá `.sudo()` de la consulta.
2. Accedé a `/propiedades` sin sesión y observá el resultado: ¿lista vacía, error de permisos, o algo distinto?
3. Explicá por qué pasa eso, conectándolo con lo que aprendiste el día 6 sobre ACL — el usuario público no pertenece a ningún grupo con permiso de lectura sobre `inmueble.property`.
4. Volvé a agregar `.sudo()`.

### Ejercicio 4 — Página sin `website=True`
1. Creá una segunda ruta de prueba `/propiedades-raw` idéntica pero con `website=False` (o sin el parámetro) y devolviendo el HTML directo con `request.make_response(...)` en vez de `request.render`.
2. Comparé visualmente: ¿aparece el header/footer del sitio en esta versión?

### Ejercicio 5 — Reto: detalle de una propiedad
Agregá la ruta `/propiedades/<int:property_id>` con el detalle de una sola propiedad:
```python
from werkzeug.exceptions import NotFound

@http.route("/propiedades/<int:property_id>", type="http", auth="public", website=True)
def property_detail(self, property_id, **kwargs):
    property_rec = request.env["inmueble.property"].sudo().search(
        [("id", "=", property_id), ("state", "in", ("new", "offer_received"))]
    )
    if not property_rec:
        raise NotFound()
    return request.render("gestion_inmobiliaria.property_detail", {"property": property_rec})
```
Creá la plantilla correspondiente, y probá tanto un id válido como uno inexistente (confirmá el 404).

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia hay entre `auth="public"`, `auth="user"` y `auth="none"`?
2. ¿Por qué un controlador con `auth="public"` a menudo necesita `sudo()` para leer datos del ORM?
3. ¿Qué te da `website=True` que no tendrías con una respuesta HTTP genérica?
4. ¿Cuál es la diferencia entre `request.render(...)` y devolver un dict directamente desde un endpoint?
5. Si sacás `sudo()` de una consulta en un controlador público y el modelo no tiene ACL de lectura para el usuario público, ¿qué pasa?

<details>
<summary>Ver respuestas</summary>

1. `auth="public"` no requiere sesión (usa el usuario público, con permisos limitados); `auth="user"` requiere sesión iniciada y redirige a login si no la hay; `auth="none"` no aplica ningún chequeo de autenticación ni de sesión.
2. Porque el usuario público normalmente no pertenece a ningún grupo con permisos ACL sobre modelos de negocio — sin `sudo()`, el `search()` devolvería vacío o fallaría por falta de permisos.
3. La integración automática con el layout del sitio (header de navegación, footer, selector de idioma) vía `website.layout`, sin que tengas que codificar esos elementos vos.
4. `request.render(...)` renderiza una plantilla QWeb y devuelve HTML listo, pensado para páginas visuales; devolver un dict directamente es el patrón para endpoints de datos (como los `type="json"` del día 19), donde Odoo serializa la estructura en vez de renderizar HTML.
5. La consulta devuelve vacío (o falla), porque el usuario público efectivamente no tiene permiso ACL para leer ese modelo — el `search()` respeta la seguridad normal si no hay `sudo()` de por medio.

</details>

## Checklist de cierre
- [ ] Sé por qué usé `sudo()` en el `search` del controlador, y confirmé qué pasa si lo saco.
- [ ] Entiendo qué agrega `website=True` a la respuesta.
- [ ] Probé los tres niveles de `auth` y vi la diferencia de comportamiento.
- [ ] Implementé la ruta de detalle con manejo de 404.
