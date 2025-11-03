from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment Manager'
    _rec_name = 'patient_id'
    _order = 'id desc'

    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: ('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    gender = fields.Selection(related='patient_id.gender')
    appointment_date = fields.Datetime(string="Appointment Date", required=True, tracking=True, default=fields.Datetime.now)
    notes = fields.Text(string="Note", tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'),
         ('cancelled', 'Cancelled')],
        string="Status", default='draft', tracking=True
    )
    doctor_id = fields.Many2one(
        'hr.employee', string="Doctor", domain=[('is_doctor', '=', True)], tracking=True
    )
    employee_ids = fields.Selection(
        [('doctor', 'Doctor'), ('nurse', 'Nurse'),('reseptionist', 'Receptionist'),('admin', 'Admin Staff')]
        ,string="Employee", tracking=True)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string="Appointment Lines")
    prescription_ids = fields.Text(related='patient_id.prescription_ids')
    other_details = fields.Html(string="Other Details")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')

    @api.model
    def create(self, vals):
        if vals.get('reference', ('New')) == ('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or ('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("Only draft appointments can be confirmed.")
            record.state = 'confirmed'
            record.message_post(body="Appointment confirmed.")

    def action_ongoing(self):
        for record in self:
            if record.state != 'confirmed':
                raise UserError("Only confirmed appointments can be marked as ongoing.")
            record.state = 'ongoing'
            record.message_post(body="Appointment is now ongoing.")

    def action_done(self):
        for record in self:
            if record.state != 'ongoing':
                raise UserError("Only confirmed appointments can be marked as done.")
            record.state = 'done'
            record.message_post(body="Appointment marked as done.")

    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError(" Completed appointments cannot be cancelled.")
            record.state = 'cancelled'
            record.message_post(body="Appointment cancelled.")

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'
            record.message_post(body="Appointment reset to draft.")

    def unlink(self):
        for record in self:
            if record.state not in ('draft', 'cancelled'):
                raise UserError("Only draft or cancelled appointments can be deleted.")
        return super(HospitalAppointment, self).unlink()
