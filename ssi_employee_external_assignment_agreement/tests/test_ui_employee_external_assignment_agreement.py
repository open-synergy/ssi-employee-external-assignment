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

        # Pre-Condition 11-terminate.md: On Progress. active_approver_user_ids
        # is computed from the approval.approval records action_confirm()
        # just created -- invalidate_cache so the very next call in the same
        # Python transaction sees them (same pattern as the "Invalidate cache
        # after confirm" step in test_data_employee_external_assignment_agreement.yaml).
        cls.agreement_terminate = _create_agreement("Terminate")
        cls.agreement_terminate.with_user(cls.admin).action_confirm()
        cls.agreement_terminate.invalidate_cache()
        cls.agreement_terminate.with_user(cls.admin).action_approve_approval()

        # Pre-Condition 12-restart.md: Rejected.
        cls.agreement_restart = _create_agreement("Restart")
        cls.agreement_restart.with_user(cls.admin).action_confirm()
        cls.agreement_restart.invalidate_cache()
        cls.agreement_restart.with_user(cls.admin).action_reject_approval()

        # Pre-Condition 13-reset-number.md: Draft, not linked to a batch
        # (manual_number_ok's additional_python_code requires
        # "not document.batch_id" -- see
        # policy_template/employee_external_assignment_agreement.xml), with
        # a manually-set document number (the "name" field is editable in
        # Draft status) so the reset is observable: name_get() renders "/"
        # as "*<id>" (see mixin_transaction.py), which only differs from
        # the manually-set number below.
        cls.agreement_reset_number = _create_agreement("Reset Number")
        cls.agreement_reset_number.with_user(cls.admin).write(
            {"name": "TOUR-EEAA-MANUAL-001"}
        )

        cls.agreement_payment_term = _create_agreement("Payment Term")

        # Pre-Condition 15-create-assignment.md: Open, with a job position
        # in Details and a matching employee eligible for the wizard.
        cls.job_create_assignment = (
            cls.env["hr.job"]
            .with_user(cls.admin)
            .create({"name": "TOUR EEAA Job Create Assignment"})
        )
        cls.employee_create_assignment = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Employee Create Assignment",
                    "job_id": cls.job_create_assignment.id,
                }
            )
        )
        cls.agreement_create_assignment = _create_agreement("Create Assignment")
        cls.agreement_create_assignment.with_user(cls.admin).write(
            {
                "detail_ids": [
                    (0, 0, {"job_id": cls.job_create_assignment.id}),
                ],
            }
        )
        cls.agreement_create_assignment.with_user(cls.admin).action_confirm()
        cls.agreement_create_assignment.invalidate_cache()
        cls.agreement_create_assignment.with_user(cls.admin).action_approve_approval()

        # Pre-Condition 16-create-from-batch.md: at least one batch record
        # exists. The batch's "name" (document number) is overridden from the
        # default "/" so the m2o dropdown can be searched by a stable, unique
        # string -- see mixin.transaction.name_get(), which otherwise renders
        # every Draft batch as "*<id>".
        cls.batch_partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Batch Partner",
                    "is_company": True,
                }
            )
        )
        cls.batch_create_from_batch = (
            cls.env["employee_external_assignment_agreement_batch"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAA Batch Create From Batch",
                    "type_id": cls.assignment_type.id,
                    "title": "TOUR EEAA Batch Create From Batch",
                    "partner_id": cls.batch_partner.id,
                    "currency_id": cls.currency.id,
                    "pricelist_id": cls.pricelist.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )

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

    def test_reset_number(self):
        """IK: docs/employee_external_assignment_agreement/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_reset_number",
            login="admin",
        )

    def test_view_payment_terms(self):
        """IK: docs/employee_external_assignment_agreement/14-view-payment-terms.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_view_payment_terms",
            login="admin",
        )

    def test_create_assignment(self):
        """IK: docs/employee_external_assignment_agreement/15-create-assignment.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_create_assignment",
            login="admin",
        )

    def test_create_from_batch(self):
        """IK: docs/employee_external_assignment_agreement/16-create-from-batch.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_create_from_batch",
            login="admin",
        )
