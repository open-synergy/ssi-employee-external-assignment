// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment.employee_external_assignment_type_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Shared navigation block reused by every tour below -- corresponds to
        // Flow 1 of every employee_external_assignment_type IK: "Open the Human
        // Resource > Configuration > Career > External Asssignment Types menu."
        // Note: the menu item label is "External Asssignment Types" (as
        // literally defined in menu.xml), while the window action -- and
        // therefore the breadcrumb title once the list is loaded -- is
        // "Employee External Assignment Types".
        function openTypeList() {
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
                    content: "Open the Career menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_career_configuration"]',
                },
                {
                    content: "Open the External Asssignment Types menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment.employee_external_assignment_type_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang, bukan
                    // sekadar "ada list di layar" (lihat patterns.md skill
                    // odoo-development-ui-test §A).
                    content: "Employee External Assignment Types list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Types)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/employee_external_assignment_type/01-create.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_type_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Human Resource > Configuration > Career >
                // External Asssignment Types menu.
                openTypeList(),
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
                        run: "text TOUR EEAT Create",
                    },
                    {
                        content: "Fill in the Code",
                        trigger: ".o_field_widget[name='code']",
                        run: "text /",
                    },

                    // Flow 4 -- On the Partner tab, Partner Selection Method is
                    // left at its "Domain" default -- asserting the allow-list
                    // values themselves is unit test territory, not tour
                    // territory.
                    {
                        content: "Open the Partner tab",
                        trigger: ".o_notebook .nav-link:contains(Partner)",
                    },
                    {
                        content: "Partner tab is displayed",
                        trigger: ".o_field_widget[name='partner_selection_method']",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 5 -- On the Employee tab, Selecton Method is left at
                    // its "Domain" default.
                    {
                        content: "Open the Employee tab",
                        trigger: ".o_notebook .nav-link:contains(Employee)",
                    },
                    {
                        content: "Employee tab is displayed",
                        trigger: ".o_field_widget[name='employee_selection_method']",
                        run: function () {
                            // Assertion only.
                        },
                    },

                    // Flow 6 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- a new record is created (availability as
                    // Type on an employee external assignment is exercised by
                    // the ssi_employee_external_assignment create tour).
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

        // IK: docs/employee_external_assignment_type/02-edit.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_type_edit",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the External Asssignment Types menu.
                openTypeList(),
                [
                    // Flow 2 -- Find and open the record to edit.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAT Edit) .o_data_cell:first",
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
                        run: "text TOUR EEAT Edit Changed",
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

        // IK: docs/employee_external_assignment_type/03-delete.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_type_delete",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the External Asssignment Types menu.
                openTypeList(),
                [
                    // Flow 2 -- Open the record to delete.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAT Delete) .o_data_cell:first",
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

                    // Flow 5 -- Click the External Asssignment Types breadcrumb
                    // to return to the list (after a delete, the form may show
                    // the next record in the list instead of navigating back on
                    // its own).
                    {
                        content:
                            "Click the Employee External Assignment Types breadcrumb",
                        trigger:
                            ".breadcrumb-item.o_back_button a:contains(Employee External Assignment Types)",
                    },

                    // Post-Condition -- the record is permanently removed; list
                    // no longer shows it.
                    {
                        content: "Record no longer in the list",
                        trigger:
                            ".o_list_view:not(:has(.o_data_row:contains(TOUR EEAT Delete)))",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/employee_external_assignment_type/04-deactivate.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_type_deactivate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the External Asssignment Types menu.
                openTypeList(),
                [
                    // Flow 2 -- Open the record to deactivate.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR EEAT Deactivate) .o_data_cell:first",
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

        // IK: docs/employee_external_assignment_type/05-activate.md
        tour.register(
            "ssi_employee_external_assignment_employee_external_assignment_type_activate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the External Asssignment Types menu.
                openTypeList(),
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
                            ".o_data_row:contains(TOUR EEAT Activate) .o_data_cell:first",
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
