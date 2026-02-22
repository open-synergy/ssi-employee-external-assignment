# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrSalaryRule(models.Model):
    _name = "hr.salary_rule"
    _inherit = [
        "hr.salary_rule",
    ]

    external_assignment_agreement_product_id = fields.Many2one(
        string="External Assignment Agreement Product",
        comodel_name="product.product",
        domain=[("type", "=", "service")],
        required=False,
        help="Product used in employee external assignment agreement.",
    )
    external_assignment_agreement_tax_ids = fields.Many2many(
        string="External Assignment Agreement Taxes",
        comodel_name="account.tax",
        relation="rel_salary_rule_2_external_assignment_agreement_tax",
        column1="hr_salary_rule_id",
        column2="tax_id",
        required=False,
        help="Taxes applied on external assignment agreement product.",
    )
