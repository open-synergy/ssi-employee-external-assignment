// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement_revenue_recognition." +
        "employee_external_assignment_type_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/employee_external_assignment_type/01-create.md (delta,
        // this module) -- Extends ssi_employee_external_assignment, aksi
        // 01-create. Navigation is sourced from the base IK Flow 1-2; the
        // only new assertion is that the PoB Product field is displayed on
        // the new Revenue Recognition tab. The tour stops here -- it does
        // not continue to fill in the remaining base fields or Save.
        tour.register(
            "ssi_employee_external_assignment_agreement_revenue_recognition_" +
                "employee_external_assignment_type_create",
            {
                test: true,
                url: "/web",
            },
            [
                tour.stepUtils.showAppsMenuItem(),
                {
                    // ── Flow 1 (base) -- Open the Human Resource app.
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
                },
                {
                    // ── Flow 1 (base) -- Open the Configuration menu.
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.menu_human_resource_configuration"]',
                },
                {
                    // ── Flow 1 (base) -- "Career" is a grouping menuitem
                    // with no action of its own, so 14.0 renders it as a
                    // non-clickable dropdown header; "External Asssignment
                    // Types" sits directly beneath it in the same dropdown.
                    content: "Open the External Asssignment Types menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment.employee_external_assignment_type_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang
                    // (lihat patterns.md skill odoo-development-ui-test §A).
                    content: "Employee External Assignment Types list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Types)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    // ── Flow 2 (base) -- Click the New button.
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
                {
                    // ── Additional Fields (delta) -- open the Revenue
                    // Recognition tab.
                    content: "Open the Revenue Recognition tab",
                    trigger: ".o_notebook .nav-link:contains(Revenue Recognition)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // ── Additional Fields (delta) -- the PoB Product field
                    // is displayed. This is where the tour stops.
                    content: "PoB Product field is displayed",
                    trigger: ".o_field_widget[name='pob_product_id']",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
