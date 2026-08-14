# Día 1 — Arquitectura de Odoo y entorno de desarrollo

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 3–4 h

## Objetivo del día
Entender qué pieza hace qué en Odoo, y tener una instancia propia corriendo.

---

## Conceptos de Odoo

### El modelo cliente-servidor
Odoo tiene dos mitades que hablan por HTTP/JSON-RPC:
- **Servidor**: proceso Python sobre Werkzeug. Ahí vive el ORM, la lógica de negocio, la seguridad y la generación de vistas/reportes.
- **Cliente web**: aplicación JavaScript (framework OWL) que corre en el navegador y renderiza lo que el servidor le manda.

Esto importa porque **toda regla de negocio real tiene que vivir en el servidor**. El cliente JS puede mejorar la experiencia (onchange, widgets), pero nunca es una barrera de seguridad ni de integridad de datos — cualquiera puede saltarse el cliente y hablar directo con el servidor (de hecho, eso es lo que vas a hacer el día 19 con XML-RPC).

### Qué es un módulo (addon), en serio
Un módulo no es "una carpeta con código": es una **unidad de despliegue autocontenida**. Declara de qué otros módulos depende (`depends`), y Odoo arma un grafo de dependencias para decidir el orden de instalación. Si tu módulo depende de `sale`, Odoo instala `sale` (y todo lo que `sale` necesite) antes que el tuyo, automáticamente.

### El ciclo de vida de un módulo
Cada módulo tiene un estado guardado en la tabla `ir.module.module`:
- `uninstalled` → nunca se instaló.
- `installed` → activo, cargando su código y datos.
- `to upgrade` → marcado para actualizar en el próximo `-u`.
- `to remove` → marcado para desinstalar.

Esto explica por qué **instalar** (`-i`) y **actualizar** (`-u`) son cosas distintas: `-i` solo corre una vez, la primera vez. Si editás un modelo o una vista después, necesitás `-u` para que Odoo vuelva a procesar esos archivos — `-i` sobre un módulo ya instalado no hace nada.

### Por qué PostgreSQL y no "cualquier base SQL"
El ORM de Odoo genera SQL pensado específicamente para PostgreSQL (secuencias para autoincrementar `id`, tipos de dato específicos, funciones propias de Postgres). No es una capa de abstracción multi-motor como Django ORM o SQLAlchemy — es Postgres o nada. Esto es una decisión de diseño, no una limitación temporal.

### Errores comunes de quien recién empieza
- Cambiar una vista XML y esperar que se refleje sola: **las vistas necesitan `-u`**, no se autorecargan ni con `--dev=all` (el autoreload de `--dev=all` es para código Python).
- Confundir la carpeta de `addons_path` con la carpeta donde uno está trabajando — si Odoo no encuentra tu módulo al instalar, primero revisá el `addons_path`.
- Pensar que "base de datos" y "módulo" son lo mismo: una base de datos es una instancia completa (con muchos módulos instalados adentro).

---

## Ejercicios prácticos

### Ejercicio 1 — Levantar el entorno (guiado)
1. Creá `docker-compose.yml`:
   ```yaml
   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_USER: odoo
         POSTGRES_PASSWORD: odoo
         POSTGRES_DB: postgres
       volumes:
         - odoo-db:/var/lib/postgresql/data
     odoo:
       image: odoo:18
       depends_on:
         - db
       ports:
         - "8069:8069"
       environment:
         HOST: db
         USER: odoo
         PASSWORD: odoo
       volumes:
         - odoo-addons:/mnt/extra-addons
   volumes:
     odoo-db:
     odoo-addons:
   ```
2. `docker compose up -d`
3. Abrí `http://localhost:8069`, creá la base `midb` **con datos de demo activados**.

### Ejercicio 2 — Modo desarrollador y exploración de modelos
1. Activá el modo desarrollador (`Ajustes → Activar el modo desarrollador`, o `/web?debug=1`).
2. Abrí un contacto existente (viene con los datos de demo), y desde `Ver → Ver Formulario` anotá el nombre técnico del modelo.
3. Repetí lo mismo con una moneda (`Contabilidad` o `Ajustes → Técnico → Monedas`) y con la compañía activa (`Ajustes → Empresas`). Anotá los 3 nombres técnicos (`res.partner`, `res.currency`, `res.company`).

### Ejercicio 3 — Diferencia entre instalar y actualizar
1. Instalá el módulo `base` explícitamente (aunque ya esté instalado, observá el mensaje):
   ```bash
   ./odoo-bin -d midb -i base --stop-after-init
   ```
2. Ahora actualizalo:
   ```bash
   ./odoo-bin -d midb -u base --stop-after-init
   ```
3. Comparé los logs de ambos comandos. ¿Ves alguna diferencia en qué se reprocesa?

### Ejercicio 4 — Primer contacto con `odoo shell`
1. Abrí una consola interactiva:
   ```bash
   ./odoo-bin shell -d midb
   ```
2. Ejecutá:
   ```python
   env["res.users"].browse(1).name
   env["res.partner"].search_count([])
   ```
3. Anotá qué devuelve cada línea y por qué (¿qué es el usuario con id 1?).

### Ejercicio 5 — Reto: instalar desde el código fuente
1. Cloná el repo y corré Odoo sin Docker:
   ```bash
   git clone https://github.com/odoo/odoo --branch 18.0 --depth 1
   ./odoo-bin --addons-path=addons -d midb2
   ```
2. Compará contra el enfoque Docker: ¿dónde quedan los logs?, ¿qué tan rápido arranca?, ¿cómo editás el código fuente de Odoo mismo si quisieras?

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia hay entre `-i` y `-u`, y por qué `-i` sobre un módulo ya instalado no hace nada?
2. ¿Por qué una regla de negocio escrita solo en JavaScript (cliente) no es una garantía de seguridad real?
3. ¿Qué información guarda la tabla `ir.module.module`?
4. ¿Por qué el ORM de Odoo no es portable a MySQL o SQL Server sin reescribir buena parte del framework?
5. Si editás una vista XML con el servidor corriendo en `--dev=all`, ¿se refleja el cambio solo? ¿Por qué sí o por qué no?

<details>
<summary>Ver respuestas</summary>

1. `-i` instala un módulo que no está en `ir.module.module` (o lo fuerza a reinstalar si lo borraste de ahí); una vez que el estado es `installed`, `-i` no vuelve a procesar sus archivos — para eso existe `-u`, que sí reprocesa modelos, vistas y datos.
2. Porque el cliente JS corre en la máquina del usuario, fuera de tu control — cualquiera puede llamar directamente al servidor (vía XML-RPC, por ejemplo) saltándose toda validación que solo exista en el navegador.
3. Guarda, por cada módulo conocido por esa base de datos, su nombre técnico, versión instalada, y estado (`uninstalled`, `installed`, `to upgrade`, `to remove`, etc.).
4. Porque genera SQL con features específicas de PostgreSQL (secuencias, tipos de dato, funciones propias) en vez de pasar por una capa de abstracción multi-motor.
5. Con `--dev=all` el código **Python** se autorecarga, pero las vistas XML no — necesitás correr `-u` explícitamente para que Odoo vuelva a leer y cargar el XML modificado.

</details>

## Checklist de cierre
- [ ] Puedo explicar qué hace el ORM y por qué vive en el servidor.
- [ ] Sé qué significan `-i`, `-u` y `--dev=all`, y en qué se diferencian.
- [ ] Tengo Odoo 18 corriendo localmente y pude entrar a `odoo shell`.
