from email.policy import default
from odoo import api, fields, models


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _order = 'sequence,id'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer( string="Sequence", default=10  )
    color_id = fields.Integer('Color Index')
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', "Tag name already exists!"),
        ('check_sequence', 'check (sequence > 0)', "Sequence must be positive number!"),

    ]
