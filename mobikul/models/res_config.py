# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

class MobikulConfigSettings(models.TransientModel):
	_name = 'mobikul.config.settings'
	_inherit = 'res.config.settings'

	def _default_mobikul(self):
		return self.env['mobikul'].search([], limit=1)

	def _default_order_mail_template(self):
		return self.env.ref('sale.email_template_edi_sale').id

	def open_mobikul_conf(self):
		return {
				'type': 'ir.actions.act_window',
				'name': 'Mobikul-App Configuration',
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'mobikul',
				'res_id': self.mobikul_app.id,
				'target': 'current',
			}

	# @api.multi
	def open_default_user(self):
		action = self.env.ref('base.action_res_users').read()[0]
		action['context'] = self.env.context
		action['res_id'] = self.env.ref('base.default_user').id
		action['views'] = [[self.env.ref('base.view_users_form').id, 'form']]
		return action

	mobikul_app = fields.Many2one('mobikul', string="Mobikul APP", default=_default_mobikul, required=True)
	app_name = fields.Char('App Name', related='mobikul_app.name')
	product_limit = fields.Integer('Limit Products per page', related='mobikul_app.product_limit')
	# color_scheme = fields.Selection(related='mobikul_app.color_scheme', string='Choose Combination')
	module_email_verification = fields.Boolean(related='mobikul_app.email_verify', string='Verify Email on signUp')
	salesperson_id = fields.Many2one('res.users', related='mobikul_app.salesperson_id', string='Salesperson')
	salesteam_id = fields.Many2one('crm.team', related='mobikul_app.salesteam_id', string='Sales Team')
	default_lang = fields.Many2one('res.lang', related='mobikul_app.default_lang', string='Default Language')
	currency_id = fields.Many2one('res.currency', related='mobikul_app.currency_id', string='Default Currency')
	pricelist_id = fields.Many2one('product.pricelist', related='mobikul_app.pricelist_id', string='Default Pricelist')
	# module_auth_oauth = fields.Boolean(string='Use external authentication providers (OAuth)')
	mobikul_reset_password = fields.Boolean(string='Enable password reset', help="This allows users to trigger a password reset from App")
	mobikul_signup = fields.Boolean(string='Enable customer sign up')
	mobikul_allow_guest = fields.Boolean(string='Allow Guests to view products on App.')
	mobikul_signup_template_user_id = fields.Many2one('res.users', string='Template user for new users created through App')
	module_auth_oauth = fields.Boolean(string='Allow social login (Gmail,Facebook,etc)', help="Use external authentication providers (OAuth)")
	mobikul_gmail_signin = fields.Boolean(string='Gmail SignIn')
	mobikul_facebook_signin = fields.Boolean(string='Facebook SignIn')
	mobikul_twitter_signin = fields.Boolean(string='Twitter SignIn')
	module_website_wishlist = fields.Boolean(string='Allow Wishlist feature on App.', help="Use external Addon to add wishlist feature in website")
	module_wk_review = fields.Boolean(string='Allow Product Review feature on App.', help="Use external Addon to add review feature in website")
	module_odoo_marketplace = fields.Boolean(string='Allow Odoo Marketplace on App.', help="Use external Addon to add Multi Vendor Marketplace in website")



	@api.model
	def get_default_auth_signup_template_user_id(self, fields):
		IrConfigParam = self.env['ir.config_parameter']
		# we use safe_eval on the result, since the value of the parameter is a nonempty string
		return {
			'mobikul_reset_password': safe_eval(IrConfigParam.get_param('auth_signup.reset_password', 'False')),
			'mobikul_signup': safe_eval(IrConfigParam.get_param('auth_signup.allow_uninvited', 'False')),
			'mobikul_signup_template_user_id': safe_eval(IrConfigParam.get_param('auth_signup.template_user_id', 'False')),
			'mobikul_allow_guest': safe_eval(IrConfigParam.get_param('mobikul.allow_guest', 'False')),
			'mobikul_gmail_signin': safe_eval(IrConfigParam.get_param('mobikul.gmail_signin', 'False')),
			'mobikul_facebook_signin': safe_eval(IrConfigParam.get_param('mobikul.facebook_signin', 'False')),
			'mobikul_twitter_signin': safe_eval(IrConfigParam.get_param('mobikul.twitter_signin', 'False')),
		}

	@api.multi
	def set_auth_signup_template_user_id(self):
		self.ensure_one()
		IrConfigParam = self.env['ir.config_parameter']
		# we store the repr of the values, since the value of the parameter is a required string
		IrConfigParam.set_param('auth_signup.reset_password', repr(self.mobikul_reset_password))
		IrConfigParam.set_param('auth_signup.allow_uninvited', repr(self.mobikul_signup))
		IrConfigParam.set_param('auth_signup.template_user_id', repr(self.mobikul_signup_template_user_id.id))
		IrConfigParam.set_param('mobikul.allow_guest', repr(self.mobikul_allow_guest))
		IrConfigParam.set_param('mobikul.gmail_signin', repr(self.mobikul_gmail_signin))
		IrConfigParam.set_param('mobikul.facebook_signin', repr(self.mobikul_facebook_signin))
		IrConfigParam.set_param('mobikul.twitter_signin', repr(self.mobikul_twitter_signin))
