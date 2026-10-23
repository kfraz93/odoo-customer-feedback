from datetime import timedelta
from odoo import models, fields
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Management for Prefabricated Homes"

    # Core Basic Information
    name = fields.Char(
        required=True,
        string="House Model Name",
        help="Official commercial model name of the prefabricated house (e.g., Stadtvilla Magdeburg)."
    )
    description = fields.Text(
        string="Description",
        help="Detailed architectural overview, customer requests, or special structural notes."
    )
    postcode = fields.Char(
        string="Postal Code",
        help="Postal code of the construction plot or regional exhibition center."
    )
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.today() + timedelta(days=90),
        help="Scheduled delivery or handover date for the finished prefabricated home."
    )

    # Images & Media
    image_1920 = fields.Image(
        string="Property Image",
        max_width=1920,
        max_height=1920,
        help="High-resolution rendering or photograph displayed on the Kanban and form view cards."
    )

    # Financial Details
    expected_price = fields.Float(
        required=True,
        string="Base Price (€)",
        help="Catalog base price of the house model before individual customizations."
    )
    selling_price = fields.Float(
        readonly=False,
        copy=False,
        string="Final Selling Price (€)",
        help="Final agreed contract price including extras, locked in upon handover."
    )

    # General Structural Features
    bedrooms = fields.Integer(
        default=2,
        string="Bedrooms",
        help="Total number of designed sleeping rooms in the floor plan."
    )
    living_area = fields.Integer(
        string="Living Area (m²)",
        help="Total usable interior floor space measured in square meters."
    )
    facades = fields.Integer(
        string="Facades",
        help="Number of finished exterior wall sides."
    )
    garage = fields.Boolean(
        string="Garage",
        help="Indicates whether a garage or carport is integrated into the package."
    )
    garden = fields.Boolean(
        string="Garden",
        help="Indicates if the property includes a dedicated garden plot."
    )
    garden_area = fields.Integer(
        string="Garden Area (m²)",
        help="Total square footage of the outdoor garden space."
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Specify the cardinal direction of the garden exposure."
    )

    # Customer / Buyer Relational Field
    partner_id = fields.Many2one(
        'res.partner',
        string="Customer / Buyer",
        help="The client who has purchased this prefabricated house model."
    )

    # Fertighaus / ScanHaus Specific Features (Stage 1 Extensions)
    construction_type = fields.Selection(
        string="Construction Method",
        selection=[
            ('holzrahmen', 'Holzrahmenbauweise (Timber Frame)'),
            ('massiv', 'Massivbauweise (Solid Construction)')
        ],
        default='holzrahmen',
        help="Select the structural construction type of the prefabricated house."
    )
    kniestock_height = fields.Float(
        string="Kniestock Height (m)",
        default=0.0,
        help="Height of the knee wall in meters (e.g., up to 2.0m for 1.5-storey homes)."
    )
    energy_efficiency = fields.Selection(
        string="Energy Standard",
        selection=[
            ('kfw40', 'KfW 40'),
            ('kfw55', 'KfW 55'),
            ('passiv', 'Passivhaus')
        ],
        default='kfw40',
        help="Energy efficiency rating standard governing insulation and subsidies."
    )
    turnkey = fields.Boolean(
        string="Schlüsselfertig (Turnkey)",
        default=True,
        help="Indicates whether the property is delivered fully finished and turnkey ready."
    )
    virtual_tour_url = fields.Char(
        string="360° Tour URL",
        help="External web link to the immersive 360-degree virtual walkthrough."
    )

    # Musterhaus Specific Features
    is_musterhaus = fields.Boolean(
        string="Is Show Home (Musterhaus)",
        default=False,
        help="Check if this property serves as a physical regional display show home."
    )
    musterhaus_location = fields.Selection(
        string="Show Home Location",
        selection=[
            ('magdeburg', 'Musterhaus Magdeburg'),
            ('chemnitz', 'Musterhaus Chemnitz'),
            ('dresden', 'Musterhaus Dresden'),
            ('rostock', 'Musterhaus Rostock'),
            ('leipzig', 'Musterhaus Leipzig'),
            ('hannover', 'Musterhaus Hannover')
        ],
        help="Regional exhibition center associated with this display model."
    )

    # Relational & State Fields
    active = fields.Boolean(
        default=True,
        help="Archiving flag. Uncheck to hide this property without deleting historical records."
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        help="Categorization link defining the overarching architectural typology."
    )
    invoice_id = fields.Many2one(
        'account.move',
        string="Generated Invoice",
        readonly=True,
        copy=False,
        help="Linked customer invoice generated automatically upon key handover."
    )

    # Workflow State (ScanHaus "Erst bauen - dann zahlen" Lifecycle)
    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('configured', 'Configured'),
            ('construction', 'Under Construction'),
            ('handover', 'Keys Handed Over'),
            ('invoiced', 'Invoiced'),
            ('cancelled', 'Cancelled')
        ],
        help="Lifecycle stage of the prefabricated house project.",
        default='draft',
        required=True,
        copy=False
    )

    # --- Action Methods & Business Logic ---

    def action_configure(self):
        """Move project state from Draft to Configured."""
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled projects cannot be configured.")
            record.state = 'configured'
        return True

    def action_construction(self):
        """Move project state from Configured to Under Construction."""
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled projects cannot go into construction.")
            record.state = 'construction'
        return True

    def action_handover(self):
        """
        Key Handover (Schlüsselübergabe):
        Triggers completion, generates invoice linked to the customer, and moves state to invoiced.
        """
        invoice = None
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled projects cannot be handed over.")

            # Real-world safety check: Ensure a customer is assigned before billing
            if not record.partner_id:
                raise UserError("Please assign a customer (Buyer) to this property before handing over keys.")

            if not record.selling_price:
                record.selling_price = record.expected_price

            # Create an automatic Customer Invoice linked to the actual customer
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,  # Uses the selected customer!
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f"Prefabricated House Delivery: {record.name} ({record.musterhaus_location or 'Standard'})",
                        'quantity': 1.0,
                        'price_unit': record.selling_price,
                    })
                ]
            }
            invoice = self.env['account.move'].create(invoice_vals)

            # Transition state and link the invoice
            record.state = 'invoiced'
            record.invoice_id = invoice.id

        # Pop open the newly created invoice view!
        if invoice and len(self) == 1:
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return True

    def action_draft(self):
        """Allow resetting a property back to draft in case of accidental clicks."""
        for record in self:
            record.state = 'draft'
        return True

    def action_cancel(self):
        """Cancel property project."""
        for record in self:
            if record.state == 'invoiced':
                raise UserError("Invoiced properties cannot be cancelled.")
            record.state = 'cancelled'
        return True