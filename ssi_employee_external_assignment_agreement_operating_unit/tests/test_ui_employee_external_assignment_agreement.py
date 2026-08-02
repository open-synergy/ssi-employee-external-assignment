# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeExternalAssignmentAgreement(HttpSavepointCase):
    """Tour tests for the agreement Operating Unit delta IK.

    Model: ``employee_external_assignment_agreement``.
    """

    @classmethod
    def setUpClass(cls):
        """Grant admin the multi-OU group the Operating Unit field needs."""
        super().setUpClass()
        # Pre-Condition: operating_unit_id is only rendered for users in
        # operating_unit.group_multi_operating_unit. Without it the tour's
        # assertion step times out even though the field is correctly
        # declared -- the field is simply never in the DOM.
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the create delta tour for the agreement.

        IK: docs/employee_external_assignment_agreement/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_employee_external_assignment_agreement_operating_unit_"
            "employee_external_assignment_agreement_create",
            login="admin",
        )
