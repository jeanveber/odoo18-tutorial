from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Inverse and validity
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # Fallback to today if create_date doesn't exist yet (during creation)
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            # Calculate validity based on the difference between deadline and create date
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError("An offer has already been accepted for this property.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "An offer price must be strictly positive.",
        ),
    ]
