# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeExternalAssignmentType(models.Model):
    _name = "employee_external_assignment_type"
    _description = "Employee External Assignment Type"
    _inherit = [
        "mixin.master_data",
        "mixin.res_partner_m2o_configurator",
    ]
    _res_partner_m2o_configurator_insert_form_element_ok = True
    _res_partner_m2o_configurator_form_xpath = "//page[@name='partner']"

    employee_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Employee Selection Method",
        required=True,
    )
    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Employees",
    )
    employee_domain = fields.Text(default="[]", string="Employee Domain")
    employee_python_code = fields.Text(
        default="result = []", string="Employee Python Code"
    )
