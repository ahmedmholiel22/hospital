# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError


class Appointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _order = "name desc"

    name = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one(
        'hospital.patient',
        string='Patient',
        required=True,
        ondelete='restrict'
    )
    doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Doctor'
    )
    age = fields.Integer(
        string='Age',
        related='patient_id.age',
        tracking=True
    )
    note = fields.Text(
        string='Description'
    )
    prescription = fields.Text(
        string='prescription'
    )
    date_appointment = fields.Date(
        string='Date'
    )
    date_checkup = fields.Datetime(
        string='check up time'
    )
    gender = fields.Selection([
        ('male', 'male'),
        ('female', 'female')
    ], required=True,
        default='male',
        invisible="1"
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        default='draft',
        string="status"
    )

    prescription_lines_ids = fields.One2many(
        'appointment.prescription.lines', 'appointment_id',
        string="Prescription Lines"
    )
    hide_sales_price = fields.Boolean(
        string="Hide Sales Price"
    )
    company_id = fields.Many2one('res.company',
                                 string='Company'
                                 )
    sequence_id = fields.Many2one(
        'ir.sequence', 'Reference Sequence',
        check_company=True, copy=False)




    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'new patient'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(Appointment, self).create(vals)
        return res

    @api.model
    def create(self, vals):
        if not vals.get('sequence_id'):
            if vals.get('patient_id') and vals.get('doctor_id'):
                patient_rec = self.env['hospital.patient'].browse(vals['patient_id'])
                doctor_rec = self.env['hospital.doctor'].browse(vals['doctor_id'])
                vals['sequence_id'] = self.env['ir.sequence'].sudo().create({
                    'name': patient_rec.name + ' ' + _('Sequence') + ' ' + doctor_rec.doctor_name,
                    'prefix': 'Appointment' + '/', 'padding': 5,
                    'company_id': vals['company_id'] or self.env.company.id
                }).id
            else:
                vals['sequence_id'] = self.env['ir.sequence'].sudo().create({
                    'name': _('Sequence') + ' ' + vals['name'],
                    'prefix': 'Appointment', 'padding': 5,
                    'company_id': vals.get('company_id') or self.env.company.id,
                }).id

        appoint_type = super(Appointment, self).create(vals)
        return appoint_type

    @api.model
    def _name_search(self, age, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if age:
            domain = ['|', ('note', operator, age), ('date_appointment', operator, age)]
        return self._search(domain, args, limit=limit, access_rights_uid=name_get_uid)

    def write(self, data):
        res = super(Appointment, self).write(data)
        sl_no = 0
        for line in self.prescription_lines_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res

    def action_print_record(self):
        record = self.env['hospital.patient'].search([('age', '>', 50)])
        for rec in record:
            rec.name = 'old Patient'
        print(record)

    @api.onchange('patient_id')
    def onchange_gender(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note

        else:
            self.gender = ''
            self.note = ''






    def unlink(self):
        patient_rec = self.mapped('patient_id')
        if self.state == 'done':
            raise ValidationError(_('Cannot Delete %s it is in Done state') % self.name)
        super(Appointment, self).unlink()
        return patient_rec.unlink()

    def unlink(self):
        appoint_rec = self.mapped('patient_id')
        super(Appointment, self).unlink()

        return appoint_rec.unlink()


    @api.returns('self', lambda x : x.id)
    def copy(self, default=None):
        if not default:
            default = {}
            default['age'] = self.name + "years"

        return super(Appointment, self).copy(default=default)



class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    sl_no = fields.Integer(string="SNO.")
    product_id = fields.Many2one('product.product', required=True)
    unit_price = fields.Float(related='product_id.list_price', string="Unit Price")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
