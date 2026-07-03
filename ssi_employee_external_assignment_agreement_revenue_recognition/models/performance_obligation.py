# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PerformanceObligation(models.Model):
    _name = "performance_obligation"
    _inherit = [
        "performance_obligation",
    ]

    agreement_detail_id = fields.Many2one(
        string="Agreement Detail",
        comodel_name="employee_external_assignment_agreement.detail",
        ondelete="set null",
        help=(
            "Agreement detail (job position) that originated this Performance Obligation. "
            "Set automatically when creating a PoB from an agreement detail line. "
            "Used to uniquely identify the PoB per detail within the same analytic account."
        ),
    )
