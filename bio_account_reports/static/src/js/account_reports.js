odoo.define('bio_account_reports.account_report', function (require) {
'use strict';


const core = require('web.core');
const { accountReportsWidget, M2MFilters } = require('account_reports.account_report');


const _t = core._t;


accountReportsWidget.include({
    custom_events: _.extend({}, accountReportsWidget.prototype.custom_events, {
        bio_factoring_filter_changed: function(event)
        {
            const self = this;

            self.report_options.account_ids = event.data.account_ids;

            return self.reload().then(function ()
            {
                self.$searchview_buttons.parent().find('.o_account_reports_filter_bio_factoring > button.dropdown-toggle').click();
            });
        },
    }),


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

        // ODOO-628: After reload from "Select All", the server normalizes
        // all-selected to "All Journals" and resets selected=false.
        // Restore visual checkmarks and client-side selected state.
        if (this._bio_select_all_journals) {
            this.$searchview_buttons.find('.js_account_report_journal_choice_filter').each(function() {
                if ($(this).data('model') === 'account.journal') {
                    $(this).addClass('selected');
                }
            });
            _.each(this.report_options.journals, function(journal) {
                if (journal.model === 'account.journal') {
                    journal.selected = true;
                }
            });
            this._bio_select_all_journals = false;
        }

        // bio_factoring filter
        if (typeof this.report_options.bio_factoring === 'boolean') {
            const self = this;
            const $filterButton = this.$searchview_buttons.find('.js_account_bio_factoring_m2m');
            $filterButton.on('click', function() {
                self.report_options.bio_factoring = !self.report_options.bio_factoring;
                self.reload();
            });

            // Оновлення тексту кнопки відповідно до стану
            const buttonText = this.report_options.bio_factoring ? _t("Factoring: On") : _t("Factoring: Off");
            $filterButton.text(buttonText);
        }
//        if (this.report_options.bio_factoring)
//        {
//            if (!this.bio_factoring_m2m_filter)
//            {
//                const fields = {};
//                if ('bio_factoring' in this.report_options)
//                {
//                    fields['account_ids'] = {
//                        label: _t("Accounts"),
//                        modelName: 'account.account',
//                        value: this.report_options.account_ids.map(Number),
//                    };
//                }
//
//                if (!_.isEmpty(fields))
//                {
//                    this.bio_factoring_m2m_filter = new M2MFilters(this, fields, 'bio_factoring_filter_changed');
//                    this.bio_factoring_m2m_filter.appendTo(this.$searchview_buttons.find('.js_account_bio_factoring_m2m'));
//                }
//            }
//            else
//            {
//                this.$searchview_buttons.find('.js_account_bio_factoring_m2m').append(this.bio_factoring_m2m_filter.$el);
//            }
//        }
    },


});


});
