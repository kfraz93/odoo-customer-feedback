from datetime import date
from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Car(models.Model):
    _name = "cars.car"
    _description = "Cars for sale"
    _order = "name asc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Car name", required=True, help="Make and model of the car")
    description = fields.Text(string="Description", help="Detailed description of the car")
    model_year = fields.Integer(string="Model year", required=True, help="Year car was made")
    vin = fields.Char(string="VIN", copy=False, help="Vehicle registration number")
    cost_price = fields.Float(string="Cost Price", required=True, digits=(10,2), help="Purchase price of vehicle")
    selling_price = fields.Float(string="Selling Price", digits=(10,2))
    profit = fields.Float(string="Profit", compute='_compute_profit', store=True, readonly=True)
    state = fields.Selection([('available', 'Available'),
                              ('sold', 'Sold'),
                              ('maintenance', 'Maintenance')
                              ],
                             string='Status',
                             default='available',
                             required=True
                             )
    customer_id = fields.Many2one('res.partner', string="Customer")
    active = fields.Boolean(default=True)
    image = fields.Binary(string="Car image", attachment=True, help="upload image of the car")
    listing_date = fields.Date(string="Listing Date", default=fields.Date.today())


    @api.depends('cost_price', 'selling_price')
    def _compute_profit(self):
        for record in self:
            record.profit = record.selling_price - record.cost_price if (
                record.selling_price) else 0.0


    @api.constrains('cost_price', 'selling_price', 'listing_date')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.cost_price:
                if record.listing_date:
                    days_since_listing = (date.today() - record.listing_date).days
                else:
                    days_since_listing = 0
                if days_since_listing < 365:
                    raise ValidationError("The selling price cannot be lower than cost price!")
