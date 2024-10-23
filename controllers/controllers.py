# -*- coding: utf-8 -*-
# from odoo import http


# class WaaneizaPurchaseCashier(http.Controller):
#     @http.route('/waaneiza_purchase_cashier/waaneiza_purchase_cashier', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/waaneiza_purchase_cashier/waaneiza_purchase_cashier/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('waaneiza_purchase_cashier.listing', {
#             'root': '/waaneiza_purchase_cashier/waaneiza_purchase_cashier',
#             'objects': http.request.env['waaneiza_purchase_cashier.waaneiza_purchase_cashier'].search([]),
#         })

#     @http.route('/waaneiza_purchase_cashier/waaneiza_purchase_cashier/objects/<model("waaneiza_purchase_cashier.waaneiza_purchase_cashier"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('waaneiza_purchase_cashier.object', {
#             'object': obj
#         })

