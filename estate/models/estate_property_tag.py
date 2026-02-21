#estate_property_tag.py
from odoo import fields, models
from random import randint


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    color = fields.Integer(
        string="Color Index",
        default=lambda self: self._default_color(),
        help="Tag color. No color means no display in kanban to distinguish internal tags from public categorization tags.",
    )

    name = fields.Char(required=True)
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A property tag name must be unique."),
    ]
