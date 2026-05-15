# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=R0903

from odoo import fields, models


class EmployeeExternalAssignmentAgreementInputType(models.Model):
    _name = "employee_external_assignment_agreement_input_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Employee External Assignment Agreement Input Type"

    default_amount = fields.Float(
        string="Default Amount",
        required=False,
        default=0.0,
        help="Default amount to be set when this input type is selected.",
    )
