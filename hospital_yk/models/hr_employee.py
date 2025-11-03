from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "HR Employee Inherit"

    employee_ids = fields.Selection(
        [('doctor','Doctor'),('nurse','Nurse'),('admin','Admin Staff')], string="Employee Type")