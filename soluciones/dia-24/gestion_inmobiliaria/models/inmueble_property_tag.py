from odoo import fields, models


class InmueblePropertyTag(models.Model):
    _name = "inmueble.property.tag"
    _description = "Etiqueta de propiedad"

    name = fields.Char(required=True)
    color = fields.Integer()
