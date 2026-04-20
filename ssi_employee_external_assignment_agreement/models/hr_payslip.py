# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=R0903


from odoo import fields, models

from odoo.addons.ssi_hr_payroll.models.hr_payslip import BrowsableObject


class ExternalAgreementInputLine(BrowsableObject):
    def sum(self, code):
        self.env.cr.execute(
            """
            SELECT sum(b.amount) as sum
            FROM employee_external_assignment_agreement as a
            JOIN employee_external_assignment_agreement_input as b
                ON a.id = b.agreement_id
            JOIN employee_external_assignment_agreement_input_type as c
                ON b.input_type_id = c.id
            WHERE a.id = %s AND c.code = %s""",
            (self.employee_id, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class HrPayslip(models.Model):
    _name = "hr.payslip"
    _inherit = [
        "hr.payslip",
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
        help="Employee External Assignment Agreement associated " "with this payslip.",
    )

    def _get_base_localdict(self, payslip):
        res = super()._get_base_localdict(payslip)
        external_aggr_inputs_dict = {}

        for external_aggr_input_line in payslip.agreement_id.input_line_ids:
            external_aggr_inputs_dict[
                external_aggr_input_line.input_type_id.code
            ] = external_aggr_input_line

        external_aggr_inputs = ExternalAgreementInputLine(
            payslip.agreement_id.id, external_aggr_inputs_dict, self.env
        )
        if external_aggr_inputs:
            res["external_aggr_inputs"] = external_aggr_inputs
        return res
