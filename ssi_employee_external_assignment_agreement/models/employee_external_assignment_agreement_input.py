# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=R0903

from odoo import api, fields, models


class EmployeeExternalAssignmentAgreementInput(models.Model):
    _name = "employee_external_assignment_agreement_input"
    _description = "Employee External Assignment Agreement Input"

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="employee_external_assignment_agreement",
        required=True,
        ondelete="cascade",
    )
    input_type_id = fields.Many2one(
        string="Input Type",
        comodel_name="employee_external_assignment_agreement_input_type",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        default=0.0,
        help="Amount for this input. Auto-filled from input type's default amount.",
    )

    @api.onchange(
        "input_type_id",
    )
    def onchange_amount(self):
        self.amount = 0.0
        if self.input_type_id:
            self.amount = self.input_type_id.default_amount
