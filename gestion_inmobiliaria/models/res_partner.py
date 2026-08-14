from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many("inmueble.property", "buyer_id", string="Propiedades compradas")

    def action_view_properties(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Propiedades",
            "res_model": "inmueble.property",
            "view_mode": "list,form",
            "domain": [("buyer_id", "=", self.id)],
        }
