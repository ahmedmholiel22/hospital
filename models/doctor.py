# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["mail.thread", 'mail.activity.mixin']  # belongs to chatter
    _description = "Hospital Doctor"
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', tracking=True)

    gender = fields.Selection([
        ('male', 'male'),
        ('female', 'female')
    ], required=True, default='male', invisible="1")
    note = fields.Text(string='Description')
    image = fields.Image(string='Image')


    def copy(self, default=None):
        if  default is None:
            default = {}
        if not default.get(self.doctor_name):
            default['doctor_name'] = _("%s (Copy)", self. doctor_name)

        return super(HospitalDoctor, self).copy(default)

