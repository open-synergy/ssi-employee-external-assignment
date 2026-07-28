# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeExternalAssignmentAgreementPaymentTermPolicy(YamlTransactionCase):
    """Regression test for terminate_ok/restart_approval_ok policy gating.

    Covers issue #29: ``terminate_ok`` and ``restart_approval_ok`` on
    ``employee_external_assignment_agreement.payment_term`` used to be
    ``restrict_state``-d to state ``open``, a state this model never
    reaches (its lifecycle is draft -> confirm -> done). Both policy
    detail records now gate on ``done`` instead.
    """

    def test_payment_term_terminate_restart_approval_policy(self):
        """Run the terminate/restart_approval policy YAML scenarios."""
        self.run_yaml_scenario(
            "test_data_employee_external_assignment_agreement_payment_term_policy.yaml"
        )
