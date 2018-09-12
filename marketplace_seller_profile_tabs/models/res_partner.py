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

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _get_seller_profile_tab_group_info(self):
        for obj in self:
            product_variant_group = self.env.ref('marketplace_seller_profile_tabs.mp_seller_profile_tab_group')
            user_obj = self.env["res.users"].sudo().search([('partner_id', '=', obj.id)])
            user_groups = user_obj.read(['groups_id'])
            if user_groups and user_groups[0].get("groups_id"):
                user_groups_ids = user_groups[0].get("groups_id")
                if product_variant_group.id in user_groups_ids:
                    obj.allow_profile_tabs = True
            else:
                obj.allow_profile_tabs = False

    allow_profile_tabs = fields.Boolean(compute="_get_seller_profile_tab_group_info", string="Allow Profile Tabs", help="Allow seller to create additional profile tabs to display extra on website.")
    seller_profile_tab_ids = fields.One2many(comodel_name='seller.profile.tabs', inverse_name='marketplace_seller_id', string='Profile Tabs')

    @api.multi
    def enable_profile_tabs_group(self):
        for obj in self:
            user = self.env["res.users"].sudo().search(
                [('partner_id', '=', obj.id)])
            if user:
                # Add seller to profile tabs group
                group = self.env.ref('marketplace_seller_profile_tabs.mp_seller_profile_tab_group')
                if group:
                    group.sudo().write({"users": [(4, user.id, 0)]})

    @api.multi
    def disable_profile_tabs_group(self):
        for obj in self:
            user = self.env["res.users"].sudo().search(
                [('partner_id', '=', obj.id)])
            if user:
                # Remove seller from profile tabs group
                group = self.env.ref('marketplace_seller_profile_tabs.mp_seller_profile_tab_group')
                if group:
                    group.sudo().write({"users": [(3, user.id, 0)]})
