# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class HrPayslip(models.Model):
    _name = "hr.payslip_line"
    _inherit = [
        "hr.payslip_line",
    ]

    agreement_payment_term_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement.payment_term",
        string="Agreement Payment Term",
        help="Employee External Assignment Agreement Payment Term "
        "associated with this payslip.",
    )
    agreement_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement",
        related="agreement_payment_term_id.agreement_id",
        string="Agreement",
        store=True,
        readonly=True,
        help="Employee External Assignment Agreement associated with this payslip.",
    )
