# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Elzhor Hospital ',
    'version': '10',
    'summary': 'Elzhor Hospital Management Software',
    'sequence': 100,
    'description': """this is the best hospital in egypt""",
    'category': 'Productivity',
    'website': 'https://www.holiel.com',
    'depends': [
        'sale',
        'mail',
        'base',
        'stock',
        # 'report_xlsx',
        'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_wizard.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/kids.xml',
        'views/patient_gender.xml',
        'views/appointment.xml',
        'views/sale.xml',
        'views/partner.xml',
        # 'report/patient_card.xml',
        # 'report/report.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'hospital/static/src/components/ListView/ListView.css',
                'hospital/static/src/components/ListView/ListView.js',
                'hospital/static/src/components/ListView/ListView.xml',
            ]},
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
