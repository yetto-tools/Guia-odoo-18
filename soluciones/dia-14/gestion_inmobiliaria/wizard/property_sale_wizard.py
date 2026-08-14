from odoo import fields, models


class PropertySaleWizard(models.TransientModel):
    _name = "inmueble.property.sale.wizard"
    _description = "Confirmar venta de propiedad"

    property_id = fields.Many2one("inmueble.property", required=True)
    final_price = fields.Float(required=True)

    def action_confirm_sale(self):
        self.ensure_one()
        self.property_id.write({"selling_price": self.final_price, "state": "sold"})
        return {"type": "ir.actions.act_window_close"}
