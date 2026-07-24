// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment.employee_external_assignment_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds to
        // Flow 1 of every employee_external_assignment IK: "Open the Human
        // Resource > Career Management > External Assignment > Assignments
        // menu." "Career Management" is a grouping menuitem with no action of
        // its own (ssi_hr/menu.xml hr_career_management_menu has no action=
        // attribute), so Odoo 14.0 renders it as the top-level clickable
        // dropdown toggle in the app navbar; "External Assignment" (this
        // module's menu.xml menu_external_assignment_root) is ALSO an
        // action-less grouping menuitem, so its children -- "Assignments" --
        // are flattened into the SAME "Career Management" dropdown. There is
        // therefore no separate "click External Assignment" step.
        function openAssignmentList() {
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
                    content: "Open the Assignments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment.employee_external_assignment_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                    // sekadar "ada list di layar" (lihat patterns.md skill
                    // odoo-development-ui-test §A).
                    content: "Employee External Assignments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // Selects an option from an open many2one autocomplete dropdown.
        function pickMany2one(fieldName, label) {
            return [
                {
                    content: "Select the " + fieldName + " field value",
                    trigger: ".o_field_many2one[name='" + fieldName + "'] input",
                    run: "text " + label,
                },
                {
                    content: "Pick " + label + " from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                    in_modal: false,
                },
            ];
        }

        // Opens the record identified by the unique employee name shown on
        // the list row (used as Pre-Condition test data marker).
        function openRecordByEmployee(employeeName) {
            return [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(" + employeeName + ") .o_data_cell:first",
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

        // IK: docs/employee_external_assignment/01-create.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
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
                ],
                // Flow 3 -- Fill in the required fields: Type, Employee.
                // Department/Manager/Job Position are auto-filled from
                // Employee via onchange and are not exercised by clicks here
                // (their auto-fill value is unit test territory).
                pickMany2one("type_id", "TOUR EEA Type"),
                pickMany2one("employee_id", "TOUR EEA Create Employee"),
                [
                    // Flow 3 -- Start Date / End Date.
                    {
                        content: "Fill in the Start Date",
                        trigger: ".o_field_widget[name='date_start'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text 01/15/2026",
                    },
                    {
                        content: "Fill in the End Date",
                        trigger: ".o_field_widget[name='date_end'] input",
                        run: "text 12/31/2026",
                    },
                ],
                // Flow 3 -- Partner (Partner Location is optional, left empty).
                pickMany2one("partner_id", "TOUR EEA Partner"),
                [
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

        // IK: docs/employee_external_assignment/02-edit.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Find and open the record to edit.
                openRecordByEmployee("TOUR EEA Edit Employee"),
                [
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

                    // Flow 4 -- Change the End Date field.
                    {
                        content: "Change the End Date",
                        trigger: ".o_field_widget[name='date_end'] input",
                        run: "text 06/30/2027",
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

        // IK: docs/employee_external_assignment/03-delete.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to delete.
                openRecordByEmployee("TOUR EEA Delete Employee"),
                [
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

                    // Flow 5 -- Click the Employee External Assignments
                    // breadcrumb to return to the list (after a delete, the
                    // form may show the next record in the list instead of
                    // navigating back on its own).
                    {
                        content: "Click the Employee External Assignments breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Employee External Assignments)",
                    },

                    // Post-Condition -- the record is permanently removed;
                    // list no longer shows it.
                    {
                        content: "Record no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR EEA Delete Employee)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment/04-confirm.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_confirm",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to confirm.
                openRecordByEmployee("TOUR EEA Confirm Employee"),
                [
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

        // IK: docs/employee_external_assignment/05-approve.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_approve",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to approve.
                openRecordByEmployee("TOUR EEA Approve Employee"),
                [
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

                    // Post-Condition -- the approval is fulfilled and status
                    // automatically changes to On Progress (confirm -> open
                    // happens automatically once approved).
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

        // IK: docs/employee_external_assignment/06-reject.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_reject",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to reject.
                openRecordByEmployee("TOUR EEA Reject Employee"),
                [
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

        // IK: docs/employee_external_assignment/10-cancel.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_cancel",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to cancel.
                openRecordByEmployee("TOUR EEA Cancel Employee"),
                [
                    // Flow 3 -- Click the Cancel button (opens the reason
                    // wizard; the rendered button name is a numeric action
                    // id, so match by label instead of button[name=...]).
                    {
                        content: "Click the Cancel button",
                        trigger:
                            ".o_statusbar_buttons button:enabled:contains('Cancel')",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        // 14.0: JANGAN prefiks `.modal` -- trigger dicari DI
                        // DALAM modal, jadi `.o_form_view` saja. Lihat
                        // patterns.md skill odoo-development-ui-test §H.
                        content: "Wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- In the wizard, select the Reason (radio
                    // widget).
                    {
                        content: "Select the cancellation reason",
                        trigger:
                            ".o_field_widget[name='cancel_reason_id'] " +
                            ".o_radio_item:contains(TOUR EEA Cancel Reason) input",
                        run: "click",
                    },

                    // Flow 5 -- Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    {
                        // The wizard's Confirm button itself carries a
                        // "Are you sure?" confirm attribute, stacking a
                        // second dialog on top; `$modal_displayed` now
                        // resolves to that topmost dialog.
                        content: "Confirm the Are you sure? dialog",
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

        // IK: docs/employee_external_assignment/11-terminate.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_terminate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to terminate.
                openRecordByEmployee("TOUR EEA Terminate Employee"),
                [
                    // Flow 3 -- Click the Terminate button (opens the reason
                    // wizard; the rendered button name is a numeric action
                    // id, so match by label instead of button[name=...]).
                    {
                        content: "Click the Terminate button",
                        trigger:
                            ".o_statusbar_buttons button:enabled:contains('Terminate')",
                        extra_trigger: ".o_form_view",
                    },
                    {
                        // 14.0: JANGAN prefiks `.modal` -- lihat patterns.md
                        // skill odoo-development-ui-test §H.
                        content: "Wizard is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- In the wizard, select the Reason (radio
                    // widget).
                    {
                        content: "Select the termination reason",
                        trigger:
                            ".o_field_widget[name='terminate_reason_id'] " +
                            ".o_radio_item:contains(TOUR EEA Terminate Reason) input",
                        run: "click",
                    },

                    // Flow 5 -- Click Confirm.
                    {
                        content: "Confirm the wizard",
                        trigger: ".modal-footer button[name='action_confirm']",
                    },
                    {
                        // Second stacked "Are you sure?" dialog from the
                        // wizard's own Confirm button.
                        content: "Confirm the Are you sure? dialog",
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

        // IK: docs/employee_external_assignment/12-restart.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_restart",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record to restart.
                openRecordByEmployee("TOUR EEA Restart Employee"),
                [
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

        // IK: docs/employee_external_assignment/13-reset-number.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_reset_number",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Assignments menu.
                openAssignmentList(),
                // Flow 2 -- Open the record whose document number will be
                // reset.
                openRecordByEmployee("TOUR EEA Reset Number Employee"),
                [
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
                    // After the reset, the form re-renders read-only, so the
                    // visible field is "display_name" (not the edit-only
                    // "name" field); name_get() renders "/" as "*<id>", which
                    // is the observable marker that the reset took effect.
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
    }
);
