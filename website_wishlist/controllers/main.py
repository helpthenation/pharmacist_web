# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import http, tools, _
import werkzeug

from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_portal.controllers.main import website_account
import re

import logging
_logger = logging.getLogger(__name__)



class website_account(website_account):

    @http.route(['/my/list'], type='http', auth="user", website=True)
    def portal_my_lists(self, **kw):
        return request.render("website_wishlist.pp_portal_my_list", {"wishlist": True})

        
class WebsiteWishlist(http.Controller):

    @http.route(['/wishlist'], type='http', auth="public", website=True)
    def wishlist(self, **post):        
        values = {
            'wishlist': request.env['website.wishlist'].get_wishlist_products() 
            }
        return http.request.render("website_wishlist.wishlist", values)



    @http.route('/wishlist/add_to_wishlist', type='json', auth='public', website=True)
    def add_to_wishlist(self, product, *args, **kwargs):
        add = request.env['res.users'].add_product(int(product))
        return add

    @http.route('/wishlist/remove_from_wishlist', type='json', auth='public', website=True)
    def remove_from_wishlist(self, product, *args, **kwargs):
        remove = request.env['res.users'].remove_product(int(product))
        return remove


    @http.route(['/wishlist/move_to_cart'], type='json', auth="public", methods=['POST'], website=True)
    def move_to_cart(self, product_id, line_id=None, add_qty=1, set_qty=None, display=True):
        # remove from wishlist part is missing
        order = request.website.sale_get_order(force_create=1)
        value = order._cart_update(product_id=int(product_id), line_id=line_id, add_qty=add_qty, set_qty=set_qty)
        if not display:
            return None
        value['cart_quantity'] = order.cart_quantity
        value['website_sale.total'] = request.website._render("website_sale.total", {
                'website_sale_order': request.website.sale_get_order()
            })
        return value

