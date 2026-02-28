from odoo import models, fields
from random import randint


class MeetingRoomAmenity(models.Model):
    _name = "mrbook.amenity"
    _description = "Room Amenity"
    name = fields.Char(string="Amenity", required=True)

    def _default_color(self):
        return randint(1, 11)

    # there are 12 default primary colors in odoo
    # secondary_variables.scss

    color = fields.Integer(
        string="Color Index",
        default=_default_color,
        help="Tag color.",
    )

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A property tag name must be unique."),
    ]
