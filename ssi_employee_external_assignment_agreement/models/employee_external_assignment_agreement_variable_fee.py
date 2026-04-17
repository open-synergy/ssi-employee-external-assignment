# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EmployeeExternalAssignmentAgreementVariableFee(models.Model):
    _name = "employee_external_assignment_agreement.variable_fee"
    _inherit = [
        "mixin.product_line_account",
    ]
    _description = "Employee External Assignment Agreement - Variable Fee"
    _table = "eaa_agreement_variable_fee"

    agreement_id = fields.Many2one(
        string="# Agreement",
        comodel_name="employee_external_assignment_agreement",
        required=True,
        ondelete="cascade",
    )
    pricelist_id = fields.Many2one(
        related="agreement_id.pricelist_id",
        store=True,
        compute_sudo=True,
    )
    product_id = fields.Many2one(
        required=True,
    )
    tax_ids = fields.Many2many(
        relation="rel_eaa_agreement_variable_fee_2_tax",
        compute_sudo=True,
    )

    @api.onchange(
        "allowed_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        pass
