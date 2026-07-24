// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_input_type_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds to
        // Flow 1 of every employee_external_assignment_agreement_input_type IK:
        // "Open the Human Resource > Configuration > Career > External
        // Assignment > Agreement Input Types menu."
        // Note: both "Career" (ssi_hr.menu_career_configuration) and
        // "External Assignment" (ssi_employee_external_assignment
        // .menu_external_assignment_config) are grouping menuitems with no
        // action= attribute, so Odoo 14.0 renders each of them as a plain,
        // non-clickable "<div class='dropdown-header'>" inside the
        // Configuration dropdown -- NOT as a data-menu-xmlid link. "Agreement
        // Input Types" is the only clickable entry among them, so there is no
        // separate "click Career" / "click External Assignment" step.
        function openInputTypeList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
                },
                {
                    content: "Open the Agreement Input Types menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_input_type_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                    // sekadar "ada list di layar" (lihat patterns.md skill
                    // odoo-development-ui-test §A).
                    content:
                        "External Assignment Agreement Input Types list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(External Assignment Agreement Input Types)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/employee_external_assignment_agreement_input_type/01-create.md
        tour.register(
            "ssi_employee_external_assignment_agreement_input_type_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Human Resource > Configuration > Career >
                // External Assignment > Agreement Input Types menu.
                openInputTypeList(),
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

                    // Flow 3 -- Fill in the required fields: Name, Code.
                    {
                        content: "Fill in the Name",
                        trigger: ".o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR EEAAIT Create",
                    },
                    {
                        content: "Fill in the Code",
                        trigger: ".o_field_widget[name='code']",
                        run: "text /",
                    },

                    // Flow 4 -- Go to the Default Amount tab and set Default
                    // Amount.
                    {
                        content: "Open the Default Amount tab",
                        trigger: ".o_notebook .nav-link:contains(Default Amount)",
                    },
                    {
                        content: "Fill in the Default Amount",
                        trigger: ".o_field_widget[name='default_amount']",
                        run: "text 100",
                    },

                    // Flow 5 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- a new record is created (availability as
                    // Input Type on an Employee External Assignment Agreement
                    // Input record is exercised by that model's own create
                    // tour, out of scope here).
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

        // IK: docs/employee_external_assignment_agreement_input_type/02-edit.md
        tour.register(
            "ssi_employee_external_assignment_agreement_input_type_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Input Types menu.
                openInputTypeList(),
                [
                    // Flow 2 -- Find and open the record to edit.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAAIT Edit) .o_data_cell:first",
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
                        content: "Change the Name",
                        trigger: ".o_field_widget[name='name']",
                        run: "text TOUR EEAAIT Edit Changed",
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

        // IK: docs/employee_external_assignment_agreement_input_type/03-delete.md
        tour.register(
            "ssi_employee_external_assignment_agreement_input_type_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Input Types menu.
                openInputTypeList(),
                [
                    // Flow 2 -- Open the record to delete.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAAIT Delete) .o_data_cell:first",
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

                    // Flow 5 -- Click the External Assignment Agreement Input
                    // Types breadcrumb to return to the list (after a delete,
                    // the form may show the next record in the list instead
                    // of navigating back on its own).
                    {
                        content:
                            "Click the External Assignment Agreement Input Types breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(External Assignment Agreement Input Types)",
                    },

                    // Post-Condition -- the record is permanently removed; list
                    // no longer shows it.
                    {
                        content: "Record no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR EEAAIT Delete)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_input_type/04-deactivate.md
        tour.register(
            "ssi_employee_external_assignment_agreement_input_type_deactivate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Input Types menu.
                openInputTypeList(),
                [
                    // Flow 2 -- Open the record to deactivate.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAAIT Deactivate) .o_data_cell:first",
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

                    // Flow 4 -- Toggle the Active field off.
                    {
                        content: "Toggle the Active field off",
                        trigger: ".o_field_widget[name='active'] input",
                        run: "click",
                    },

                    // Flow 5 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- Archived ribbon appears on the form.
                    {
                        content: "Archived ribbon is displayed",
                        trigger: ".o_form_view .ribbon:visible:contains(Archived)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_agreement_input_type/05-activate.md
        tour.register(
            "ssi_employee_external_assignment_agreement_input_type_activate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Agreement Input Types menu.
                openInputTypeList(),
                [
                    // Flow 2 -- Enable the Archived filter in the search bar.
                    {
                        content: "Wait for the list data to finish loading",
                        trigger: ".o_list_view .o_data_row",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Open the Filters menu",
                        trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                        run: function () {
                            // Dropdown Owl 14.0 tidak selalu terbuka oleh klik
                            // sintetis default -- pakai klik browser asli.
                            this.$anchor[0].click();
                        },
                    },
                    {
                        content: "Enable the Archived filter",
                        trigger: ".o_filter_menu .o_menu_item:contains(Archived) a",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },

                    // Flow 3 -- Open the archived record to reactivate.
                    {
                        content: "Open the archived record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAAIT Activate) .o_data_cell:first",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open",
                        trigger: ".o_form_view",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 4 -- Click the Edit button.
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

                    // Flow 5 -- Toggle the Active field on.
                    {
                        content: "Toggle the Active field on",
                        trigger: ".o_field_widget[name='active'] input",
                        run: "click",
                    },

                    // Flow 6 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- Archived ribbon no longer appears.
                    {
                        content: "Archived ribbon is no longer displayed",
                        trigger:
                            ".o_form_view:not(:has(.ribbon:visible:contains(Archived)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
