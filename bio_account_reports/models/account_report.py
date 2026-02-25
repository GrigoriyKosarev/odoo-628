
from odoo import models, fields, api


class AccountReport(models.Model):
    _inherit = "account.report"

    filter_currency_eur = fields.Boolean(string="Currency EUR",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_EUR'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_huf = fields.Boolean(string="Currency HUF",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_HUF'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_ron = fields.Boolean(string="Currency RON",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_RON'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_pln = fields.Boolean(string="Currency PLN",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_PLN'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_czk = fields.Boolean(string="Currency CZK",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_CZK'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_gbp = fields.Boolean(string="Currency GBP",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_GBP'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_uah = fields.Boolean(string="Currency UAH",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_UAH'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)
    filter_currency_usd = fields.Boolean(string="Currency USD",  # ODOO-445
                                         compute=lambda x: x._compute_report_option_filter('filter_currency_USD'),
                                         readonly=False, store=True, depends=['root_report_id'], company_dependent=True,)

    def _init_options_currency_eur(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_eur and previous_options:
            options['currency_EUR'] = previous_options.get('currency_EUR', False)
        else:
            options['currency_EUR'] = False

    def _init_options_currency_huf(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_huf and previous_options:
            options['currency_HUF'] = previous_options.get('currency_HUF', False)
        else:
            options['currency_HUF'] = False

    def _init_options_currency_ron(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_ron and previous_options:
            options['currency_RON'] = previous_options.get('currency_RON', False)
        else:
            options['currency_RON'] = False

    def _init_options_currency_pln(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_pln and previous_options:
            options['currency_PLN'] = previous_options.get('currency_PLN', False)
        else:
            options['currency_PLN'] = False

    def _init_options_currency_czk(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_czk and previous_options:
            options['currency_CZK'] = previous_options.get('currency_CZK', False)
        else:
            options['currency_CZK'] = False

    def _init_options_currency_gbp(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_gbp and previous_options:
            options['currency_GBP'] = previous_options.get('currency_GBP', False)
        else:
            options['currency_GBP'] = False

    def _init_options_currency_uah(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_uah and previous_options:
            options['currency_UAH'] = previous_options.get('currency_UAH', False)
        else:
            options['currency_UAH'] = False

    def _init_options_currency_usd(self, options, previous_options=None):  # ODOO-445
        if self.filter_currency_usd and previous_options:
            options['currency_USD'] = previous_options.get('currency_USD', False)
        else:
            options['currency_USD'] = False

    @api.model
    def _get_options_currency_domain(self, options, domain):  # ODOO-445
        if options.get('currency_EUR'):
            domain += [('currency_id.id', '=', '1')]
        if options.get('currency_HUF'):
            domain += [('currency_id.id', '=', '11')]
        if options.get('currency_RON'):
            domain += [('currency_id.id', '=', '28')]
        if options.get('currency_PLN'):
            domain += [('currency_id.id', '=', '17')]
        if options.get('currency_CZK'):
            domain += [('currency_id.id', '=', '9')]
        if options.get('currency_GBP'):
            domain += [('currency_id.id', '=', '142')]
        if options.get('currency_UAH'):
            domain += [('currency_id.id', '=', '22')]
        if options.get('currency_USD'):
            domain += [('currency_id.id', '=', '2')]
        return domain

    def _get_options_domain(self, options, date_scope):  # ODOO-445
        domain = super()._get_options_domain(options, date_scope)
        self._get_options_currency_domain(options, domain)
        return domain

    # ODOO-631
    @staticmethod
    def _report_custom_engine_cash_flow_analytic_cash_outflow(expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None):

        domain = [('account_id.account_type', 'in', ('asset_cash', 'liability_credit_card')), ('credit', '>', 0.0)]
        if options.get('date', False):
            domain += [('date', '>=', options['date']['date_from']), ('date', '<=', options['date']['date_to'])]
        if options.get('single_company', False):
            domain += [('company_id', 'in', options['single_company'])]

        # move_lines = expressions[0].env['account.move.line'].search(domain)
        move_lines = expressions[0].env['account.move.line'].read_group(domain,
                                                                        ['balance', 'cash_flow_analytic_account_id'],
                                                                        ['cash_flow_analytic_account_id'],
                                                                        )
        result = {}
        for ml in move_lines:
            # key = ml.cash_flow_analytic_account_id.id if ml.cash_flow_analytic_account_id else None
            # if key not in result:
            #     result[key] = {'analytic_account_id': key,
            #                    'bio_balance': 0.0,
            #                    'budget': 0.0,
            #                    'remaining_balance': 0.0,
            #                    'achievement': 0.0,
            #                    }
            # result[key]['bio_balance'] += ml.balance or 0.0
            key = ml['cash_flow_analytic_account_id'][0] if ml['cash_flow_analytic_account_id'] else None
            result[key] = {'analytic_account_id': key,
                           'bio_balance': ml['balance'],
                           'budget': 0.0,
                           'remaining_balance': 0.0,
                           'achievement': 0.0,
                           }
        if result:
            budget_domain = [('analytic_account_id', 'in', list(result.keys())),
                             ('crossovered_budget_state', 'in', ['confirm', 'done']), ]
            if options.get('date', False):
                budget_domain += [('date_from', '>=', options['date']['date_from']),
                                  ('date_to', '<=', options['date']['date_to']), ]
            if options.get('single_company', False):
                budget_domain += [('company_id', 'in', options['single_company']), ]

            budget_lines = expressions[0].env['crossovered.budget.lines'].read_group(budget_domain,
                                                                                     ['planned_amount', 'analytic_account_id'],
                                                                                     ['analytic_account_id'])
            for b_l in budget_lines:
                acc_id = b_l['analytic_account_id'][0]
                if acc_id in result:
                    result[acc_id]['budget'] = b_l['planned_amount']
                    result[acc_id]['remaining_balance'] = result[acc_id]['budget'] - abs(result[acc_id]['bio_balance'])
                    result[acc_id]['achievement'] = abs(result[acc_id]['bio_balance']) / result[acc_id]['budget'] * 100

        if current_groupby == 'cash_flow_analytic_account_id':
            res = [(key, values) for key, values in result.items()]
        else:
            # balance_total = sum(val['bio_balance'] for val in result.values())
            # budget_total = sum(val['budget'] for val in result.values())
            # res = {'bio_balance': balance_total,
            #        'analytic_account_id': None,
            #        'budget': budget_total,
            #        'remaining_balance': budget_total - abs(balance_total),
            #        'achievement': abs(balance_total) / budget_total * 100,
            #        }
            res = {'bio_balance': 0.0,
                   'analytic_account_id': None,
                   'budget': 0.0,
                   'remaining_balance': 0.0,
                   'achievement': 0.0,
                   }
        return res
