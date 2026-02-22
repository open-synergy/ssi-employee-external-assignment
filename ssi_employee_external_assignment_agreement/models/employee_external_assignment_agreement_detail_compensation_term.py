# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeExternalAssignmentAgreementDetailCompensationTerm(models.Model):
    _name = "employee_external_assignment_agreement.detail.compensation_term"
    _description = "Employee External Assignment Agreement - Detail - Compensation Term"
    _table = "eea_agreement_detail_compensation_term"

    detail_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement.detail",
        string="Agreement Detail",
        required=True,
        ondelete="cascade",
    )
    agreement_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement",
        string="Agreement",
        related="detail_id.agreement_id",
        store=True,
        compute_sudo=True,
    )
    currency_id = fields.Many2one(
        related="agreement_id.currency_id",
        store=True,
        compute_sudo=True,
    )
    rule_id = fields.Many2one(
        comodel_name="hr.salary_rule",
        string="Salary Rule",
        required=True,
    )
    fixed_amount = fields.Boolean(
        string="Fixed Amount",
        default=True,
        help="Indicates if the amount is fixed or based on a percentage.",
        required=True,
    )
    minimum_amount = fields.Monetary(
        string="Minimum Amount",
        default=0.0,
        help="Minimum amount for the compensation term.",
        required=True,
        currency_field="currency_id",
    )
    maximum_amount = fields.Monetary(
        string="Maximum Amount",
        default=0.0,
        help="Maximum amount for the compensation term.",
        required=True,
        currency_field="currency_id",
    )
