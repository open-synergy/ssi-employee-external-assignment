# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"
    _name = "hr.employee.base"

    external_assignment_ids = fields.One2many(
        string="External Assignments",
        comodel_name="employee_external_assignment",
        inverse_name="employee_id",
        help="External assignments of the employee.",
    )
    external_assignment_id = fields.Many2one(
        string="Current External Assignment",
        comodel_name="employee_external_assignment",
        compute="_compute_external_assignment_id",
        store=True,
        compute_sudo=True,
        help="The current active external assignment, if any.",
    )
    external_assignment_partner_id = fields.Many2one(
        string="External Assignment Partner",
        comodel_name="res.partner",
        related="external_assignment_id.partner_id",
        store=True,
        help="Partner of the current active external assignment.",
    )
    external_assignment_location_id = fields.Many2one(
        string="External Assignment Location",
        comodel_name="res.partner",
        related="external_assignment_id.partner_location_id",
        store=True,
        help="Location of the current active external assignment.",
    )

    @api.depends("external_assignment_ids.state", "external_assignment_ids")
    def _compute_external_assignment_id(self):
        for rec in self:
            active_assignment = rec.external_assignment_ids.filtered(
                lambda r: r.state == "open"
            )
            rec.external_assignment_id = (
                active_assignment[:1] if active_assignment else False
            )
