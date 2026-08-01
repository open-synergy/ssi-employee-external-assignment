// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_batch_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds to
        // Flow 1 of every employee_external_assignment_agreement_batch IK:
        // "Open the Human Resource > Career Management > External Assignment >
        // Agreement Batches menu."
        // Note: "Career Management" (ssi_hr.hr_career_management_menu) is a
        // second-level app menu, so it is always clickable in the top navbar
        // even without an action= attribute. "External Assignment"
        // (ssi_employee_external_assignment.menu_external_assignment_root) is
        // a third-level grouping menuitem with no action= attribute, so Odoo
        // 14.0 renders it as a plain, non-clickable "<div
        // class='dropdown-header'>" inside the Career Management dropdown --
        // NOT as a data-menu-xmlid link. "Agreement Batches" is the only
        // clickable entry among them, so there is no separate "click External
        // Assignment" step.
        function openAgreementBatchList() {
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
                    content: "Open the Agreement Batches menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_batch_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                    // sekadar "ada list di layar" (lihat patterns.md skill
                    // odoo-development-ui-test §A).
                    content:
                        "Employee External Assignment Agreement Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Agreement Batches)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/employee_external_assignment_agreement_batch/01-create.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
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

                    // Flow 3 -- Fill in the required fields: Type, Partner,
                    // Title, Date Start, Date End, Currency, Pricelist.
                    {
                        content: "Select the Type",
                        trigger: ".o_field_many2one[name='type_id'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR EEAB Type",
                    },
                    {
                        content: "Pick the Type from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEAB Type)",
                        in_modal: false,
                    },
                    {
                        content: "Select the Partner",
                        trigger: ".o_field_many2one[name='partner_id'] input",
                        run: "text TOUR EEAB Create Partner",
                    },
                    {
                        content: "Pick the Partner from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEAB Create Partner)",
                        in_modal: false,
                    },
                    {
                        content: "Fill in the Title",
                        trigger: ".o_field_widget[name='title']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR EEAB Create",
                    },
                    {
                        content: "Fill in the Date Start",
                        trigger: ".o_field_widget[name='date_start'] input",
                        run: "text 01/01/2026",
                    },
                    {
                        content: "Fill in the Date End",
                        trigger: ".o_field_widget[name='date_end'] input",
                        run: "text 12/31/2026",
                    },
                    {
                        content: "Select the Currency",
                        trigger: ".o_field_many2one[name='currency_id'] input",
                        run: "text EUR",
                    },
                    {
                        content: "Pick the Currency from the dropdown",
                        trigger: ".ui-autocomplete .ui-menu-item a:contains(EUR)",
                        in_modal: false,
                    },
                    {
                        content: "Select the Pricelist",
                        trigger: ".o_field_many2one[name='pricelist_id'] input",
                        run: "text Public Pricelist",
                    },
                    {
                        content: "Pick the Pricelist from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(Public Pricelist)",
                        in_modal: false,
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

        // IK: docs/employee_external_assignment_agreement_batch/02-edit.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to edit.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Edit) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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

                    // Flow 4 -- Change the required fields.
                    {
                        content: "Change the Title",
                        trigger: ".o_field_widget[name='title']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR EEAB Edit Changed",
                    },

                    // Flow 5 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- the record is updated with the new
                    // values.
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

        // IK: docs/employee_external_assignment_agreement_batch/03-delete.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to delete.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Delete) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Click Action > Delete.
                    {
                        content: "Open the Action menu",
                        trigger: ".o_cp_action_menus button:contains(Action)",
                    },
                    {
                        content: "Click Delete",
                        // Item Action menu adalah komponen Owl; cocokkan LABEL
                        // PERSIS -- :contains(Delete) sebagai substring bisa
                        // keliru menunjuk item lain. Lihat patterns.md skill
                        // odoo-development-ui-test §I.
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

                    // Flow 5 -- Return to the Agreement Batches list (after a
                    // delete, the form may show the next record in the list
                    // instead of navigating back on its own).
                    {
                        content:
                            "Click the Employee External Assignment Agreement Batches breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Employee External Assignment Agreement Batches)",
                    },

                    // Post-Condition -- the record is permanently removed;
                    // list no longer shows it.
                    {
                        content: "Record no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR EEAB Partner Delete)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/04-confirm.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_confirm",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to confirm.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Confirm) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/05-approve.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_approve",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to approve.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Approve) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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
                    // confirm -> open transition runs automatically right
                    // after approval: status changes directly to On
                    // Progress.
                    {
                        content: "Status is On Progress",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/06-reject.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_reject",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to reject.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Reject) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/10-cancel.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_cancel",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to cancel.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Cancel) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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

                    // Flow 4 -- Select the Reason (rendered as a radio list).
                    // The label is rendered INSIDE the wizard modal (unlike a
                    // many2one autocomplete dropdown, which is appended to
                    // <body>), so the default in_modal:true scoping is kept --
                    // see the note on 14.0 in-modal triggers in patterns.md §H.
                    {
                        content: "Select the cancellation reason",
                        trigger:
                            ".o_field_widget[name='cancel_reason_id'] label:contains(TOUR EEAB Cancel Reason)",
                    },

                    // Flow 5 -- Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    {
                        // The wizard's Confirm button itself carries a
                        // stacked "Are you sure?" dialog (confirm= attribute)
                        // -- $modal_displayed resolves to the topmost visible
                        // modal, so this targets that stacked dialog.
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
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/11-terminate.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_terminate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to terminate.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Terminate) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Click the Terminate button.
                    {
                        content: "Click the Terminate button",
                        trigger: ".o_statusbar_buttons button:contains(Terminate)",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        content: "Wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- Select the Reason (rendered as a radio list).
                    // The label is rendered INSIDE the wizard modal, so the
                    // default in_modal:true scoping is kept -- see the note on
                    // 14.0 in-modal triggers in patterns.md §H.
                    {
                        content: "Select the termination reason",
                        trigger:
                            ".o_field_widget[name='terminate_reason_id'] label:contains(TOUR EEAB Terminate Reason)",
                    },

                    // Flow 5 -- Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    {
                        content: "Confirm the stacked dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },

                    // Post-Condition -- status changes to Terminated.
                    {
                        content: "Status is Terminated",
                        trigger:
                            ".o_statusbar_status .o_arrow_button[data-value='terminate'].btn-primary",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/12-restart.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record to restart.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Restart) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/13-reset-number.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_reset_number",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record whose document number will
                    // be reset.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Reset Number) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

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

                    // Post-Condition -- document number returns to "/".
                    // After the reset, the form re-renders read-only, so
                    // the visible field is "display_name" (not the
                    // edit-only "name" field); name_get() renders "/" as
                    // "*<id>", which is the observable marker that the
                    // reset took effect (see mixin_transaction.py in
                    // ssi_transaction_mixin).
                    {
                        content: "Document number is reset (display name shows *)",
                        trigger:
                            ".oe_title .o_field_widget[name='display_name']:contains(*)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/14-view-agreements.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_view_agreements",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the record.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner View Agreements) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Click the Agreements smart button.
                    {
                        content: "Click the Agreements smart button",
                        trigger: "button[name='action_open_agreements']",
                    },

                    // Post-Condition -- a list view opens showing the
                    // Agreements linked to this batch.
                    {
                        content:
                            "Employee External Assignment Agreements list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Agreements)",
                        extra_trigger: ".o_list_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_batch/15-generate-agreements.md
        tour.register(
            "ssi_employee_external_assignment_agreement_batch_generate_agreements",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Batches menu.
                openAgreementBatchList(),
                [
                    // Flow 2 -- Open the batch record.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAB Partner Generate Agreements) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 3 -- Go to the Agreements tab.
                    {
                        content: "Open the Agreements tab",
                        trigger: ".o_notebook .nav-link:contains(Agreements)",
                    },

                    // Flow 4 -- Click the Generate Agreements button.
                    {
                        content: "Click the Generate Agreements button",
                        trigger: "button:contains(Generate Agreements)",
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

                    // Flow 5 -- Fill in Number of Agreements (left at its
                    // default of 1, no Agreements line added), Receivable
                    // Account, and Journal.
                    {
                        content: "Select the Receivable Account",
                        trigger:
                            ".o_field_many2one[name='receivable_account_id'] input",
                        run: "text TOUR EEAB Receivable",
                    },
                    {
                        content: "Pick the Receivable Account from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEAB Receivable)",
                        in_modal: false,
                    },
                    {
                        content: "Select the Journal",
                        trigger: ".o_field_many2one[name='journal_id'] input",
                        run: "text TOUR EEAB Journal",
                    },
                    {
                        content: "Pick the Journal from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR EEAB Journal)",
                        in_modal: false,
                    },

                    // Flow 6 -- Click Generate.
                    {
                        content: "Click Generate",
                        trigger: ".modal-footer button[name='action_generate']",
                    },

                    // Flow 7 -- Click OK on the confirmation dialog.
                    {
                        // The wizard's Generate button carries a stacked
                        // "Are you sure?" dialog (confirm= attribute) --
                        // $modal_displayed resolves to the topmost visible
                        // modal, so this targets that stacked dialog.
                        content: "Confirm the stacked dialog",
                        trigger: ".modal-footer button.btn-primary",
                        in_modal: true,
                    },

                    // Post-Condition -- a list view opens showing the newly
                    // generated agreements.
                    {
                        content: "Generated Agreements list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(Generated Agreements)",
                        extra_trigger: ".o_list_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
