// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_employee_external_assignment_agreement_operating_unit." +
        "employee_external_assignment_agreement_batch_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/employee_external_assignment_agreement_batch/01-create.md
        // (delta, this module) -- Extends
        // ssi_employee_external_assignment_agreement, aksi 01-create.
        // Navigation is sourced from the base IK Flow 1-2; the only new
        // assertion is that the Operating Unit field is displayed. The
        // tour stops here -- it does not continue to fill in the
        // remaining base fields or Save.
        tour.register(
            "ssi_employee_external_assignment_agreement_operating_unit_" +
                "employee_external_assignment_agreement_batch_create",
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
                    // ── Flow 1 (base) -- Open the Career Management menu.
                    content: "Open the Career Management menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_hr.hr_career_management_menu"]',
                },
                {
                    // ── Flow 1 (base) -- Open the Agreement Batches menu.
                    content: "Open the Agreement Batches menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_employee_external_assignment_agreement.employee_external_assignment_agreement_batch_menu"]',
                },
                {
                    // Gerbang: tunggu action TUJUAN benar-benar terpasang
                    // (lihat patterns.md skill odoo-development-ui-test §A).
                    content:
                        "Employee External Assignment Agreement Batches list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Employee External Assignment Agreement Batches)",
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
                    // ── Additional Fields (delta) -- the Operating Unit
                    // field is displayed on the create form. This is where
                    // the tour stops.
                    content: "Operating Unit field is displayed",
                    trigger: ".o_field_widget[name='operating_unit_id']",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
