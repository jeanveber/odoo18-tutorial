from odoo import api, fields, models


class DispatchRequest(models.Model):
    _name = "dispatch.request"
    _description = "Plumbing Dispatch Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Request Title", required=True, tracking=True)
    client_name = fields.Char(string="Client Name", required=True)
    client_address = fields.Char(string="Client Address", required=True)
    plumber_id = fields.Many2one(
        "res.users",
        string="Assigned Plumber",
        required=True,
        tracking=True,
    )
    description = fields.Text(string="Problem Description")
    date_scheduled = fields.Date(string="Scheduled Date", tracking=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )
    duration_label = fields.Char(
        string="Status Label",
        compute="_compute_duration_label",
        store=False,
    )

    @api.depends("status")
    def _compute_duration_label(self):
        labels = {
            "new": "Just opened",
            "in_progress": "Work in progress",
            "done": "Completed",
        }
        for record in self:
            record.duration_label = labels.get(record.status, "Unknown")
