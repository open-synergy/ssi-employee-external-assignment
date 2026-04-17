# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class EmployeeExternalAssignment(
    models.Model
):  # pylint: disable=too-few-public-methods
    _name = "employee_external_assignment"
    _inherit = [
        "employee_external_assignment",
        "mixin.single_operating_unit",
    ]

    @api.depends("type_id", "operating_unit_id")
    def _compute_allowed_employee_ids(self):  # pylint: disable=missing-return
        super()._compute_allowed_employee_ids()
        for record in self:
            if record.operating_unit_id and record.allowed_employee_ids:
                ou = record.operating_unit_id
                record.allowed_employee_ids = record.allowed_employee_ids.filtered(
                    lambda e, ou=ou: e.operating_unit_id == ou
                )
