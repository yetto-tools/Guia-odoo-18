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

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"
        return offers

    def action_accept(self):
        for offer in self:
            offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id).write(
                {"status": "refused"}
            )
            offer.status = "accepted"
            offer.property_id.write(
                {
                    "state": "offer_accepted",
                    "buyer_id": offer.partner_id.id,
                    "selling_price": offer.price,
                }
            )
            offer.property_id.message_post(
                body=f"Oferta de {offer.partner_id.name} aceptada por {offer.price}."
            )
            offer.property_id.activity_schedule(
                "mail.mail_activity_data_todo",
                summary="Preparar contrato de venta",
                user_id=offer.property_id.salesperson_id.id,
            )

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
