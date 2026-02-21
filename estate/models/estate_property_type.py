from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    description = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A property type name must be unique."),
    ]


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Real Estate Property Type Line"

