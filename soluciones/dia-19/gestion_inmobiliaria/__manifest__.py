{
    "name": "Gestión Inmobiliaria",
    "version": "18.0.1.0.0",
    "category": "Inmobiliaria",
    "summary": "Gestión de propiedades, ofertas y agentes",
    "depends": ["base", "mail", "website"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/property_sale_wizard_views.xml",
        "views/inmueble_property_views.xml",
        "views/inmueble_property_kanban_views.xml",
        "views/res_partner_views.xml",
        "views/inmueble_templates.xml",
        "report/inmueble_property_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "gestion_inmobiliaria/static/src/js/state_badge.js",
            "gestion_inmobiliaria/static/src/js/state_badge.xml",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
