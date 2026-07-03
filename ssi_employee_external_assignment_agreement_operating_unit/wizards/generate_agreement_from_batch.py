# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GenerateAgreementFromBatch(models.TransientModel):
    _name = "generate_agreement_from_batch"
    _inherit = "generate_agreement_from_batch"

    def _prepare_agreement_vals(self, line):
        result = super()._prepare_agreement_vals(line)
        operating_unit_id = getattr(self.batch_id, "operating_unit_id", False)
        if operating_unit_id:
            result["operating_unit_id"] = operating_unit_id.id
        return result
