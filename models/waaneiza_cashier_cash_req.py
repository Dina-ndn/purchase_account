# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WaaneizaCashierCashReq(models.Model):
    _name = 'waaneiza.cashier.cash.req'
    _inherit = ['waaneiza.cashier.cash.req']

    pur_inv_id = fields.Many2one('account.move',string='Vendor Bill Invoice')
    # pur_order_id = fields.Many2one('purchase.order',string='Purchase Order')
    pur_order_name = fields.Char(string='Purchase Order',store=True,index=True,readonly=True)
    pur_order_name_test = fields.Char(string='Purchase Order Code',store=True,index=True,readonly=True)

    @api.onchange('pur_inv_id')           
    def _onchange_pur_inv(self):
        for rec in self:
            rec.pur_order_name = rec.pur_inv_id.invoice_origin
            if rec.pur_inv_id.id > 0:
                # rec.e_id=rec.cash_sale_id.emp_id_info
                rec.company_id = rec.pur_inv_id.company_id.id
                # rec.pur_order_name = rec.pur_inv_id.invoice_origin
                rec.pur_order_name_test = rec.pur_order_name
                rec.pur_inv_id = rec.pur_inv_id.id
                for line in rec.pur_inv_id:
                    rec.requisition_details_lines = [(0,0,{
                        'sr_number':'1',
                        'amount':line.amount_total,
                        'currency':line.currency_id.id,
                        'remarks':'Cash Requestion for Product Purchase',
                    })]
                # rec.requested_by_process = rec.pur_inv_id.partner_id.id
            else:
                pass
    
    def action_done(self):
        self.state = "done"
        self.pur_inv_id.state = 'requisition'
    
    def action_purchase_cashdraw(self):
        return {
            'res_model': 'waaneiza.cashier.cashdrawing',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_cashdrawing_form_view").id,
            'target': 'self.'
        }
    
    ############### Start Count Cashdrawing ###############
    
    def action_view_pur_cashdrawing(self, counts=False, context=None):
        if not counts:
            # Invoice_ids may be filtered depending on the user. To ensure we get all
            # counts related to the purchase order, we read them in sudo to fill the
            # cache.
            # self.sudo()._read(['cashdrawing_ids'])
            counts = self.cashdrawing_ids
        if len(counts) > 1:
            result = self.env['ir.actions.act_window']._for_xml_id('waaneiza_purchase_cashier.action_waaneiza_purchase_cashdrawing')
            result['domain'] = [('id', 'in', counts.ids)]
            return result

        elif len(counts) <= 1:
            return {
            'res_model': 'waaneiza.cashier.cashdrawing',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_purchase_cashier.purchase_cashdrawing_form_view").id,
            'target': 'self.',
            'res_id': counts.id
        }

    ############### End Count Cashdrawing ###############
    
    