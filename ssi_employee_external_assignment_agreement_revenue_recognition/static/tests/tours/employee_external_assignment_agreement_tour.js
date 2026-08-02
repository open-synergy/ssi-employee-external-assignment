// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement_revenue_recognition." +
        "employee_external_assignment_agreement_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block -- corresponds to Flow 1 of every
        // employee_external_assignment_agreement IK: "Open the Human
        // Resource > Career Management > External Assignment > Agreements
        // menu." (same block used by the base module's own tour).
        function openAgreementList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Career Management menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.hr_career_management_menu"]',
                },
                {
                    content: "Open the Agreements menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang
                    // (lihat patterns.md skill odoo-development-ui-test §A).
                    content:
                        "Employee External Assignment Agreements list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Agreements)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/employee_external_assignment_agreement/01-create.md
        // (delta, this module) -- Extends
        // ssi_employee_external_assignment_agreement, aksi 01-create.
        // Navigation and field-filling for the Type is sourced from the
        // base IK Flow 1-3; the new assertion is that the Create PoB
        // button (Inline Actions: action_create_pob) is displayed on a
        // Details row. The tour stops here -- it does not continue to
        // fill in the remaining base fields or Save.
        tour.register(
            "ssi_employee_external_assignment_agreement_revenue_recognition_" +
                "employee_external_assignment_agreement_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 (base) -- Open the Agreements menu.
                openAgreementList(),
                [
                    // Flow 2 (base) -- Click the New button.
                    {
                        content: "Click New",
                        trigger: ".o_list_button_add",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open in edit mode",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 (base, partial) -- Select the Type. Job_id's
                    // domain on the Details row (parent.allowed_job_ids)
                    // depends on Type, so it must be selected before a
                    // detail line can be added.
                    {
                        content: "Select the Type",
                        trigger: ".o_field_many2one[name='type_id'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR EEARR Create Type",
                    },
                    {
                        content: "Pick the Type from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEARR Create Type)",
                        in_modal: false,
                    },

                    // Modified Flow (delta) -- open the Details tab and
                    // add one line, so the Create PoB button rendered on
                    // that row can be asserted.
                    {
                        content: "Open the Details tab",
                        trigger: ".o_notebook .nav-link:contains(Details)",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        content: "Click Add a line on the Details table",
                        trigger:
                            ".o_field_widget[name='detail_ids'] .o_field_x2many_list_row_add a",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        // Dialog: JANGAN prefiks trigger dengan ".modal" di
                        // 14.0 -- lihat catatan patterns.md skill
                        // odoo-development-ui-test §H.
                        content: "Detail line dialog is open",
                        trigger: ".o_field_many2one[name='job_id']",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Select the Job",
                        trigger: ".o_field_many2one[name='job_id'] input",
                        run: "text TOUR EEARR Create Job",
                    },
                    {
                        content: "Pick the Job from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEARR Create Job)",
                        in_modal: false,
                    },
                    {
                        content: "Save the detail line",
                        trigger: ".modal-footer button.btn-primary",
                    },

                    // Modified Flow (delta) -- the Create PoB button is
                    // displayed on the new Details row. This is where the
                    // tour stops.
                    {
                        content: "Create PoB button is displayed on the Details row",
                        trigger:
                            ".o_field_widget[name='detail_ids'] .o_data_row:last button[name='action_create_pob']",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement/07-create-pob.md
        // (new, this module) -- standalone IK (S4), since state "open" has
        // no host IK to hold the inline step. The Pre-Condition record
        // (status On Progress, PoB Product configured on Type, one Details
        // line) is prepared in setUpClass -- not by clicking through the
        // UI, since building that state is not part of this action's Flow.
        tour.register(
            "ssi_employee_external_assignment_agreement_revenue_recognition_" +
                "employee_external_assignment_agreement_create_pob",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreements menu.
                openAgreementList(),
                [
                    // Flow 2 -- Open the record to act on (status On
                    // Progress).
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEARR Create PoB Partner) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- On the Details tab, click the gear button
                    // Create PoB on the row.
                    {
                        content: "Open the Details tab",
                        trigger: ".o_notebook .nav-link:contains(Details)",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        content: "Click the Create PoB button on the Details row",
                        trigger:
                            ".o_field_widget[name='detail_ids'] .o_data_row:first button[name='action_create_pob']",
                        extra_trigger: ".o_form_view",
                    },

                    // Post-Condition -- the # PoB column on that row is
                    // filled. Before the click it is an empty readonly
                    // many2one (zero-width, invisible to the tour); it
                    // only becomes visible once a Performance Obligation
                    // is linked -- see patterns.md skill
                    // odoo-development-ui-test §O.
                    {
                        content: "# PoB column is filled on the Details row",
                        trigger:
                            ".o_field_widget[name='detail_ids'] .o_data_row:first .o_field_widget[name='pob_id']",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
