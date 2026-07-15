# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementPaymentTermFee(YamlTransactionCase):
    def test_employee_external_assignment_agreement_payment_term_fee(self):
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_payment_term_fee.yaml"
        )
