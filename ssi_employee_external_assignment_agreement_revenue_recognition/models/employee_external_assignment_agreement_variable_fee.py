# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmployeeExternalAssignmentAgreementVariableFee(models.Model):
    _name = "employee_external_assignment_agreement.variable_fee"
    _inherit = [
        "employee_external_assignment_agreement.variable_fee",
    ]

    pob_id = fields.Many2one(
        string="# PoB",
        comodel_name="performance_obligation",
        compute="_compute_pob_id",
        store=False,
        compute_sudo=True,
        help=(
            "Performance Obligation linked to this variable fee line. "
            "Identified by matching the agreement's analytic account and this line's product."
        ),
    )

    @api.depends(
        "agreement_id.analytic_account_id",
        "product_id",
    )
    def _compute_pob_id(self):
        PoB = self.env["performance_obligation"]
        for record in self:
            result = False
            if record.agreement_id.analytic_account_id and record.product_id:
                pobs = PoB.search(
                    [
                        (
                            "source_analytic_account_id",
                            "=",
                            record.agreement_id.analytic_account_id.id,
                        ),
                        ("product_id", "=", record.product_id.id),
                    ]
                )
                if pobs:
                    result = pobs[0]
            record.pob_id = result

    def action_create_pob(self):
        for record in self.sudo():
            record._create_pob()

    def _create_pob(self):
        self.ensure_one()
        if self.pob_id:
            return True
        PoB = self.env["performance_obligation"]
        data = self._prepare_pob_data()
        PoB.create(data)

    def _prepare_pob_data(self):
        self.ensure_one()
        xmlid = (
            "ssi_revenue_recognition."
            "field_performance_obligation_acceptance__qty_manual_fulfillment"
        )
        manual_field = self.env.ref(xmlid, raise_if_not_found=False)
        if not manual_field:
            error_message = _(
                """
Context: Create Performance Obligation from agreement variable fee
Database ID: %s
Problem: Fulfillment field reference "%s" was not found
Solution: Make sure module ssi_revenue_recognition is installed and up to date
"""
                % (self.id, xmlid)
            )
            raise UserError(error_message)
        return {
            "source_analytic_account_id": self.agreement_id.analytic_account_id.id,
            "title": self.name,
            "date": self.agreement_id.date,
            "product_id": self.product_id.id,
            "currency_id": self.currency_id.id,
            "uom_quantity": self.uom_quantity,
            "uom_id": self.uom_id.id if self.uom_id else self.product_id.uom_id.id,
            "price_unit": self.price_unit,
            "progress_completion_method": "input",
            "revenue_recognition_timing": "point_in_time",
            "fulfillment_field_id": manual_field.id,
        }
