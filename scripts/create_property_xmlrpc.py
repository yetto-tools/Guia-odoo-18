"""Script externo: crea una propiedad en Odoo vía XML-RPC.

No forma parte del módulo gestion_inmobiliaria — corre por fuera, como
cualquier integración de terceros. Requiere solo la librería estándar.
"""
import xmlrpc.client

url = "http://localhost:8069"
db = "midb"
username = "admin"
password = "admin"  # o una API Key generada en Ajustes de la cuenta

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
new_id = models.execute_kw(
    db, uid, password,
    "inmueble.property", "create",
    [{"name": "Creada por API externa", "expected_price": 120000}],
)
print("Creada con id:", new_id)

available = models.execute_kw(
    db, uid, password,
    "inmueble.property", "get_available_properties",
    [[]],
)
print("Propiedades disponibles:", available)
