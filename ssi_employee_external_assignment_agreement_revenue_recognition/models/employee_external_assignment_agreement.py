# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class EmployeeExternalAssignmentAgreement(models.Model):
    _name = "employee_external_assignment_agreement"
    _inherit = [
        "employee_external_assignment_agreement",
    ]

    pob_ids = fields.Many2many(
        string="Performance Obligations",
        comodel_name="performance_obligation",
        compute="_compute_pob_ids",
        help=(
            "All Performance Obligations linked to this agreement via its analytic account. "
            "Refreshed whenever the analytic account changes."
        ),
    )
    amount_total_pob = fields.Monetary(
        string="Total Performance Obligation",
        currency_field="currency_id",
        related="analytic_account_id.amount_total_pob",
        store=True,
        help=(
            "Sum of all PoB amounts linked to this agreement's analytic account. "
            "Sourced from the analytic account's computed total."
        ),
    )

    @api.depends("analytic_account_id")
    def _compute_pob_ids(self):
        PoB = self.env["performance_obligation"]
        for record in self:
            if record.analytic_account_id:
                record.pob_ids = PoB.search(
                    [
                        (
                            "source_analytic_account_id",
                            "=",
                            record.analytic_account_id.id,
                        )
                    ]
                )
            else:
                record.pob_ids = PoB

    def action_open_pob(self):
        self.ensure_one()
        result = {
            "name": "Performance Obligations",
            "type": "ir.actions.act_window",
            "res_model": "performance_obligation",
            "view_mode": "tree,form",
            "domain": [
                (
                    "source_analytic_account_id",
                    "=",
                    self.analytic_account_id.id,
                )
            ],
        }
        return result

    @ssi_decorator.post_open_action()
    def _20_assign_source_analytic_to_pob(self):
        """Backfill source_analytic_account_id on PoB created before AA existed."""
        self.ensure_one()
        if self.analytic_account_id:
            self.pob_ids.filtered(lambda p: not p.source_analytic_account_id).write(
                {"source_analytic_account_id": self.analytic_account_id.id}
            )
