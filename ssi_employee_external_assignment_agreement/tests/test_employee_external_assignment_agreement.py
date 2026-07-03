# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreement(YamlTransactionCase):
    def test_employee_external_assignment_agreement(self):
        self.run_yaml_scenario("test_data_employee_external_assignment_agreement.yaml")

    def test_onchange_usage_id_from_type(self):
        """Changing type_id must populate usage_id from the type's default usage."""
        account_type = self.env["account.account.type"].search(
            [("type", "=", "other")], limit=1
        )
        account = self.env["account.account"].create(
            {
                "name": "Test Onchange Usage Account",
                "code": "999210",
                "user_type_id": account_type.id,
            }
        )
        usage_type = self.env["product.usage_type"].create(
            {
                "name": "Test Onchange Usage Type",
                "code": "EEAAOC001",
                "account_id": account.id,
            }
        )
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Onchange Type",
                "code": "EEAAOCT001",
                "employee_selection_method": "domain",
                "employee_domain": "[]",
                "job_selection_method": "domain",
                "job_domain": "[]",
                "salary_rule_selection_method": "domain",
                "salary_rule_domain": "[]",
                "other_fee_category_selection_method": "domain",
                "other_fee_category_domain": "[]",
                "other_fee_selection_method": "domain",
                "other_fee_domain": "[]",
                "usage_id": usage_type.id,
            }
        )
        form = Form(self.env["employee_external_assignment_agreement"])
        form.type_id = assignment_type
        self.assertEqual(form.usage_id.id, usage_type.id)

        other_assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Onchange Type Without Usage",
                "code": "EEAAOCT002",
                "employee_selection_method": "domain",
                "employee_domain": "[]",
                "job_selection_method": "domain",
                "job_domain": "[]",
                "salary_rule_selection_method": "domain",
                "salary_rule_domain": "[]",
                "other_fee_category_selection_method": "domain",
                "other_fee_category_domain": "[]",
                "other_fee_selection_method": "domain",
                "other_fee_domain": "[]",
            }
        )
        form.type_id = other_assignment_type
        self.assertFalse(form.usage_id._origin)
