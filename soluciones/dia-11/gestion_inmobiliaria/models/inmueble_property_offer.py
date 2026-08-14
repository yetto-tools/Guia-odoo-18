from odoo import api, fields, models


class InmueblePropertyOffer(models.Model):
    _name = "inmueble.property.offer"
    _description = "Oferta sobre una propiedad"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Aceptada"), ("refused", "Rechazada")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Comprador")
    property_id = fields.Many2one("inmueble.property", required=True, string="Propiedad")
    validity = fields.Integer(default=7, string="Validez (días)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days
