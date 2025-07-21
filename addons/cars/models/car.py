from email.policy import default

from odoo import models, fields, api

class Car(models.Model):
    _name = "cars.car"
    _description = "Cars for sale"
    _order = "name_asc"
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


    @api.depends('cost_price', 'selling_price')
    def _compute_profit(self):
        for record in self:
            record.profit = record.selling_price - record.cost_price if (
                record.selling_price) else 0.0