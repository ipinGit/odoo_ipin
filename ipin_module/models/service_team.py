from odoo import api, fields, models

class ServiceTeam(models.Model):
    _name = 'service.team'
    
    name = fields.Char('Name') # Team Name: char, mandatory
    team_leader = fields.Many2one('res.user', string='Team Leader') #: many2one dari res.user, mandatory
    team_members = fields.Many2many('res.users', string='Team Members') # Team Members: many2many dari res.user
