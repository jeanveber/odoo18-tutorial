from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    booking_ids = fields.One2many(
        comodel_name="mrbook.booking",
        inverse_name="user_id",
        string="Bookings",  # noqa: E501
    )  # noqa: E501

    booking_count = fields.Integer(
        string="Booking Count", compute="_compute_booking_count"
    )

    @api.depends("booking_ids")
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids)

    def action_view_bookings(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Bookings",
            "res_model": "mrbook.booking",
            "view_mode": "list,form",
            "target": "current",
            "domain": [("user_id", "=", self.id)],
        }
