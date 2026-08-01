// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_payment_term_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds
        // to Flow 1 of every employee_external_assignment_agreement.payment_term
        // IK: "Open the Human Resource > Career Management > External
        // Assignment > Payment Terms menu." Same third-level "External
        // Assignment" grouping menu (non-clickable dropdown-header) used by
        // the Agreements menu -- see employee_external_assignment_agreement_tour.js.
        function openPaymentTermList() {
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
                    content: "Open the Payment Terms menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_payment_term_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang,
                    // bukan sekadar "ada list di layar" (lihat patterns.md
                    // skill odoo-development-ui-test §A).
                    content:
                        "Employee External Assignment Agreement Payment Terms list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Agreement Payment Terms)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // Every scenario below shares ONE Agreement/Partner (see setUpClass
        // in test_ui_employee_external_assignment_agreement_payment_term.py),
        // so the Partner column cannot disambiguate rows in the Payment
        // Terms list. Each scenario is instead given its own, non-overlapping
        // Date Start, and the row is looked up by that date instead.
        function openRecordByDateStart(dateStart) {
            return [
                {
                    content: "Open the record (Date Start " + dateStart + ")",
                    trigger:
                        ".o_data_row:contains(" + dateStart + ") .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/employee_external_assignment_agreement_payment_term/01-create.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Payment Terms menu.
                openPaymentTermList(),
                [
                    // Flow 2 -- Click the New button.
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

                    // Flow 3 -- Select the Agreement. Only ONE Agreement
                    // record exists in this test class, and its display name
                    // is an internal "*<id>" placeholder (mixin.transaction
                    // name_get() fallback for a Draft "/" document number) --
                    // not typeable. Click the (empty) field: minLength:0
                    // triggers a blank name_search that lists every match,
                    // which here is exactly the one Agreement.
                    {
                        content: "Open the Agreement dropdown",
                        trigger: ".o_field_many2one[name='agreement_id'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "click",
                    },
                    {
                        content: "Pick the only Agreement from the dropdown",
                        trigger: ".ui-autocomplete .ui-menu-item:first a",
                        in_modal: false,
                    },

                    // Flow 3 (cont.) -- Fill in Date Start / Date End.
                    {
                        content: "Fill in the Date Start",
                        trigger: ".o_field_widget[name='date_start'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text 03/01/2027",
                    },
                    {
                        content: "Fill in the Date End",
                        trigger: ".o_field_widget[name='date_end'] input",
                        run: "text 03/31/2027",
                    },

                    // Flow 4 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- a new record is created in Draft
                    // status.
                    {
                        content: "Record is saved",
                        trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/02-edit.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("01/01/2026"), [
                // Flow 3 -- Click the Edit button.
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Change a required field.
                {
                    content: "Change the Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/28/2026",
                },

                // Flow 5 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the record is updated.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/03-delete.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("02/01/2026"), [
                // Flow 3 -- Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    // Item Action menu adalah komponen Owl; cocokkan
                    // LABEL PERSIS -- lihat patterns.md skill
                    // odoo-development-ui-test §I.
                    content: "Click Delete",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Delete";
                            }
                        );
                        $delete[0].click();
                    },
                },

                // Flow 4 -- Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Flow 5 -- Return to the Payment Terms list.
                {
                    content:
                        "Click the Employee External Assignment Agreement Payment Terms breadcrumb",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Employee External Assignment Agreement Payment Terms)",
                },

                // Post-Condition -- the record is permanently removed.
                {
                    content: "Record no longer in the list",
                    trigger: ".o_list_view:not(:has(.o_data_row:contains(02/01/2026)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/04-confirm.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_confirm",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("03/01/2026"), [
                // Flow 3 -- Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Waiting for
                // Approval.
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/05-approve.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_approve",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("04/01/2026"), [
                // Flow 3 -- Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- single approval level, so the
                // confirm -> done transition runs automatically right
                // after approval: status changes directly to Done.
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/06-reject.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_reject",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("05/01/2026"), [
                // Flow 3 -- Click the Reject button.
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Rejected.
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/10-cancel.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_cancel",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("06/01/2026"), [
                // Flow 3 -- Click the Cancel button.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Wizard: JANGAN prefiks trigger dengan ".modal" di
                    // 14.0 -- lihat catatan patterns.md skill
                    // odoo-development-ui-test §H.
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Select the Reason.
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] label:contains(TOUR EEAAPT Cancel Reason)",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    // Stacked "Are you sure?" dialog (confirm= attribute
                    // on the wizard's Confirm button).
                    content: "Confirm the stacked dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/12-restart.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("08/01/2026"), [
                // Flow 3 -- Click the Restart button.
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status returns to Draft.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/13-reset-number.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_reset_number",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("07/01/2026"), [
                // Flow 3 -- Click the Reset Document Number button.
                {
                    content: "Click the Reset Document Number button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reset_document_number']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- document number returns to "/". After
                // the reset, the form re-renders read-only, so the visible
                // field is "display_name" (not the edit-only "name"
                // field); name_get() renders "/" as "*<id>", which is the
                // observable marker that the reset took effect (see
                // mixin_transaction.py in ssi_transaction_mixin).
                {
                    content: "Document number is reset (display name shows *)",
                    trigger:
                        ".oe_title .o_field_widget[name='display_name']:contains(*)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/14-load-external-assignment.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_load_external_assignment",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("09/01/2026"), [
                // Flow 3 -- Open the Included Assignments tab.
                {
                    content: "Open the Included Assignments tab",
                    trigger: ".o_notebook .nav-link:contains(Included Assignments)",
                },

                // Flow 4 -- Click the External Assignments (load) button.
                {
                    content: "Click the External Assignments (refresh) button",
                    trigger:
                        ".o_form_view button[name='action_load_external_assignment']",
                },

                // Post-Condition -- matching External Assignments are
                // loaded: a row appears in the field.
                {
                    content: "An External Assignment row is loaded",
                    trigger:
                        ".o_field_widget[name='external_assignment_ids'] .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/15-view-external-assignments.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_view_external_assignments",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("10/01/2026"), [
                // Flow 3 -- Open the Included Assignments tab.
                {
                    content: "Open the Included Assignments tab",
                    trigger: ".o_notebook .nav-link:contains(Included Assignments)",
                },

                // Flow 4 -- Click the External Assignments (view) button.
                {
                    content: "Click the External Assignments (list) button",
                    trigger:
                        ".o_form_view button[name='action_open_external_assignments']",
                },

                // Post-Condition -- a list view opens showing the
                // Employee External Assignments linked to this record.
                {
                    content: "Employee External Assignments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/16-reload-payslip.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_reload_payslip",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("11/01/2026"), [
                // Flow 3 -- Open the Payslips tab.
                {
                    content: "Open the Payslips tab",
                    trigger: ".o_notebook .nav-link:contains(Payslips)",
                },

                // Flow 4 -- Click the Payslips (reload) button.
                {
                    content: "Click the Payslips (refresh) button",
                    trigger: ".o_form_view button[name='action_reload_payslip']",
                },

                // Post-Condition -- matching Payslips are linked: a row
                // appears in the field.
                {
                    content: "A Payslip row is loaded",
                    trigger: ".o_field_widget[name='payslip_ids'] .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/17-load-payslip-line.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_load_payslip_line",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("12/01/2026"), [
                // Flow 3 -- Open the Payslip Lines tab.
                {
                    content: "Open the Payslip Lines tab",
                    trigger: ".o_notebook .nav-link:contains(Payslip Lines)",
                },

                // Flow 4 -- Click the Payslip Lines (load) button.
                {
                    content: "Click the Payslip Lines (refresh) button",
                    trigger: ".o_form_view button[name='action_load_payslip_line']",
                },

                // Post-Condition -- matching Payslip Lines are loaded and
                // Payment Term Rules are (re)generated: a row appears in
                // the Payment Term Rules list.
                {
                    content: "A Payment Term Rule row is loaded",
                    trigger: ".o_field_widget[name='rule_ids'] .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/18-create-invoice.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_create_invoice",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("01/01/2027"), [
                // Flow 3 -- Open the Invoice tab.
                {
                    content: "Open the Invoice tab",
                    trigger: ".o_notebook .nav-link:contains(Invoice)",
                },

                // Flow 4 -- Click the Create Invoice button.
                {
                    content: "Click the Create Invoice button",
                    trigger: ".o_form_view button[name='action_create_invoice']",
                },

                // Post-Condition -- an Invoice is created and linked: the
                // Invoice field now shows the internal-link icon that
                // Odoo only renders once a many2one has a value.
                {
                    content: "The Invoice field now has a value",
                    trigger: ".o_field_widget[name='invoice_id'] .o_external_button",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );

        // IK: docs/employee_external_assignment_agreement_payment_term/19-delete-invoice.md
        tour.register(
            "ssi_employee_external_assignment_agreement_payment_term_delete_invoice",
            {
                test: true,
                url: "/web",
            },
            [].concat(openPaymentTermList(), openRecordByDateStart("02/01/2027"), [
                // Flow 3 -- Open the Invoice tab.
                {
                    content: "Open the Invoice tab",
                    trigger: ".o_notebook .nav-link:contains(Invoice)",
                },

                // Flow 4 -- Click the Delete Invoice button.
                {
                    content: "Click the Delete Invoice button",
                    trigger: ".o_form_view button[name='action_delete_invoice']",
                },

                // Post-Condition -- the Invoice is unlinked: the Create
                // Invoice button (only visible while invoice_id is
                // empty) reappears.
                {
                    content: "The Create Invoice button is visible again",
                    trigger:
                        ".o_form_view button[name='action_create_invoice']:visible",
                    run: function () {
                        // Assertion only.
                    },
                },
            ])
        );
    }
);
