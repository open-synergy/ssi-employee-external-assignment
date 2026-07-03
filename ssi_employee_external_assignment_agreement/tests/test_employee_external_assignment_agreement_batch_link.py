# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementBatchLink(YamlTransactionCase):
    def test_employee_external_assignment_agreement_batch_link(self):
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_batch_link.yaml"
        )

    def _create_common(self):
        journal = self.env["account.journal"].search(
            [("type", "in", ["general", "sale", "purchase", "bank", "cash"])],
            limit=1,
        )
        receivable_account = self.env["account.account"].search(
            [("user_type_id.type", "=", "receivable")], limit=1
        )
        currency = self.env["res.currency"].search([], limit=1)
        pricelist = self.env["product.pricelist"].search([], limit=1)
        partner = self.env["res.partner"].create(
            {
                "name": "Test Guard/Constrain Partner",
                "is_company": True,
            }
        )
        assignment_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Guard/Constrain Type",
                "code": "TEEABLPY001",
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
        batch = self.env["employee_external_assignment_agreement_batch"].create(
            {
                "type_id": assignment_type.id,
                "title": "Test Guard/Constrain Batch",
                "partner_id": partner.id,
                "currency_id": currency.id,
                "pricelist_id": pricelist.id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        return {
            "journal": journal,
            "receivable_account": receivable_account,
            "currency": currency,
            "pricelist": pricelist,
            "partner": partner,
            "assignment_type": assignment_type,
            "batch": batch,
        }

    def test_guard_action_confirm_raises_when_batch_driven(self):
        """Calling action_confirm directly on a batch-linked agreement
        must be rejected; only cascading from the batch is allowed."""
        data = self._create_common()
        agreement = self.env["employee_external_assignment_agreement"].create(
            {
                "batch_id": data["batch"].id,
                "type_id": data["assignment_type"].id,
                "title": "Test Guard Agreement",
                "partner_id": data["partner"].id,
                "receivable_account_id": data["receivable_account"].id,
                "journal_id": data["journal"].id,
                "currency_id": data["currency"].id,
                "pricelist_id": data["pricelist"].id,
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
            }
        )
        with self.assertRaises(UserError):
            agreement.action_confirm()

    def test_constrain_period_outside_batch_raises(self):
        """An agreement's period must stay within its batch's period."""
        data = self._create_common()
        with self.assertRaises(ValidationError):
            self.env["employee_external_assignment_agreement"].create(
                {
                    "batch_id": data["batch"].id,
                    "type_id": data["assignment_type"].id,
                    "title": "Test Out Of Period Agreement",
                    "partner_id": data["partner"].id,
                    "receivable_account_id": data["receivable_account"].id,
                    "journal_id": data["journal"].id,
                    "currency_id": data["currency"].id,
                    "pricelist_id": data["pricelist"].id,
                    "date_start": "2026-01-01",
                    "date_end": "2027-01-31",
                }
            )

    def test_constrain_different_partner_raises(self):
        """An agreement linked to a batch must share the batch's partner."""
        data = self._create_common()
        other_partner = self.env["res.partner"].create(
            {
                "name": "Test Other Partner",
                "is_company": True,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["employee_external_assignment_agreement"].create(
                {
                    "batch_id": data["batch"].id,
                    "type_id": data["assignment_type"].id,
                    "title": "Test Mismatched Partner Agreement",
                    "partner_id": other_partner.id,
                    "receivable_account_id": data["receivable_account"].id,
                    "journal_id": data["journal"].id,
                    "currency_id": data["currency"].id,
                    "pricelist_id": data["pricelist"].id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )

    def test_onchange_snapshot_from_batch(self):
        """Selecting batch_id on the agreement Form must snapshot
        type_id, partner_id, contact_partner_id, period, currency, and
        pricelist from the batch, even though several of these fields are
        also targeted by pre-existing onchange handlers triggered by
        type_id/partner_id/currency_id (which must not wipe the snapshot)."""
        data = self._create_common()
        contact = self.env["res.partner"].create(
            {
                "name": "Test Batch Contact",
                "type": "contact",
                "parent_id": data["partner"].id,
            }
        )
        data["batch"].write({"contact_partner_id": contact.id})

        # Sanity: start the Form with a DIFFERENT type/partner so the
        # existing onchange_partner_id/onchange_partner_location_id chains
        # actually have something to reset, proving the batch snapshot wins.
        other_type = self.env["employee_external_assignment_type"].create(
            {
                "name": "Test Guard/Constrain Other Type",
                "code": "TEEABLPY002",
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
        other_partner = self.env["res.partner"].create(
            {
                "name": "Test Other Starting Partner",
                "is_company": True,
            }
        )

        form = Form(self.env["employee_external_assignment_agreement"])
        form.type_id = other_type
        form.partner_id = other_partner
        form.title = "Test Snapshot Agreement"
        form.receivable_account_id = data["receivable_account"]
        form.journal_id = data["journal"]
        form.batch_id = data["batch"]

        self.assertEqual(form.type_id.id, data["assignment_type"].id)
        self.assertEqual(form.partner_id.id, data["partner"].id)
        self.assertEqual(form.contact_partner_id.id, contact.id)
        self.assertEqual(form.date_start, data["batch"].date_start)
        self.assertEqual(form.date_end, data["batch"].date_end)
        self.assertEqual(form.currency_id.id, data["batch"].currency_id.id)
        self.assertEqual(form.pricelist_id.id, data["batch"].pricelist_id.id)
