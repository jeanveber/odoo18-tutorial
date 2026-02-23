from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MeetingRoomBooking(models.Model):
    _name = "mrbook.booking"
    _description = "Meeting Room Booking"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]  # here it's gonna be used way more

    name = fields.Char(string="Ref", required=True, tracking=True, copy=False)
    # it's a relational field
    room_id = fields.Many2one(
        "meeting.room", string="Room", required=True, tracking=True
    )
    user_id = fields.Many2one(
        "res.users",
        string="Booked By",
        default=lambda self: self.env.user,
        tracking=True,
    )
    start_datetime = fields.Datetime(string="Start", required=True)
    end_datetime = fields.Datetime(string="End", required=True)
    duration = fields.Float(
        string="Duration (hours)", compute="_compute_duration", store=True
    )
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
            else:
                record.duration = 0.0

    @api.constrains("start_datetime", "end_datetime")
    def _check_dates(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.end_datetime <= record.start_datetime:
                    raise ValidationError("End time must be after start time.")

    @api.constrains("room_id", "start_datetime", "end_datetime")
    def _check_double_booking(self):
        for record in self:  # fking black keeps changing
            has_required_fields = (
                record.room_id
                and record.start_datetime
                and record.end_datetime  # noqa: F401
            )
            if not has_required_fields:
                continue

            overlapping = self.env["mrbook.booking"].search(
                [
                    ("room_id", "=", record.room_id.id),  # srch our room
                    ("id", "!=", record.id),  # exclude current record
                    (
                        "status",
                        "!=",
                        "cancelled",
                    ),  # canceled bookings don't occupy room
                    ("start_datetime", "<", record.end_datetime),
                    ("end_datetime", ">", record.start_datetime),
                ]
            )
            if overlapping:
                raise ValidationError(
                    f"Room '{record.room_id.name}"
                    f"' is already booked during this time slot."
                )
