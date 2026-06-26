# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PerformanceObligationAcceptance(models.Model):
    _name = "performance_obligation_acceptance"
    _inherit = [
        "performance_obligation_acceptance",
    ]

    payslip_line_ids = fields.Many2many(
        string="Payslip Lines",
        comodel_name="hr.payslip_line",
        relation="pob_acceptance_payslip_line_rel",
        column1="acceptance_id",
        column2="payslip_line_id",
        help=(
            "Payslip lines that contribute to fulfillment of this acceptance period. "
            "Linked manually in Phase 1, populated automatically in Phase 2 by the "
            "payment term post-done action. The sum of their totals becomes the "
            "recognized revenue amount for the period."
        ),
    )
    qty_payslip_fulfillment = fields.Float(
        string="Payslip Fulfillment Amount",
        compute="_compute_qty_payslip_fulfillment",
        store=True,
        digits="Account",
        help=(
            "Sum of total amounts from all linked payslip lines. "
            "Used as fulfillment_field_id for labor-type Performance Obligations, "
            "implementing the as-invoiced practical expedient (PSAK 115 para B16)."
        ),
    )

    @api.depends("payslip_line_ids.total")
    def _compute_qty_payslip_fulfillment(self):
        for rec in self:
            rec.qty_payslip_fulfillment = sum(rec.payslip_line_ids.mapped("total"))
