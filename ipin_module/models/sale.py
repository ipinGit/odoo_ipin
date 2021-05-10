from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean('Booking Order?')
    team = fields.Many2one('service.team', string='Team')
    team_leader = fields.Many2one('res.users', string='Team Leader')
    team_members = fields.Many2many('res.users', string='Team Members')
    booking_start = fields.Datetime('Booking Start')
    booking_end = fields.Datetime('Booking End')

    @api.model
    def create(self, vals):
        context = self._context or {}
        action = context.get('params',{}).get('action', False)
        this_action = self.env.ref('ipin_module.action_booking_orders').id
        if action and action == this_action:
        	vals.update({'is_booking_order': True})
        return super(SaleOrder, self).create(vals)
    