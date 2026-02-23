from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DispatchRequest(models.Model):
    _name = "dispatch.request"
    _description = "Plumbing Dispatch Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Request Title", required=True, tracking=True)
    client_name = fields.Char(string="Client Name", required=True)
    client_address = fields.Char(string="Client Address", required=True)
    plumber_id = fields.Many2one(
        "res.users", string="Assigned Plumber", required=True, tracking=True
    )
    description = fields.Text(string="Problem Description")
    note = fields.Text(string="Progress Notes", tracking=True)
    date_scheduled = fields.Date(string="Scheduled Date", tracking=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
            ("failed", "Failed"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )
    # computing days left
    days_until = fields.Char(
        string="Due In",
        compute="_compute_days_until",
        store=False,
    )

    @api.depends("date_scheduled")
    def _compute_days_until(self):
        for record in self:
            if record.date_scheduled:
                delta = record.date_scheduled - fields.Date.today()
                record.days_until = f"{delta.days} days"
            else:
                record.days_until = "No date set"

    @api.constrains("date_scheduled")
    def _check_date_scheduled(self):
        today = fields.Date.today()
        for record in self:
            if record.date_scheduled and record.date_scheduled <= today:
                raise ValidationError("Scheduled date cannot be in the past!")

    def action_set_in_progress(self):
        self.status = "in_progress"

    def action_set_done(self):
        self.status = "done"

    def action_cancel(self):
        self.status = "cancelled"

    def action_fail(self):
        self.status = "failed"
