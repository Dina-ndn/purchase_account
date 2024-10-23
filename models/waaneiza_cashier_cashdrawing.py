# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WaaneizaCashierCashdrawing(models.Model):
    _name = 'waaneiza.cashier.cashdrawing'
    _inherit = ['waaneiza.cashier.cashdrawing']

    pur_expense_id = fields.Many2one('waaneiza.pur.sett',string="Expense Settlement", index=True, store=True)
    pur_expense_lines = fields.One2many('waaneiza.pur.sett','cash_drawing_srn',string="Expense Settlement Lines", index=True, copy=False, store=True, readonly=False)
    pur_expense_ids = fields.Many2many('waaneiza.pur.sett', compute="_compute_sett_count", string='Expense', copy=False, store=True)
    pur_expense_count = fields.Integer(compute="_compute_sett_count", string='Expense Count', copy=False, default=0, store=True)
    pur_inv_id = fields.Many2one('account.move',string='Vendor Bill Invoice')

    @api.onchange('requisition_id')
    def _onchange_pur_req(self):
        for rec in self:
            if rec.requisition_id.pur_inv_id:
                # rec.amount = rec.requisition_id.total_amount
                rec.type_of_cashdrawing_select = 'PCO'
            else:
                pass

    def action_done(self):
        self.state = "done"
        self.requisition_id.pur_inv_id.state = 'cashdraw'

    @api.depends('pur_expense_lines')
    def _compute_sett_count(self):
        for order in self:
            count = order.mapped('pur_expense_lines')
            order.pur_expense_ids = count
            order.pur_expense_count = len(count)
    
    def action_view_pur_expense(self, invoices=False, context=None):
        if not invoices:
            # Invoice_ids may be filtered depending on the user. To ensure we get all
            # invoices related to the purchase order, we read them in sudo to fill the
            # cache.
            # self.sudo()._read(['invoice_ids'])
            invoices = self.pur_expense_ids
        if len(invoices) > 1:
            result = self.env['ir.actions.act_window']._for_xml_id('waaneiza_purchase_cashier.action_purchase_settlement')
            result['domain'] = [('id', 'in', invoices.ids)]
            return result

        elif len(invoices) <= 1:
            return {
            'res_model': 'waaneiza.pur.sett',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_settlement_form_view").id,
            'target': 'self.',
            'res_id': invoices.id
        }

    def action_pur_settlement(self):
        return {
            'res_model': 'waaneiza.pur.sett',
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_settlement_form_view").id,
            'target': 'self.'
        }
