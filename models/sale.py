# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_description = fields.Char(string='Sale Description')
    confirmed_user_id = fields.Many2one('res.users',
                                        string='Confirmed User')
    test = fields.Boolean(compute='_compute_test_delivery', string='Test')

    def _compute_test_delivery(self):
        for rec in self:
            record = rec.env['stock.picking'].search(
                [('origin', '=', rec.name)])
            if record['state'] == 'done':
                rec.test = True
            else:
                rec.test = False


    def action_confirm(self):
        print("success................")
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id

