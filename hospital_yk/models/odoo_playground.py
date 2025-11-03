from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

class OdooPlayGround(models.Model):
    _name = 'odoo.playground'
    _description = "Odoo Playground"

    # Available variables for code execution
    DEFAULT_ENV_VARIABLES = '''
    # self: Current object
    # self.env: Odoo Environment in which the action is triggered
    # self.env.user: Current user (as an instance)
    # self.env.company: Current company (as an instance)
    # self.env.cr: Database cursor
    # self.env.ref: Reference to a record by XML ID
    # self.env['res.partner']: Example of accessing a model
    # self.env['res.users']: Access to Users model
    # self.env.lang: Current language code (en_US)
    '''

    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code', default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string='Result')

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = str(
                safe_eval(self.code.strip(), {'self': model})
            )
        except Exception as e:
            self.result = str(e)
