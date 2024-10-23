# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'utm.mixin']

    pur_req_id = fields.One2many('waaneiza.cashier.cash.req','pur_inv_id',string="Purchase CashRequisition", index=True, copy=False, store=True, readonly=False)
    req_count = fields.Integer(compute="_compute_req_count", string='Requestion Counts', copy=False, default=0, store=True)
    req_ids = fields.Many2many('waaneiza.cashier.cash.req', compute="_compute_req_count", string='Cash Requestion', copy=False, store=True)
    # state = fields.Selection(selection_add=[('requestion', 'Cash Requestion'),('cashdraw', 'Cash Drawing'),('settlement', 'Purchase Settlement')],tracking=True, ondelete={'requestion': 'cascade','cashdraw': 'cascade','settlement': 'cascade'})

    def action_pur_req(self):
        # self.write({'state': 'requestion'})
        return {
            'res_model': 'waaneiza.cashier.cash.req',
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_cash_req_form_view").id,
            'target': 'self.'
        }
    
    @api.depends('pur_req_id')
    def _compute_req_count(self):
        for count in self:
            counts = count.mapped('pur_req_id')
            count.req_ids = counts
            count.req_count = len(counts)
    
    def action_view_pur_req(self, counts=False, context=None):
        if not counts:
            counts = self.req_ids
        if len(counts) > 1:
            result = self.env['ir.actions.act_window']._for_xml_id('waaneiza_purchase_cashier.action_purchase_requestion')
            result['domain'] = [('id', 'in', counts.ids)]
            return result

        elif len(counts) == 1:
            return {
            'res_model': 'waaneiza.cashier.cash.req',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_cash_req_form_view").id,
            'target': 'self.',
            'res_id': counts.id
        }
    
    # def action_pur_cashdraw(self):
    #     if self.req_count != 0:
    #         self.write({'state': 'cashdraw'})
    
    # def action_pur_settlement(self):
    #     # self.write({'state': 'settlement'})
    #     return {
    #         'res_model': 'waaneiza.exp.sett',
    #         'type': 'ir.actions.act_window',
    #         'tag': 'reload',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_settlement_form_view").id,
    #         'target': 'self.'
    #     }