# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EmployeeExternalAssignmentAgreementPaymentTermRule(models.Model):
    _name = "employee_external_assignment_agreement.payment_term.rule"
    _description = "Employee External Assignment Agreement - Detail - Rule"
    _table = "eea_agreement_payment_term_rule"

    payment_term_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement.payment_term",
        string="Agreement Payment Term",
        required=True,
        ondelete="cascade",
    )
    rule_id = fields.Many2one(
        comodel_name="hr.salary_rule",
        string="Salary Rule",
        required=True,
    )
    payslip_line_ids = fields.Many2many(
        comodel_name="hr.payslip_line",
        compute="_compute_payslip_line_ids",
        string="Payslip Lines",
        compute_sudo=True,
        store=True,
        relation="rel_eea_payment_term_rule_2_payslip_line",
        column1="payment_term_rule_id",
        column2="payslip_line_id",
    )
    currency_id = fields.Many2one(
        related="payment_term_id.currency_id",
        store=True,
        compute_sudo=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
    )
    tax_ids = fields.Many2many(
        comodel_name="account.tax",
        string="Taxes",
        relation="rel_eea_payment_term_rule_2_account_tax",
        column1="payment_term_rule_id",
        column2="tax_id",
    )
    amount_subtotal = fields.Monetary(
        string="Subtotal Amount",
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
    invoice_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Invoice Line",
        readonly=True,
        ondelete="restrict",
    )

    @api.depends(
        "payment_term_id",
        "rule_id",
    )
    def _compute_payslip_line_ids(self):
        for record in self:
            line_domain = [
                ("id", "in", record.payment_term_id.payslip_detail_ids.ids),
                ("rule_id", "=", record.rule_id.id),
            ]
            payslip_line_ids = self.env["hr.payslip_line"].search(line_domain)
            record.payslip_line_ids = payslip_line_ids

    @api.depends(
        "payslip_line_ids",
        "payslip_line_ids.total",
        "product_id",
        "tax_ids",
    )
    def _compute_amount_total(self):
        for record in self:
            subtotal = tax = total = 0.0
            subtotal = total = sum(record.payslip_line_ids.mapped("total"))
            if record.tax_ids:
                taxes = record.tax_ids.compute_all(
                    subtotal,
                    record.currency_id,
                    1.0,
                    product=record.product_id,
                    partner=False,
                )
                tax = sum(t.get("amount", 0.0) for t in taxes.get("taxes", []))
                total = taxes["total_included"]
                subtotal = taxes["total_excluded"]
            record.amount_subtotal = subtotal
            record.amount_tax = tax
            record.amount_total = total

    def _get_invoice_line_account(self):
        self.ensure_one()
        account = False
        agreement = self.payment_term_id.agreement_id
        if agreement.usage_id and self.product_id:
            account = self.product_id._get_product_account(
                usage_code=agreement.usage_id.code
            )
        if not account:
            account = self.product_id.property_account_income_id
        return account

    def _get_invoice_line_analytic_account(self):
        self.ensure_one()
        return self.payment_term_id.agreement_id.analytic_account_id

    def _create_invoice_line(self):
        self.ensure_one()
        invoice = self.payment_term_id.invoice_id
        data = {
            "move_id": invoice.id,
            "product_id": self.product_id.id,
            "quantity": 1.0,
            "account_id": self._get_invoice_line_account().id,
            "analytic_account_id": self._get_invoice_line_analytic_account().id,
            "price_unit": self.amount_total,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "name": f"{self.rule_id.name} - {self.payment_term_id.name}",
        }
        invoice_line = (
            self.env["account.move.line"]
            .with_context(check_move_validity=False)
            .create(data)
        )
        invoice.with_context(
            check_move_validity=False
        )._move_autocomplete_invoice_lines_values()
        self.write(
            {
                "invoice_line_id": invoice_line.id,
            }
        )
