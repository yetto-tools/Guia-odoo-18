from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class InmuebleProperty(models.Model):
    _name = "inmueble.property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Propiedad en venta"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Superficie construida (m²)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Superficie de jardín (m²)")
    garden_orientation = fields.Selection(
        selection=[("north", "Norte"), ("south", "Sur"), ("east", "Este"), ("west", "Oeste")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "Nueva"),
            ("offer_received", "Oferta recibida"),
            ("offer_accepted", "Oferta aceptada"),
            ("sold", "Vendida"),
            ("cancelled", "Cancelada"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one("inmueble.property.type", string="Tipo")
    tag_ids = fields.Many2many("inmueble.property.tag", string="Etiquetas")
    buyer_id = fields.Many2one("res.partner", string="Comprador", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Agente", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("inmueble.property.offer", "property_id", string="Ofertas")

    total_area = fields.Integer(compute="_compute_total_area", string="Superficie total (m²)")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("El precio esperado debe ser positivo.")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def get_available_properties(self):
        return self.search([("state", "in", ("new", "offer_received"))]).sorted(
            key=lambda r: r.expected_price
        )

    def get_available_properties_data(self):
        return [
            {"id": p.id, "name": p.name, "expected_price": p.expected_price}
            for p in self.get_available_properties()
        ]

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("No se puede cancelar una propiedad vendida.")
            record.state = "cancelled"
