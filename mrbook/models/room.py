from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


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

    # had bunch of bool fields, projector, whiteboard, etc.
    # decided to change them to amenities
    # which is just TAGS
    # comodel name is name of field of values
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

    # we override unlink directly
    """
    def unlink(self):
        for rec in self:
            domain = [('room_id','=',rec.id)]
            bookings = self.env["mrbook.booking"].search(domain)
            if bookings:
                raise UserError(error_message)
        return super().unlink() # does the actual deletion

    """

    @api.ondelete(at_uninstall=False)
    def _check_booking(self):
        for rec in self:
            domain = [("room_id", "=", rec.id)]
            bookings = self.env["mrbook.booking"].search(domain)
            if bookings:
                raise UserError(
                    f"Can't' delete. The following room has been booked: {rec.name}"  # noqa: E501
                )
