# Día 25 — Migraciones y actualizaciones de versión

**Semana:** 4 — Calidad, performance y profesionalización
**Duración estimada:** 3–4 h

## Objetivo del día
Escribir un script de migración post-actualización, y entender por qué hace falta un mecanismo separado del código normal del módulo.

---

## Conceptos de Odoo

### El problema que resuelven las migraciones
Cuando actualizás tu módulo (`-u`), Odoo compara tu código actual contra el estado de la base de datos y ajusta el esquema automáticamente en muchos casos (agregar una columna nueva, por ejemplo, es automático). Pero hay cambios que Odoo **no puede inferir solo**: si renombrás un campo, Odoo ve "un campo viejo desaparecido" y "un campo nuevo aparecido" como dos eventos no relacionados — no sabe que en realidad querías preservar los datos del viejo en el nuevo. Ahí es donde entra un script de migración: código explícito que vos escribís para manejar esa transición de datos que el framework no puede adivinar.

### Los tres momentos: `pre`, `post`, `end`
- **`pre-migrate.py`**: corre **antes** de que Odoo sincronice el nuevo esquema de tu módulo con la base de datos. En este punto, la tabla todavía tiene la estructura **vieja** — por eso solo tenés `cr` (el cursor de base de datos crudo) disponible, y trabajás con SQL directo, no con el ORM (los modelos Python ya reflejan la definición *nueva*, que todavía no existe en la tabla).
- **`post-migrate.py`**: corre **después** de que el esquema ya se sincronizó (las columnas nuevas ya existen, las eliminadas ya se fueron). Acá sí podés construir un `env` completo y usar el ORM normalmente.
- **`end-migrate.py`**: corre al final de **todo** el proceso de actualización (después de que todos los módulos terminaron su propia migración), útil para ajustes que dependen de que otros módulos también hayan terminado de migrar.

### Por qué `pre-migrate` no tiene acceso al ORM completo
El ORM de Odoo construye su modelo en memoria a partir de las clases Python actuales — en el momento de `pre-migrate`, esas clases ya reflejan la versión **nueva** del código, pero la base de datos todavía tiene el esquema **viejo**. Si intentaras usar `env["mi.modelo"]` ahí, el ORM esperaría columnas que todavía no existen. Por eso `pre-migrate` trabaja con SQL crudo vía `cr.execute(...)`, que no depende de que el esquema Python y el de la base coincidan.

### La carpeta y el nombre de versión importan
Los scripts van en `migrations/<version>/`, donde `<version>` tiene que **coincidir exactamente** con el valor de `version` en el manifest en el momento en que Odoo detecta que está actualizando **hacia** esa versión (compara la versión instalada actualmente contra la del manifest). Si tu manifest dice `18.0.2.0.0` pero tu carpeta se llama `18.0.2.0.1`, el script simplemente no se ejecuta — sin error visible, solo silencio.

### OpenUpgrade: migraciones entre versiones *mayores* de Odoo
Todo lo anterior es para migraciones **dentro de tu propio módulo** (mismo Odoo, distintas versiones de tu módulo). Migrar de Odoo 17 a Odoo 18 (cambios en el core mismo) es un problema mucho más grande, que el proyecto comunitario **OpenUpgrade** aborda con scripts de migración para los módulos core de Odoo entre versiones mayores — vale la pena conocerlo aunque hoy no lo uses directamente.

---

## Ejercicios prácticos

### Ejercicio 1 — Script post-migration (guiado)

`migrations/18.0.2.0.0/post-migrate.py`:
```python
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    properties = env["inmueble.property"].search([("garden_area", "=", 0), ("garden", "=", True)])
    properties.write({"garden_area": 10})
```
Subí la versión del manifest a `18.0.2.0.0`, creá la carpeta con este script, actualizá el módulo, y confirmá en el log que corrió.

### Ejercicio 2 — Provocar el "silencio" de una versión mal nombrada
1. Renombrá la carpeta a `18.0.2.0.1` (sin cambiar el manifest, que sigue en `18.0.2.0.0`).
2. Modificá el script para que haga algo fácilmente verificable (por ejemplo, escribir un valor obviamente distinto).
3. Actualizá el módulo y confirmá que el script **no corrió** — sin ningún error visible, simplemente no pasó nada.
4. Corregí el nombre de la carpeta de vuelta y confirmá que ahora sí corre.

### Ejercicio 3 — Simular un `pre-migrate` real
1. Simulá el caso de "renombrar un campo": agregá un campo nuevo `total_bedrooms` a `inmueble.property` (como sinónimo intencional de `bedrooms`, para el ejercicio).
2. Escribí `migrations/18.0.3.0.0/pre-migrate.py` que copie el valor de la columna vieja a la nueva usando SQL crudo:
   ```python
   def migrate(cr, version):
       cr.execute("UPDATE inmueble_property SET total_bedrooms = bedrooms")
   ```
3. Subí la versión del manifest a `18.0.3.0.0`, actualizá, y confirmá que los valores se copiaron correctamente antes de que la lógica normal del módulo tocara esos datos.
4. Revertí este cambio de prueba (no lo necesitás en el módulo final) dejando la versión y los campos como estaban.

### Ejercicio 4 — Diferencia observable entre `pre` y `post`
1. En el mismo script de migración de prueba del ejercicio 3, intentá agregar también un `env["inmueble.property"].search([])` dentro del `pre-migrate.py` (usando el ORM, no SQL crudo).
2. Corré la migración y observá el error — confirmá que efectivamente falla o se comporta mal, porque en ese punto el esquema todavía no está sincronizado con las clases Python actuales.
3. Mové esa misma línea a un `post-migrate.py` en la misma carpeta de versión, y confirmá que ahí sí funciona sin problema.

### Ejercicio 5 — Reto: investigar OpenUpgrade
- Buscá el repositorio de OpenUpgrade y ubicá, dentro de su estructura, un script de migración real para algún módulo core de Odoo entre dos versiones mayores (por ejemplo, un cambio de campo en `sale` o `account` entre dos versiones).
- Leélo y compará su estructura contra los scripts que escribiste hoy — identificá qué patrones se repiten (uso de `cr.execute`, manejo de columnas renombradas, etc.).

---

## Preguntas de repaso conceptual

1. ¿Qué tipo de cambio en tu módulo requiere necesariamente un script de migración, en vez de confiar en que Odoo lo detecte solo al actualizar?
2. ¿Por qué `pre-migrate.py` no puede usar el ORM normal (`env["modelo"]`) de forma confiable?
3. ¿Qué diferencia de timing hay entre `post-migrate.py` y `end-migrate.py`?
4. Si el nombre de la carpeta de migración no coincide exactamente con la versión del manifest, ¿qué pasa al actualizar el módulo?
5. ¿Qué problema resuelve OpenUpgrade que tus propios scripts de migración de módulo no resuelven?

<details>
<summary>Ver respuestas</summary>

1. Cambios donde Odoo no puede inferir la intención automáticamente a partir de la comparación de esquemas — típicamente renombrar un campo (Odoo lo ve como "uno desaparecido, otro nuevo", no como una migración de datos), o transformaciones de datos que dependen de lógica de negocio.
2. Porque en ese punto la base de datos todavía tiene el esquema **viejo**, mientras que las clases Python ya reflejan el esquema **nuevo** — usar el ORM ahí generaría inconsistencias, porque esperaría columnas que todavía no existen en la tabla real.
3. `post-migrate.py` corre después de que el esquema de **ese módulo específico** ya se sincronizó; `end-migrate.py` corre después de que **todos** los módulos de la actualización completa terminaron su propia migración — útil para ajustes que dependen de que otros módulos también hayan terminado.
4. El script simplemente no se ejecuta, sin ningún error visible — Odoo solo corre los scripts de la carpeta cuyo nombre coincide exactamente con la versión detectada en el manifest.
5. Resuelve migraciones de datos y esquema para los módulos **core** de Odoo entre versiones **mayores** del propio Odoo (por ejemplo, de 17 a 18) — un problema mucho más grande que migrar tu propio módulo entre sus propias versiones internas.

</details>

## Checklist de cierre
- [ ] Sé la diferencia entre lo que podés hacer en `pre-migrate` vs `post-migrate`, y lo comprobé provocando el error.
- [ ] Entiendo por qué la versión del manifest tiene que coincidir exactamente con el nombre de la carpeta.
- [ ] Provoqué y observé el "silencio" de una migración con nombre de carpeta incorrecto.
- [ ] Ubiqué un ejemplo real de migración en el repositorio de OpenUpgrade.
