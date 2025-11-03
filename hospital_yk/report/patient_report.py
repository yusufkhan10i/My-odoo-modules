from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PatientReport(models.AbstractModel):
    _name = 'report.hospital_yk.patient_report'
    _description = 'Patient Report'

    def _get_report_values(self, docids, data=None):
        if not docids:
            raise UserError("Please select at least one record to generate the report.")
        docs = self.env['hospital.patient'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hospital.patient',
            'docs': docs,
            'data': data,
        }

        # You can add more methods or data processing as needed for the report.
class PatientCard(models.AbstractModel):
    _name = 'report.hospital_yk.patient_card'
    _description = 'Patient Card Report'

    def _get_report_values(self, docids, data=None):
        if not docids:
            raise UserError("Please select at least one record to generate the report.")
        docs = self.env['hospital.patient'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hospital.patient',
            'docs': docs,
            'data': data,
        }
    # You can add more methods or data processing as needed for the report.

