# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignment(YamlTransactionCase):
    def test_employee_external_assignment(self):
        self.run_yaml_scenario("test_data_employee_external_assignment.yaml")

    def test_onchange_partner_location_cleared_on_partner_change(self):
        """Changing partner_id must clear partner_location_id."""
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Onchange Test Type",
                "code": "OCT001",
            }
        )
        partner = self.env["res.partner"].create({"name": "Onchange Partner"})
        employee = self.env["hr.employee"].create({"name": "Onchange Employee"})
        form = Form(self.env["employee_external_assignment"])
        form.type_id = assignment_type
        form.employee_id = employee
        form.partner_id = partner
        form.date_start = "2026-01-01"
        form.date_end = "2026-12-31"
        # Change partner: partner_location_id should be cleared
        new_partner = self.env["res.partner"].create({"name": "New Onchange Partner"})
        form.partner_id = new_partner
        self.assertFalse(form.partner_location_id._origin)

    def test_onchange_type_clears_partner_and_employee(self):
        """Changing type_id must clear partner_id and employee_id."""
        type1 = self.env["employee_external_assignment_type"].create(
            {"name": "Type OCH 1", "code": "OCH001"}
        )
        type2 = self.env["employee_external_assignment_type"].create(
            {"name": "Type OCH 2", "code": "OCH002"}
        )
        partner = self.env["res.partner"].create({"name": "OCH Partner"})
        employee = self.env["hr.employee"].create({"name": "OCH Employee"})
        form = Form(self.env["employee_external_assignment"])
        form.type_id = type1
        form.employee_id = employee
        form.partner_id = partner
        form.date_start = "2026-01-01"
        form.date_end = "2026-12-31"
        # Change type: partner_id and employee_id should be cleared
        form.type_id = type2
        self.assertFalse(form.partner_id._origin)
        self.assertFalse(form.employee_id._origin)
