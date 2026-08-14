# De 0 a Pro: Odoo 18 Developer en 30 Días

Guía de estudio intensiva para pasar de "sabe programar" a "puede desarrollar módulos Odoo 18 en producción" en 30 días de práctica dirigida.

> El contenido real de cada día (teoría, código y ejercicios) está en [`dias/`](./dias/) — un archivo por día. Este documento es el mapa; cada `dias/dia-XX-*.md` es el material de estudio de ese día puntual.

## Perfil de partida

- Ya programás: conocés Python, POO, algo de HTML/XML y SQL.
- Nunca tocaste Odoo: no conocés el ORM, la estructura de módulos ni el ciclo de vida de una instalación.
- Dedicación sugerida: 2 a 3 horas por día. Los fines de semana de cada semana (días 7, 14, 21) son de repaso e integración, no de contenido nuevo.

## Base técnica de esta guía

- **Odoo 18 Community** (los conceptos aplican igual a Enterprise, salvo los módulos privativos).
- **Python 3.11+**, **PostgreSQL 15+**.
- Entorno recomendado: **Docker + docker-compose** para no ensuciar el sistema, editor **VSCode** con la extensión "Odoo IDE" o "Odoo Snippets".

## Proyecto integrador

Todo el contenido técnico se practica construyendo, en capas, un mismo módulo: **`gestion_inmobiliaria`** (gestión de propiedades en venta, ofertas y agentes). Es un dominio simple de modelar pero suficientemente rico para tocar relaciones, estados, seguridad, reportes, wizards y API externa — el mismo patrón que usa el tutorial oficial de desarrollo de Odoo con su módulo "Inmobiliaria".

Al día 30 vas a tener un módulo instalable, con seguridad, reportes, vista Kanban, un endpoint externo y tests, apto para mostrar como portafolio.

---

## Semana 1 — Fundamentos y ORM básico (Días 1-7)

### Día 1 — Arquitectura de Odoo y entorno de desarrollo

- **Temas**: modelo cliente-servidor de Odoo, rol del ORM, qué es un addon/módulo, PostgreSQL como única base de datos soportada, estructura de carpetas del código fuente de Odoo (`odoo/`, `addons/`, `odoo-bin`).
- **Práctica**: levantar Odoo 18 con Docker Compose (imagen `odoo:18` + `postgres:15`), crear tu primera base de datos desde el asistente web, explorar 2-3 apps instaladas (Contactos, Ventas) para reconocer el patrón Vista Lista / Formulario / Búsqueda.
- **Comandos clave**:
  ```bash
  docker compose up -d
  # o, corriendo desde el source de Odoo:
  ./odoo-bin --addons-path=addons -d midb --dev=all
  ```
- **Entregable**: instancia corriendo en `http://localhost:8069`, base de datos creada, usuario admin funcionando.

### Día 2 — Anatomía de un módulo

- **Temas**: `__manifest__.py` (name, version, depends, data, installable), convención de carpetas (`models/`, `views/`, `security/`, `data/`, `wizard/`, `report/`), qué hace `__init__.py` en cada nivel, ciclo instalar/actualizar.
- **Práctica**: generar el esqueleto del módulo con el scaffold de Odoo e instalarlo.
  ```bash
  ./odoo-bin scaffold gestion_inmobiliaria addons/
  ./odoo-bin -d midb -i gestion_inmobiliaria --stop-after-init
  ```
- **Entregable**: módulo visible e instalado en Apps (sin funcionalidad todavía).

### Día 3 — ORM: modelos y campos básicos

- **Temas**: `models.Model`, atributos `_name` y `_description`, tipos de campo base (`Char`, `Text`, `Integer`, `Float`, `Boolean`, `Date`, `Datetime`, `Selection`), campos implícitos (`id`, `create_date`, `write_date`, `create_uid`).
- **Práctica**: crear `inmueble.property` con campos: nombre, descripción, fecha de disponibilidad, precio esperado, superficie, orientación de jardín (Selection), estado.
- **Entregable**: modelo cargado y verificable desde `odoo shell`.
  ```python
  env['inmueble.property'].create({'name': 'Casa de prueba', 'expected_price': 150000})
  ```

### Día 4 — Vistas: Form, List, Search, acciones y menús

- **Temas**: `ir.ui.view` (arch XML), `ir.actions.act_window`, `ir.ui.menu`, jerarquía de menús, cómo Odoo resuelve qué vista mostrar.
- **Práctica**: vista formulario y vista lista para `inmueble.property`, acción de ventana y menú de nivel superior + submenú.
- **Entregable**: CRUD completo funcionando desde la interfaz web (crear, editar, listar, eliminar propiedades).

### Día 5 — Relaciones entre modelos

- **Temas**: `Many2one`, `One2many`, `Many2many`, campo `related`, opciones comunes (`ondelete`, `domain`, `context`, `string`).
- **Práctica**: modelos `inmueble.property.type` (tipo de inmueble) y `inmueble.property.tag` (etiquetas tipo "Lujo", "Renovado"), relacionados con `inmueble.property`. Agregar widget `many2many_tags` en la vista.
- **Entregable**: una propiedad con tipo asignado y varias etiquetas, visibles y editables desde el formulario.

### Día 6 — Seguridad: grupos, ACL y record rules

- **Temas**: `ir.model.access.csv` (permisos CRUD por modelo y grupo), `res.groups`, categorías de seguridad, `ir.rule` (reglas a nivel de fila) y su diferencia con los ACL.
- **Práctica**: crear grupo "Agente Inmobiliario" (solo ve sus propias propiedades) y "Gerente Inmobiliario" (ve todas). Aplicar una `ir.rule` con dominio sobre `user_id`.
- **Entregable**: probar con dos usuarios distintos que la seguridad efectivamente filtra los registros.

### Día 7 — Integración y repaso semana 1

- **Práctica**: pulir el módulo: agregar breadcrumbs correctos, un smart button contador ("N ofertas") aunque todavía no exista el modelo de ofertas (dejalo como TODO), revisar que el manifest declare bien las dependencias (`base`, `mail`).
- **Checklist de repaso**: ¿podés explicar la diferencia entre ACL y record rule? ¿Sabés qué pasa si actualizás un módulo sin cambiar la vista? ¿Entendés por qué el orden en `data` del manifest importa?
- **Recursos**: documentación oficial — sección "Tutorials: Getting started" en `odoo.com/documentation/18.0`.

---

## Semana 2 — Lógica de negocio y ORM avanzado (Días 8-14)

### Día 8 — Campos computados y related

- **Temas**: `@api.depends`, `compute=`, `store=True/False`, diferencia entre campo `related` y campo `compute` que lee un `related`, cuándo conviene `store`.
- **Práctica**: campo computado "superficie total" (superficie construida + superficie de jardín) en `inmueble.property`.

### Día 9 — Validaciones: constrains y onchange

- **Temas**: `@api.constrains` + `ValidationError`, `@api.onchange` + `UserError`, diferencia entre validar en Python vs `_sql_constraints`.
- **Práctica**: constraint que impide precio de venta negativo; onchange que sugiere el precio mínimo aceptable al setear el tipo de propiedad.

### Día 10 — Métodos ORM avanzados

- **Temas**: `search`, `search_read`, `search_count`, `browse`, `filtered`, `mapped`, `sorted`, operaciones batch (`create` con lista de diccionarios, `write` sobre recordsets), `sudo()`, `with_context()`, `with_user()`.
- **Práctica**: método que, dado un recordset de propiedades, devuelva solo las disponibles ordenadas por precio usando `filtered` + `sorted` en vez de queries manuales.

### Día 11 — Herencia de modelos y vistas

- **Temas**: herencia clásica (`_inherit` sin `_name` nuevo) vs herencia por delegación (`_inherits`), extensión de vistas con XPath (`position="after"`, `"inside"`, `"replace"`).
- **Práctica**: extender `res.partner` para mostrar, en su formulario, un smart button con las propiedades donde ese contacto es comprador.

### Día 12 — Wizards y acciones de servidor

- **Temas**: `models.TransientModel`, ciclo de vida de un wizard, botones que invocan `ir.actions.act_window` con `target="new"`, `ir.actions.server`.
- **Práctica**: wizard "Aceptar oferta" que, al confirmarse, marca la oferta como aceptada y las demás como rechazadas, y cambia el estado de la propiedad.

### Día 13 — Automatización, mail y actividades

- **Temas**: `ir.cron` (tareas programadas), `mail.thread` y `mail.activity.mixin` (chatter, seguidores, actividades), plantillas de correo (`mail.template`).
- **Práctica**: al aceptar una oferta, registrar un mensaje en el chatter de la propiedad y crear una actividad de seguimiento para el agente.

### Día 14 — Máquina de estados y repaso semana 2

- **Temas**: patrón de campo `state` (Selection) + botones que disparan transiciones, atributos `invisible`/`readonly` condicionados por estado en la vista.
- **Práctica**: flujo completo `Nuevo → Oferta Recibida → Oferta Aceptada → Vendido` (con `Cancelado` como salida alternativa), botones visibles solo en el estado correspondiente.
- **Checklist de repaso**: ¿podés explicar cuándo usar `_inherit` vs `_inherits`? ¿Sabés por qué un wizard no persiste datos salvo que vos los escribas explícitamente en otro modelo?

---

## Semana 3 — Frontend, reportes e integraciones (Días 15-21)

### Día 15 — QWeb y reportes PDF

- **Temas**: `ir.actions.report`, motor de plantillas QWeb, directivas (`t-field`, `t-esc`, `t-if`, `t-foreach`), diferencia entre reporte QWeb-HTML y QWeb-PDF (wkhtmltopdf).
- **Práctica**: reporte "Ficha de propiedad" imprimible en PDF con foto, precio y características.

### Día 16 — Vistas avanzadas

- **Temas**: vistas Kanban, Calendar, Graph y Pivot; decoraciones condicionales (`decoration-danger`, etc.); widgets de campo más usados (`priority`, `statusbar`, `many2many_tags`).
- **Práctica**: vista Kanban de propiedades agrupada por estado, con tarjeta mostrando precio y etiquetas.

### Día 17 — Website y Portal

- **Temas**: controladores HTTP (`@http.route`), plantillas QWeb de sitio web (`website.layout`), diferencia entre página pública y portal de cliente autenticado.
- **Práctica**: página pública `/propiedades` que liste las propiedades disponibles leyendo del ORM.

### Día 18 — OWL: el framework JS de Odoo

- **Temas**: componentes OWL (`Component`, `useState`, templates XML separados), cómo se registran widgets de campo personalizados en el registry de campos.
- **Práctica**: widget de campo simple que muestre un badge de color según el estado de la propiedad.

### Día 19 — APIs externas: XML-RPC / JSON-RPC / REST

- **Temas**: autenticación externa (`common.authenticate`), llamadas `execute_kw` vía XML-RPC, exponer un endpoint propio con `@http.route(type="json"/"http", auth="...")`.
- **Práctica**: script Python externo (fuera de Odoo) que se conecta por XML-RPC y crea una propiedad.

### Día 20 — Import/Export de datos y data files

- **Temas**: archivos de datos XML/CSV, atributo `noupdate`, datos de demo vs datos de configuración, `external ids` (`ir.model.data`) y por qué son la base de la portabilidad de un módulo.
- **Práctica**: cargar datos iniciales de tipos de propiedad vía XML, y probar la importación de propiedades desde un CSV por la UI.

### Día 21 — Repaso e integración semana 3

- **Práctica**: dejar el módulo con reporte PDF, vista Kanban, página pública y endpoint externo funcionando juntos; revisar que el manifest declare `assets` si agregaste JS/CSS propios.
- **Checklist de repaso**: ¿entendés la diferencia entre `auth="public"`, `"user"` y `"none"` en un controlador? ¿Sabés por qué QWeb de reportes y QWeb de website comparten motor pero no todos los mismos helpers?

---

## Semana 4 — Calidad, performance y profesionalización (Días 22-30)

### Día 22 — Testing

- **Temas**: `TransactionCase` para tests de lógica, `HttpCase` para tests que necesitan HTTP, tours en JS para flujos de UI end-to-end, filtrado con `--test-tags`.
- **Práctica**: tests unitarios que cubran la creación de una propiedad, la validación del constraint de precio y el flujo de aceptar oferta.
  ```bash
  ./odoo-bin -d midb --test-tags /gestion_inmobiliaria --stop-after-init
  ```

### Día 23 — Performance y buenas prácticas ORM

- **Temas**: problema N+1 y cómo el prefetch del ORM lo mitiga, `read_group` para agregaciones eficientes, `index=True` en campos usados para filtrar/ordenar, `_sql_constraints` vs constraints en Python (costo).
- **Práctica**: detectar y corregir un bucle que hace `search` dentro de un `for`, reemplazándolo por una sola consulta batch.

### Día 24 — Multi-compañía y multi-moneda

- **Temas**: campo `company_id` y reglas multi-company implícitas, campos monetarios (`Monetary` + `res.currency`), cómo Odoo aísla datos entre compañías.
- **Práctica**: agregar `company_id` a `inmueble.property` y validar el aislamiento con dos compañías.

### Día 25 — Migraciones y actualizaciones de versión

- **Temas**: scripts de migración (`migrations/<version>/pre-*.py`, `post-*.py`, `end-*.py`), qué cambia estructuralmente entre versiones mayores de Odoo, el proyecto OpenUpgrade como referencia.
- **Práctica**: escribir un script `post-migration` de ejemplo que renombre un campo antiguo a uno nuevo sin perder datos.

### Día 26 — Deployment y producción

- **Temas**: `odoo.conf` (workers, `proxy_mode`, límites de memoria/CPU por worker), Nginx como proxy inverso y terminador SSL, estrategia de backup (base de datos + filestore).
- **Práctica**: armar un `docker-compose` de producción con Odoo + PostgreSQL + Nginx delante.

### Día 27 — Calidad de código y flujo de trabajo

- **Temas**: linters específicos de Odoo (`pylint-odoo`), formateo con `ruff`/`black`, hooks de `pre-commit`, convenciones de commits y PRs que usa la comunidad OCA.
- **Práctica**: configurar `pre-commit` en el repo del módulo y limpiar los warnings que reporte sobre tu código de las semanas anteriores.

### Día 28 — Ecosistema OCA y módulos de terceros

- **Temas**: qué es la Odoo Community Association (OCA), cómo está organizado su GitHub (`github.com/OCA`), cómo leer y adaptar un módulo de terceros sin romperlo, cómo instalar un módulo OCA en tu entorno.
- **Práctica**: clonar un repositorio OCA relevante a tu dominio, instalar un módulo y leer su código para identificar los patrones vistos en las semanas 1-3.

### Día 29 — Portafolio y preparación de certificación

- **Temas**: qué evalúa la certificación técnica de Odoo, cómo documentar un módulo para portafolio (README con capturas, GIF o video corto de la demo).
- **Práctica**: escribir el README de `gestion_inmobiliaria`, subir el módulo a un repositorio público en GitHub.

### Día 30 — Proyecto final y plan de crecimiento continuo

- **Práctica**: demo completa de punta a punta del módulo (crear propiedad → recibir ofertas → aceptar oferta → chatter/actividad → reporte PDF → endpoint externo). Checklist final "¿está listo para producción?" (seguridad revisada, tests pasando, sin `print()` de debug, manifest correcto).
- **Plan post-30-días**: elegir una especialización (Accounting, Manufacturing, Inventory, POS o Website/eCommerce) y profundizar leyendo el código fuente de ese módulo core de Odoo — es la mejor fuente de patrones avanzados.
- **Comunidad para seguir aprendiendo**: documentación oficial (`odoo.com/documentation`), foro oficial (`odoo.com/forum`), código fuente y issues (`github.com/odoo/odoo`), Runbot para ver builds e instancias de prueba (`runbot.odoo.com`), OCA (`github.com/OCA`).

---

## Apéndice: chuleta de comandos

```bash
# Instalar un módulo
./odoo-bin -d midb -i nombre_modulo --stop-after-init

# Actualizar un módulo tras cambios
./odoo-bin -d midb -u nombre_modulo --stop-after-init

# Modo desarrollo (autoreload, assets sin minificar, qweb sin cache)
./odoo-bin -d midb --dev=all

# Consola interactiva con el entorno cargado
./odoo-bin shell -d midb

# Correr tests de un módulo
./odoo-bin -d midb --test-tags /nombre_modulo --stop-after-init

# Crear el esqueleto de un módulo nuevo
./odoo-bin scaffold nombre_modulo ruta/addons/
```

## Apéndice: estructura mínima de un módulo

```
gestion_inmobiliaria/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── inmueble_property.py
├── views/
│   └── inmueble_property_views.xml
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
├── data/
│   └── inmueble_data.xml
├── wizard/
│   ├── __init__.py
│   └── accept_offer_wizard.py
└── report/
    └── inmueble_property_report.xml
```
