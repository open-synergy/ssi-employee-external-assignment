# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeExternalAssignmentType(models.Model):
    _name = "employee_external_assignment_type"
    _inherit = [
        "employee_external_assignment_type",
    ]

    pob_product_id = fields.Many2one(
        string="PoB Product",
        comodel_name="product.product",
        domain=[("type", "=", "service")],
        help=(
            "Representative service product used as product_id when creating "
            "a Performance Obligation from an agreement detail (job position). "
            "Must be a service-type product with a valid unit of measure."
        ),
    )
