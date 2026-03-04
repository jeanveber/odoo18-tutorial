from odoo import fields, models


class MeetingRoomChangeStatus(models.AbstractModel):
    _name = "mrbook.change_status"
    _description = "Meeting Room Change Status"
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    def action_confirm(self):
        for rec in self:
            rec.status = "confirmed"

    def action_draft(self):
        for rec in self:
            rec.status = "draft"

    def action_cancel(self):
        for rec in self:
            rec.status = "cancelled"
