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
            var journals = self.report_options.journals || [];
            for (var i = 0; i < journals.length; i++) {
                if (journals[i].model === 'account.journal') {
                    journals[i].selected = true;
                }
            }
            delete self.report_options.__journal_group_action;
            self._bio_select_all_journals = true;
            self.reload();
        });

        // ODOO-628: After reload from "Select All", the server normalizes
        // all-selected to "All Journals" and resets selected=false.
        // Restore visual checkmarks and client-side selected state.
        if (this._bio_select_all_journals) {
            var journals = this.report_options.journals || [];
            for (var i = 0; i < journals.length; i++) {
                if (journals[i].model === 'account.journal') {
                    journals[i].selected = true;
                }
            }
            this.$searchview_buttons.find('.js_account_report_journal_choice_filter').each(function() {
                if ($(this).data('model') === 'account.journal') {
                    this.classList.add('selected');
                }
            });
            this._bio_select_all_journals = false;
        }

    },


});


});
