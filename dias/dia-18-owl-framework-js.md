# Día 18 — OWL: el framework JS de Odoo

**Semana:** 3 — Frontend, reportes e integraciones
**Duración estimada:** 3–4 h

## Objetivo del día
Crear un widget de campo propio: un badge de color según el estado.

---

## Conceptos de Odoo

### Por qué Odoo tiene su propio framework JS (OWL) en vez de usar React/Vue directo
OWL (Odoo Web Library) es un framework de componentes reactivo, con una API deliberadamente similar a React (hooks, componentes, templates declarativos), pero integrado nativamente con el sistema de vistas, el ORM del lado cliente, y el bundling de assets de Odoo. No necesitás saber React para usarlo, pero si lo conocés, los conceptos (estado reactivo, props, ciclo de vida) transfieren directo.

### La separación componente/template no es opcional
A diferencia de React (donde JSX mezcla lógica y markup en el mismo archivo), OWL separa deliberadamente:
- El archivo `.js` define la **clase** (lógica, propiedades computadas, manejo de eventos).
- El archivo `.xml` define el **template** (markup declarativo con directivas `t-*`), referenciado por nombre desde `static template = "..."`.

Esto es consistente con cómo Odoo ya maneja QWeb en reportes y website — un mismo lenguaje de templates en todo el ecosistema.

### El registry: cómo Odoo descubre tu widget sin configuración manual
`registry.category("fields").add("state_badge", {...})` no es solo "guardar en un diccionario" — es el mecanismo central por el cual **cualquier** vista de **cualquier** modelo puede usar `widget="state_badge"` sin que el core de Odoo sepa nada de tu módulo de antemano. El registry es un patrón de extensión: tu módulo se "engancha" al sistema existente en vez de que el sistema tenga que conocerte.

### `standardFieldProps`: el contrato que todo widget de campo respeta
Cualquier widget de campo recibe, como mínimo, `record` (el registro completo, con `.data` para acceder a todos sus campos), `name` (el nombre del campo que está renderizando), y algunas props más de configuración. `standardFieldProps` es la definición de ese contrato — extender tus props con `...standardFieldProps` asegura que tu componente sea compatible con cómo el sistema de vistas invoca a cualquier widget.

### Registrar assets: por qué no alcanza con crear el archivo
Un archivo `.js` en `static/src/` no se carga automáticamente — tenés que declararlo explícitamente en la clave `assets` del manifest, dentro del **bundle** correspondiente (`web.assets_backend` para cosas del backend administrativo, `web.assets_frontend` para el sitio público, etc.). Si tu widget "no aparece", el primer sospechoso es siempre un asset no declarado o declarado en el bundle equivocado.

---

## Ejercicios prácticos

### Ejercicio 1 — Widget de badge de estado (guiado)

`static/src/js/state_badge.js`:
```javascript
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const COLORS = {
    new: "info",
    offer_received: "warning",
    offer_accepted: "warning",
    sold: "success",
    cancelled: "danger",
};

export class StateBadge extends Component {
    static template = "gestion_inmobiliaria.StateBadge";
    static props = { ...standardFieldProps };

    get badgeClass() {
        return `badge text-bg-${COLORS[this.props.record.data[this.props.name]] || "secondary"}`;
    }
}

registry.category("fields").add("state_badge", { component: StateBadge });
```

`static/src/js/state_badge.xml`:
```xml
<templates xml:space="preserve">
    <t t-name="gestion_inmobiliaria.StateBadge">
        <span t-att-class="badgeClass" t-esc="props.record.data[props.name]"/>
    </t>
</templates>
```

Manifest:
```python
"assets": {
    "web.assets_backend": [
        "gestion_inmobiliaria/static/src/js/state_badge.js",
        "gestion_inmobiliaria/static/src/js/state_badge.xml",
    ],
},
```

Uso en la vista: `<field name="state" widget="state_badge"/>`. Actualizá el módulo (recordá `--dev=all` para no pelear con caché de assets) y verificá el badge de color.

### Ejercicio 2 — Provocar el error de "olvidé registrar el asset"
1. Comentá temporalmente la línea del `.js` (no la del `.xml`) dentro de `assets` en el manifest.
2. Actualizá el módulo y recargá la página con el campo `state_badge` — abrí la consola del navegador (F12) y confirmá el tipo de error que aparece (típicamente, el widget no se encuentra registrado).
3. Volvé a agregar la línea y confirmá que se soluciona.

### Ejercicio 3 — Inspeccionar `standardFieldProps` en el código fuente
1. Localizá el archivo `standard_field_props.js` dentro del código fuente de Odoo (carpeta `addons/web/static/src/views/fields/`).
2. Identificá qué props exactas define (más allá de `record` y `name`).
3. Agregá al componente `StateBadge` una prop opcional propia, `readonly`, tomándola de `this.props.readonly` (ya viene incluida en `standardFieldProps`) y usala para, por ejemplo, aplicar una clase CSS distinta si el campo está en modo solo lectura.

### Ejercicio 4 — Widget en `web.assets_frontend`
1. Repetí el registro del mismo widget (o uno simplificado) pero declarándolo en `web.assets_frontend` en vez de `web.assets_backend`.
2. Intentá usarlo en la página pública `/propiedades` del día 17 (vas a necesitar renderizarlo dentro de una plantilla que monte OWL, lo cual es más avanzado — si no llegás a integrarlo completo, al menos confirmá en la consola del navegador que el bundle `web.assets_frontend` efectivamente incluye tu archivo tras actualizar el módulo).

### Ejercicio 5 — Reto: tooltip con la fecha de disponibilidad
Agregá un atributo `title` (tooltip HTML nativo del navegador) al `<span>` del template, mostrando la fecha de disponibilidad de la propiedad al pasar el mouse sobre el badge. Vas a necesitar acceder a otro campo del mismo registro desde el componente (`this.props.record.data.date_availability`) y formatearlo como string legible.

---

## Preguntas de repaso conceptual

1. ¿Por qué OWL separa la lógica (`.js`) del template (`.xml`) en archivos distintos, en vez de mezclarlos como JSX?
2. ¿Qué hace exactamente `registry.category("fields").add(...)`, y por qué le permite a Odoo "descubrir" tu widget sin configuración adicional del core?
3. ¿Qué te garantiza extender tus props con `...standardFieldProps`?
4. Si creaste un archivo `.js` de un widget pero no lo declaraste en `assets` del manifest, ¿qué vas a observar al intentar usarlo?
5. ¿Cuál es la diferencia de propósito entre el bundle `web.assets_backend` y `web.assets_frontend`?

<details>
<summary>Ver respuestas</summary>

1. Es una decisión de consistencia con el resto del ecosistema de Odoo (QWeb ya se usa en reportes y website con esa misma separación markup/lógica), y facilita que el motor de templates procese el XML de forma independiente del bundling del JS.
2. Registra tu componente bajo un nombre string en un registro central (`registry`) que el sistema de vistas consulta dinámicamente al encontrar `widget="nombre"` en cualquier XML — el core de Odoo no necesita conocer tu módulo de antemano, solo sabe consultar ese registro por nombre en tiempo de ejecución.
3. Que tu componente reciba y exponga las props mínimas que cualquier widget de campo necesita (`record`, `name`, y las demás del contrato estándar), garantizando compatibilidad con cómo el sistema de vistas invoca a los widgets.
4. El widget no se va a registrar en el cliente — al intentar usarlo, la consola del navegador va a mostrar un error de que el widget/componente no se encuentra.
5. `web.assets_backend` es para JS/CSS que corre en la interfaz administrativa (backend); `web.assets_frontend` es para lo que corre en las páginas públicas del sitio web — son bundles separados que se cargan en contextos distintos.

</details>

## Checklist de cierre
- [ ] Sé dónde se registra un widget de campo (`registry.category("fields")`).
- [ ] Entiendo por qué el template va en un XML separado y no inline en el JS.
- [ ] Provoqué el error de asset no declarado y lo corregí.
- [ ] Sé qué bundle corresponde a widgets del backend vs del frontend.
