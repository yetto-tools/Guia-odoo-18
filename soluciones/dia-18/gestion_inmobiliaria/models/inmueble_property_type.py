from odoo import fields, models


class InmueblePropertyType(models.Model):
    _name = "inmueble.property.type"
    _description = "Tipo de propiedad"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
