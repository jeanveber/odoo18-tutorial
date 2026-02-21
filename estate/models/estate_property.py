# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#estate_property.py

from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    last_seen = fields.Datetime("Last seen", default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        help="State of the property",
        default="new",
        copy=False,
        required=True,
    )
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True, copy=False, default=69.69)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garages = fields.Boolean()
    gardens = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation Type",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
        help="Type is used for garden orientation selection",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    # stat_Button
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # stat button end

    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Property Offers"
    )

    # area compute
    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best price
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("gardens")
    def _onchange_gardens(self):
        if self.gardens:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "canceled"
        return True

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "A property expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "A property selling price must be strictly positive.",
        ),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise UserError(
                    _(
                        "Selling price can not be lower than 90 per cent of the expected price."
                    )
                )
