from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import date

from odoo.tools import conditional


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Manager'
    _rec_name = 'name'

    name = fields.Char(
        string="Name", required=True, tracking=True
    )
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', string='Partner')
    date_of_birth = fields.Date(string="DOB", tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender", tracking=True
    )
    active = fields.Boolean(string="Active", default=True)
    tag_ids = fields.Many2many(
        'patient.tag', 'patient_tag_rel', 'patient_id', 'tag_id', string="Tags", tracking=True
    )
    age = fields.Integer(
        string="Age", compute='_compute_age', store=True, tracking=True
    )
    notes = fields.Text(
        string="Notes", tracking=True
    )
    appointment_ids = fields.One2many(
        'hospital.appointment', 'patient_id', string="Appointments"
    )
    mobile = fields.Char(
        string="Mobile", tracking=True
    )
    email = fields.Char(
        string="Email", tracking=True
    )
    address = fields.Text(
        string="Address", tracking=True
    )
    guardian = fields.Selection(
        [('Father', 'Father'), ('Mother', 'Mother'), ('Brother', 'Brother'), ('Sister', 'Sister'),
         ('Friend', 'Friend')], string="Guardian Relation", tracking=True)
    guardian_name = fields.Char(
        string="Guardian Name", tracking=True
    )
    guardian_mobile = fields.Char(
        string="Guardian Mobile", tracking=True
    )
    medical_history = fields.Text(
        string="Medical History", tracking=True
    )
    appointment_date = fields.Datetime(
        string="Next Appointment Date", tracking=True
    )
    doctor_name = fields.Char(
        string="Doctor Name", related='doctor_id.name', readonly=True, tracking=True
    )
    doctor_id = fields.Many2one(
        'hr.employee', string="Doctor", tracking=True
    )
    prescription_ids = fields.Text(
        string="Prescription", tracking=True
    )
    meditation = fields.Text(
        string="Meditation", tracking=True
    )
    image = fields.Image(
        string="Image", max_width=1920, max_height=1920, tracking=True
    )
    dosage = fields.Text(
        string="Dosage", tracking=True
    )
    instructions = fields.Text(
        string="Instructions", tracking=True
    )
    company = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company, tracking=True
    )
    your_logo = fields.Binary(
        string="Your Logo", related='company.logo', readonly=False
    )
    other_details = fields.Html(string="Other Details"
    )
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])


    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError(("The entered date of birth is not acceptable"))


    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                age = today.year - record.date_of_birth.year - (
                        (today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
                record.age = age
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if vals.get('reference', ('New')) == ('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or ('New')
        result = super(HospitalPatient, self).create(vals)
        return result