# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = "Marketplace Product Template"

    def _get_default_category_id(self):
        if self.marketplace_seller_id:
            mp_categ = self.env['marketplace.config.settings'].sudo().get_default_values().get('internal_categ')
            if mp_categ:
                return mp_categ.id
        elif self._context.get("pass_default_categ"):
            return False
        return super(ProductTemplate, self)._get_default_category_id()

    @api.model
    def _set_seller_id(self):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return user_obj.partner_id.id
        return self.env['res.partner']

    @api.model
    def _set_product_state(self):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return "draft"
        return False

    @api.model
    def _get_pending_qty_request(self):
        for obj in self:
            mp_stock_obj = self.env["marketplace.stock"].search(
                [('product_temp_id', '=', obj.id), ('state', '=', 'requested')])
            obj.pending_qty_request = True if mp_stock_obj else False

    categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, default=_get_default_category_id,
        required=True, help="Select category for the current product")
    status = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), (
        'approved', 'Approved'), ('rejected', 'Rejected')], "Marketplace Status", default=_set_product_state, copy=False, track_visibility='onchange')
    qty = fields.Float(string="Initial Quantity",
                       help="Initial quantity of the product which you want to update in warehouse for inventory purpose.", copy=False)
    template_id = fields.Many2one(
        "product.template", string="Product Template Id", copy=False)
    marketplace_seller_id = fields.Many2one(
        "res.partner", string="Seller", default=_set_seller_id, copy=False, track_visibility='onchange', help="If product has seller then it will consider as marketplace product else it will consider as simple product.")
    color = fields.Integer('Color Index')
    pending_qty_request = fields.Boolean(
        string="Request Pending", compute=_get_pending_qty_request)

    @api.onchange("marketplace_seller_id")
    def onchange_seller_id(self):
        self.status = "draft" if self.marketplace_seller_id and not self.status else False
        self.categ_id = self.env['marketplace.config.settings'].sudo().get_default_values().get('internal_categ')

    @api.multi
    def toggle_website_published(self):
        """ Inverse the value of the field ``website_published`` on the records in ``self``. """
        for record in self:
            record.website_published = not record.website_published

    @api.multi
    def auto_approve(self):
        for obj in self:
            if obj.marketplace_seller_id.auto_product_approve:
                obj.write({"status": "pending"})
                obj.sudo().approved()
            else:
                obj.write({"status": "pending"})
        return True

    @api.multi
    def approved(self):
        for obj in self:
            if not obj.marketplace_seller_id:
                raise Warning(
                    _("Marketplace seller id is not assign to this product."))
            if obj.marketplace_seller_id.state == "approved":
                obj.write({"sale_ok": True})
                obj.set_initial_qty()
                obj.sudo().write({"status": "approved"})
                template = self.env['mail.template']
                config_setting_obj = self.env[
                    'marketplace.config.settings'].sudo().get_default_values()
                if config_setting_obj["enable_notify_admin_on_product_approve_reject"] and config_setting_obj.has_key("notify_admin_on_product_approve_reject") and config_setting_obj["notify_admin_on_product_approve_reject"]:
                    # Notify to admin by admin when product approved
                    temp_id = config_setting_obj[
                        "notify_admin_on_product_approve_reject"]
                    if temp_id:
                        template.browse(temp_id).send_mail(obj.id, True)
                if config_setting_obj["enable_notify_seller_on_product_approve_reject"] and config_setting_obj.get("notify_seller_on_product_approve_reject", False):
                    # Notify to Seller by admin  when product approved
                    temp_id2 = config_setting_obj[
                        "notify_seller_on_product_approve_reject"]
                    if temp_id2:
                        template.browse(temp_id2).send_mail(obj.id, True)
            else:
                raise Warning(
                    _("Marketplace seller of this product is not approved."))
        return True

    @api.multi
    def reject(self):
        for product_obj in self:
            if product_obj.status in ("draft", "pending", "approved") and product_obj.marketplace_seller_id:
                product_obj.write(
                    {"sale_ok": False, "website_published": False, "status": "rejected"})
                template = self.env['mail.template']
                config_setting_obj = self.env[
                    'marketplace.config.settings'].sudo().get_default_values()
                if config_setting_obj["enable_notify_admin_on_product_approve_reject"] and config_setting_obj.has_key("notify_admin_on_product_approve_reject") and config_setting_obj["notify_admin_on_product_approve_reject"]:
                    # Notify to admin by admin  when product rejected
                    temp_id = config_setting_obj[
                        "notify_admin_on_product_approve_reject"]
                    if temp_id:
                        template.browse(temp_id).send_mail(product_obj.id, True)
                if config_setting_obj["enable_notify_seller_on_product_approve_reject"] and config_setting_obj.get("notify_seller_on_product_approve_reject", False):
                    # Notify to Seller by admin  when product rejected
                    temp_id2 = config_setting_obj[
                        "notify_seller_on_product_approve_reject"]
                    if temp_id2:
                        template.browse(temp_id2).send_mail(product_obj.id, True)

    # Called in server action
    @api.multi
    def approve_product(self):
        for product_obj in self:
            if product_obj.status == "pending" and product_obj.marketplace_seller_id:
                product_obj.approved()
                # product_obj.write({"status": "approved"})

    # Called in server action
    @api.multi
    def reject_product(self):
        for product_obj in self:
            if product_obj.status in ("draft", "pending", "approved") and product_obj.marketplace_seller_id:
                # product_obj.write({"status": "rejected"})
                product_obj.reject()


    @api.model
    def create(self, vals):
        ''' Set default false to sale_ok and purchase_ok for seller product'''
        partner = self.env["res.partner"].sudo().browse(vals.get("marketplace_seller_id", False)) or self.env.user.partner_id
        if partner and partner.sudo().seller:
            if not vals.get("sale_ok", False):
                vals["sale_ok"] = False
            if not vals.get("purchase_ok", False):
                vals["purchase_ok"] = False
            vals["type"] = "product"
            if not vals.get("status", False):
                vals["status"] = "draft"
            config_setting_obj = self.env[
                'marketplace.config.settings'].sudo().get_default_values()
            if config_setting_obj['internal_categ']:
                vals["categ_id"] = config_setting_obj['internal_categ']
        product_template = super(ProductTemplate, self).create(vals)
        return product_template

    @api.multi
    def set_initial_qty(self):
        for template_obj in self:
            if len(self) == 1:
                if template_obj.qty < 0:
                    raise Warning(_('Initial Quantity can not be negative'))
            if not template_obj.marketplace_seller_id.location_id:
                raise Warning(_("Seller has no location/warehouse."))
            if template_obj.qty > 0:
                vals = {
                    'product_id': template_obj.product_variant_ids[0].id,
                    'product_temp_id': template_obj.id,
                    'new_quantity': template_obj.qty,
                    'location_id': template_obj.marketplace_seller_id.location_id.id or False,  # Phase 2
                    'note': _("Initial Quantity."),
                    'state': "requested",
                }
                mp_product_stock = self.env['marketplace.stock'].create(vals)
                mp_product_stock.auto_approve()

    def disable_seller_all_products(self, seller_id):
        if seller_id:
            product_objs = self.search(
                [("marketplace_seller_id", "=", seller_id), ("status", "not in", ["draft", "rejected"])])
            product_objs.reject()

    @api.multi
    def set_pending(self):
        for rec in self:
            rec.auto_approve()

    @api.multi
    def send_to_draft(self):
        for rec in self:
            rec.write({"status": "draft"})

    @api.multi
    def write(self, vals):
        if vals.get("marketplace_seller_id", False):
            for rec in self:
                if rec.marketplace_seller_id and rec.status not in ["draft", "pending"]:
                    raise UserError(_('You cannot change the seller of the product that already contains seller.'))
        return super(ProductTemplate, self).write(vals)

    @api.multi
    def mp_action_view_sales(self):
        self.ensure_one()
        action = self.env.ref('odoo_marketplace.wk_seller_slae_order_line_action')
        product_ids = self.product_variant_ids.ids
        tree_view_id = self.env.ref('odoo_marketplace.wk_seller_product_order_line_tree_view')
        form_view_id = self.env.ref('odoo_marketplace.wk_seller_product_order_line_form_view')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
            'target': action.target,
            'context': "{'default_product_id': " + str(product_ids[0]) + "}",
            'res_model': action.res_model,
            'domain': [('state', 'in', ['sale', 'done']), ('product_id.product_tmpl_id', '=', self.id)],
        }

    @api.multi
    def pending_qty_stock_request(self):
        for rec in self:
            pending_stock = self.env["marketplace.stock"].search([('product_temp_id','=',rec.id),('state','=','requested')])
            return {
                'name':'Update Marketplace Product Quantity',
                'type':'ir.actions.act_window',
                'res_model':'marketplace.stock',
                'view_mode':'form',
                'view_type':'form',
                'res_id' : pending_stock[0].id,
                'target':'current',
            }

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def toggle_website_published(self):
        """ Inverse the value of the field ``website_published`` on the records in ``self``. """
        for record in self:
            record.product_tmpl_id.toggle_website_published()

    @api.multi
    def mp_action_view_sales(self):
        self.ensure_one()
        action = self.env.ref('odoo_marketplace.wk_seller_slae_order_line_action')
        tree_view_id = self.env.ref('odoo_marketplace.wk_seller_product_order_line_tree_view')
        form_view_id = self.env.ref('odoo_marketplace.wk_seller_product_order_line_form_view')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
            'target': action.target,
            'context': "{'default_product_id': " + str(self.id) + "}",
            'res_model': action.res_model,
            'domain': [('state', 'in', ['sale', 'done']), ('product_id', '=', self.id)],
        }

    @api.multi
    def pending_qty_stock_request(self):
        for rec in self:
            pending_stock = self.env["marketplace.stock"].search([('product_id','=',rec.id),('state','=','requested')])
            return {
                'name':'Update Marketplace Product Quantity',
                'type':'ir.actions.act_window',
                'res_model':'marketplace.stock',
                'view_mode':'form',
                'view_type':'form',
                'res_id' : pending_stock[0].id,
                'target':'current',
            }
