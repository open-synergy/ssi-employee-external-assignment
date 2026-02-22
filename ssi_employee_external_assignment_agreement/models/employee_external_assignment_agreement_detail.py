# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EmployeeExternalAssignmentAgreementDetail(models.Model):
    _name = "employee_external_assignment_agreement.detail"
    _description = "Employee External Assignment Agreement - Detail"

    agreement_id = fields.Many2one(
        comodel_name="employee_external_assignment_agreement",
        string="Agreement",
        required=True,
        ondelete="cascade",
    )
    job_id = fields.Many2one(
        comodel_name="hr.job",
        string="Job Position",
        required=True,
        help="Job position for the external assignment.",
    )
    allowed_salary_rule_ids = fields.Many2many(
        comodel_name="hr.salary_rule",
        string="Allowed Salary Rules",
        help="Salary rules that can be selected for compensation terms in this job position.",
        related="agreement_id.allowed_salary_rule_ids",
        store=False,
        compute_sudo=True,
    )
    all_salary_rule_ids = fields.Many2many(
        comodel_name="hr.salary_rule",
        string="Salary Rules",
        help="All salary rules associated with this job position.",
        compute_sudo=True,
        store=True,
        relation="rel_external_assignment_agreement_detail_2_salary_rule",
        column1="detail_id",
        column2="salary_rule_id",
        compute="_compute_all_salary_rule_ids",
    )
    quantity = fields.Integer(
        string="Quantity",
        required=True,
        default=1,
        help="Number of employees for this job position in the external assignment.",
    )
    quantity_available = fields.Integer(
        string="Quantity Available",
        compute="_compute_quantity_available",
        store=False,
        compute_sudo=True,
        help="Number of available positions for this job position in the external assignment.",
    )
    quantity_diff = fields.Integer(
        string="Quantity Difference",
        compute="_compute_quantity_diff",
        store=False,
        compute_sudo=True,
        help="Difference between quantity and quantity available.",
    )
    compensation_term_ids = fields.One2many(
        comodel_name="employee_external_assignment_agreement.detail.compensation_term",
        inverse_name="detail_id",
        string="Compensation Terms",
        help="Compensation terms associated with this job position.",
    )

    @api.depends(
        "agreement_id.assignment_ids",
        "agreement_id.assignment_ids.job_id",
        "agreement_id.assignment_ids.state",
    )
    def _compute_quantity_available(self):
        for record in self:
            assigned_count = self.env["employee_external_assignment"].search_count(
                [
                    ("agreement_id", "=", record.agreement_id.id),
                    ("job_id", "=", record.job_id.id),
                    ("state", "=", "open"),
                ]
            )
            record.quantity_available = assigned_count

    @api.depends("quantity", "quantity_available")
    def _compute_quantity_diff(self):
        for record in self:
            record.quantity_diff = record.quantity - record.quantity_available

    @api.depends(
        "compensation_term_ids",
        "compensation_term_ids.rule_id",
    )
    def _compute_all_salary_rule_ids(self):
        for record in self:
            all_salary_rule_ids = self.env["hr.salary_rule"]
            for compensation_term in record.compensation_term_ids:
                all_salary_rule_ids |= compensation_term.rule_id
            record.all_salary_rule_ids = all_salary_rule_ids
