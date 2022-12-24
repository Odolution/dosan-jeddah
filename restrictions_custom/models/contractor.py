from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class Inherit_PurchaseReq(models.Model):
    _inherit = "purchase.requisition.line"
    contractor = fields.Many2one(
        'res.partner', string="Contractor", domain="[('category_id', '=', 6)]")


class Inherit_PurchaseRequi(models.Model):
    _inherit = "purchase.requisition"
    project_lv = fields.Char(string="Project", compute="site_req_projcet")

    def site_req_projcet(self):
        for rec in self:
            if rec.line_ids:
                for i in rec.line_ids:
                    #rec.project_lv = i.account_analytic_id.name
                    PRL = self.env['account.analytic.account'].search(
                        [('id', '=', i.account_analytic_id.id)])
                    rec["project_lv"] = PRL.name
                    #raise UserError(PRL.name)

    # def site_req_projcet(self):
    #     site_req = self.env['purchase.requisition'].search([()])
    #     for rec in site_req:
    #         if rec.line_ids:
    #             for i in rec.line_ids:
    #                 if i.account_analytic_id:
    #                     rec['project_lv'] = i.account_analytic_id.name
    #                 else:
    #                     rec['project_lv'] = "-"

    def create_aljazira_rfq(self):
        aljazira = self.env['res.partner'].search([('id', "=", 15)])
        for record in self:
            if record.vendor_id == aljazira and record.order_count == 0:

                new_rfq = self.env['purchase.order'].create({
                    'state': 'draft',
                    'requisition_id': self.id,
                    'partner_id': self.vendor_id.id,
                    'currency_id': self.currency_id.id,
                    'date_planned': datetime.today(),
                    'date_order': datetime.today(),
                    'po_type': self.po_type_site,



                })
                for mov_id in self.line_ids:
                    rfq_lines = self.env['purchase.order.line'].create({
                        'order_id': new_rfq.id,
                        'product_id': mov_id.product_id.id,
                        'product_onhand_po': mov_id.product_onhand,
                        'product_code_po': mov_id.product_code,
                        'name': mov_id.product_id.name,
                        'product_qty': mov_id.product_qty,
                        'price_unit': mov_id.product_id.lst_price,
                        'account_analytic_id': mov_id.account_analytic_id.id,
                        'date_planned': datetime.today(),
                        'price_subtotal': mov_id.product_qty*mov_id.price_unit,


                    })
