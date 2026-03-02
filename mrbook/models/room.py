from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MeetingRoom(models.Model):
    _name = "mrbook.room"  # model identifier and table name
    _description = "Meeting Room"

    _inherit = ["mail.thread"]

    _rec_name = "name"  # changed for testing
    # add tracking for all later
    name = fields.Char(string="Room Name", required=True, tracking=True)
    capacity = fields.Integer(string="Capacity", tracking=True)
    location = fields.Char(string="Location / Floor", tracking=True)
    active = fields.Boolean(default=True)
    # so we can disable rooms for some time

    # had bunch of bool fields, projector, whiteboard, etc
    # decided to change them to amenities
    # which is just TAGS
    amenity_ids = fields.Many2many("mrbook.amenity", string="Amenities")
    booking_ids = fields.One2many(
        "mrbook.booking", "room_id", string="Bookings"
    )  # noqa: E501

    notes = fields.Text(string="Notes")

    @api.constrains("capacity")
    def _check_capacity(self):
        for record in self:
            print(record)
            print(record.capacity)
            if record.capacity <= 0:
                raise ValidationError("Capacity cannot be less than 0 or 0")
