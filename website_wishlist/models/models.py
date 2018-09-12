# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models, tools, _


class Users(models.Model):
    _inherit = 'res.users'

    @api.multi
    def add_product(self, template_id):
        User = self.env.user
        if User.partner_id:
            vals = {
                'template_id': template_id,
                'partner_id':User.partner_id.id,
                'user_id': User.id,
            }
            self.env['website.wishlist'].create(vals)
            if User.partner_id.website_wishlist:
                return len(User.partner_id.website_wishlist)
        return False

    @api.multi
    def remove_product(self, template_id):
        User = self.env.user
        if User.partner_id:
            wishlist_line_obj = self.env['website.wishlist'].search([('template_id','=',template_id),('partner_id','=',User.partner_id.id)])
            if wishlist_line_obj:
                wishlist_line_obj.sudo().unlink()
                if User.partner_id.website_wishlist:
                    return len(User.partner_id.website_wishlist)
        return False


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def get_wishlist_products(self):
        User = self.env.user
        if User.partner_id.website_wishlist:
            return User.partner_id.website_wishlist
        return []

    @api.multi
    def check_wishlist_product(self):
        User, product_ids = self.env.user, []
        if User.partner_id.website_wishlist:
            for wishlist_line in User.partner_id.website_wishlist:
                product_ids.append(wishlist_line.template_id.id)
            if product_ids:
                return product_ids
        return []

    @api.multi
    def get_user_wl_products(self):
        user_wishlist_products = []
        for wishlist in self.env.user.partner_id.website_wishlist:
            if wishlist:
                user_wishlist_products.append(
                    wishlist.template_id.product_tmpl_id)
        return user_wishlist_products


class Partner(models.Model):
    _inherit = 'res.partner'

    website_wishlist = fields.One2many('website.wishlist','partner_id', string='Wishlist')


class WebsiteWishlist(models.Model):
    _name = "website.wishlist"

    @api.model
    def create(self, vals):
        if vals.has_key('template_id') and vals.has_key('partner_id'):
            check = self.search([('template_id','=',vals['template_id']),('partner_id','=',vals['partner_id'])])
            if check:
                return check[0]
        return super(WebsiteWishlist, self).create(vals)

    @api.multi
    def get_wishlist_products(self):
        User = self.env.user
        if User.partner_id.website_wishlist:
            return User.partner_id.website_wishlist
        return False

    template_id = fields.Many2one('product.product',string='Product')
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Integer(string='User ID')

