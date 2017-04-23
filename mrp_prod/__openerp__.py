# -*- coding: utf-8 -*-
{
    'name': "mrp_prod",

    'summary': """
       """,

    'description': """
        with this module you can add daily records for the workcenters and employees and trace them then calculation work efficiency
    """,

    'author': "Ramadan Khalil",
    'contact': "rkhalil1990@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'MRP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mrp',
                'mrp_operations',
                'hr',
                'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'mrp_pro_view.xml',
        "reports/record_report_view.xml",
        "reports/reports_view.xml",
        "reports/external_layout.xml",

    ],

    # only loaded in demonstration mode
    # 'demo': [
    #    'demo.xml',
    # ],
}
