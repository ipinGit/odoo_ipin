# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Work Order and Service Team',
    'category': 'Website',
    'summary': 'Manage Work Order and Service Team for Sales',
    'website': '',
    'version': '1.0',
    'description': """
    Here is the best descriptions one would ever made
        """,
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/service_team_view.xml',
        'views/work_order_view.xml',
    ],
    'installable': True,
}
