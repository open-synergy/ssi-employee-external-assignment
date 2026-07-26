# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeExternalAssignmentType(models.Model):
    _name = "employee_external_assignment_type"
    _inherit = [
        "employee_external_assignment_type",
    ]

    job_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Job Selection Method",
        required=True,
    )
    job_ids = fields.Many2many(
        comodel_name="hr.job",
        string="Jobs",
        relation="eea_type_2_hr_job_rel",
        column1="type_id",
        column2="hr_job_id",
    )
    job_domain = fields.Text(default="[]", string="Job Domain")
    job_python_code = fields.Text(default="result = []", string="Job Python Code")

    salary_rule_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Salary Rule Selection Method",
        required=True,
    )
    salary_rule_ids = fields.Many2many(
        comodel_name="hr.salary_rule",
        string="Salary Rules",
        relation="eea_type_hr_2_salary_rule_rel",
        column1="type_id",
        column2="hr_salary_rule_id",
    )
    salary_rule_domain = fields.Text(default="[]", string="Salary Rule Domain")
    salary_rule_python_code = fields.Text(
        default="result = []", string="Salary Rule Python Code"
    )

    other_fee_category_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Other Fee Category Selection Method",
        required=True,
    )
    other_fee_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Other Fee Categories",
        relation="eea_type_2_other_fee_category_rel",
        column1="type_id",
        column2="other_fee_category_id",
    )
    other_fee_category_domain = fields.Text(
        default="[]", string="Other Fee Category Domain"
    )
    other_fee_category_python_code = fields.Text(
        default="result = []", string="Other Fee Category Python Code"
    )

    other_fee_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Other Fee Selection Method",
        required=True,
    )
    other_fee_ids = fields.Many2many(
        comodel_name="product.product",
        string="Other Fees",
        relation="eea_type_2_other_fee_rel",
        column1="type_id",
        column2="other_fee_id",
    )
    other_fee_domain = fields.Text(default="[]", string="Other Fee Domain")
    other_fee_python_code = fields.Text(
        default="result = []", string="Other Fee Python Code"
    )

    usage_id = fields.Many2one(
        comodel_name="product.usage_type",
        string="Usage",
        help="Default usage that determines which account is used when "
        "generating invoices for agreements of this type.",
    )

    receivable_account_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Receivable Account Selection Method",
        required=True,
    )
    receivable_account_ids = fields.Many2many(
        comodel_name="account.account",
        string="Receivable Accounts",
        relation="eea_type_2_receivable_account_rel",
        column1="type_id",
        column2="account_id",
    )
    receivable_account_domain = fields.Text(
        default="[]", string="Receivable Account Domain"
    )
    receivable_account_python_code = fields.Text(
        default="result = []", string="Receivable Account Python Code"
    )

    journal_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Journal Selection Method",
        required=True,
    )
    journal_ids = fields.Many2many(
        comodel_name="account.journal",
        string="Journals",
        relation="eea_type_2_journal_rel",
        column1="type_id",
        column2="journal_id",
    )
    journal_domain = fields.Text(default="[]", string="Journal Domain")
    journal_python_code = fields.Text(
        default="result = []", string="Journal Python Code"
    )

    usage_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Usage Selection Method",
        required=True,
    )
    usage_ids = fields.Many2many(
        comodel_name="product.usage_type",
        string="Usages",
        relation="eea_type_2_usage_type_rel",
        column1="type_id",
        column2="usage_type_id",
    )
    usage_domain = fields.Text(default="[]", string="Usage Domain")
    usage_python_code = fields.Text(default="result = []", string="Usage Python Code")

    analytic_group_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Analytic Group Selection Method",
        required=True,
    )
    analytic_group_ids = fields.Many2many(
        comodel_name="account.analytic.group",
        string="Analytic Groups",
        relation="eea_type_2_analytic_group_rel",
        column1="type_id",
        column2="analytic_group_id",
    )
    analytic_group_domain = fields.Text(default="[]", string="Analytic Group Domain")
    analytic_group_python_code = fields.Text(
        default="result = []", string="Analytic Group Python Code"
    )
