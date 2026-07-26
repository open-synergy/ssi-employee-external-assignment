# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee External Assignment Agreement + Operating Unit",
    "version": "14.0.1.4.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_employee_external_assignment_agreement",
        "ssi_operating_unit_mixin",
        "ssi_financial_accounting_operating_unit",
        "ssi_employee_external_assignment_operating_unit",
    ],
    "data": [
        "security/res_group/res_group_data.xml",
        "security/ir_rule/ir_rule_data.xml",
        "views/employee_external_assignment_agreement_batch_views.xml",
        "views/employee_external_assignment_agreement_views.xml",
        "views/employee_external_assignment_agreement_payment_term_views.xml",
        "views/create_employee_external_assignment_views.xml",
    ],
}
