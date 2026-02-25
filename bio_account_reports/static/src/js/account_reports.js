odoo.define('bio_account_reports.account_report', function (require) {
'use strict';


const core = require('web.core');
const { accountReportsWidget, M2MFilters } = require('account_reports.account_report');


const _t = core._t;


accountReportsWidget.include({
    render_searchview_buttons: function()
    {
        this._super.apply(this, arguments);

        // ODOO-628: "Select All" button for journals filter
        var self = this;
        $('.js_account_report_journal_select_all', this.$searchview_buttons).click(function (ev) {
            ev.preventDefault();
            _.each(self.report_options.journals, function(journal) {
                if (journal.model === 'account.journal') {
                    journal.selected = true;
                }
            });
            delete self.report_options.__journal_group_action;
            self._bio_select_all_journals = true;
            self.reload();
        });

    },


});


});
