from odoo import models, fields


class MeetingRoom(models.Model):
    _name = "mrbook.room"  # model identifier and table name
    _description = "Meeting Room"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]  # we inherit the activity button, scheduled tasks, reminders.
    # the message log, followers list,
    # email integration, internal notes, logging field changes

    name = fields.Char(string="Room Name", required=True, tracking=True)
    capacity = fields.Integer(string="Capacity", tracking=True)
    location = fields.Char(string="Location / Floor", tracking=True)
    active = fields.Boolean(default=True)  # I mean, we do not wanna delete
