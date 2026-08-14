# Día 28 — Ecosistema OCA y módulos de terceros

**Semana:** 4 — Calidad, performance y profesionalización
**Duración estimada:** 2–3 h

## Objetivo del día
Leer código de producción real, no solo tutoriales, y saber dónde buscar antes de reinventar algo.

---

## Conceptos de Odoo

### Qué es la OCA y por qué existe
La **Odoo Community Association** es una organización sin fines de lucro que coordina el desarrollo colaborativo de módulos open source para Odoo, mantenidos por una comunidad de partners y desarrolladores independientes (no por Odoo S.A., la empresa). Existe porque muchas necesidades son comunes a cientos de implementaciones distintas (reportes financieros específicos de un país, integraciones con transportistas, utilidades técnicas) — en vez de que cada consultora reinvente lo mismo, la OCA centraliza y mantiene esas soluciones con estándares de calidad compartidos.

### Organización por repositorio y por rama
GitHub de la OCA (`github.com/OCA`) no es un monorepo — está organizado en **decenas de repositorios separados por área funcional** (utilidades de servidor, temas de reportes, herramientas de inventario, etc.), y cada repositorio mantiene **una rama por versión de Odoo** (`18.0`, `17.0`, etc.), porque el código de un módulo casi siempre necesita ajustes entre versiones mayores de Odoo (recordá el cambio `tree` → `list` del día 4, por ejemplo).

### Por qué leer código OCA es distinto de leer un tutorial
Un tutorial (como esta misma guía) simplifica deliberadamente para enseñar un concepto a la vez. Código OCA real está optimizado para producción: maneja casos borde, tiene tests, respeta convenciones de commit y de PR revisadas por otros desarrolladores, y a menudo expone patrones que no aparecen en ningún tutorial porque solo emergen de resolver problemas reales repetidamente (mixins reutilizables, abstracciones para evitar duplicación entre módulos relacionados del mismo repositorio, etc.).

### Antes de escribir algo desde cero
Una pregunta que vale la pena hacerse sistemáticamente antes de implementar una funcionalidad no trivial: "¿esto ya lo resolvió alguien de forma robusta?" Buscar en OCA primero no es solo ahorro de tiempo — un módulo con años de uso en producción real y múltiples contribuyentes probablemente maneja casos borde que vos ni habías considerado.

---

## Ejercicios prácticos

### Ejercicio 1 — Clonar e instalar un módulo OCA (guiado)
1. Elegí un repositorio OCA relacionado a algo que te interese (por ejemplo `server-tools` para utilidades generales, o `reporting-engine` para reportes).
2. Cloná la rama `18.0`:
   ```bash
   git clone https://github.com/OCA/<repo> --branch 18.0 --depth 1
   ```
3. Instalá un módulo pequeño de ese repo en tu entorno local (agregando la carpeta a tu `addons_path`).
4. Confirmá que instala sin errores y explorá su funcionalidad desde la UI.

### Ejercicio 2 — Identificar patrones ya conocidos
Leyendo el código del módulo que instalaste, encontrá y anotá al menos un ejemplo concreto de cada uno de estos patrones vistos en semanas anteriores:
- [ ] Un ACL en `ir.model.access.csv` (día 6).
- [ ] Una herencia con `_inherit` (día 11).
- [ ] Un campo computado con `@api.depends` (día 8).
- [ ] Una vista heredada con XPath (día 11).

### Ejercicio 3 — Comparar la calidad de un manifest OCA contra el tuyo
1. Abrí el `__manifest__.py` del módulo OCA que elegiste.
2. Compará su estructura contra la de `gestion_inmobiliaria`: ¿qué claves adicionales tiene que vos no usaste (`license`, `maintainers`, `development_status`, `website`)?
3. Agregá al menos 2 de esas claves faltantes a tu propio manifest, siguiendo el mismo estilo.

### Ejercicio 4 — Leer el CONTRIBUTING o README del repositorio
1. Leé el archivo `README.rst` o `CONTRIBUTING.md` del repositorio que clonaste.
2. Identificá: ¿qué convención de branch usan?, ¿qué se espera en un Pull Request?, ¿corren tests automáticos (CI) sobre cada contribución?
3. Anotá 2-3 diferencias entre ese flujo de trabajo formal y cómo trabajaste vos hasta ahora en este curso.

### Ejercicio 5 — Reto: patrón nuevo, no visto en esta guía
Encontrá, dentro del módulo que instalaste, un patrón que **no** hayas visto en esta guía — por ejemplo:
- Un mixin reutilizable (una clase abstracta pensada para que otros modelos la incluyan).
- `_sql_constraints` combinado con `@api.constrains` para la misma regla, cubriendo tanto el caso de importaciones masivas como el de la UI.
- Un uso avanzado de `read_group` o `_read_group` que no viste el día 23.

Escribí, en tus propias palabras, qué problema resuelve ese patrón y por qué lo eligieron en vez de una alternativa más simple.

---

## Preguntas de repaso conceptual

1. ¿Qué es la OCA, y en qué se diferencia de Odoo S.A. (la empresa que desarrolla el core de Odoo)?
2. ¿Por qué el GitHub de la OCA está organizado en múltiples repositorios en vez de uno solo?
3. ¿Por qué cada repositorio OCA mantiene una rama separada por versión de Odoo?
4. ¿Qué ventaja tiene leer código OCA de producción frente a solo seguir tutoriales?
5. Antes de implementar una funcionalidad no trivial desde cero, ¿qué pregunta vale la pena hacerse primero?

<details>
<summary>Ver respuestas</summary>

1. La OCA es una organización sin fines de lucro que coordina desarrollo colaborativo de módulos open source mantenidos por la comunidad (partners y desarrolladores independientes); Odoo S.A. es la empresa que desarrolla y vende el core de Odoo (Community y Enterprise) — son entidades distintas con propósitos distintos.
2. Porque agrupa módulos por área funcional, facilitando que cada equipo/consultora dependa solo de los repositorios relevantes a su trabajo, en vez de tener que clonar un monorepo gigante con todo mezclado.
3. Porque el código de un módulo frecuentemente necesita ajustes de sintaxis y API entre versiones mayores de Odoo (como el cambio `tree` → `list` en la 18), por lo que el mismo módulo no puede ser compatible con múltiples versiones sin adaptaciones.
4. Código real de producción maneja casos borde, tiene tests, y expone patrones que solo emergen de resolver problemas reales repetidamente — algo que un tutorial simplifica deliberadamente para enseñar un concepto a la vez.
5. Si esa necesidad ya fue resuelta de forma robusta por la comunidad (buscando primero en OCA u otros módulos existentes), antes de invertir tiempo reinventando una solución que probablemente no maneje los mismos casos borde que una con años de uso real.

</details>

## Checklist de cierre
- [ ] Instalé y probé un módulo OCA real en mi entorno local.
- [ ] Identifiqué ejemplos concretos de 4 patrones ya conocidos dentro de código ajeno.
- [ ] Mejoré mi propio manifest comparándolo contra el de un módulo OCA.
- [ ] Encontré y expliqué con mis palabras un patrón nuevo no visto en esta guía.
