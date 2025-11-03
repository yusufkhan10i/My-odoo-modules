from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class CollegeStudent(models.Model):
    _name = "college.student"
    _description = "College Student"
