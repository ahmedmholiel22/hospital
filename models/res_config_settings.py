# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(
        string='cancel days',
        config_parameter='hospital.cancel_days'
    )

    due_date = fields.Datetime(
        string='Date Of Birth',
        config_parameter='hospital.due_date'
    )