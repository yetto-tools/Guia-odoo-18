from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class InmueblePortal(http.Controller):
    @http.route("/propiedades", type="http", auth="public", website=True)
    def list_properties(self, **kwargs):
        properties = request.env["inmueble.property"].sudo().search(
            [("state", "in", ("new", "offer_received"))]
        )
        return request.render("gestion_inmobiliaria.properties_list", {"properties": properties})

    @http.route("/propiedades/<int:property_id>", type="http", auth="public", website=True)
    def property_detail(self, property_id, **kwargs):
        property_rec = request.env["inmueble.property"].sudo().search(
            [("id", "=", property_id), ("state", "in", ("new", "offer_received"))]
        )
        if not property_rec:
            raise NotFound()
        return request.render("gestion_inmobiliaria.property_detail", {"property": property_rec})
