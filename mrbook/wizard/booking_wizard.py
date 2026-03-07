from odoo import models, fields


class MeetingRoomBookingWizard(models.TransientModel):
    _name = "mrbook.booking.wizard"
    _description = "Create Booking"

    reference = fields.Char(
        string="Reference",
        required=True,
        tracking=True,
        copy=False,
        default="New",  # noqa: E501
    )

    user_id = fields.Many2one(
        "res.users",
        string="Booked By",
        default=lambda self: self.env.user,
        tracking=True,
    )
    room_id = fields.Many2one("mrbook.room", string="Room", required=True)
    start_datetime = fields.Datetime(string="Start", required=True)
    end_datetime = fields.Datetime(string="End", required=True)
    notes = fields.Text(string="Notes")

    def action_create_booking(self):
        self.env["mrbook.booking"].create(
            {
                "user_id": self.user_id.id,
                "room_id": self.room_id.id,
                "start_datetime": self.start_datetime,
                "end_datetime": self.end_datetime,
                "notes": self.notes,
            }
        )

        # return {'type': 'ir.actions.act_window_close'}
        return {"type": "ir.actions.client", "tag": "reload"}

    # updates page to show info

    # some logic here
