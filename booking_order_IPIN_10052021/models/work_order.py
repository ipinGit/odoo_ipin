from odoo import api, fields, models

class WorkOrder(models.Model):
    _name = 'work.order'
    
    number = fields.Char('WO Number', required=True, readonly=True) # a. WO Number: gunakan sequence baru, dengan Prefix WO, auto created, readonly
    order_ref = fields.Many2one('sale.order', string='Booking Order Ref') # b. Booking Order Reference: many2one dari sale.order, auto filled, readonly
    team = fields.Many2one('service.team') # c. Team: many2one dari service_team, mandatory
    team_leader = fields.Many2one('res.users', string='Team Leader') # d. Team Leader: many2one dari res.user, mandatory
    team_members = fields.Many2many('res.users', string='Team Members') # e. Team Members: many2many dari res.user
    planned_start = fields.Datetime('Planned Start', required=True) # f. Planned Start: Datetime, mandatory
    planned_end = fields.Datetime('Planned End', required=True) # g. Planned End: Datetime, mandatory
    date_start = fields.Datetime('Date Start', readonly=True) # h. Date Start: Datetime, readonly
    date_end = fields.Datetime('Date End', readonly=True) # i. Date End: Datetime, readonly
    state = fields.Selection([('pending', 'Pending'),
                            ('progress', 'In Progress'),
                            ('done', 'Done'),
                            ('cancelled', 'Cancelled')], string='Status', default='pending', index=True, track_visibility='onchange', copy=False) # j. State: selection (Pending, In Progress, Done, Cancelled)
    notes = fields.Text('Notes') # k. Notes: textarea

    @api.onchange('team')
    def onchange_order_team(self):
        self.team_leader = self.team.team_leader
        self.team_members = self.team.team_members

    @api.model
    def default_get(self, default_fields):
        seq = self.env.ref('booking_order_IPIN_10052021.sequence_work_order_id')
        res = super(WorkOrder, self).default_get(default_fields)
        number_next = seq.number_next_actual + seq.number_increment
        name_seq = seq.get_next_char(number_next)
        res['number'] = name_seq
        return res

    @api.multi
    def action_start_work(self):
        self.state = 'progress'
        self.date_start = fields.datetime.now()

    @api.multi
    def action_end_work(self):
        self.state = 'done'
        self.date_end = fields.datetime.now()

    @api.multi
    def action_reset(self):
        self.date_start = False

    @api.multi
    def action_cancel(self):
        self.state = 'cancelled'

    

class WorkOrderCancel(models.TransientModel):
    _name = 'work.order.cancel.wizard'
    reason = fields.Char('Reason for Cancellation', required=True)

    @api.multi
    def cancel_work_order(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for record in self.env['work.order'].browse(active_ids):
            record.notes = (record.notes or '') + self.reason
            
            record.action_cancel()
        return {'type': 'ir.actions.act_window_close'}
