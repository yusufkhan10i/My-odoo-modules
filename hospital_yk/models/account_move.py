from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    appointment_id = fields.Many2one(
        'hospital.appointment', string='Appointment'
    )
