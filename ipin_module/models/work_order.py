from odoo import api, fields, models

class WorkOrder(models.Model):
    _name = 'work.order'
    
    number = fields.Char('WO Number', required=True, readonly=True) # a. WO Number: gunakan sequence baru, dengan Prefix WO, auto created, readonly
    order_ref = fields.Many2one('sale.order', string='Booking Order Ref') # b. Booking Order Reference: many2one dari sale.order, auto filled, readonly
    team = fields.Many2one('service.team') # c. Team: many2one dari service_team, mandatory
    team_leader = fields.Many2one('res.user', string='Team Leader') # d. Team Leader: many2one dari res.user, mandatory
    team_members = fields.Many2many('res.users', string='Team Members') # e. Team Members: many2many dari res.user
    planned_start = fields.Datetime('Planned Start', required=True) # f. Planned Start: Datetime, mandatory
    planned_end = fields.Datetime('Planned End', required=True) # g. Planned End: Datetime, mandatory
    date_start = fields.Datetime('Date Start', readonly=True) # h. Date Start: Datetime, readonly
    date_end = fields.Datetime('Date End', readonly=True) # i. Date End: Datetime, readonly
    state = fields.Selection([('pending', 'Pending'),
                            ('progress', 'In Progress'),
                            ('done', 'Done'),
                            ('cancelled', 'Cancelled')], string='Status') # j. State: selection (Pending, In Progress, Done, Cancelled)
    notes = fields.Text('Notes') # k. Notes: textarea
    