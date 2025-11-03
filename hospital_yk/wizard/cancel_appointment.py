import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError, AccessError

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"
    _inherit = ['hospital.appointment']
    _rec_name = 'patient_id'

    @api.model
    def default_get(self, fields):
        res =  super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        print("Default get executed", res)
        print("...Context..", self.env.context)
        if  self.env.context.get('reference'):
            res['appointment_id'] = self.env.context.get('reference')
        return res


    appointment_id = fields.Many2one('hospital.appointment', string="Appointment" )
    reason = fields.Text(string="Reason", default="Test Reason")
    date_cancel = fields.Date(string="Cancellation Date")
    appointment_date = fields.Datetime(string="Appointment Date", required=True, tracking=True, default=fields.Datetime.now)


    def action_cancel(self):
        if self.appointment_id.appointment_date == fields.Date.today():
            raise ValidationError("Sorry,cancellation is not allowed on the same day of booking !")
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
