# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementBatch(YamlTransactionCase):
    def test_employee_external_assignment_agreement_batch(self):
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_batch.yaml"
        )

    def test_onchange_partner_id_reset_on_type_change(self):
        """Changing type_id on the batch must clear partner_id."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Onchange Batch Partner",
                "is_company": True,
            }
        )
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Onchange Batch Type",
                "code": "EEABOCT001",
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
        other_assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Onchange Batch Other Type",
                "code": "EEABOCT002",
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
        form = Form(self.env["employee_external_assignment_agreement_batch"])
        form.type_id = assignment_type
        form.partner_id = partner
        form.type_id = other_assignment_type
        self.assertFalse(form.partner_id._origin)

    def test_onchange_partner_location_id_reset_on_partner_change(self):
        """Changing partner_id on the batch must clear partner_location_id."""
        partner = self.env["res.partner"].create(
            {
                "name": "Test Onchange Batch Location Partner",
                "is_company": True,
            }
        )
        location = self.env["res.partner"].create(
            {
                "name": "Test Onchange Batch Location",
                "type": "other",
                "parent_id": partner.id,
            }
        )
        other_partner = self.env["res.partner"].create(
            {
                "name": "Test Onchange Batch Other Partner",
                "is_company": True,
            }
        )
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Onchange Batch Location Type",
                "code": "EEABOCT003",
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
        form = Form(self.env["employee_external_assignment_agreement_batch"])
        form.type_id = assignment_type
        form.partner_id = partner
        form.partner_location_id = location
        form.partner_id = other_partner
        self.assertFalse(form.partner_location_id._origin)
