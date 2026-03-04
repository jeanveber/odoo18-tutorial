from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MeetingRoomBooking(models.Model):
    _name = "mrbook.booking"
    _description = "Meeting Room Booking"
    _inherit = ["mail.thread"]

    reference = fields.Char(
        string="Reference",
        required=True,
        tracking=True,
        copy=False,
        default="New",  # noqa: E501
    )
    _rec_name = "reference"
    room_id = fields.Many2one(
        "mrbook.room",
        string="Room",
        required=True,
        tracking=True,
        ondelete="restrict",  # noqa: E501
    )
    # added ondelete restriction
    amenity_ids = fields.Many2many(
        string="Amenities", related="room_id.amenity_ids", readonly=True
    )
    # related field

    user_id = fields.Many2one(
        "res.users",
        string="Booked By",
        default=lambda self: self.env.user,
        tracking=True,
    )  # we take odoo users and assign them as users
    start_datetime = fields.Datetime(string="Start", required=True)
    end_datetime = fields.Datetime(string="End", required=True)
    duration = fields.Float(
        string="Duration (hours)", compute="_compute_duration", store=True
    )  # I might need to sort duration
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )
    notes = fields.Text(string="Notes")

    @api.depends("start_datetime", "end_datetime")
    def _compute_duration(self):
        for record in self:
            if (
                record.start_datetime and record.end_datetime
            ):  # if those records aren't empty, not False by default
                time_diff = record.end_datetime - record.start_datetime
                record.duration = time_diff.total_seconds() / 3600

    @api.constrains("start_datetime", "end_datetime")
    def _check_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.end_datetime <= record.start_datetime:
                    raise ValidationError("End time must be after start time.")

                time_diff = record.end_datetime - record.start_datetime
                # datetime is lit date and time
                duration_hours = time_diff.total_seconds() / 3600
                if duration_hours < 0.5:
                    raise ValidationError(
                        "Booking can't be less than 30 minutes!"
                    )  # noqa: F401
                if duration_hours > 8:
                    raise ValidationError(
                        "Booking can't be more than 8 hours!"
                    )  # noqa: F401
                if record.start_datetime <= fields.Datetime.now():
                    raise ValidationError("Start time mustn't be in the past")

    # add double booking constraint

    def action_confirm(self):
        for rec in self:
            rec.status = "confirmed"

    def action_draft(self):
        for rec in self:
            rec.status = "draft"

    def action_cancel(self):
        for rec in self:
            rec.status = "cancelled"

    @api.model_create_multi
    def create(self, vals_list):
        print("Checking if it created", vals_list)
        for vals in vals_list:
            if not vals.get("reference") or vals["reference"] == "New":
                vals["reference"] = self.env["ir.sequence"].next_by_code(
                    "mrbook.booking"
                )
        return super().create(vals_list)

    # I've tried putting return before, it didn't update New
    # it returned and didn't do anything after.

    # returns next value from the sequence,
    # passes value to ref
    # then this vals list goes to create method
