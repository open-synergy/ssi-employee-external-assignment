# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCreateEmployeeExternalAssignmentOperatingUnit(YamlTransactionCase):
    def test_create_employee_external_assignment_operating_unit(self):
        self.run_yaml_scenario(
            "test_data_create_employee_external_assignment_operating_unit.yaml"
        )
