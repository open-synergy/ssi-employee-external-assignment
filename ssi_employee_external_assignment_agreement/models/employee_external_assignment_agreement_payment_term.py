# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignmentAgreementPaymentTerm(models.Model):
    _name = "employee_external_assignment_agreement.payment_term"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.transaction_date_duration",
    ]
    _description = "Employee External Assignment Agreement - Payment Term"

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    agreement_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement",
        string="# Agreement",
        required=True,
        ondelete="cascade",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Agreement Date",
        related="agreement_id.date",
        store=True,
        compute_sudo=True,
    )
    type_id = fields.Many2one(
        related="agreement_id.type_id",
        store=True,
        compute_sudo=True,
    )
    partner_id = fields.Many2one(
        related="agreement_id.partner_id",
        store=True,
        compute_sudo=True,
    )
    contact_partner_id = fields.Many2one(
        related="agreement_id.contact_partner_id",
        store=True,
        compute_sudo=True,
    )
    currency_id = fields.Many2one(
        related="agreement_id.currency_id",
        store=True,
        compute_sudo=True,
    )
    pricelist_id = fields.Many2one(
        related="agreement_id.pricelist_id",
        store=True,
        compute_sudo=True,
    )
    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Invoice",
        help="Linked invoice for this payment term.",
        readonly=True,
    )
    external_assignment_ids = fields.Many2many(
        comodel_name="employee_external_assignment",
        relation="rel_agreement_payment_term_2_external_assignment",
        column1="payment_term_id",
        column2="external_assignment_id",
        string="External Assignments",
        help="External assignments associated with this payment term.",
    )
    employee_ids = fields.Many2many(
        string="Employees",
        comodel_name="hr.employee",
        compute="_compute_employee_ids",
        store=False,
        compute_sudo=True,
        help="Employees associated with the external assignments in this payment term.",
    )
    payslip_ids = fields.One2many(
        comodel_name="hr.payslip",
        inverse_name="agreement_payment_term_id",
        string="Payslips",
        help="Payslips associated with this payment term.",
    )
    payslip_detail_ids = fields.One2many(
        comodel_name="hr.payslip_line",
        inverse_name="agreement_payment_term_id",
        string="Payslip Details",
        help="Payslip details associated with this payment term.",
    )
    rule_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.payment_term.rule",
        inverse_name="payment_term_id",
        string="Payment Term Rules",
        help="Payment term rules associated with this payment term.",
    )

    # Total
    amount_untaxed_rule = fields.Monetary(
        string="Untaxed Amount from Rules",
        currency_field="currency_id",
        compute="_compute_amount_total",
        store=True,
        compute_sudo=True,
    )
    amount_tax = fields.Monetary(
        string="Tax Amount",
        currency_field="currency_id",
        compute="_compute_amount_total",
        store=True,
        compute_sudo=True,
    )
    amount_total = fields.Monetary(
        string="Total Amount",
        currency_field="currency_id",
        compute="_compute_amount_total",
        store=True,
        compute_sudo=True,
    )

    # Invoice Link
    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Invoice",
        help="Linked invoice for this payment term.",
        readonly=True,
    )

    @api.depends(
        "rule_ids",
        "rule_ids.amount_subtotal",
        "rule_ids.amount_tax",
        "rule_ids.amount_total",
    )
    def _compute_amount_total(self):
        for record in self:
            rule_untaxed = sum(record.rule_ids.mapped("amount_subtotal"))
            rule_tax = sum(record.rule_ids.mapped("amount_tax"))
            record.amount_untaxed_rule = rule_untaxed
            record.amount_tax = rule_tax
            record.amount_total = rule_untaxed + rule_tax

    @api.depends("external_assignment_ids", "external_assignment_ids.employee_id")
    def _compute_employee_ids(self):
        for record in self:
            employee_ids = record.external_assignment_ids.mapped("employee_id").ids
            record.employee_ids = [(6, 0, employee_ids)]

    def action_reload_payslip(self):
        for record in self.sudo():
            record._reload_payslip()

    def action_load_payslip_line(self):
        for record in self.sudo():
            record._load_payslip_line()
            record._load_rules()

    def action_load_external_assignment(self):
        for record in self.sudo():
            record._load_external_assignment()

    def action_open_external_assignments(self):
        self.ensure_one()
        return {
            "name": "Employee External Assignments",
            "type": "ir.actions.act_window",
            "res_model": "employee_external_assignment",
            "view_mode": "tree,form",
            "domain": [
                (
                    "id",
                    "in",
                    self.external_assignment_ids.ids,  # pylint: disable=no-member
                )
            ],
        }

    def action_create_invoice(self):
        for record in self.sudo():
            record._create_invoice()

    def action_delete_invoice(self):
        for record in self.sudo():
            record._delete_invoice()

    def action_disconnect_invoice(self):
        for record in self.sudo():
            record._disconnect_invoice()

    def action_mark_as_manual(self):
        for record in self.sudo():
            record._mark_as_manual()

    def action_unmark_as_manual(self):
        for record in self.sudo():
            record._unmark_as_manual()

    def _mark_as_manual(self):
        self.ensure_one()
        self.write(
            {
                "manually_control": True,
            }
        )

    def _unmark_as_manual(self):
        self.ensure_one()
        self.write(
            {
                "manually_control": False,
            }
        )

    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.move"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        for rule in self.rule_ids:
            rule._create_invoice_line()  # pylint: disable=no-member
        for fee in self.agreement_id.other_fee_ids:
            self._create_fee_invoice_line(invoice, fee)
        for fee in self.agreement_id.variable_fee_ids:
            self._create_fee_invoice_line(invoice, fee)

    def _create_fee_invoice_line(self, invoice, fee):
        self.ensure_one()
        data = {
            "move_id": invoice.id,
            "product_id": fee.product_id.id,
            "quantity": getattr(fee, "uom_quantity", 1.0) or 1.0,
            "account_id": fee.product_id.property_account_income_id.id,
            "price_unit": fee.price_unit,
            "tax_ids": [(6, 0, fee.tax_ids.ids)],
            "name": fee.name or fee.product_id.name,
        }
        (
            self.env["account.move.line"]
            .with_context(check_move_validity=False)
            .create(data)
        )
        invoice.with_context(
            check_move_validity=False
        )._move_autocomplete_invoice_lines_values()

    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        # TODO: Hapus juga relasi di detail_ids jika ada  # pylint: disable=fixme
        self.rule_ids.write({"invoice_line_id": False})  # pylint: disable=no-member
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()

    def _disconnect_invoice(self):
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    def _prepare_invoice_data(self):
        self.ensure_one()
        agreement = self.agreement_id
        return {
            "date": date.today(),
            "ref": agreement.name,
            "move_type": "out_invoice",
            "journal_id": agreement.journal_id.id,
            "partner_id": agreement.partner_id.id,
            "currency_id": self.currency_id.id,
            "invoice_user_id": False,
            "invoice_date": date.today(),
            "invoice_date_due": date.today(),  # TODO  # pylint: disable=fixme
            "invoice_origin": agreement.name,
            "invoice_payment_term_id": False,  # TODO  # pylint: disable=fixme
            "payment_reference": agreement.title,
        }

    def _load_external_assignment(self):
        self.ensure_one()
        # Kosongkan dulu external_assignment_ids
        self.external_assignment_ids = [(5, 0, 0)]
        # Cari semua external agreement yang:
        # 1. Date Start dan Date End berada di antara date_start dan date_end dari agreement
        # 2. Partner sama dengan partner dari agreement
        ExternalAssignment = self.env[  # pylint: disable=invalid-name
            "employee_external_assignment"
        ]
        agreement = self.agreement_id
        external_assignment_domain = [
            ("date_start", ">=", agreement.date_start),
            ("date_end", "<=", agreement.date_end),
            ("partner_id", "=", agreement.partner_id.id),
        ]
        external_assignments = ExternalAssignment.search(external_assignment_domain)
        self.external_assignment_ids = [(6, 0, external_assignments.ids)]

    def _load_payslip_line(self):
        self.ensure_one()
        agreement = self.agreement_id
        # Kosongkan dulu payslip_detail_ids
        self.payslip_detail_ids = [(5, 0, 0)]
        # Cari semua payslip line yang terkait dengan payslip yang ada di payslip_ids
        PayslipLine = self.env["hr.payslip_line"]  # pylint: disable=invalid-name
        # Loop compensation term pada detail agreement
        for detail in agreement.detail_ids:
            for compensation in detail.compensation_term_ids:
                # Susun domain untuk mencari payslip line
                payslip_line_domain = [
                    ("payslip_id", "in", self.payslip_ids.ids),
                    ("rule_id", "=", compensation.rule_id.id),
                ]
                payslip_lines = PayslipLine.search(payslip_line_domain)
                self.payslip_detail_ids = [(4, pid) for pid in payslip_lines.ids]

    def _load_rules(self):
        self.ensure_one()
        # Kosongkan dulu rule_ids
        self.rule_ids = [(5, 0, 0)]
        # Loop compensation term pada detail agreement
        agreement = self.agreement_id
        for detail in agreement.all_salary_rule_ids:
            rule_vals = {
                "payment_term_id": self.id,
                "rule_id": detail.id,
                "product_id": detail.external_assignment_agreement_product_id.id,
                "tax_ids": [(6, 0, detail.external_assignment_agreement_tax_ids.ids)],
            }
            self.env["employee_external_assignment_agreement.payment_term.rule"].create(
                rule_vals
            )

    def _reload_payslip(self):
        self.payslip_ids.write({"agreement_payment_term_id": False})
        payslip_domain = [
            ("agreement_payment_term_id", "=", False),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("employee_id", "in", self.employee_ids.ids),
            ("state", "=", "done"),
        ]
        payslips = self.env["hr.payslip"].search(payslip_domain)
        payslips.write({"agreement_payment_term_id": self.id})

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res
