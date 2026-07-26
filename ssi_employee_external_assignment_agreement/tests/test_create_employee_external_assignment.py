# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCreateEmployeeExternalAssignment(YamlTransactionCase):
    def test_create_employee_external_assignment(self):
        self.run_yaml_scenario("test_data_create_employee_external_assignment.yaml")

    def test_action_create_assignment_returns_action(self):
        """Python murni -- pemicu P1 (L-01: action `call` membuang nilai balik).

        `action_create_assignment` mengembalikan dict ``ir.actions.act_window``
        yang dibatasi pada assignment yang baru dibuat; YAML tidak bisa
        meng-assert nilai balik method sama sekali.
        """
        admin = self.env.ref("base.user_admin")
        journal = self.env["account.journal"].search(
            [("type", "in", ["general", "sale", "purchase", "bank", "cash"])],
            limit=1,
        )
        receivable_account = self.env["account.account"].search(
            [("user_type_id.type", "=", "receivable")], limit=1
        )
        currency = self.env["res.currency"].search(
            [("active", "in", [True, False])], limit=1
        )
        pricelist = self.env["product.pricelist"].search([], limit=1)
        partner = self.env["res.partner"].create(
            {"name": "Test CEEA Partner P1", "is_company": True}
        )
        assignment_type = (
            self.env["employee_external_assignment_type"]
            .with_user(admin)
            .create(
                {
                    "name": "Test CEEA P1 Type",
                    "code": "TCEEAP1",
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
        )
        job = self.env["hr.job"].create({"name": "Test CEEA Job P1"})
        employee = self.env["hr.employee"].create(
            {"name": "Test CEEA Employee P1", "job_id": job.id}
        )
        agreement = (
            self.env["employee_external_assignment_agreement"]
            .with_user(admin)
            .create(
                {
                    "type_id": assignment_type.id,
                    "title": "Test CEEA Agreement P1",
                    "partner_id": partner.id,
                    "receivable_account_id": receivable_account.id,
                    "journal_id": journal.id,
                    "currency_id": currency.id,
                    "pricelist_id": pricelist.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "detail_ids": [(0, 0, {"job_id": job.id})],
                }
            )
        )
        agreement.with_user(admin).action_confirm()
        agreement.invalidate_cache()
        agreement.with_user(admin).action_approve_approval()
        self.assertEqual(agreement.state, "open")

        wizard = (
            self.env["create_employee_external_assignment"]
            .with_user(admin)
            .create(
                {
                    "agreement_id": agreement.id,
                    "employee_ids": [(6, 0, [employee.id])],
                }
            )
        )
        action = wizard.with_user(admin).action_create_assignment()

        created = self.env["employee_external_assignment"].search(
            [("agreement_id", "=", agreement.id), ("employee_id", "=", employee.id)]
        )
        self.assertEqual(len(created), 1)
        self.assertEqual(action["res_model"], "employee_external_assignment")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["domain"], [("id", "in", created.ids)])
