# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'BIO Accounting Reports',
    'summary': 'View and create reports (bio)',
    'category': 'Accounting/Accounting',
    'version': '16.0.3.0.2',
    'long_description': """
BIO Accounting Reports
======================
    """,
    'license': 'LGPL-3',
    'depends': ['account_reports',
                'account',
                'selferp_cashflow_analytic'],  # ODOO-631
    'data': [
        'data/aged_partner_balance.xml',
        'data/account_report_cash_flow_analytic_data.xml',  # ODOO-631
        'views/account_report_view.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'bio_account_reports/static/src/js/account_reports.js',
    #     ],
    # },
    'auto_install': False,
    'installable': True,
}
