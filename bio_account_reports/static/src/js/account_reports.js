odoo.define('bio_account_reports.account_report', function (require) {
'use strict';


const core = require('web.core');
const { accountReportsWidget, M2MFilters } = require('account_reports.account_report');


const _t = core._t;


accountReportsWidget.include({

    // ODOO-628: Detect "All Journals" state — when no journal has selected=true,
    // the server treats it as all journals included. Show checkmarks accordingly.
    _bio_isAllJournalsState: function() {
        var journals = this.report_options.journals || [];
        var hasAnyJournal = false;
        for (var i = 0; i < journals.length; i++) {
            if (journals[i].model === 'account.journal') {
                hasAnyJournal = true;
                if (journals[i].selected) {
                    return false;
                }
            }
        }
        return hasAnyJournal;
    },

    // ODOO-628: Mark all journal checkboxes as selected (data + DOM).
    _bio_checkAllJournals: function() {
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
    },

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
            self.reload();
        });

        // ODOO-628: When in "All Journals" state (server resets selected=false
        // for all journals), restore visual checkmarks so the UI is consistent —
        // "All Journals" means all are included, so all should appear checked.
        if (this._bio_isAllJournalsState()) {
            this._bio_checkAllJournals();
        }

    },


});


});
