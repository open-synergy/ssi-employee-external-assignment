# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class EmployeeExternalAssignment(models.Model):
    _name = "employee_external_assignment"
    _inherit = [
        "employee_external_assignment",
    ]

    agreement_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement",
        string="# Agreement",
        help="The agreement associated with this external assignment.",
        ondelete="set null",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
