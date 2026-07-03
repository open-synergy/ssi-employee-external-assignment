# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementBatchOperatingUnit(YamlTransactionCase):
    def test_employee_external_assignment_agreement_batch_operating_unit(self):
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_batch_operating_unit.yaml"
        )

    def test_batch_operating_unit_mismatch_raises(self):
        """Writing an agreement's operating unit different from its linked
        batch's operating unit must raise UserError."""
        operating_unit = self.env["operating.unit"].search([], limit=1)
        other_operating_unit = self.env["operating.unit"].create(
            {
                "name": "Test Mismatch OU Secondary",
                "code": "TMOU-SEC",
                "partner_id": self.env.ref("base.main_partner").id,
                "company_id": self.env.ref("base.main_company").id,
            }
        )
        currency = self.env["res.currency"].search(
            [("active", "in", [True, False])], limit=1
        )
        pricelist = self.env["product.pricelist"].search([], limit=1)
        journal = self.env["account.journal"].search(
            [("type", "in", ["general", "sale", "purchase", "bank", "cash"])],
            limit=1,
        )
        receivable_account = self.env["account.account"].search(
            [("user_type_id.type", "=", "receivable")], limit=1
        )
        partner = self.env["res.partner"].create(
            {"name": "Test Mismatch OU Partner", "is_company": True}
        )
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Mismatch OU Type",
                "code": "TMOU-01",
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
        batch = (
            self.env["employee_external_assignment_agreement_batch"]
            .with_user(self.env.ref("base.user_admin"))
            .create(
                {
                    "type_id": assignment_type.id,
                    "title": "Test Mismatch OU Batch",
                    "partner_id": partner.id,
                    "currency_id": currency.id,
                    "pricelist_id": pricelist.id,
                    "operating_unit_id": operating_unit.id,
                    "date": "2026-01-01",
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )
        agreement = (
            self.env["employee_external_assignment_agreement"]
            .with_user(self.env.ref("base.user_admin"))
            .create(
                {
                    "batch_id": batch.id,
                    "type_id": assignment_type.id,
                    "title": "Test Mismatch OU Agreement",
                    "partner_id": partner.id,
                    "receivable_account_id": receivable_account.id,
                    "journal_id": journal.id,
                    "currency_id": currency.id,
                    "pricelist_id": pricelist.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )
        with self.assertRaises(UserError):
            agreement.write({"operating_unit_id": other_operating_unit.id})
