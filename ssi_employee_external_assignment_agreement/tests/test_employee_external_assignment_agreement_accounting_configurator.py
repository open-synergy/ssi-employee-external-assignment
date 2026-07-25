# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementAccountingConfigurator(
    YamlTransactionCase
):
    def test_employee_external_assignment_agreement_accounting_configurator(self):
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_accounting_configurator.yaml"
        )
