# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EmployeeExternalAssignmentAgreementPaymentTerm(
    models.Model
):  # pylint: disable=too-few-public-methods
    _name = "employee_external_assignment_agreement.payment_term"
    _inherit = [
        "employee_external_assignment_agreement.payment_term",
        "mixin.single_operating_unit",
    ]
