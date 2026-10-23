from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True, string="House Category")
    sequence = fields.Integer(default=10, help="Used to order property types.")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Associated Houses")