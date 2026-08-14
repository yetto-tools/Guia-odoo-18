from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    properties = env["inmueble.property"].search([("garden_area", "=", 0), ("garden", "=", True)])
    properties.write({"garden_area": 10})
