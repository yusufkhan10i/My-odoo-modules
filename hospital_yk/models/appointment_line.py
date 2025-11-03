from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    price = fields.Float(string="Price", default=0.0)
    note = fields.Text(string="Note")
    total = fields.Float(string="Total", compute='_compute_total', store=True)
    patient_id = fields.Many2one(related='appointment_id.patient_id', string="Patient", store=True)

    @api.depends('quantity', 'price')
    def _compute_total(self):
        for line in self:
            line.total = (line.quantity or 0.0) * (line.price or 0.0)

    def action_view_invoice(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('appointment_id', '=', self.appointment_id.id)])
        if not invoices:
            raise UserError("No invoices found for this appointment.")
        return {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoices.ids)],
            'context': {'create': False}
        }

    def action_create_invoice(self):
        self.ensure_one()
        if self.appointment_id.state != 'done':
            raise UserError("Invoices can only be created for completed appointments.")
        # Determine partner: prefer patient.partner_id (res.partner)
        partner = self.patient_id.partner_id if self.patient_id else None
        if not partner:
            raise UserError("Patient has no related partner to create an invoice.")
        # Determine price_unit: use line price if set, otherwise product's list price
        price_unit = self.price if self.price else (self.product_id.list_price if self.product_id else 0.0)
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'appointment_id': self.appointment_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'quantity': self.quantity,
                'price_unit': price_unit,
                'name': self.product_id.name,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'context': {'default_move_type': 'out_invoice'}
        }