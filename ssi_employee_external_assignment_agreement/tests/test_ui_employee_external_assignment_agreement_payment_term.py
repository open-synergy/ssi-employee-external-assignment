# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreementPaymentTerm(HttpSavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition IK disiapkan di sini -- BUKAN lewat klik UI.
        cls.currency = cls.env.ref("base.EUR")
        cls.pricelist = cls.env.ref("product.list0")
        cls.expense_account_type = cls.env.ref("account.data_account_type_expenses")

        cls.journal = (
            cls.env["account.journal"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Journal",
                    "code": "TEEAPTJ",
                    "type": "general",
                }
            )
        )
        cls.receivable_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Receivable",
                    "code": "TEEAPT01",
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
                    "name": "TOUR EEAAPT Type",
                    "code": "TEEAPTAT",
                }
            )
        )
        # Global cancel reason so it is selectable regardless of whether
        # ssi_transaction_cancel_mixin demo data is loaded.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Cancel Reason",
                    "code": "TEEAPTCR",
                    "global_use": True,
                }
            )
        )

        # Only ONE Agreement exists for the whole class. Its own
        # mixin.transaction "name" stays "/" while in Draft, so
        # mixin.transaction.name_get() falls back to a per-record "*<id>"
        # placeholder (see mixin_transaction.py) -- meaning the "Agreement"
        # many2one on the Payment Term create form cannot be searched by
        # typed text (name_search filters on the real "name" field, which is
        # "/" for every draft agreement). With exactly one Agreement in
        # existence, clicking the (empty) field still reliably shows exactly
        # one match in the dropdown -- see 01-create.md / the create tour.
        cls.partner = (
            cls.env["res.partner"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Partner",
                    "is_company": True,
                }
            )
        )
        cls.agreement = (
            cls.env["employee_external_assignment_agreement"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": cls.assignment_type.id,
                    "title": "TOUR EEAAPT Agreement",
                    "partner_id": cls.partner.id,
                    "receivable_account_id": cls.receivable_account.id,
                    "journal_id": cls.journal.id,
                    "currency_id": cls.currency.id,
                    "pricelist_id": cls.pricelist.id,
                    "date_start": "2026-01-01",
                    "date_end": "2026-12-31",
                }
            )
        )

        # NOTE on how tour steps find "the record to <action>" in the
        # Payment Terms list: every scenario's Payment Term shares the SAME
        # Agreement/Partner above (the list shows "Agreement", "Partner" --
        # both identical across rows), so each scenario below is given its
        # own, non-overlapping Date Start/Date End instead, and the tour
        # looks up the row by that unique date.
        def _create_payment_term(label, date_start, date_end):
            return (
                cls.env["employee_external_assignment_agreement.payment_term"]
                .with_user(cls.admin)
                .create(
                    {
                        "agreement_id": cls.agreement.id,
                        "date_start": date_start,
                        "date_end": date_end,
                    }
                )
            )

        cls.payment_term_edit = _create_payment_term("Edit", "2026-01-01", "2026-01-31")
        cls.payment_term_delete = _create_payment_term(
            "Delete", "2026-02-01", "2026-02-28"
        )
        cls.payment_term_confirm = _create_payment_term(
            "Confirm", "2026-03-01", "2026-03-31"
        )

        # Pre-Condition 05-approve.md / 06-reject.md: Waiting for Approval.
        cls.payment_term_approve = _create_payment_term(
            "Approve", "2026-04-01", "2026-04-30"
        )
        cls.payment_term_approve.with_user(cls.admin).action_confirm()

        cls.payment_term_reject = _create_payment_term(
            "Reject", "2026-05-01", "2026-05-31"
        )
        cls.payment_term_reject.with_user(cls.admin).action_confirm()

        # Pre-Condition 10-cancel.md: Draft (one of the allowed states).
        cls.payment_term_cancel = _create_payment_term(
            "Cancel", "2026-06-01", "2026-06-30"
        )

        # Pre-Condition 12-restart.md: Rejected. active_approver_user_ids is
        # computed from the approval.approval records action_confirm() just
        # created -- invalidate_cache so the very next call in the same
        # Python transaction sees them (same pattern used by the parent
        # employee_external_assignment_agreement UI test).
        cls.payment_term_restart = _create_payment_term(
            "Restart", "2026-08-01", "2026-08-31"
        )
        cls.payment_term_restart.with_user(cls.admin).action_confirm()
        cls.payment_term_restart.invalidate_cache()
        cls.payment_term_restart.with_user(cls.admin).action_reject_approval()

        # Pre-Condition 13-reset-number.md: Draft, with a manually-set
        # document number (the "name" field is editable in Draft status) so
        # the reset is observable: name_get() renders "/" as "*<id>" (see
        # mixin_transaction.py), which only differs from the manually-set
        # number below.
        cls.payment_term_reset_number = _create_payment_term(
            "Reset Number", "2026-07-01", "2026-07-31"
        )
        cls.payment_term_reset_number.with_user(cls.admin).write(
            {"name": "TOUR-EEAAPT-MANUAL-001"}
        )

        # --- Payroll fixtures shared by the "load"/"reload" scenarios ---
        cls.debit_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Debit Account",
                    "code": "TEEAPT02",
                    "user_type_id": cls.expense_account_type.id,
                }
            )
        )
        cls.credit_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Credit Account",
                    "code": "TEEAPT03",
                    "user_type_id": cls.expense_account_type.id,
                }
            )
        )
        cls.income_account = (
            cls.env["account.account"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Income Account",
                    "code": "TEEAPT04",
                    "user_type_id": cls.expense_account_type.id,
                }
            )
        )
        cls.rule_category = (
            cls.env["hr.salary_rule_category"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Rule Category",
                    "code": "TEEAPTRC",
                }
            )
        )
        cls.product_tmpl = (
            cls.env["product.template"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Rule Product",
                    "type": "service",
                    "property_account_income_id": cls.income_account.id,
                }
            )
        )
        cls.product = cls.env["product.product"].search(
            [("product_tmpl_id", "=", cls.product_tmpl.id)], limit=1
        )
        cls.salary_rule = (
            cls.env["hr.salary_rule"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Salary Rule",
                    "code": "TEEAPTSR",
                    "category_id": cls.rule_category.id,
                    "sequence": 10,
                    "condition_python": "result = True",
                    "amount_python": "result = 100.0",
                    "debit_account_id": cls.debit_account.id,
                    "credit_account_id": cls.credit_account.id,
                    "external_assignment_agreement_product_id": cls.product.id,
                }
            )
        )
        cls.structure = (
            cls.env["hr.salary_structure"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Structure",
                    "code": "TEEAPTST",
                    "rule_ids": [(6, 0, [cls.salary_rule.id])],
                }
            )
        )
        cls.payslip_type = (
            cls.env["hr.payslip_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Payslip Type",
                    "code": "TEEAPTPT",
                    "journal_id": cls.journal.id,
                }
            )
        )
        cls.employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR EEAAPT Employee",
                    "salary_structure_id": cls.structure.id,
                }
            )
        )
        # Falls inside the shared Agreement's 2026-01-01 / 2026-12-31 range,
        # which is what action_load_external_assignment() filters against
        # (NOT the Payment Term's own date_start/date_end).
        cls.assignment = (
            cls.env["employee_external_assignment"]
            .with_user(cls.admin)
            .create(
                {
                    "type_id": cls.assignment_type.id,
                    "partner_id": cls.partner.id,
                    "employee_id": cls.employee.id,
                    "date_start": "2026-01-15",
                    "date_end": "2026-01-20",
                }
            )
        )

        # Pre-Condition 14-load-external-assignment.md: Draft, no External
        # Assignment linked yet -- the tour itself loads cls.assignment.
        cls.payment_term_load_assignment = _create_payment_term(
            "Load Assignment", "2026-09-01", "2026-09-30"
        )

        # Pre-Condition 15-view-external-assignments.md: External
        # Assignment already linked directly (Pre-Condition setup, not via
        # the Flow being tested).
        cls.payment_term_view_assignment = _create_payment_term(
            "View Assignment", "2026-10-01", "2026-10-31"
        )
        cls.payment_term_view_assignment.write(
            {"external_assignment_ids": [(6, 0, [cls.assignment.id])]}
        )

        # Pre-Condition 16-reload-payslip.md: External Assignment already
        # linked (so employee_ids includes cls.employee), and a Payslip in
        # Done status for that employee, dated inside the Payment Term's own
        # date_start/date_end, NOT YET linked to this Payment Term -- the
        # tour's Reload click is what links it.
        cls.payment_term_reload_payslip = _create_payment_term(
            "Reload Payslip", "2026-11-01", "2026-11-30"
        )
        cls.payment_term_reload_payslip.write(
            {"external_assignment_ids": [(6, 0, [cls.assignment.id])]}
        )
        cls.payslip_reload = (
            cls.env["hr.payslip"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": cls.employee.id,
                    "type_id": cls.payslip_type.id,
                    "structure_id": cls.structure.id,
                    "journal_id": cls.journal.id,
                    "date": "2026-11-15",
                    "date_start": "2026-11-01",
                    "date_end": "2026-11-30",
                }
            )
        )
        # Line created directly (bypassing the payroll computation engine --
        # out of scope here, this is UI/UX coverage only) so the Payslip can
        # reach Done: action_done() posts an accounting move from line_ids,
        # which requires at least one line with a non-zero amount.
        cls.env["hr.payslip_line"].with_user(cls.admin).create(
            {
                "payslip_id": cls.payslip_reload.id,
                "rule_id": cls.salary_rule.id,
                "rate": 100.0,
                "amount": 100.0,
                "quantity": 1.0,
            }
        )
        cls.payslip_reload.with_user(cls.admin).action_confirm()
        cls.payslip_reload.invalidate_cache()
        cls.payslip_reload.with_user(cls.admin).action_approve_approval()
        cls.payslip_reload.invalidate_cache()

        # Pre-Condition 17-load-payslip-line.md: a Job Position + a
        # Compensation Term on the Agreement referencing cls.salary_rule, and
        # a Payslip already linked to this Payment Term (agreement_payment_
        # term_id) with a Payslip Line for that same rule. The Payslip's own
        # status does not matter for this action -- it stays Draft.
        cls.job = (
            cls.env["hr.job"].with_user(cls.admin).create({"name": "TOUR EEAAPT Job"})
        )
        cls.detail = (
            cls.env["employee_external_assignment_agreement.detail"]
            .with_user(cls.admin)
            .create(
                {
                    "agreement_id": cls.agreement.id,
                    "job_id": cls.job.id,
                }
            )
        )
        cls.compensation_term = (
            cls.env["employee_external_assignment_agreement.detail.compensation_term"]
            .with_user(cls.admin)
            .create(
                {
                    "detail_id": cls.detail.id,
                    "rule_id": cls.salary_rule.id,
                }
            )
        )
        cls.payment_term_load_payslip_line = _create_payment_term(
            "Load Payslip Line", "2026-12-01", "2026-12-31"
        )
        cls.payment_term_load_payslip_line.write(
            {"external_assignment_ids": [(6, 0, [cls.assignment.id])]}
        )
        cls.payslip_line_source = (
            cls.env["hr.payslip"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": cls.employee.id,
                    "type_id": cls.payslip_type.id,
                    "structure_id": cls.structure.id,
                    "journal_id": cls.journal.id,
                    "date": "2026-12-15",
                    "date_start": "2026-12-01",
                    "date_end": "2026-12-31",
                    "agreement_payment_term_id": cls.payment_term_load_payslip_line.id,
                }
            )
        )
        cls.env["hr.payslip_line"].with_user(cls.admin).create(
            {
                "payslip_id": cls.payslip_line_source.id,
                "rule_id": cls.salary_rule.id,
                "rate": 100.0,
                "amount": 100.0,
                "quantity": 1.0,
            }
        )

        # Pre-Condition 18-create-invoice.md: no Invoice linked yet.
        cls.payment_term_create_invoice = _create_payment_term(
            "Create Invoice", "2027-01-01", "2027-01-31"
        )

        # Pre-Condition 19-delete-invoice.md: Invoice already linked
        # (Pre-Condition setup, not via the Flow being tested).
        cls.payment_term_delete_invoice = _create_payment_term(
            "Delete Invoice", "2027-02-01", "2027-02-28"
        )
        cls.payment_term_delete_invoice.with_user(cls.admin).action_create_invoice()

    def test_create(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/01-create.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_create",
            login="admin",
        )

    def test_edit(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/02-edit.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_edit",
            login="admin",
        )

    def test_delete(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/03-delete.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_delete",
            login="admin",
        )

    def test_confirm(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/04-confirm.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_confirm",
            login="admin",
        )

    def test_approve(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/05-approve.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_approve",
            login="admin",
        )

    def test_reject(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/06-reject.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_reject",
            login="admin",
        )

    def test_cancel(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/10-cancel.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_cancel",
            login="admin",
        )

    def test_restart(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/12-restart.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_restart",
            login="admin",
        )

    def test_reset_number(self):
        """IK: docs/.../payment_term/13-reset-number.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_reset_number",
            login="admin",
        )

    def test_load_external_assignment(self):
        """IK: docs/.../payment_term/14-load-external-assignment.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_load_external_assignment",
            login="admin",
        )

    def test_view_external_assignments(self):
        """IK: docs/.../payment_term/15-view-external-assignments.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_view_external_assignments",
            login="admin",
        )

    def test_reload_payslip(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/16-reload-payslip.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_reload_payslip",
            login="admin",
        )

    def test_load_payslip_line(self):
        """IK: docs/.../payment_term/17-load-payslip-line.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_load_payslip_line",
            login="admin",
        )

    def test_create_invoice(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/18-create-invoice.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_create_invoice",
            login="admin",
        )

    def test_delete_invoice(self):
        """IK: docs/employee_external_assignment_agreement_payment_term/19-delete-invoice.md"""
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_payment_term_delete_invoice",
            login="admin",
        )
