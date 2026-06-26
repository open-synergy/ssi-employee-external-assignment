# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmployeeExternalAssignmentAgreementDetail(models.Model):
    _name = "employee_external_assignment_agreement.detail"
    _inherit = [
        "employee_external_assignment_agreement.detail",
    ]

    pob_id = fields.Many2one(
        string="# PoB",
        comodel_name="performance_obligation",
        compute="_compute_pob_id",
        store=False,
        compute_sudo=True,
        help=(
            "Performance Obligation linked to this job position detail. "
            "Identified by matching the agreement's analytic account and this detail record."
        ),
    )

    @api.depends(
        "agreement_id.analytic_account_id",
    )
    def _compute_pob_id(self):
        PoB = self.env["performance_obligation"]
        for record in self:
            result = False
            if record.agreement_id.analytic_account_id and record.id:
                pobs = PoB.search(
                    [
                        (
                            "source_analytic_account_id",
                            "=",
                            record.agreement_id.analytic_account_id.id,
                        ),
                        ("agreement_detail_id", "=", record.id),
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
            "ssi_employee_external_assignment_agreement_revenue_recognition."
            "field_performance_obligation_acceptance__qty_payslip_fulfillment"
        )
        fulfillment_field = self.env.ref(xmlid, raise_if_not_found=False)
        if not fulfillment_field:
            error_message = _(
                """
Context: Create Performance Obligation from agreement detail
Database ID: %s
Problem: Fulfillment field reference "%s" was not found
Solution: Make sure module
ssi_employee_external_assignment_agreement_revenue_recognition
is installed and up to date
"""
                % (self.id, xmlid)
            )
            raise UserError(error_message)
        pob_product = self.agreement_id.type_id.pob_product_id
        if not pob_product:
            error_message = _(
                """
Context: Create Performance Obligation from agreement detail
Database ID: %s
Problem: PoB Product is not configured on the agreement type
Solution: Set the PoB Product field on the agreement type configuration
"""
                % self.id
            )
            raise UserError(error_message)
        return {
            "source_analytic_account_id": self.agreement_id.analytic_account_id.id,
            "title": self.job_id.name,
            "date": self.agreement_id.date,
            "product_id": pob_product.id,
            "currency_id": self.agreement_id.currency_id.id,
            "uom_quantity": 0.0,
            "uom_id": pob_product.uom_id.id,
            "price_unit": 1.0,
            "progress_completion_method": "input",
            "revenue_recognition_timing": "over_time",
            "fulfillment_field_id": fulfillment_field.id,
            "agreement_detail_id": self.id,
        }
