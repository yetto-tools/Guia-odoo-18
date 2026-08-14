# Día 2 — Anatomía de un módulo

**Semana:** 1 — Fundamentos y ORM básico
**Duración estimada:** 3–4 h

## Objetivo del día
Crear el esqueleto del módulo `gestion_inmobiliaria` e instalarlo, vacío pero funcional.

---

## Conceptos de Odoo

### El manifest es el "contrato" del módulo
`__manifest__.py` es un diccionario Python que le dice a Odoo todo lo que necesita saber **antes** de tocar tu código: de qué depende, qué archivos cargar, y cómo mostrarse. Claves centrales:
- `name`, `summary`, `category` → metadata visible en Apps.
- `version` → formato `X.Y.z.a.b.c`, donde `X.Y` normalmente coincide con la versión de Odoo (`18.0`) y el resto es tu versionado propio del módulo (lo vas a usar el día 25 para migraciones).
- `depends` → lista de módulos requeridos. Odoo instala primero las dependencias, en orden topológico.
- `data` → archivos XML/CSV que se cargan **en orden**, al instalar o actualizar.
- `installable` → si es `False`, Odoo directamente ignora el módulo (útil para deshabilitar algo sin borrarlo).
- `application` → si es `True`, aparece en el launcher de Apps con ícono propio; si es `False`, es un módulo "técnico" que no se autoinstala visible.

### Por qué el orden en `data` importa
Los archivos se procesan secuencialmente. Si tu vista de seguridad referencia un grupo que se define en un archivo que va **después** en la lista, la carga falla con un error de referencia no encontrada. La convención (y la que vas a seguir en este curso) es: seguridad primero, después vistas, después datos de demo/configuración, después reportes.

### La cadena de `__init__.py`
Hay dos niveles:
- El `__init__.py` de la **raíz** del módulo importa el paquete `models` (y luego `wizard`, `controllers`, etc. a medida que los agregues).
- El `__init__.py` de **cada subcarpeta** (`models/`, `wizard/`...) importa cada archivo `.py` individual.

Si olvidás agregar una línea de import en cualquiera de los dos niveles, la clase existe en el archivo pero Odoo nunca la carga — es el error de principiante más común ("¿por qué mi modelo no aparece?").

### Instalable vs. Aplicación
Un módulo puede ser `installable=True, application=False` (por ejemplo, un módulo técnico que solo agrega un campo a otro modelo) o `installable=True, application=True` (un módulo con entidad propia, como el tuyo). No todo lo que instalás necesita ser una "app" visible.

---

## Ejercicios prácticos

### Ejercicio 1 — Generar y limpiar el esqueleto (guiado)
1. ```bash
   ./odoo-bin scaffold gestion_inmobiliaria addons/
   ```
2. Reemplazar el manifest generado por:
   ```python
   {
       "name": "Gestión Inmobiliaria",
       "version": "18.0.1.0.0",
       "category": "Inmobiliaria",
       "summary": "Gestión de propiedades, ofertas y agentes",
       "depends": ["base", "mail"],
       "data": [],
       "installable": True,
       "application": True,
   }
   ```
3. Borrar el modelo de ejemplo que trae el scaffold y dejar `models/__init__.py` vacío.
4. Instalar:
   ```bash
   ./odoo-bin -d midb -i gestion_inmobiliaria --stop-after-init
   ```
5. Verificar en `Ajustes → Apps` que aparece instalado.

### Ejercicio 2 — Provocar el error de "olvidé el import"
1. Creá un archivo `models/dummy.py` con un modelo trivial (`_name = "inmueble.dummy"`, un campo `name`).
2. **No lo importes** desde `models/__init__.py`.
3. Actualizá el módulo y, desde `odoo shell`, intentá `env["inmueble.dummy"]`. Confirmá el `KeyError`.
4. Ahora agregá el import faltante, actualizá de nuevo, y repetí el `env["inmueble.dummy"]` — debería funcionar. Borrá el archivo dummy al terminar.

### Ejercicio 3 — Provocar el error de orden en `data`
1. Creá un archivo de seguridad mínimo que referencie un grupo con `ref="algun_grupo_inexistente_todavia"`.
2. Ponelo en `data` **antes** de que el grupo esté definido en otro archivo.
3. Actualizá el módulo y leé el mensaje de error completo — identificá qué te está diciendo exactamente.
4. Corregí el orden y confirmá que ahora carga bien.

### Ejercicio 4 — `installable=False`
1. Cambiá temporalmente `installable` a `False` en el manifest.
2. Reiniciá Odoo y mirá la lista de Apps disponibles (`Actualizar lista de aplicaciones` si hace falta) — confirmá que tu módulo ya no aparece como instalable.
3. Volvé a poner `installable=True`.

### Ejercicio 5 — Reto: ícono y categoría propios
- Agregá `static/description/icon.png` (cualquier imagen 128×128).
- Creá una `category` propia ("Inmobiliaria") en vez de usar "Inmobiliaria" genérico, y usala en el manifest.

---

## Preguntas de repaso conceptual

1. ¿Qué pasa si tu módulo depende de `sale` y vos no instalaste `sale` manualmente?
2. ¿Por qué un modelo definido en un `.py` puede "no existir" para Odoo aunque el archivo esté bien escrito?
3. ¿Qué significa que los archivos de `data` se procesen "en orden"?
4. ¿Cuál es la diferencia práctica entre `installable=False` y simplemente no instalar el módulo?
5. Dado el formato de versión `18.0.1.0.0`, ¿qué parte identifica la versión de Odoo y qué parte es tuya?

<details>
<summary>Ver respuestas</summary>

1. Odoo resuelve el grafo de dependencias automáticamente: al instalar tu módulo, instala `sale` (y lo que `sale` a su vez necesite) antes, sin que lo pidas explícitamente.
2. Porque falta el `import` en algún `__init__.py` de la cadena (subcarpeta o raíz) — Odoo solo carga lo que efectivamente se importa, no escanea el disco buscando clases.
3. Que Odoo los lee de arriba a abajo tal como aparecen en la lista `data`; si un archivo referencia algo (un grupo, una vista) que otro archivo define más abajo en la lista, la carga falla.
4. `installable=False` mantiene el código en disco pero Odoo lo ignora completamente (no aparece, no se puede instalar); no instalarlo simplemente significa que todavía no corriste `-i`, pero sigue siendo instalable si quisieras.
5. `18.0` es la versión de Odoo con la que es compatible; `1.0.0` es el versionado propio del módulo (lo vas a incrementar en el día 25 al escribir una migración).

</details>

## Checklist de cierre
- [ ] Entiendo qué hace cada clave del manifest que usé.
- [ ] Provoqué y corregí el error de "olvidé el import".
- [ ] Provoqué y corregí un error de orden en `data`.
- [ ] El módulo se instala sin errores.
