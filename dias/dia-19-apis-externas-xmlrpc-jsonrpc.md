# Día 19 — APIs externas: XML-RPC / JSON-RPC / REST

**Semana:** 3 — Frontend, reportes e integraciones
**Duración estimada:** 3–4 h

## Objetivo del día
Crear una propiedad desde un script Python externo a Odoo, y entender las alternativas de integración.

---

## Conceptos de Odoo

### Odoo no tiene una API REST "oficial" tradicional — tiene XML-RPC/JSON-RPC
A diferencia de frameworks que exponen REST por convención, la vía **nativa** y estable de Odoo para integraciones externas es XML-RPC (y su equivalente JSON-RPC). Esto no es una limitación: es literalmente el mismo protocolo que usa el propio cliente web de Odoo para hablar con el servidor. Cualquier cosa que puedas hacer desde la UI, la podés hacer por este camino.

### Los dos endpoints y su propósito
- `/xmlrpc/2/common`: solo para autenticación (`authenticate(db, user, password, {})`, que devuelve un `uid` numérico).
- `/xmlrpc/2/object`: para todo lo demás, vía `execute_kw(db, uid, password, modelo, metodo, args, kwargs)`.

`execute_kw` es genérico: `metodo` puede ser `"create"`, `"write"`, `"search"`, `"read"`, o **cualquier método propio** que hayas definido en tu modelo — la integración externa tiene el mismo poder que el código interno, siempre sujeta a los mismos ACL y record rules del usuario autenticado (no hay bypass de seguridad por venir de "afuera").

### Por qué la seguridad del día 6 sigue aplicando acá
Autenticarte con `authenticate()` no te da superpoderes — obtenés un `uid` que representa a ese usuario específico, con sus grupos y permisos normales. Si autenticás como el "agente" del día 6, y ese usuario solo puede ver sus propias propiedades, el `search` vía XML-RPC también va a estar filtrado por esa record rule. Es el mismo motor de seguridad, sin importar el canal de entrada.

### `type="json"` como alternativa a XML-RPC crudo
En vez de que un cliente externo hable XML-RPC directamente, podés exponer tu propio endpoint (`@http.route(..., type="json")`) con la forma exacta que necesites, devolviendo solo los campos que querés exponer, con la lógica de negocio que decidas. Es más control, pero más trabajo — vos definís el contrato en vez de heredar el genérico de `execute_kw`.

### Autenticación sin sesión de navegador: API Keys
`auth="user"` funciona con cookies de sesión, pensado para el navegador. Para integraciones máquina-a-máquina (sin sesión de navegador), Odoo permite generar una **API Key** por usuario (`Ajustes de la cuenta → Seguridad de la cuenta → Nuevas claves de API`), que se usa **en vez de la contraseña real** tanto en XML-RPC como en ciertos endpoints — así no exponés la contraseña real del usuario en un script o integración de terceros, y podés revocar la key sin cambiar la contraseña.

---

## Ejercicios prácticos

### Ejercicio 1 — Crear una propiedad por XML-RPC (guiado)

```python
import xmlrpc.client

url, db, username, password = "http://localhost:8069", "midb", "admin", "admin"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
new_id = models.execute_kw(
    db, uid, password,
    "inmueble.property", "create",
    [{"name": "Creada por API externa", "expected_price": 120000}],
)
print("Creada con id:", new_id)
```
Corré el script contra tu instancia local, verificá en la UI.

### Ejercicio 2 — Confirmar que la seguridad del día 6 aplica igual
1. Repetí el script de arriba, pero autenticando como el usuario "agente" del día 6 en vez de `admin`.
2. Llamá `execute_kw` con método `"search"` y dominio vacío `[[]]` sobre `inmueble.property` — confirmá que solo trae las propiedades de ese agente, igual que en la UI.
3. Intentá `create` de una propiedad con `salesperson_id` de **otro** agente, si el ACL/record rule lo permite o lo bloquea — confirmá el comportamiento y explicá por qué.

### Ejercicio 3 — Llamar a un método propio, no solo CRUD genérico
1. Usá el script para invocar el método `get_available_properties` que escribiste el día 10, vía `execute_kw` con `metodo="get_available_properties"` y `args=[[]]`.
2. Confirmá que devuelve los mismos resultados que verías llamándolo desde `odoo shell`.

### Ejercicio 4 — Generar y usar una API Key
1. Desde `Ajustes de la cuenta → Seguridad de la cuenta`, generá una API Key para tu usuario admin.
2. Modificá el script del ejercicio 1 para usar esa key en vez de la contraseña real (mismo parámetro `password` en `execute_kw`, pero con el valor de la key).
3. Confirmá que funciona igual, y después revocá la key desde la misma pantalla y confirmá que el script ya no puede autenticarse con esa key vieja.

### Ejercicio 5 — Reto: endpoint JSON propio
Exponé un endpoint interno como alternativa a XML-RPC crudo:
```python
@http.route("/api/propiedades", type="json", auth="user")
def api_properties(self, **kwargs):
    properties = request.env["inmueble.property"].search([("state", "=", "new")])
    return [{"id": p.id, "name": p.name, "price": p.expected_price} for p in properties]
```
Probalo con una herramienta como `curl` o `requests`, armando el sobre JSON-RPC correcto (`{"jsonrpc": "2.0", "method": "call", "params": {...}}`), y compará la complejidad de esta integración contra la del XML-RPC genérico del ejercicio 1.

---

## Preguntas de repaso conceptual

1. ¿Qué diferencia de propósito hay entre `/xmlrpc/2/common` y `/xmlrpc/2/object`?
2. Si autenticás por XML-RPC como un usuario con permisos restringidos (como el "agente" del día 6), ¿el `search` vía XML-RPC ignora esas restricciones o las respeta?
3. ¿Qué ventaja tiene una API Key sobre usar la contraseña real del usuario en una integración externa?
4. ¿Podés invocar, vía `execute_kw`, un método propio que vos definiste en tu modelo (no solo `create`/`write`/`search`)?
5. ¿Qué control adicional ganás al exponer tu propio endpoint `type="json"` frente a usar XML-RPC genérico?

<details>
<summary>Ver respuestas</summary>

1. `/xmlrpc/2/common` solo sirve para autenticar y obtener un `uid`; `/xmlrpc/2/object` es el endpoint genérico para ejecutar cualquier método sobre cualquier modelo (`execute_kw`), una vez autenticado.
2. Las respeta completamente — el `uid` obtenido representa a ese usuario específico, con sus grupos, ACL y record rules normales; no hay ningún bypass de seguridad por usar XML-RPC en vez de la UI.
3. Podés revocarla sin cambiar la contraseña real del usuario, y no exponés esa contraseña real en scripts o integraciones de terceros que podrían filtrarse.
4. Sí — `execute_kw` es genérico respecto al nombre del método; podés invocar cualquier método público de tu modelo, no solo las operaciones CRUD estándar.
5. Control total sobre la forma exacta de la respuesta (qué campos exponer, qué lógica de negocio aplicar antes de responder) — con XML-RPC genérico heredás el comportamiento estándar de `create`/`search`/etc., sin poder moldear la respuesta a tu medida.

</details>

## Checklist de cierre
- [ ] Puedo explicar la firma completa de `execute_kw`.
- [ ] Confirmé que la seguridad del día 6 aplica igual vía XML-RPC.
- [ ] Generé y usé una API Key en vez de una contraseña real.
- [ ] Probé la integración desde un proceso realmente externo a Odoo, no desde `odoo shell`.
