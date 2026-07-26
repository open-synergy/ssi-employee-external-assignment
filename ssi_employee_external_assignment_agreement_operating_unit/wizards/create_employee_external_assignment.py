# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CreateEmployeeExternalAssignment(models.TransientModel):
    """Restrict the Create Assignment wizard to the agreement's OU.

    Shows the agreement's operating unit for information, narrows the
    employee choices to that same operating unit, and stamps it on
    every assignment the wizard creates.
    """

    _name = "create_employee_external_assignment"
    _inherit = "create_employee_external_assignment"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        related="agreement_id.operating_unit_id",
        store=False,
        readonly=True,
        compute_sudo=True,
        help="Operating unit of the agreement this wizard was launched "
        "from. Informational only; new assignments always inherit it "
        "from the agreement.",
    )

    @api.depends("agreement_id.operating_unit_id")
    def _compute_allowed_employee_ids(self):
        """Narrow the base employee choices to the agreement's OU.

        Calls ``super()`` first, then, when the agreement has an
        operating unit, keeps only employees whose ``operating_unit_id``
        matches it. Agreements without an operating unit leave the
        base result untouched.
        """
        super()._compute_allowed_employee_ids()
        for record in self:
            operating_unit = record.agreement_id.operating_unit_id
            if operating_unit and record.allowed_employee_ids:
                record.allowed_employee_ids = record.allowed_employee_ids.filtered(
                    lambda e, ou=operating_unit: e.operating_unit_id == ou
                )

    def _prepare_assignment_vals(self, employee):
        """Add the agreement's operating unit to the assignment values.

        :param employee: the ``hr.employee`` record to create the
            assignment for
        :return: dict of ``employee_external_assignment`` values,
            including ``operating_unit_id`` when the agreement has one
        """
        result = super()._prepare_assignment_vals(employee)
        operating_unit = self.agreement_id.operating_unit_id
        if operating_unit:
            result["operating_unit_id"] = operating_unit.id
        return result
