# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import datetime, timezone, timedelta,date

class CreateAppointmentWiz(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment"

    date_appoint = fields.Date(string='Date', required=True)
    patient_id = fields.Many2one('hospital.patient',
                                 string='Patient', required=True,
                                 domain=[('state', 'in', ['draft', 'confirm'])])

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWiz, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        res['date_appoint'] = date.today()
        return res

    def create_appointment_action(self):
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appoint,
        }
        self.env['hospital.appointment'].create(vals)

    def action_appointment_view(self):
        action = self.env.ref('hospital.action_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action


