# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError
from datetime import datetime, timezone, timedelta,date
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = "id desc"


    name = fields.Char(
        string='Name',
        required=True
    )
    reference = fields.Char(
        string='Patient Reference',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    date_of_birth = fields.Datetime(
        string='Date Of Birth',
    )
    due_date = fields.Date(
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('elzhor_hospital.due_date')
    )

    age = fields.Integer(
        string='Age',
        tracking=True,
        compute='_compute_age',
        search='_search_age',
        inverse='_inverse_compute_age',
        store='True'
    )

    gender = fields.Selection([
        ('male', 'male'),
        ('female', 'female')
    ], required=True,
        default='male',
        invisible="1"
    )
    note = fields.Text(
        string='Description'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        default='draft',
        string="status"
    )
    responsible_id = fields.Many2one(
        'res.partner',
        string='Responsible'
    )
    appointment_count = fields.Integer(
        string='Appointment Count',
        compute='_compute_appointment_count',
        store=True
        )
    image = fields.Image(
        string='Image'
    )
    appointment_ids = fields.One2many(
        'hospital.appointment',
        'patient_id',
        string="Appointments"
    )
    color = fields.Integer(
        string='Color',
    )

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'new patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')

        res = super(HospitalPatient, self).create(vals)
        return res

    @api.depends('appointment_ids') #used depends becase attribute store=True in the field appointment_count
    def _compute_appointment_count(self):
        for rec in self:
          appointment_count = self.env["hospital.appointment"].search_count([('patient_id', '=', rec.id)])
          rec.appointment_count = appointment_count


    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'


    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s - %s]' % (rec.name, rec.id)))
        return res



    
    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['gender'] = 'male'
        res['note'] = 'the default description'
        return res




    @api.depends('date_of_birth')
    def _compute_age(self):
        age_now = date.today().year
        for rec in self:
            if not rec.date_of_birth:
                rec.age = 0
            else:
                rec.age = age_now - rec.date_of_birth.year

    @api.depends('date_of_birth')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        print("start year........" , start_of_year)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]




    # @api.constrains('name')
    # def check_name(self):
    #     for rec in self:
    #         res = self.env["hospital.patient"].search([('name', '=', 'rec.name'), ('id', '=', 'rec.id')]
    #         if res:
    #             raise ValidationError(_("Name % Already exists." %rec.name))

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                    raise ValidationError(_("Age Cannot Be Zero"))


    def preview_open_appointment(self):
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',

            }

    def action_rainbow(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successful',
                'type': 'rainbow_man',
            }
        }

