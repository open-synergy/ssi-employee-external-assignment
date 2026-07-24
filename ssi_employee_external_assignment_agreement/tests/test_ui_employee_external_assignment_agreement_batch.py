# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreementBatch(HttpSavepointCase):
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
        cls.assignment_type = (
            cls.env["employee_external_assignment_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAB Type",
                    "code": "/",
                }
            )
        )
        # Partner used only by the 01-create tour itself (typed/picked live in
        # the browser, never searched for in a list). Named so it is NOT a
        # prefix of the per-scenario "TOUR EEAB Partner <Label>" partners
        # created below -- otherwise typing this name into the autocomplete
        # would also match those and make the dropdown pick ambiguous.
        cls.partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAB Create Partner",
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
                    "name": "TOUR EEAB Cancel Reason",
                    "code": "TEEABCR",
                    "global_use": True,
                }
            )
        )
        cls.terminate_reason = (
            cls.env["base.terminate_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAB Terminate Reason",
                    "code": "TEEABTR",
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
        # the row by that partner's name instead of the batch title.
        def _create_batch(label):
            partner = (
                cls.env["res.partner"]
                .with_user(cls.admin)
                .create(
                    {
                        "name": "TOUR EEAB Partner %s" % label,
                        "is_company": True,
                    }
                )
            )
            return (
                cls.env["employee_external_assignment_agreement_batch"]
                .with_user(cls.admin)
                .create(
                    {
                        "type_id": cls.assignment_type.id,
                        "title": "TOUR EEAB %s" % label,
                        "partner_id": partner.id,
                        "currency_id": cls.currency.id,
                        "pricelist_id": cls.pricelist.id,
                        "date_start": "2026-01-01",
                        "date_end": "2026-12-31",
                    }
                )
            )

        cls.batch_edit = _create_batch("Edit")
        cls.batch_delete = _create_batch("Delete")
        cls.batch_confirm = _create_batch("Confirm")

        # Pre-Condition 05-approve.md / 06-reject.md: Waiting for Approval.
        cls.batch_approve = _create_batch("Approve")
        cls.batch_approve.with_user(cls.admin).action_confirm()

        cls.batch_reject = _create_batch("Reject")
        cls.batch_reject.with_user(cls.admin).action_confirm()

        # Pre-Condition 10-cancel.md: Draft (one of the allowed states).
        cls.batch_cancel = _create_batch("Cancel")

        # Pre-Condition 11-terminate.md: On Progress. active_approver_user_ids
        # is computed from the approval.approval records action_confirm()
        # just created -- invalidate_cache so the very next call in the same
        # Python transaction sees them (same pattern used for the agreement
        # model's own UI test).
        cls.batch_terminate = _create_batch("Terminate")
        cls.batch_terminate.with_user(cls.admin).action_confirm()
        cls.batch_terminate.invalidate_cache()
        cls.batch_terminate.with_user(cls.admin).action_approve_approval()

        # Pre-Condition 12-restart.md: Rejected.
        cls.batch_restart = _create_batch("Restart")
        cls.batch_restart.with_user(cls.admin).action_confirm()
        cls.batch_restart.invalidate_cache()
        cls.batch_restart.with_user(cls.admin).action_reject_approval()

        cls.batch_view_agreements = _create_batch("View Agreements")

    def test_create(self):
        """IK: docs/employee_external_assignment_agreement_batch/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment_agreement_batch/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment_agreement_batch/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_delete",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/employee_external_assignment_agreement_batch/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/employee_external_assignment_agreement_batch/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/employee_external_assignment_agreement_batch/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/employee_external_assignment_agreement_batch/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_cancel",
            login="admin",
        )

    def test_terminate(self):
        """IK: docs/employee_external_assignment_agreement_batch/11-terminate.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_terminate",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/employee_external_assignment_agreement_batch/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_restart",
            login="admin",
        )

    def test_view_agreements(self):
        """IK: docs/employee_external_assignment_agreement_batch/14-view-agreements.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_batch_view_agreements",
            login="admin",
        )
