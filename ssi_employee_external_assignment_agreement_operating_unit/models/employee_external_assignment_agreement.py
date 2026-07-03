# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmployeeExternalAssignmentAgreement(models.Model):
    _name = "employee_external_assignment_agreement"
    _inherit = [
        "employee_external_assignment_agreement",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_id",
        store=True,
        readonly=False,
        help="Operating unit for this agreement. When linked to a batch it "
        "follows the batch's operating unit; standalone agreements can set "
        "it freely.",
    )

    @api.depends("batch_id", "batch_id.operating_unit_id")
    def _compute_operating_unit_id(self):
        for record in self:
            if record.batch_id and record.batch_id.operating_unit_id:
                record.operating_unit_id = record.batch_id.operating_unit_id
            else:
                record.operating_unit_id = record.operating_unit_id

    @api.constrains("batch_id", "operating_unit_id")
    def _check_batch_operating_unit(self):
        for record in self:
            batch = record.batch_id
            if (
                batch
                and batch.operating_unit_id
                and record.operating_unit_id != batch.operating_unit_id
            ):
                error_message = (
                    _(
                        """
Context: Validate agreement operating unit against its batch
Database ID: %s
Problem: The agreement operating unit differs from the batch operating unit
Solution: Keep the agreement operating unit identical to the batch operating unit (%s)
"""
                    )
                    % (
                        record.id,
                        batch.operating_unit_id.display_name,
                    )
                )
                raise UserError(error_message)
