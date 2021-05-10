from odoo import api, fields, models
import logging
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean('Booking Order?')
    team = fields.Many2one('service.team', string='Team', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members', required=True)
    booking_start = fields.Datetime('Booking Start', required=True)
    booking_end = fields.Datetime('Booking End', required=True)

    @api.model
    def create(self, vals):
        context = self._context or {}
        action = context.get('params',{}).get('action', False)
        this_action = self.env.ref('booking_order_IPIN_10052021.action_booking_orders').id
        if action and action == this_action:
            vals.update({'is_booking_order': True})
        return super(SaleOrder, self).create(vals)

    @api.onchange('team')
    def onchange_order_team(self):
        self.team_leader = self.team.team_leader
        self.team_members = self.team.team_members

    @api.multi
    def action_check_team_availibity(self):
        self.ensure_one()
        wo = self.env['work.order'].search([('team', '=', self.team.id), ('state', 'not in', ['done', 'cancelled'])])
        overlap = False
        order_ref = False
        if len(wo) != 0:
            for w in wo:
                start1 = datetime.strptime(self.booking_start, DATETIME_FORMAT)
                end1 = datetime.strptime(self.booking_end, DATETIME_FORMAT)
                start2 = datetime.strptime(w.planned_start, DATETIME_FORMAT)
                end2 = datetime.strptime(w.planned_end, DATETIME_FORMAT)
                if ((end1-start1)+(end2-start2))>(max(end1,end2)-min(start1,start2)):
                    overlap = True
                    order_ref = w.order_ref
                    break
        if overlap:
            raise Warning('Team already has work order during that period on %s' % order_ref.name)
        else:
            raise Warning('Team is available')

        # ((end1-start1)+(end2-start2))>(max(end1,end2)-min(start1,start2))