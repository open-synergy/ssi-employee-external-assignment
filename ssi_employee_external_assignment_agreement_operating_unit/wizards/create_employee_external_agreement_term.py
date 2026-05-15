# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CreateEmployeeExternalAgreementTerm(models.TransientModel):
    _name = "create_employee_external_agreement_term"
    _inherit = "create_employee_external_agreement_term"

    def _prepare_payment_term_vals(self, date_start, date_end):
        result = super()._prepare_payment_term_vals(date_start, date_end)
        operating_unit_id = getattr(self.agreement_id, "operating_unit_id", False)
        if operating_unit_id:
            result["operating_unit_id"] = operating_unit_id.id
        return result
