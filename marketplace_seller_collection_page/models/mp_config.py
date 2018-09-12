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

from odoo import models,fields,api,_

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = 'marketplace.config.settings'

    group_allow_seller_for_collection = fields.Boolean(
        string= "Enable to allow Seller to Make Product Collections",
        group= 'odoo_marketplace.marketplace_seller_group',
        implied_group= 'marketplace_seller_collection_page.group_for_mp_collections',
    )

    @api.one
    def set_default_values(self):
        res = super(MarketplaceConfigSettings, self).set_default_values()
        self.env['ir.values'].sudo().set_default(
            'marketplace.config.settings', 'group_allow_seller_for_collection', self.group_allow_seller_for_collection)
        return res

    @api.model
    def get_default_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_default_values()
        group_allow_seller_for_collection = self.env['ir.values'].get_default(
                'marketplace.config.settings', 'group_allow_seller_for_collection')
        res.update({
            'group_allow_seller_for_collection':group_allow_seller_for_collection,
        })
        return res
