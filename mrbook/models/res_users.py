from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    booking_ids = fields.One2many(
        "mrbook.booking", "user_id", string="Bookings"
    )  # noqa: E501
