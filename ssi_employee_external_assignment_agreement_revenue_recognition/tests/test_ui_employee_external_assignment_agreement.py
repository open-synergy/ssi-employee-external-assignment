# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreement(HttpSavepointCase):
    """Tour tests for the ``employee_external_assignment_agreement`` PoB IK."""

    @classmethod
    def setUpClass(cls):
        """Prepare the records used by the create and create-pob tours."""
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        cls.currency = cls.env.ref("base.EUR")
        cls.pricelist = cls.env.ref("product.list0")
        cls.journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR Journal",
                    "code": "TEEARRJ",
                    "type": "general",
                }
            )
        )
        cls.account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR Receivable",
                    "code": "TEEARR1",
                    "user_type_id": cls.env.ref(
                        "account.data_account_type_receivable"
                    ).id,
                    "reconcile": True,
                }
            )
        )

        # Pre-Condition docs/employee_external_assignment_agreement/01-create.md
        # (Modified Flow, this module's delta): a Type (no PoB Product
        # needed -- the create tour only asserts the button is displayed,
        # it never clicks it) and a Job selectable on the Details dialog.
        cls.create_type = (
            cls.env["employee_external_assignment_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR Create Type",
                    "code": "/",
                }
            )
        )
        cls.create_job = (
            cls.env["hr.job"]
            .with_user(cls.admin)
            .create({"name": "TOUR EEARR Create Job"})
        )

        # Pre-Condition docs/employee_external_assignment_agreement/07-create-pob.md:
        # status On Progress, PoB Product configured on Type, one Details
        # line already linked to a Job.
        cls.pob_product = (
            cls.env["product.product"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR PoB Product",
                    "type": "service",
                }
            )
        )
        cls.create_pob_type = (
            cls.env["employee_external_assignment_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR Create PoB Type",
                    "code": "/",
                    "pob_product_id": cls.pob_product.id,
                }
            )
        )
        cls.create_pob_job = (
            cls.env["hr.job"]
            .with_user(cls.admin)
            .create({"name": "TOUR EEARR Create PoB Job"})
        )
        cls.create_pob_partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEARR Create PoB Partner",
                    "is_company": True,
                }
            )
        )
        cls.agreement_create_pob = (
            cls.env["employee_external_assignment_agreement"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": cls.create_pob_type.id,
                    "title": "TOUR EEARR Create PoB",
                    "partner_id": cls.create_pob_partner.id,
                    "receivable_account_id": cls.account.id,
                    "journal_id": cls.journal.id,
                    "currency_id": cls.currency.id,
                    "pricelist_id": cls.pricelist.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                    "detail_ids": [
                        (0, 0, {"job_id": cls.create_pob_job.id, "quantity": 1})
                    ],
                }
            )
        )
        cls.agreement_create_pob.with_user(cls.admin).action_confirm()
        # approval.approval records created by action_confirm() are read by
        # action_approve_approval() in the same transaction -- invalidate
        # the cache so it sees them (same pattern used by the base
        # module's test_ui_employee_external_assignment_agreement.py).
        cls.agreement_create_pob.invalidate_cache()
        cls.agreement_create_pob.with_user(cls.admin).action_approve_approval()

    def test_create(self):
        """Run the create delta tour for the agreement.

        IK: docs/employee_external_assignment_agreement/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_revenue_recognition_"
            "employee_external_assignment_agreement_create",
            login="admin",
        )

    def test_create_pob(self):
        """Run the standalone Create PoB tour on an On Progress agreement.

        IK: docs/employee_external_assignment_agreement/07-create-pob.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_revenue_recognition_"
            "employee_external_assignment_agreement_create_pob",
            login="admin",
        )
