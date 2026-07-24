# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreement(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        # "EUR" (base) and "Public Pricelist" (product.list0) are core, non-demo
        # Odoo data always present, and Public Pricelist's currency defaults to
        # the main company currency (EUR) at install time -- so the two always
        # match the domain [('currency_id', '=', currency_id)] on
        # pricelist_id.
        cls.currency = cls.env.ref("base.EUR")
        cls.pricelist = cls.env.ref("product.list0")
        cls.journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Journal",
                    "code": "TEEAJ",
                    "type": "general",
                }
            )
        )
        cls.account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Receivable",
                    "code": "TEEAA1",
                    "user_type_id": cls.env.ref(
                        "account.data_account_type_receivable"
                    ).id,
                    "reconcile": True,
                }
            )
        )
        cls.assignment_type = (
            cls.env["employee_external_assignment_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Type",
                    "code": "/",
                }
            )
        )
        # Partner used only by the 01-create tour itself (typed/picked live in
        # the browser, never searched for in a list). Named so it is NOT a
        # prefix of the per-scenario "TOUR EEAA Partner <Label>" partners
        # created below -- otherwise typing this name into the autocomplete
        # would also match those and make the dropdown pick ambiguous.
        cls.partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Create Partner",
                    "is_company": True,
                }
            )
        )
        # Global cancel/terminate reasons so they are selectable regardless of
        # whether ssi_transaction_cancel_mixin/ssi_transaction_terminate_mixin
        # demo data is loaded.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Cancel Reason",
                    "code": "TEEAACR",
                    "global_use": True,
                }
            )
        )
        cls.terminate_reason = (
            cls.env["base.terminate_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Terminate Reason",
                    "code": "TEEAATR",
                    "global_use": True,
                }
            )
        )

        # NOTE on how tour steps find "the record to <action>" in the list:
        # the default list view shows "# Document" (display_name, i.e. the
        # document number -- "/" for every Draft record, since the sequence
        # only applies once a record reaches Open) and "Partner", but NOT
        # "Title". Document number is therefore useless to disambiguate rows,
        # so each scenario below gets its OWN partner and the tour looks up
        # the row by that partner's name instead of the agreement title.
        def _create_agreement(label):
            partner = (
                cls.env["res.partner"]
                .with_user(cls.admin)
                .create(
                    {
                        "name": "TOUR EEAA Partner %s" % label,
                        "is_company": True,
                    }
                )
            )
            return (
                cls.env["employee_external_assignment_agreement"]
                .with_user(cls.admin)
                .create(
                    {
                        "type_id": cls.assignment_type.id,
                        "title": "TOUR EEAA %s" % label,
                        "partner_id": partner.id,
                        "receivable_account_id": cls.account.id,
                        "journal_id": cls.journal.id,
                        "currency_id": cls.currency.id,
                        "pricelist_id": cls.pricelist.id,
                        "date_start": "2026-01-01",
                        "date_end": "2026-12-31",
                    }
                )
            )

        cls.agreement_edit = _create_agreement("Edit")
        cls.agreement_delete = _create_agreement("Delete")
        cls.agreement_confirm = _create_agreement("Confirm")

        # Pre-Condition 05-approve.md / 06-reject.md: Waiting for Approval.
        cls.agreement_approve = _create_agreement("Approve")
        cls.agreement_approve.with_user(cls.admin).action_confirm()

        cls.agreement_reject = _create_agreement("Reject")
        cls.agreement_reject.with_user(cls.admin).action_confirm()

        # Pre-Condition 10-cancel.md: Draft (one of the allowed states).
        cls.agreement_cancel = _create_agreement("Cancel")

        # Pre-Condition 11-terminate.md: On Progress.
        cls.agreement_terminate = _create_agreement("Terminate")
        cls.agreement_terminate.with_user(cls.admin).action_confirm()
        cls.agreement_terminate.with_user(cls.admin).action_approve_approval()

        # Pre-Condition 12-restart.md: Rejected.
        cls.agreement_restart = _create_agreement("Restart")
        cls.agreement_restart.with_user(cls.admin).action_confirm()
        cls.agreement_restart.with_user(cls.admin).action_reject_approval()

        cls.agreement_payment_term = _create_agreement("Payment Term")

    def test_create(self):
        """IK: docs/employee_external_assignment_agreement/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment_agreement/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment_agreement/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_delete",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/employee_external_assignment_agreement/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/employee_external_assignment_agreement/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/employee_external_assignment_agreement/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/employee_external_assignment_agreement/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_cancel",
            login="admin",
        )

    def test_terminate(self):
        """IK: docs/employee_external_assignment_agreement/11-terminate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_terminate",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/employee_external_assignment_agreement/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_restart",
            login="admin",
        )

    def test_view_payment_terms(self):
        """IK: docs/employee_external_assignment_agreement/14-view-payment-terms.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_view_payment_terms",
            login="admin",
        )
