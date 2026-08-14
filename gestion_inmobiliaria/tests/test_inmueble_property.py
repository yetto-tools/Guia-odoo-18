from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestInmuebleProperty(TransactionCase):
    def test_negative_price_raises(self):
        with self.assertRaises(ValidationError):
            self.env["inmueble.property"].create(
                {"name": "Inválida", "expected_price": -100}
            )

    def test_offer_moves_property_to_offer_received(self):
        property_rec = self.env["inmueble.property"].create(
            {"name": "Casa test", "expected_price": 100000}
        )
        partner = self.env["res.partner"].create({"name": "Comprador Test"})
        self.env["inmueble.property.offer"].create(
            {"property_id": property_rec.id, "partner_id": partner.id, "price": 95000}
        )
        self.assertEqual(property_rec.state, "offer_received")

    def test_garden_onchange(self):
        with Form(self.env["inmueble.property"]) as f:
            f.name = "Con jardín"
            f.expected_price = 100000
            f.garden = True
            self.assertEqual(f.garden_area, 10)
            self.assertEqual(f.garden_orientation, "north")
