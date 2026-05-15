# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EmployeeExternalAssignmentAgreementPaymentTerm(models.Model):
    _name = "employee_external_assignment_agreement.payment_term"
    _inherit = [
        "employee_external_assignment_agreement.payment_term",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_id",
        store=True,
        readonly=False,
        help="Operating unit for this payment term. Defaults from the agreement.",
    )

    @api.depends("agreement_id", "agreement_id.operating_unit_id")
    def _compute_operating_unit_id(self):
        for record in self:
            if record.agreement_id and record.agreement_id.operating_unit_id:
                record.operating_unit_id = record.agreement_id.operating_unit_id
            else:
                record.operating_unit_id = record.operating_unit_id

    def _prepare_invoice_data(self):
        result = super()._prepare_invoice_data()
        if self.operating_unit_id:
            result["operating_unit_id"] = self.operating_unit_id.id
        return result
