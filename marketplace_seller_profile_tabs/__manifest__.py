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

{
  "name"                 :  "Odoo Marketplace Seller Profile Tabs",
  "summary"              :  "Provide marketplace seller Tabs Option for describing seller's other details on seller profile.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Profile-Tabs.html",
  "description"          :  "https://webkul.com/blog/odoo-marketplace-seller-profile-tabs/",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_profile_tabs&version=10.0&lifetime=120&lout=1&custom_url=/",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                                'security/marketplace_security.xml',
                                'security/ir.model.access.csv',
                                'data/profile_tab_data.xml',
                                'views/marketplace_config_view.xml',
                                'views/res_partner_views.xml',
                                'views/profile_tabs.xml',
                                'views/template.xml',

                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  45.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
